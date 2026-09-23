import json
import logging
import os
import re
import unicodedata
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from config.datasets import DATASETS_CONFIG, get_table_name, get_dataset_config
from llm.router import get_llm
from metadata.loader import load_metadata
from services.relationship_service import Relationship, relationship_service
from services.sql_service import extract_sql
from services.analytical_contract import SQL_INSTRUCTIONS, contract_errors, prepare_sql, normalize
from services.generation_diagnostics import record

logger = logging.getLogger(__name__)

try:
    from sqlglot import exp, parse_one
except Exception as exc:  # pragma: no cover - fail closed when dependency is missing
    raise RuntimeError(
        "sqlglot is required for multibase SQL validation. Install backend requirements before running the application."
    ) from exc


@dataclass(frozen=True)
class DatasetSelection:
    datasets: List[str]
    cross_dataset: bool
    reason: str
    routing_mode: str


@dataclass(frozen=True)
class SqlValidationResult:
    valid: bool
    tables: List[str]
    joins: List[str]
    ctes: List[str]
    errors: List[str]


class MultibaseService:
    """Coordena seleção de datasets, prompt multibase e validação estrutural."""

    def __init__(self, relationship_service_instance=relationship_service):
        self.relationship_service = relationship_service_instance

    def select_datasets(self, question: str, model_name: str, candidate_datasets: Sequence[str]) -> DatasetSelection:
        candidates = [dataset for dataset in candidate_datasets if dataset in DATASETS_CONFIG]
        if not candidates:
            candidates = list(DATASETS_CONFIG.keys())

        keyword_selection = self._detect_keyword_datasets(question, candidates)
        if keyword_selection:
            return DatasetSelection(
                datasets=keyword_selection,
                cross_dataset=len(keyword_selection) > 1,
                reason="Domínio(s) explicitamente identificado(s) na pergunta",
                routing_mode=(
                    "heuristic_multi_dataset"
                    if len(keyword_selection) > 1
                    else "heuristic_single_dataset"
                ),
            )

        prompt_lines = [
            "Selecione um ou mais datasets para a pergunta abaixo.",
            "Responda SOMENTE com JSON válido no formato:",
            '{"datasets": ["id"], "cross_dataset": false, "reason": "..."}',
            "Se a pergunta exigir mais de uma base, marque cross_dataset como true.",
            "Não invente datasets inexistentes.",
            "",
            f"Pergunta: {question}",
            "",
            "Datasets disponíveis:"
        ]

        for dataset_id in candidates:
            config = get_dataset_config(dataset_id)
            prompt_lines.append(
                f"- {dataset_id}: {config.get('name', '')} | {config.get('dominio', '')} | {config.get('description', '')}"
            )

        prompt_lines.append("")
        prompt_lines.append("Relacionamentos interdomínio disponíveis:")
        available_relationships = [
            relationship
            for relationship in self.relationship_service.list_relationships()
            if relationship.source_dataset in candidates and relationship.target_dataset in candidates
        ]
        if available_relationships:
            for relationship in available_relationships:
                prompt_lines.append(
                    f"- {relationship.source_dataset} <-> {relationship.target_dataset}: "
                    f"{relationship.description}"
                )
        else:
            prompt_lines.append("- Nenhum relacionamento interdomínio cadastrado.")
        prompt_lines.append("Selecione todos os datasets exigidos pela pergunta, mesmo quando ainda não houver relacionamento cadastrado entre eles.")
        prompt_lines.append("Não omita um domínio necessário apenas para transformar a pergunta em consulta monobase.")

        try:
            llm = get_llm(model_name)
            response = llm.generate(
                "\n".join(prompt_lines),
                response_format="json",
                num_predict=160,
                temperature=0.0,
                timeout_s=int(os.getenv("OLLAMA_ROUTING_TIMEOUT", "30")),
                max_retries=1,
            )
            parsed = self._parse_selection_response(response, candidates)
            if parsed:
                return parsed
        except Exception as exc:
            logger.warning(f"Falha na seleção por LLM: {exc}")

        fallback = self._fallback_selection(question, candidates)
        return DatasetSelection(
            datasets=fallback,
            cross_dataset=len(fallback) > 1,
            reason="Fallback heurístico por palavras-chave",
            routing_mode="fallback",
        )

    def _parse_selection_response(self, response: str, valid_datasets: Sequence[str]) -> Optional[DatasetSelection]:
        if not response:
            return None

        try:
            payload = json.loads(response)
        except Exception:
            match = re.search(r"\{.*\}", response, re.DOTALL)
            if not match:
                return None
            try:
                payload = json.loads(match.group(0))
            except Exception:
                return None

        datasets = payload.get("datasets")
        if not isinstance(datasets, list):
            return None

        validated = [dataset for dataset in datasets if dataset in valid_datasets and dataset in DATASETS_CONFIG]
        if not validated:
            return None

        reason = str(payload.get("reason", ""))
        cross_dataset = bool(payload.get("cross_dataset", len(validated) > 1))
        return DatasetSelection(
            datasets=validated,
            cross_dataset=cross_dataset,
            reason=reason,
            routing_mode="llm",
        )

    def _fallback_selection(self, question: str, candidate_datasets: Sequence[str]) -> List[str]:
        detected = self._detect_keyword_datasets(question, candidate_datasets)
        return detected if detected else [candidate_datasets[0]]

    @staticmethod
    def _normalize_question_text(value: str) -> str:
        normalized = unicodedata.normalize("NFKD", value.lower())
        without_accents = "".join(char for char in normalized if not unicodedata.combining(char))
        return re.sub(r"\s+", " ", without_accents).strip()

    @classmethod
    def _detect_keyword_datasets(cls, question: str, candidate_datasets: Sequence[str]) -> List[str]:
        q = cls._normalize_question_text(question)
        detected = []
        keyword_map = {
            "covid-19-vacinacao": [
                "vacina", "vacinas", "vacinacao", "covid", "dose", "doses", "imunizacao",
                "pfizer", "astrazeneca",
            ],
            "leitos": [
                "leito", "leitos",
                "cama", "camas",
            ],
            "surtos-srag": [
                "srag", "sindrome respiratoria", "febre", "tosse", "dispneia",
                "notificacao", "notificacoes", "vigilancia epidemiologica",
            ],
            "atencao-basica": [
                "ubs", "unidade basica", "unidades basicas", "atencao basica",
                "atencao primaria", "posto de saude", "postos de saude",
                "saude da familia",
            ],
        }

        for dataset_id in candidate_datasets:
            if any(re.search(r"(?<!\w)" + re.escape(keyword) + r"(?!\w)", q) for keyword in keyword_map.get(dataset_id, [])):
                detected.append(dataset_id)

        # Ambiguous field names never add a second domain to an explicit selection.
        if not detected and re.search(r"\b(?:uti|hospital|hospitais)\b", q):
            if "leitos" in candidate_datasets:
                detected.append("leitos")
        return detected

    def build_multibase_context(self, datasets: Sequence[str], relationships: Sequence[Relationship]) -> Dict[str, object]:
        metadata_by_dataset = {}
        for dataset_id in datasets:
            metadata_by_dataset[dataset_id] = json.loads(load_metadata(dataset_id))

        return {
            "datasets": list(datasets),
            "metadata": metadata_by_dataset,
            "relationships": [relationship.__dict__ for relationship in relationships],
        }

    def build_multibase_prompt(
        self,
        question: str,
        selected_datasets: Sequence[str],
        relationships: Sequence[Relationship],
    ) -> str:
        context = self.build_multibase_context(selected_datasets, relationships)
        prompt_parts = [
            "Você é um especialista em SQL ClickHouse.",
            "Responda SOMENTE com SQL válido, sem explicações, sem markdown.",
            "FROM/JOIN só podem usar as tabelas físicas listadas abaixo ou CTEs definidas na consulta.",
            "Identificadores de datasets/relacionamentos NÃO são tabelas.",
            "Se houver relacionamento muitos-para-muitos, faça pré-agregação antes do JOIN.",
            "Não crie joins nem colunas fora do contexto fornecido.",
            "",
            f"Pergunta: {question}",
            "",
            "Tabelas físicas autorizadas:",
        ]

        for dataset_id in selected_datasets:
            config = get_dataset_config(dataset_id)
            metadata = context["metadata"][dataset_id]
            columns = metadata.get("colunas_principais") or metadata.get("columns") or {}
            prompt_parts.append(
                f"- FROM {get_table_name(dataset_id)} | {config.get('dominio', '')}"
            )
            prompt_parts.append(f"  Colunas permitidas: {', '.join(columns.keys())}")
            join_fields = {
                name.lower()
                for relationship in relationships
                for dataset, name in ((relationship.source_dataset, relationship.source_column),
                                      (relationship.target_dataset, relationship.target_column))
                if dataset == dataset_id
            }
            for name, detail in columns.items():
                if name.lower() in join_fields or re.search(r"\b" + re.escape(name) + r"\b", question, re.IGNORECASE):
                    description = detail.get("description") or detail.get("descricao") or ""
                    dtype = detail.get("type") or detail.get("tipo") or ""
                    prompt_parts.append(f"  Campo de referência: {get_table_name(dataset_id)}.{name} ({dtype}): {description}")

        prompt_parts.append("")
        prompt_parts.append("Relacionamentos permitidos:")
        if relationships:
            for relationship in relationships:
                prompt_parts.append(
                    f"- Chave de junção: {relationship.source_table}.{relationship.source_column} = {relationship.target_table}.{relationship.target_column} | "
                    f"cardinalidade {relationship.cardinality} | pré-agregação {relationship.requires_preaggregation}"
                )
                if relationship.analytical_notes:
                    prompt_parts.append(f"  Restrição analítica: {relationship.analytical_notes}")
                if relationship.use_latest_target_period and relationship.target_temporal_column:
                    prompt_parts.append(
                        f"  Regra temporal: filtre {relationship.target_table}.{relationship.target_temporal_column} "
                        f"pela maior competência disponível antes de agregar."
                    )
        else:
            prompt_parts.append("- Nenhum relacionamento autorizado encontrado.")

        prompt_parts.append("")
        prompt_parts.append("Regras:")
        prompt_parts.append("- Use only SELECT or WITH followed by SELECT")
        prompt_parts.append("- Preserve os alias e colunas de junção permitidas")
        prompt_parts.append("- Para muitos-para-muitos, agregue cada lado antes do JOIN")
        prompt_parts.append("- Entidades comuns/presentes nas duas bases: INNER JOIN. FULL OUTER JOIN inclui entidades presentes em apenas uma base e muda a resposta.")
        prompt_parts.append("- Calcule cada métrica na sua base de origem: identificador de notificação não substitui CNES. Não use COALESCE para intercambiar métricas de entidades diferentes.")
        prompt_parts.append("- Dialeto: ClickHouse")
        prompt_parts.append("- Retorne apenas SQL")
        prompt_parts.append(SQL_INSTRUCTIONS)
        prompt_parts.append(f"Pergunta a responder (preserve os filtros de cada entidade): {question}")
        filter_hints = self._positive_code_filter_hints(question, selected_datasets, relationships)
        if filter_hints:
            prompt_parts.append("Filtros de códigos pedidos (aplique nas respectivas bases antes de agregar): " + "; ".join(filter_hints))
            prompt_parts.append("Positivo refere-se a esses códigos numéricos, não a exames laboratoriais. Não acrescente condições clínicas que não foram solicitadas.")

        return "\n".join(prompt_parts)

    def _positive_code_filter_hints(self, question, selected_datasets, relationships):
        """Build positive-code hints from numeric schema fields."""
        q = normalize(question)
        if re.search(r'\b(?:nao|sem|exceto|exclu\w*)\b[^.;,]{0,50}\bpositivos?\b', q):
            # Negated requests need broader language understanding.
            return []
        municipal = bool(re.search(r'municipios? positivos?|codigos? positivos? de municipio', q))
        join_fields = {(r.source_table, r.source_column.lower()) for r in relationships}
        join_fields |= {(r.target_table, r.target_column.lower()) for r in relationships}
        hints = []
        for dataset in selected_datasets:
            table = get_table_name(dataset)
            for name, detail in self._allowed_columns_for_table(table).items():
                dtype = str(detail.get('type') or detail.get('tipo') or '').lower()
                if 'int' not in dtype:
                    continue
                explicit = bool(re.search(r'\b' + re.escape(name.lower()) + r'\s+(?:distintos?\s+)?positivos?\b', q))
                description = normalize(str(detail.get('description') or detail.get('descricao') or ''))
                municipal_key = municipal and (table, name.lower()) in join_fields and 'municipio' in description
                if explicit or municipal_key:
                    hints.append(f'{table}.{name} > 0')
        return hints

    def generate_sql(
        self,
        question: str,
        model_name: str,
        selected_datasets: Sequence[str],
        relationships: Sequence[Relationship],
        sql_validator=None,
    ) -> Tuple[Optional[str], str]:
        if len(selected_datasets) <= 1:
            return None, "single_dataset"

        if not self.relationships_cover(selected_datasets, relationships):
            return None, "no_relationship"

        if os.getenv("SQL_GENERATION_STRATEGY", "deterministic_first").lower() == "deterministic_first":
            deterministic_sql = self.build_deterministic_fallback_sql(
                selected_datasets,
                relationships,
                question,
            )
            if deterministic_sql:
                return deterministic_sql, "deterministic_rule"

        prompt = self.build_multibase_prompt(question, selected_datasets, relationships)
        llm = get_llm(model_name)

        try:
            response = llm.generate(
                prompt,
                num_predict=int(os.getenv("OLLAMA_SQL_NUM_PREDICT", "512")),
                temperature=0.0,
                timeout_s=int(os.getenv("OLLAMA_SQL_TIMEOUT", "180")),
                max_retries=1,
            )
        except Exception as exc:
            logger.warning(f"Falha ao gerar SQL multibase via LLM: {exc}")
            record('sql_generation_exception', error=str(exc))
            return None, "llm_error"

        for attempt in range(2):
            try:
                sql = prepare_sql(extract_sql(response), question)
                errors = contract_errors(sql, question, self._allowed_columns_by_dataset(selected_datasets))
                sql = self.canonicalize_sql_identifiers(sql, selected_datasets)
                validation = self.validate_sql(sql, selected_datasets, relationships)
                errors.extend(validation.errors)
                if not errors and sql_validator is not None:
                    errors.extend(sql_validator(sql))
            except Exception:
                sql, errors = None, ["SQL inválido"]
            record('sql_validation', attempt=attempt + 1, sql=sql, errors=list(errors))
            if not errors:
                return sql, "llm"
            logger.warning("SQL multibase rejeitada na tentativa %s: %s", attempt + 1, "; ".join(errors))
            if attempt == 0:
                try:
                    response = llm.generate(prompt + "\nCorrija: " + str(sql) + "\n" + "; ".join(errors),
                        num_predict=int(os.getenv("OLLAMA_SQL_NUM_PREDICT", "512")), temperature=0.0,
                        timeout_s=int(os.getenv("OLLAMA_SQL_TIMEOUT", "180")), max_retries=1)
                except Exception as exc:
                    record('sql_generation_exception', error=str(exc))
                    break
        return None, "llm_error"

    @staticmethod
    def relationships_cover(datasets, relationships):
        """Every selected dataset must belong to one connected authorized graph."""
        selected = set(datasets)
        if not selected:
            return False
        seen = {next(iter(selected))}
        while True:
            previous = set(seen)
            for rel in relationships:
                edge = {rel.source_dataset, rel.target_dataset}
                if edge <= selected and edge & seen:
                    seen |= edge
            if seen == previous:
                return seen == selected

    def build_deterministic_fallback_sql(
        self,
        selected_datasets: Sequence[str],
        relationships: Sequence[Relationship],
        question: str = "",
    ) -> Optional[str]:
        if not self.relationships_cover(selected_datasets, relationships):
            return None
        q = self._normalize_question_text(question).strip(" ?.")
        # Full matching is intentional: unrecognized filters must not disappear.
        count_pattern = r"(?:em )?quantos municipios (?:ha|possuem|tem) (?:casos|registros|notificacoes) de srag e (?:tambem )?(?:ubs|unidades basicas de saude)(?: cadastradas)?"
        list_pattern = r"(?:quais|liste(?: todos os)?) municipios (?:possuem|com) (?:casos|registros|notificacoes) de srag e (?:ubs|unidades basicas de saude)(?:,? e quais sao os respectivos totais)?"
        beds_pattern = r"(?:compare|liste) (?:doses(?: aplicadas)?|registros de vacinacao) e leitos(?: de uti)? por estado"
        municipality_count = bool(re.fullmatch(count_pattern, q))
        municipality_list = bool(re.fullmatch(list_pattern, q))
        if set(selected_datasets) == {"surtos-srag", "atencao-basica"} and not (municipality_count or municipality_list):
            return None
        if set(selected_datasets) == {"covid-19-vacinacao", "leitos"} and not re.fullmatch(beds_pattern, q):
            return None
        if set(selected_datasets) == {"covid-19-vacinacao", "leitos"} and relationships:
            relationship = next(
                (item for item in relationships if item.id == "vacinacao_leitos_uf"),
                None,
            )
            if relationship and relationship.requires_preaggregation:
                bed_metric = "UTI_TOTAL_EXIST" if "uti" in q else "LEITOS_EXISTENTES"
                bed_alias = "total_uti_beds" if "uti" in q else "total_beds"
                return f"""
WITH
vaccination_by_state AS (
    SELECT
        {relationship.source_column} AS uf,
        COUNT(*) AS total_doses
    FROM {relationship.source_table}
    WHERE {relationship.source_column} != ''
    GROUP BY {relationship.source_column}
),
beds_by_state AS (
    SELECT
        {relationship.target_column} AS uf,
        SUM({bed_metric}) AS {bed_alias}
    FROM {relationship.target_table}
    WHERE {relationship.target_column} != ''
      AND {relationship.target_temporal_column} = (
          SELECT MAX({relationship.target_temporal_column})
          FROM {relationship.target_table}
      )
    GROUP BY {relationship.target_column}
)
SELECT
    v.uf,
    v.total_doses,
    b.{bed_alias}
FROM vaccination_by_state AS v
INNER JOIN beds_by_state AS b
    ON v.uf = b.uf
ORDER BY v.total_doses DESC, b.{bed_alias} DESC
""".strip()

        if set(selected_datasets) == {"surtos-srag", "atencao-basica"} and relationships:
            relationship = relationships[0]
            if relationship.requires_preaggregation:
                asks_municipality_count = municipality_count
                if asks_municipality_count:
                    return f"""
WITH
srag_municipalities AS (
    SELECT DISTINCT {relationship.source_column} AS ibge
    FROM {relationship.source_table}
),
ubs_municipalities AS (
    SELECT DISTINCT {relationship.target_column} AS ibge
    FROM {relationship.target_table}
)
SELECT COUNT(*) AS total_municipios
FROM srag_municipalities AS s
INNER JOIN ubs_municipalities AS u
    ON s.ibge = u.ibge
""".strip()

                return f"""
WITH
srag_by_municipality AS (
    SELECT
        {relationship.source_column} AS ibge,
        COUNT(*) AS total_srag
    FROM {relationship.source_table}
    GROUP BY {relationship.source_column}
),
ubs_by_municipality AS (
    SELECT
        {relationship.target_column} AS ibge,
        COUNT(DISTINCT cnes) AS total_ubs
    FROM {relationship.target_table}
    GROUP BY {relationship.target_column}
)
SELECT
    s.ibge,
    s.total_srag,
    u.total_ubs
FROM srag_by_municipality AS s
INNER JOIN ubs_by_municipality AS u
    ON s.ibge = u.ibge
ORDER BY s.total_srag DESC, s.ibge ASC
""".strip()

        return None

    def canonicalize_sql_identifiers(self, sql: str, selected_datasets: Sequence[str]) -> str:
        """Reescreve tabelas e colunas com a grafia física configurada."""

        parsed = parse_one(sql, read="clickhouse")
        cte_names = {cte.alias_or_name.lower() for cte in parsed.find_all(exp.CTE)}
        allowed_tables = {
            get_table_name(dataset).lower(): get_table_name(dataset)
            for dataset in selected_datasets
        }
        from sqlglot.optimizer.scope import Scope, traverse_scope

        for table_node in parsed.find_all(exp.Table):
            name = table_node.name.lower()
            if name not in cte_names and name in allowed_tables:
                table_node.set("this", exp.to_identifier(allowed_tables[name]))

        # Resolve reused aliases within their own scopes.
        for scope in traverse_scope(parsed):
            sources = {}
            source_aliases = {alias.lower(): alias for alias in scope.sources}
            for alias, source in scope.sources.items():
                if isinstance(source, Scope):
                    names = source.expression.named_selects
                elif isinstance(source, exp.Table) and source.name in allowed_tables.values():
                    names = self._allowed_columns_for_table(source.name)
                else:
                    names = []
                sources[alias.lower()] = {name.lower(): name for name in names}
            output_aliases = {node.alias.lower() for node in scope.expression.expressions if node.alias}
            for column in scope.columns:
                key = column.name.lower()
                if column.table:
                    canonical = sources.get(column.table.lower(), {}).get(key)
                else:
                    # Preserve explicit projection aliases.
                    if key in output_aliases and not column.find_ancestor(exp.Alias):
                        # Qualify WHERE fields to prevent aggregate-alias substitution.
                        owners = [(alias, names[key]) for alias, names in sources.items() if key in names]
                        where = scope.expression.args.get("where")
                        if where is not None and column.find_ancestor(exp.Where) is where and len(owners) == 1:
                            alias, name = owners[0]
                            column.set("this", exp.to_identifier(name))
                            column.set("table", exp.to_identifier(source_aliases[alias]))
                        continue
                    matches = {names[key] for names in sources.values() if key in names}
                    canonical = next(iter(matches)) if len(matches) == 1 else None
                if canonical:
                    column.set("this", exp.to_identifier(canonical))

        return parsed.sql(dialect="clickhouse")

    def validate_sql(self, sql: str, selected_datasets: Sequence[str], relationships: Sequence[Relationship]) -> SqlValidationResult:
        if len(selected_datasets) > 1 and not self.relationships_cover(selected_datasets, relationships):
            return SqlValidationResult(False, [], [], [], ["Relacionamentos não cobrem todas as bases selecionadas"])
        if not sql:
            return SqlValidationResult(False, [], [], [], ["SQL vazio"])

        sql_clean = sql.strip()
        if ";" in sql_clean.rstrip(";"):
            return SqlValidationResult(False, [], [], [], ["Múltiplas instruções não são permitidas"])

        if re.search(r"--|/\*|\*/", sql_clean):
            return SqlValidationResult(False, [], [], [], ["Comentários não são permitidos"])

        try:
            parsed = parse_one(sql_clean, read="clickhouse")
        except Exception as exc:
            return SqlValidationResult(False, [], [], [], [f"Falha ao parsear SQL: {exc}"])

        if not isinstance(parsed, (exp.Select, exp.Union)):
            return SqlValidationResult(False, [], [], [], ["A consulta deve começar com SELECT ou WITH seguido de SELECT"])

        cte_names = {cte.alias_or_name for cte in parsed.find_all(exp.CTE)} if hasattr(parsed, "find_all") else set()
        table_nodes = [node for node in parsed.find_all(exp.Table)]
        physical_tables = []
        alias_to_table = {}
        for table_node in table_nodes:
            table_name = table_node.name
            table_alias = table_node.alias_or_name
            if table_name not in cte_names:
                physical_tables.append(table_name)
                alias_to_table[table_alias.lower()] = table_name

        physical_tables = list(dict.fromkeys(physical_tables))

        allowed_tables = {get_table_name(dataset) for dataset in selected_datasets}
        invalid_tables = [table for table in physical_tables if table not in allowed_tables]
        if invalid_tables:
            return SqlValidationResult(False, physical_tables, [], list(cte_names), [f"Tabelas não autorizadas: {', '.join(invalid_tables)}"])

        missing_tables = sorted(allowed_tables - set(physical_tables))
        if len(selected_datasets) > 1 and missing_tables:
            return SqlValidationResult(False, physical_tables, [], list(cte_names), [f"Tabelas selecionadas ausentes da consulta: {', '.join(missing_tables)}"])

        joins = []
        allowed_pairs = self._allowed_join_pairs(relationships)
        selected_columns = self._allowed_columns_by_dataset(selected_datasets)
        selected_columns_lower = {column.lower() for column in selected_columns}
        output_aliases = {alias.lower() for alias in self._extract_output_aliases(parsed)}

        for column_ref in self._extract_column_references(parsed):
            column_name = column_ref["column"]
            table_alias = column_ref.get("table")

            if table_alias and table_alias.lower() in cte_names:
                continue

            if table_alias and table_alias.lower() in alias_to_table:
                allowed_columns = {
                    allowed_column.lower()
                    for allowed_column in self._allowed_columns_for_table(alias_to_table[table_alias.lower()]).keys()
                }
                if column_name.lower() not in allowed_columns:
                    return SqlValidationResult(False, physical_tables, joins, list(cte_names), [f"Coluna não autorizada: {table_alias}.{column_name}"])
                continue

            if column_name.lower() in selected_columns_lower or column_name.lower() in output_aliases:
                continue

            return SqlValidationResult(False, physical_tables, joins, list(cte_names), [f"Coluna não autorizada: {column_name}"])

        if self._contains_write_operation(parsed):
            return SqlValidationResult(False, physical_tables, joins, list(cte_names), ["Comando de escrita não permitido"])

        join_nodes = list(parsed.find_all(exp.Join))
        if len(selected_datasets) > 1 and not join_nodes:
            return SqlValidationResult(False, physical_tables, joins, list(cte_names), ["Consulta multibase sem JOIN reconhecível"])

        preaggregated_pairs: Dict[str, set[str]] = {}
        for relationship in relationships:
            if relationship.requires_preaggregation and {
                relationship.source_dataset,
                relationship.target_dataset,
            }.issubset(set(selected_datasets)):
                pairs = self._preaggregated_join_pairs(parsed, relationship)
                if not pairs:
                    return SqlValidationResult(
                        False,
                        physical_tables,
                        joins,
                        list(cte_names),
                        [f"A junção exige pré-agregação dos dois lados antes do JOIN: "
                         f"agregue {relationship.source_table} por {relationship.source_column} "
                         f"e {relationship.target_table} por {relationship.target_column} em CTEs/subconsultas separadas"],
                    )
                preaggregated_pairs[relationship.id] = pairs

        for join_node in join_nodes:
            # Scalar aggregate CTEs do not multiply source rows.
            if (len(selected_datasets) == 1
                    and not join_node.args.get("on")
                    and not join_node.args.get("side")
                    and self._scalar_cte_cross_join(parsed, join_node)):
                continue
            on_expression = join_node.args.get("on")
            if on_expression is None:
                return SqlValidationResult(False, physical_tables, joins, list(cte_names), ["JOIN sem condição ON não é permitido"])
            if join_node.args.get("kind") and str(join_node.args.get("kind")).upper() == "CROSS":
                return SqlValidationResult(False, physical_tables, joins, list(cte_names), ["CROSS JOIN não autorizado"])

            join_text = on_expression.sql(dialect="clickhouse")
            joins.append(join_text)
            normalized = self._normalize_join_condition(join_text)

            if any(normalized in pairs for pairs in preaggregated_pairs.values()):
                continue

            if len(selected_datasets) == 1 and self._same_base_grouped_join(parsed, join_node):
                continue

            if normalized not in allowed_pairs:
                return SqlValidationResult(False, physical_tables, joins, list(cte_names), [f"JOIN não autorizado: {join_text}"])

        return SqlValidationResult(True, physical_tables, joins, list(cte_names), [])

    @staticmethod
    def _same_base_grouped_join(parsed, join):
        """Allow equality of unique group keys within one authorized dataset."""
        from sqlglot.optimizer.scope import Scope, traverse_scope
        on = join.args.get('on')
        if not isinstance(on, exp.EQ) or not all(isinstance(c, exp.Column) and c.table for c in (on.this,on.expression)):
            return False
        parent = join.find_ancestor(exp.Select)
        scope = next((s for s in traverse_scope(parsed) if s.expression is parent), None)
        if scope is None or on.this.table == on.expression.table:
            return False
        for column in (on.this, on.expression):
            source = scope.sources.get(column.table)
            if not isinstance(source, Scope) or not isinstance(source.expression, exp.Select):
                return False
            query = source.expression
            group = query.args.get('group')
            if not group or len(group.expressions) != 1 or not isinstance(group.expressions[0], exp.Column):
                return False
            projection = next((p for p in query.expressions if p.alias_or_name == column.name), None)
            if projection is None or not isinstance(projection.unalias(), exp.Column):
                return False
            if group.expressions[0].name not in {projection.alias_or_name, projection.unalias().name}:
                return False
        return True

    @staticmethod
    def _scalar_cte_cross_join(parsed, join):
        scalar_names = set()
        for cte in parsed.find_all(exp.CTE):
            query = cte.this
            if not isinstance(query, exp.Select) or query.args.get("group"):
                continue
            if any(agg.find_ancestor(exp.Select) is query and not agg.find_ancestor(exp.Window)
                   for agg in query.find_all(exp.AggFunc)):
                scalar_names.add(cte.alias_or_name.lower())
        parent = join.find_ancestor(exp.Select)
        source = parent.args.get("from_") or parent.args.get("from") if parent else None
        if not source:
            return False
        sources = [source.this] + [item.this for item in parent.args.get("joins", [])]
        # Allow one non-scalar source alongside scalar CTEs.
        return (len(sources) >= 2 and all(isinstance(item, exp.Table) for item in sources)
                and sum(item.name.lower() not in scalar_names for item in sources) <= 1)

    def _allowed_join_pairs(self, relationships: Sequence[Relationship]) -> List[str]:
        allowed_pairs = []
        for relationship in relationships:
            allowed_pairs.append(f"{relationship.source_column}={relationship.target_column}")
            allowed_pairs.append(f"{relationship.target_column}={relationship.source_column}")
        return allowed_pairs

    def _allowed_columns_by_dataset(self, selected_datasets: Sequence[str]) -> List[str]:
        allowed_columns = []
        for dataset_id in selected_datasets:
            allowed_columns.extend(self._allowed_columns_for_table(get_table_name(dataset_id)).keys())
        return allowed_columns

    @staticmethod
    def _allowed_columns_for_table(table_name: str) -> Dict[str, dict]:
        table_to_dataset = {get_table_name(dataset_id): dataset_id for dataset_id in DATASETS_CONFIG.keys()}
        dataset_id = table_to_dataset.get(table_name)
        if not dataset_id:
            return {}
        metadata = json.loads(load_metadata(dataset_id))
        schema_columns = metadata.get("colunas_principais") or metadata.get("columns") or {}
        if not isinstance(schema_columns, dict):
            return {}
        if DATASETS_CONFIG[dataset_id].get("physical_column_case") == "lower":
            return {column_name.lower(): column_info for column_name, column_info in schema_columns.items()}
        return schema_columns

    @staticmethod
    def _extract_column_references(parsed) -> List[Dict[str, Optional[str]]]:
        column_names = []
        for column_node in parsed.find_all(exp.Column):
            column_name = column_node.name
            if column_name:
                table_name = column_node.table or None
                column_names.append({"table": table_name, "column": column_name})
        return column_names

    @staticmethod
    def _extract_output_aliases(parsed) -> List[str]:
        aliases = []
        for alias_node in parsed.find_all(exp.Alias):
            alias_name = alias_node.alias
            if alias_name:
                aliases.append(alias_name)
        return aliases

    @staticmethod
    def _contains_write_operation(parsed) -> bool:
        forbidden_names = ["Insert", "Update", "Delete", "Drop", "Create", "Alter", "Truncate"]
        forbidden_classes = []
        for class_name in forbidden_names:
            expression_class = getattr(exp, class_name, None)
            if expression_class is not None:
                forbidden_classes.append(expression_class)

        if not forbidden_classes:
            return False

        return any(isinstance(node, tuple(forbidden_classes)) for node in parsed.walk())

    @staticmethod
    def _normalize_join_condition(join_text: str) -> str:
        normalized = re.sub(r"\b[a-zA-Z_][\w]*\.", "", join_text.lower())
        normalized = re.sub(r"\s+", "", normalized)
        normalized = normalized.replace("`", "")
        return normalized

    @staticmethod
    def _preaggregated_join_pairs(parsed, relationship: Relationship) -> set[str]:
        """Retorna pares de chaves de saída de CTEs que agregam cada lado da relação."""

        def cte_key_alias(cte, physical_table: str, relationship_column: str) -> Optional[str]:
            query = cte.this
            table_names = {table.name.lower() for table in query.find_all(exp.Table)}
            if physical_table.lower() not in table_names:
                return None

            group = query.args.get("group")
            is_distinct = bool(query.args.get("distinct"))
            if group is not None:
                grouped_columns = {column.name.lower() for column in group.find_all(exp.Column)}
            elif is_distinct:
                grouped_columns = {
                    column.name.lower()
                    for expression in query.expressions
                    for column in expression.find_all(exp.Column)
                }
            else:
                return None

            if relationship_column.lower() not in grouped_columns:
                return None

            if not is_distinct and not any(isinstance(node, exp.AggFunc) for node in query.walk()):
                return None

            for expression in query.expressions:
                if isinstance(expression, exp.Alias):
                    source_columns = list(expression.this.find_all(exp.Column))
                    if any(column.name.lower() == relationship_column.lower() for column in source_columns):
                        return expression.alias.lower()
                if isinstance(expression, exp.Column) and expression.name.lower() == relationship_column.lower():
                    return expression.name.lower()

            return None

        source_aliases = []
        target_aliases = []
        for cte in list(parsed.find_all(exp.CTE)) + list(parsed.find_all(exp.Subquery)):
            source_alias = cte_key_alias(cte, relationship.source_table, relationship.source_column)
            if source_alias:
                source_aliases.append(source_alias)

            target_alias = cte_key_alias(cte, relationship.target_table, relationship.target_column)
            if target_alias:
                target_aliases.append(target_alias)

        pairs = set()
        for source_alias in source_aliases:
            for target_alias in target_aliases:
                pairs.add(f"{source_alias}={target_alias}")
                pairs.add(f"{target_alias}={source_alias}")
        return pairs

    @staticmethod
    def _is_preaggregated_srag_ubs_query(sql: str, selected_datasets: Sequence[str], normalized_join: str) -> bool:
        selected_set = set(selected_datasets)
        if selected_set != {"surtos-srag", "atencao-basica"}:
            return False

        sql_lower = sql.lower()
        if "count(*) as total_srag" not in sql_lower:
            return False

        if "count(distinct cnes) as total_ubs" not in sql_lower and "count(distinct a.cnes) as total_ubs" not in sql_lower:
            return False

        return normalized_join == "ibge=ibge"

    @staticmethod
    def _extract_tables_with_regex(sql: str, cte_names: Optional[Sequence[str]] = None) -> List[str]:
        tables = []
        cte_name_set = {name.lower() for name in cte_names or []}
        for match in re.finditer(r"\b(?:FROM|JOIN)\s+([a-zA-Z_][\w]*)", sql, re.IGNORECASE):
            table_name = match.group(1).lower()
            if table_name not in cte_name_set:
                tables.append(table_name)
        return tables

    @staticmethod
    def _extract_joins_with_regex(sql: str) -> List[str]:
        joins = []
        for match in re.finditer(r"\bON\s+(.+?)(?:\bJOIN\b|\bWHERE\b|\bGROUP BY\b|\bORDER BY\b|\bLIMIT\b|$)", sql, re.IGNORECASE | re.DOTALL):
            join_text = re.sub(r"\s+", " ", match.group(1).strip())
            joins.append(join_text)
        return joins

    @staticmethod
    def _extract_cte_names_with_regex(sql: str) -> List[str]:
        return [match.group(1).lower() for match in re.finditer(r"\b([a-zA-Z_][\w]*)\s+AS\s*\(", sql, re.IGNORECASE)]


multibase_service = MultibaseService()
