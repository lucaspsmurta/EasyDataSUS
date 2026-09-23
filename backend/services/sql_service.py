import re
import logging
import json
import os
import sys
from pathlib import Path

# Adicionar diretório parent (backend/) ao path para permitir imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.analytical_contract import SQL_INSTRUCTIONS, contract_errors, prepare_sql
from services.generation_diagnostics import record
from services.safe_fallback import fallback_sql
from llm.router import get_llm
from config.datasets import get_table_name, get_dataset_config

logger = logging.getLogger(__name__)


def _get_schema_columns(schema: dict) -> dict:
    """Retorna o mapa de colunas aceitando os formatos antigo e novo do schema."""

    if not isinstance(schema, dict):
        return {}

    for key in ("colunas_principais", "columns"):
        columns = schema.get(key)
        if isinstance(columns, dict) and columns:
            return columns

    return {}


def _get_schema_value(schema: dict, *keys: str, default=""):
    """Obtém o primeiro valor não vazio entre chaves alternativas do schema."""

    if not isinstance(schema, dict):
        return default

    for key in keys:
        value = schema.get(key)
        if value not in (None, "", {}, []):
            return value

    return default


def _get_column_text(column_info: dict, *keys: str, default=""):
    """Obtém o primeiro texto não vazio entre chaves alternativas da coluna."""

    if not isinstance(column_info, dict):
        return default

    for key in keys:
        value = column_info.get(key)
        if value not in (None, "", {}, []):
            return value

    return default


def _format_examples(examples) -> str:
    if isinstance(examples, list):
        return ", ".join(str(example) for example in examples)
    if examples not in (None, "", {}, []):
        return str(examples)
    return ""

def extract_sql(text: str) -> str:
    """Keep complete CTEs; reject partial SQL, prose and multiple statements."""
    from sqlglot import parse, exp
    if not isinstance(text, str) or not text.strip():
        return None
    blocks = re.findall(r"```(?:sql)?\s*([\s\S]*?)```", text, re.IGNORECASE)
    if len(blocks) > 1:
        return None
    candidate = blocks[0].strip() if blocks else text.strip()
    start = re.search(r"\b(?:WITH|SELECT)\b", candidate, re.IGNORECASE)
    if not start:
        return None
    candidate = candidate[start.start():].strip()
    try:
        statements = parse(candidate, read="clickhouse")
        if len(statements) != 1 or not isinstance(statements[0], exp.Query):
            return None
        return candidate.rstrip(';').strip()
    except Exception:
        return None

def validate_sql_syntax(sql: str, dataset: str = "covid-19-vacinacao", original_question: str = "") -> bool:
    """
    Valida sintaxe básica de SQL para um dataset específico.
    
    Args:
        sql: Query SQL a validar
        dataset: Dataset esperado (padrão: "covid-19-vacinacao")
        original_question: Pergunta original para validar consistência (ex: detectar SELECT * em "quantas...")
    
    Returns:
        True se SQL é válido, False caso contrário
    """
    if not sql:
        return False
    
    sql_clean = sql.strip().upper()
    sql_compact = re.sub(r"\s+", "", sql_clean)
    
    # Validação básica.
    if not (sql_clean.startswith("SELECT") or sql_clean.startswith("WITH")):
        logger.warning("SQL não começa com SELECT ou WITH")
        return False
    
    if "FROM" not in sql_clean:
        logger.warning("SQL não possui FROM")
        return False
    
    # Tabela esperada para o dataset.
    try:
        expected_table = get_table_name(dataset)
    except ValueError as e:
        logger.warning(f"Dataset inválido: {e}")
        return False
    
    if expected_table not in sql_clean.lower():
        logger.warning(f"SQL não referencia tabela '{expected_table}' do dataset '{dataset}'")
        return False
    
    # CRÍTICO: Validar que "SELECT *" não é usado para perguntas de contagem
    if original_question:
        original_lower = original_question.lower()
        is_count_question = any(original_lower.startswith(q) for q in ["quantas", "quantos", "qual é o total", "qual é a quantidade"])
        
        # Se é pergunta de contagem, NÃO pode ser SELECT *
        if is_count_question and "SELECT *" in sql_clean:
            logger.warning(f"ERRO CRÍTICO: Pergunta sobre 'quantas/quantos' gerou SELECT * (deve ser COUNT): {sql[:100]}")
            return False
    
    # Verificar comandos perigosos
    forbidden = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE", "TRUNCATE"]
    for cmd in forbidden:
        if f" {cmd} " in f" {sql_clean} ":
            logger.warning(f"SQL contém comando proibido: {cmd}")
            return False

    # Validação semântica mínima: impede agregações válidas sintaticamente,
    # mas incompatíveis com a intenção analítica da pergunta.
    question_lower = original_question.lower() if original_question else ""
    asks_by_state = any(term in question_lower for term in ("por estado", "por uf", "cada estado", "estados"))
    asks_municipality = any(term in question_lower for term in ("município", "municipio", "cidade"))
    asks_ranking = any(term in question_lower for term in ("maior", "maiores", "mais", "ranking", "top"))

    if dataset == "covid-19-vacinacao" and asks_by_state and asks_ranking:
        if "GROUP BY" not in sql_clean or not re.search(r"\b(?:COUNT|UNIQEXACT)\s*\(", sql_clean):
            logger.warning("Ranking de vacinação por estado exige GROUP BY e COUNT")
            return False
        if "MAX(PACIENTE_ENDERECO_UF)" in sql_clean:
            logger.warning("Código de UF não pode ser maximizado como métrica")
            return False

    if dataset == "leitos" and "uti" in question_lower:
        if "uti neonatal" in question_lower and "estado" in question_lower and any(term in question_lower for term in ("menor", "menores", "mínima", "minima")):
            required_fragments = ("SUM(UTI_NEONATAL_EXIST)", "GROUP BY UF", "MAX(COMP)")
            if not all(fragment in sql_clean for fragment in required_fragments):
                logger.warning("Menor quantidade de UTI neonatal por estado exige SUM(UTI_NEONATAL_EXIST), GROUP BY UF e competência mais recente")
                return False
        if asks_by_state and (
            "SUM(UTI_" not in sql_clean
            or "GROUP BY" not in sql_clean
            or "MAX(COMP)" not in sql_clean
        ):
            logger.warning("Capacidade de UTI por estado exige SUM, GROUP BY e competência mais recente")
            return False
        if original_question.lower().startswith("quais") and asks_municipality:
            if "COUNT(*)" in sql_clean or "WHERE" not in sql_clean or "MAX(COMP)" not in sql_clean:
                logger.warning("Listagem de municípios com UTI exige filtro de capacidade e competência")
                return False

    asks_ratio = any(
        term in question_lower
        for term in ("proporção", "proporcao", "percentual", "porcentagem", "em relação")
    )
    if dataset == "leitos" and asks_ratio and "leitos sus" in question_lower:
        required_fragments = (
            "SUM(LEITOS_SUS)",
            "SUM(LEITOS_EXISTENTES)",
            "MAX(COMP)",
        )
        if not all(fragment in sql_clean for fragment in required_fragments) or "/" not in sql_clean:
            logger.warning("Proporção de leitos SUS exige somas, divisão, agrupamento e competência mais recente")
            return False

    if dataset == "leitos" and any(term in question_lower for term in ("tipo de unidade", "tipo da unidade")) and any(term in question_lower for term in ("maior", "volume")):
        required_fragments = ("DS_TIPO_UNIDADE", "SUM(LEITOS_EXISTENTES)", "GROUP BY")
        if not all(fragment in sql_clean for fragment in required_fragments):
            logger.warning("Volume de leitos por tipo de unidade exige DS_TIPO_UNIDADE, SUM(LEITOS_EXISTENTES) e GROUP BY")
            return False

    if dataset == "surtos-srag" and asks_by_state:
        if "GROUP BY" not in sql_clean or not re.search(r"\b(?:COUNT|UNIQEXACT)\s*\(", sql_clean):
            logger.warning("Notificações de SRAG por estado exigem GROUP BY e COUNT")
            return False

    if dataset == "surtos-srag" and "distribuição" in question_lower and "sintoma" in question_lower:
        required_fragments = ("FEBRE", "TOSSE", "DISPNEIA")
        if not all(fragment in sql_clean for fragment in required_fragments):
            logger.warning("Distribuição de sintomas de SRAG exige campos clínicos de sintomas")
            return False

    if dataset == "surtos-srag" and asks_ratio and any(term in question_lower for term in ("comorbidade", "comorbidades")):
        required_fragments = ("CARDIOPATI", "DIABETES", "ASMA")
        if not all(fragment in sql_clean for fragment in required_fragments) or "/" not in sql_clean:
            logger.warning("Proporção de comorbidades exige campos de comorbidade divididos pelo total")
            return False

    if dataset == "atencao-basica" and asks_municipality and asks_ranking:
        if "GROUP BY" not in sql_clean or not re.search(r"\b(?:COUNT|UNIQEXACT)\s*\(", sql_clean):
            logger.warning("Ranking municipal de UBS exige GROUP BY e COUNT")
            return False
        if "MAX(IBGE)" in sql_clean:
            logger.warning("Código IBGE não pode ser maximizado como métrica")
            return False
    
    return True


def _format_columns_from_schema(schema: dict) -> str:
    """
    Formata informações de colunas a partir do schema JSON para uso no prompt.
    
    Args:
        schema: Dicionário do schema com "colunas_principais"
    
    Returns:
        String formatada com descrição das colunas
    """
    colunas_info = ""
    for col_name, col_info in _get_schema_columns(schema).items():
        tipo = _get_column_text(col_info, "tipo", "type", default="String")
        descricao = _get_column_text(col_info, "descricao", "description", default="")
        exemplos = _get_column_text(col_info, "exemplos", "examples", "valores_possiveis", default=[])
        
        colunas_info += f"- {col_name} ({tipo}): {descricao}"
        formatted_examples = _format_examples(exemplos)
        if formatted_examples:
            colunas_info += f" → Exemplos: {formatted_examples}"
        colunas_info += "\n"
    
    return colunas_info


def _generate_examples_for_dataset(dataset: str, schema: dict, table_name: str) -> str:
    """
    Gera exemplos SQL específicos para um dataset.
    
    Evita hardcoding mantendo exemplos genéricos por tema.
    Se não houver exemplos específicos, retorna exemplos genéricos.
    
    Args:
        dataset: ID do dataset
        schema: Dicionário do schema
    
    Returns:
        String com exemplos SQL formatados
    """
    examples_map = {
        "covid-19-vacinacao": """
EXEMPLO 1 - Genérico (sem filtro de vacina):
Pergunta: Quantas doses foram aplicadas em SP?
SELECT COUNT(*) FROM vacinacao WHERE paciente_endereco_uf = 'SP'

EXEMPLO 2 - Específico (com filtro de vacina):
Pergunta: Quantas doses de Pfizer foram aplicadas em SP?
SELECT COUNT(*) FROM vacinacao WHERE paciente_endereco_uf = 'SP' AND vacina_nome = 'Pfizer'

EXEMPLO 3 - Agrupar por vacina:
Pergunta: Quantas doses por vacina?
SELECT vacina_nome, COUNT(*) as total FROM vacinacao GROUP BY vacina_nome ORDER BY total DESC

EXEMPLO 4 - Com dose específica:
Pergunta: Quantas 2ª doses foram aplicadas?
SELECT COUNT(*) FROM vacinacao WHERE vacina_descricao_dose = '2ª dose'

EXEMPLO 5 - Evolução temporal:
Pergunta: Qual foi a evolução mensal de vacinação?
SELECT toYYYYMM(vacina_dataAplicacao) as mes, COUNT(*) as total FROM vacinacao GROUP BY mes ORDER BY mes

EXEMPLO 6 - Estatísticas numéricas:
Pergunta: Qual é a idade média das pessoas vacinadas?
SELECT AVG(paciente_idade) as idade_media FROM vacinacao

Pergunta: Qual é a idade mínima e máxima?
SELECT MIN(paciente_idade) as minima, MAX(paciente_idade) as maxima FROM vacinacao
        """,
        "leitos": """
EXEMPLO 1 - Capacidade total:
Pergunta: Qual é a capacidade total de leitos?
SELECT SUM(LEITOS_EXISTENTES) as total_leitos FROM leitos

EXEMPLO 2 - Leitos por estado:
Pergunta: Qual estado tem mais leitos?
SELECT UF, SUM(LEITOS_EXISTENTES) as total_leitos FROM leitos GROUP BY UF ORDER BY total_leitos DESC

EXEMPLO 3 - Leitos SUS por estado:
Pergunta: Qual é a cobertura SUS por estado?
SELECT UF, SUM(LEITOS_EXISTENTES) as leitos_total, SUM(LEITOS_SUS) as leitos_sus, ROUND((SUM(LEITOS_SUS) / SUM(LEITOS_EXISTENTES)) * 100, 2) as percentual_sus FROM leitos GROUP BY UF ORDER BY percentual_sus DESC

EXEMPLO 4 - UTI disponível:
Pergunta: Quantos leitos de UTI adulto estão disponíveis pelo SUS?
SELECT SUM(UTI_ADULTO_SUS) as uti_adulto_sus FROM leitos

EXEMPLO 5 - UTI especializada com filtro:
Pergunta: Quais cidades têm UTI neonatal?
SELECT MUNICIPIO, UF, UTI_NEONATAL_EXIST FROM leitos WHERE UTI_NEONATAL_EXIST > 0 ORDER BY MUNICIPIO LIMIT 100

EXEMPLO 6 - Por tipo de gestão:
Pergunta: Qual é a distribuição de leitos por tipo de gestão?
SELECT TP_GESTAO, SUM(LEITOS_EXISTENTES) as total_leitos, SUM(LEITOS_SUS) as leitos_sus FROM leitos GROUP BY TP_GESTAO ORDER BY total_leitos DESC

EXEMPLO 7 - UTI por região:
Pergunta: Qual região tem mais leitos de UTI?
SELECT REGIAO, SUM(UTI_TOTAL_EXIST) as uti_total FROM leitos GROUP BY REGIAO ORDER BY uti_total DESC
        """,
        "surtos-srag": """
EXEMPLO 1 - Total de notificações por UF:
Pergunta: Quantos casos de SRAG foram notificados por estado?
SELECT SG_UF_NOT, COUNT(*) as total FROM srag GROUP BY SG_UF_NOT ORDER BY total DESC

EXEMPLO 2 - Casos por ano:
Pergunta: Qual ano teve mais notificações?
SELECT year(DT_NOTIFIC) as ano, COUNT(*) as total FROM srag GROUP BY ano ORDER BY total DESC

EXEMPLO 3 - Casos por sexo:
Pergunta: Qual a distribuição por sexo?
SELECT CS_SEXO, COUNT(*) as total FROM srag GROUP BY CS_SEXO ORDER BY total DESC

EXEMPLO 4 - Idade média:
Pergunta: Qual é a idade média dos casos?
SELECT AVG(NU_IDADE_N) as idade_media FROM srag
        """,
        "atencao-basica": """
EXEMPLO 1 - Total de UBS por UF:
Pergunta: Quantas UBS existem por estado?
SELECT UF, COUNT(*) as total FROM atencao_basica GROUP BY UF ORDER BY total DESC

EXEMPLO 2 - UBS por município:
Pergunta: Quais municípios têm mais UBS?
SELECT IBGE, COUNT(*) as total FROM atencao_basica GROUP BY IBGE ORDER BY total DESC

EXEMPLO 3 - UBS por bairro:
Pergunta: Qual é a distribuição de UBS por bairro?
SELECT BAIRRO, COUNT(*) as total FROM atencao_basica GROUP BY BAIRRO ORDER BY total DESC

EXEMPLO 4 - Coordenadas geográficas:
Pergunta: Quais UBS têm latitude e longitude válidas?
SELECT NOME, UF, IBGE, LATITUDE, LONGITUDE FROM atencao_basica WHERE LATITUDE IS NOT NULL AND LONGITUDE IS NOT NULL LIMIT 100
        """,
    }
    
    # Retorna exemplos específicos se existem, senão um genérico
    return examples_map.get(dataset, f"""
EXEMPLO 1: Contar linhas
SELECT COUNT(*) FROM {table_name or 'tabela'}

EXEMPLO 2: Agrupar por coluna
SELECT coluna1, COUNT(*) as total FROM {table_name or 'tabela'} GROUP BY coluna1 ORDER BY total DESC

EXEMPLO 3: Com filtro
SELECT COUNT(*) FROM {table_name or 'tabela'} WHERE coluna1 = 'valor'
    """)


def _get_sql_rules_for_dataset(dataset: str, schema: dict) -> str:
    """
    Gera regras de SQL específicas para um dataset com base em seu schema.
    
    Args:
        dataset: ID do dataset
        schema: Dicionário do schema
    
    Returns:
        String com regras formatadas
    """
    rules_map = {
        "covid-19-vacinacao": """
Regras para vacinação:
1. Conte registros com COUNT(*); pessoas/municípios distintos exigem COUNT(DISTINCT chave).
2. Se pergunta menciona estado → use paciente_endereco_uf
3. Se pergunta menciona município → use paciente_endereco_nmMunicipio
4. Se pergunta menciona NOME DE VACINA ESPECÍFICO (Pfizer, AstraZeneca, etc) → filtre com vacina_nome
5. Filtre por vacina_nome apenas quando uma vacina específica for mencionada
6. Use vacina_descricao_dose com rótulos '1ª Dose', '2ª Dose', 'Reforço'. Se a pergunta fornecer literal exato, preserve-o; busca sem distinguir maiúsculas exige normalização explícita.
7. Se pergunta menciona data/período → use vacina_dataAplicacao
8. Se pergunta menciona "idade" (média, mínima, máxima) → use paciente_idade com AVG/MIN/MAX
9. Se pergunta menciona "sexo" → use paciente_enumSexoBiologico com COUNT(*) GROUP BY
10. Não use DATE() ou datetime() - use toDate(), toYYYYMM()
11. Respeite maiúsculas/minúsculas de estados ('SP', não 'sp')
12. Igualdade literal usa =; busca parcial sem distinção de maiúsculas usa positionCaseInsensitiveUTF8.
13. Só use LIMIT quando explicitamente solicitado; preserve todos os empates.
        """,
        "leitos": """
Regras para leitos:
1. Se pergunta menciona "leitos" genericamente → use LEITOS_EXISTENTES
2. Se pergunta menciona "leitos SUS" → use LEITOS_SUS
3. Se pergunta menciona "UTI" → use UTI_TOTAL_EXIST ou UTI_TOTAL_SUS
4. Se pergunta menciona "UTI adulto" → use UTI_ADULTO_EXIST ou UTI_ADULTO_SUS
5. Se pergunta menciona "UTI pediátrica" → use UTI_PEDIATRICO_EXIST ou UTI_PEDIATRICO_SUS
6. Se pergunta menciona "UTI neonatal" → use UTI_NEONATAL_EXIST ou UTI_NEONATAL_SUS
7. Se pergunta menciona "UTI queimados" → use UTI_QUEIMADO_EXIST ou UTI_QUEIMADO_SUS
8. Se pergunta menciona "UTI coronariana" → use UTI_CORONARIANA_EXIST ou UTI_CORONARIANA_SUS
9. Use SUM() para colunas de leitos (LEITOS_*, UTI_*) ao agrupar por estado/região/município
10. Se pergunta menciona "qual tem mais", "qual estado", "ranking" com leitos → use SUM() + GROUP BY + ORDER BY DESC
11. Se pergunta menciona estado → use UF
12. Se pergunta menciona região → use REGIAO
13. Se pergunta menciona cidade/município → use MUNICIPIO
14. Se pergunta menciona "tipo de gestão" → use TP_GESTAO
15. Percentual SUS: 100.0 * SUM(LEITOS_SUS) / NULLIF(SUM(LEITOS_EXISTENTES), 0).
16. Para contar capacidade de leitos, use SUM() em colunas de capacidade
17. Não limite resultados sem pedido explícito.
18. Leitos são fotografias por competência: ao agregar capacidade sem período explícito, filtre COMP = (SELECT MAX(COMP) FROM leitos)
19. Se a pergunta mencionar competência mais recente, o filtro pela maior COMP é obrigatório
        """,
    "surtos-srag": """
Regras para SRAG:
1. Se perguntar por estado/UF, use SG_UF_NOT
2. Se perguntar por município de notificação, use CO_MUN_NOT
3. Se perguntar por sexo, use CS_SEXO
4. Idade usa NU_IDADE_N e TP_IDADE: 1=dias, 2=meses, 3=anos; não trate dias/meses como anos.
5. Se perguntar por notificação ou período, use DT_NOTIFIC
6. Se perguntar por início dos sintomas, use DT_SIN_PRI
7. Série mensal usa ano e mês; semana epidemiológica usa SEM_NOT com o ano de DT_NOTIFIC.
8. Para distribuição por categoria, use GROUP BY com COUNT(*)
9. Não assuma nomes de municípios quando a base só tiver código IBGE
    """,
    "atencao-basica": """
Regras para atenção básica:
1. Se perguntar por quantidade de UBS, use COUNT(*)
2. Se perguntar por estado, use UF
3. Se perguntar por município, use IBGE
4. Se perguntar por nome da unidade, use NOME
5. Se perguntar por bairro, use BAIRRO
6. Se perguntar por geolocalização, use LATITUDE e LONGITUDE
7. Não use SUM() para contar unidades; use COUNT(*)
8. Não limite resultados sem pedido explícito.
    """,
    }
    
    # Retorna regras específicas do dataset.
    return rules_map.get(dataset, "")


def generate_sql(
    question,
    metadata,
    model_name,
    dataset: str = "covid-19-vacinacao",
    return_mode: bool = False,
    sql_validator=None,
):
    """
    Gera SQL com contexto de domínio e uma tentativa de correção.
    
    Usa metadados, contrato analítico e fallback de gramática restrita.
    
    Args:
        question: Pergunta em linguagem natural
        metadata: JSON string com metadados do dataset (inclui schema)
        model_name: Nome do modelo LLM
        dataset: ID do dataset (padrão: "covid-19-vacinacao")
    
    Returns:
        Query SQL válida ou None se falhar
    """
    logger.info(f"Gerando SQL para: {question[:50]}... (dataset: {dataset})")

    def pack(sql_value, mode):
        return (sql_value, mode) if return_mode else sql_value

    strategy = os.getenv("SQL_GENERATION_STRATEGY", "deterministic_first").lower()
    if strategy == "deterministic_first":
        deterministic = fallback_sql(question, dataset)
        if deterministic:
            return pack(deterministic, "deterministic_rule")

    llm = get_llm(model_name)
    
    # Schema informado pelos metadados.
    try:
        schema_info = json.loads(metadata)
    except json.JSONDecodeError:
        logger.error(f"Erro ao parsejar metadata JSON para dataset {dataset}")
        return pack(fallback_sql(question, dataset), "deterministic_fallback")
    
    # Tabela física do dataset.
    try:
        table_name = get_table_name(dataset)
    except ValueError as e:
        logger.error(f"Dataset inválido: {e}")
        return pack(fallback_sql(question, dataset), "deterministic_fallback")
    
    # Colunas disponíveis para o prompt.
    colunas_info = _format_columns_from_schema(schema_info)
    schema_columns = _get_schema_columns(schema_info)
    schema_description = _get_schema_value(schema_info, "descricao", "description", default="N/A")
    
    # Regras específicas do dataset.
    dataset_rules = _get_sql_rules_for_dataset(dataset, schema_info)

    prompt = f"""Você gera SQL ClickHouse. Responda apenas SQL.
{SQL_INSTRUCTIONS}
Dataset: {dataset}; tabela: {table_name}
Descrição: {schema_description}
Colunas e significados:
{colunas_info}
Regras do domínio:
{dataset_rules}
Pergunta: {question}
"""

    try:
        response = llm.generate(
            prompt,
            num_predict=int(os.getenv("OLLAMA_SQL_NUM_PREDICT", "512")),
            temperature=0.0,
            timeout_s=int(os.getenv("OLLAMA_SQL_TIMEOUT", "180")),
            max_retries=1,
        )
        logger.debug(f"Resposta LLM (primeira 200 chars): {response[:200]}")
        
        sql = extract_sql(response)
        errors = []
        for attempt in range(2):
            try:
                sql = prepare_sql(sql, question) if sql else None
                errors = contract_errors(sql, question, schema_columns) if sql else ["SQL vazio"]
                if sql and not validate_sql_syntax(sql, dataset, question):
                    errors.append("Consulta inválida ou incompatível com a intenção")
                if sql:
                    from services.multibase_service import multibase_service
                    canonical = multibase_service.canonicalize_sql_identifiers(sql, [dataset])
                    errors.extend(multibase_service.validate_sql(canonical, [dataset], []).errors)
                    sql = canonical
                    if not errors and sql_validator is not None:
                        errors.extend(sql_validator(sql))
            except Exception:
                errors = ["SQL não pôde ser analisado"]
            record('sql_validation', attempt=attempt + 1, sql=sql, errors=list(errors))
            if not errors:
                break
            logger.warning("SQL rejeitada na tentativa %s: %s", attempt + 1, "; ".join(errors))
            if attempt == 0:
                response = llm.generate(
                    prompt + "\nCorrija a tentativa anterior:\n" + str(sql) +
                    "\nProblemas: " + "; ".join(errors),
                    num_predict=int(os.getenv("OLLAMA_SQL_NUM_PREDICT", "512")),
                    temperature=0.0, timeout_s=int(os.getenv("OLLAMA_SQL_TIMEOUT", "180")), max_retries=1,
                )
                sql = extract_sql(response)
        if errors:
            fallback = fallback_sql(question, dataset)
            return pack(fallback, "deterministic_fallback" if fallback else "llm_error")

        logger.info(f"SQL gerado com sucesso para {dataset}: {sql[:50]}...")
        return pack(sql, "llm")
        
    except Exception as e:
        logger.error(f"Erro ao gerar SQL: {e}")
        record('sql_generation_exception', error=str(e))
        return pack(fallback_sql(question, dataset), "deterministic_fallback")
