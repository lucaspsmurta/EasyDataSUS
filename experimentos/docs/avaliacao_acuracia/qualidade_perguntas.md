# Avaliação da qualidade das perguntas

O módulo `backend.evaluation.question_quality` avalia enunciados usando Ollama, sem executar consultas SQL. As classificações são preliminares. A avaliação histórica permaneceu exploratória; suas inconsistências estão na [auditoria do piloto](auditoria_perguntas_v5.md) e no [diagnóstico isolado](diagnostico_isolado_v1.md).

O avaliador implementa o protocolo v6 e usa o catálogo v5 por padrão. Os relatórios preservados com nomes `qualidade_perguntas_v4_avaliador_*` foram produzidos com enunciados v4. A versão do avaliador e a versão do catálogo são identificações diferentes. Não reaproveite checkpoints entre catálogos ou protocolos.

O procedimento separa formulação, extração de requisitos, mapeamento para metadados e suporte. Validações locais verificam estrutura, evidências e consistência, mas não certificam a correção semântica da LLM. Metadados também não comprovam cobertura dos dados ou execução do sistema.

## Preparar fichas sem chamar a LLM

```powershell
python -m backend.evaluation.question_quality --catalog docs/avaliacao_acuracia/catalogo_68_v5.json --output-prefix experimentos/qualidade_perguntas_v5_nova --prepare-only
```

Use um prefixo novo. São gerados JSON com o estado da avaliação, relatório Markdown e fichas `.review.json`. As fichas permitem registrar avaliação documentada por pergunta e critério. Criar os arquivos não conclui a avaliação.

## Executar o avaliador exploratório

Com Ollama disponível, uma execução pode ser iniciada ou retomada no mesmo prefixo, desde que entradas, metadados, modelo e protocolo coincidam:

```powershell
python -m backend.evaluation.question_quality --catalog docs/avaliacao_acuracia/catalogo_68_v5.json --output-prefix experimentos/qualidade_perguntas_v5_nova --ids 12 65 68 --resume --timeout 600
```

`--ids` limita os casos executados; os demais continuam pendentes. Remover esse argumento solicita a avaliação do restante do catálogo. Inspecione os julgamentos antes de ampliar o uso. Temperatura zero e seed fixa não garantem correção. As respostas brutas e tentativas são preservadas, inclusive quando rejeitadas. Falhas ou classificações pendentes não equivalem a reprovação da pergunta.

## Rubrica proposta

1. Completude contextual: escopo necessário de população, período, local e filtros.
2. Especificidade analítica: medida, entidade contada, agrupamento e comparação.
3. Ausência de ambiguidade: interpretações alternativas que mudam o resultado.
4. Disponibilidade dos dados: possibilidade de resposta segundo os metadados.
5. Suporte da implementação: recursos e relacionamentos descritos nos metadados.

As três primeiras dimensões tratam da formulação; as duas últimas são condições de resposta. Metadados não comprovam cobertura dos CSVs nem funcionamento do código. Ausência de evidência deve resultar em `not_assessable`, não em uma conclusão positiva. Falta de suporte não implica pergunta mal formulada.

Estados: `pass`, `partial`, `fail`, `not_applicable`, `not_assessable`, `pending`. O percentual de atendimento usa apenas pass/partial/fail, com denominador explícito. Não se calcula nota global; categorias diferentes podem apontar a mesma deficiência e não devem ser somadas como falhas independentes.

## Contexto e prevenção de influência dos gabaritos

Somente ID e enunciado são extraídos do catálogo. SQLs, resultados esperados, especificações privadas, bases esperadas e comportamento esperado não são enviados à LLM. Por padrão, não há contexto adicional. Se havia contexto efetivamente disponível ao sistema, forneça um arquivo de texto com `--context-file caminho.txt`, usando outro prefixo. Não inclua gabaritos ou informações vistas apenas pelo avaliador. Os metadados atuais são disponibilizados para avaliar suporte; não completam silenciosamente o enunciado nas dimensões de formulação.

Para comparar versões originais, use `--question-field original_question` e outro prefixo. A comparação deve reconhecer que os metadados são os atuais, não necessariamente os históricos. Não altere os enunciados do experimento já realizado a partir das sugestões: crie outra versão.

## Revisão

No `.review.json`, preencha as entradas revisadas com status, `justification`, `reviewer`, `reviewed_at` (data ISO, por exemplo `2026-09-25`) e `review_kind` (`human` ou `ai_assisted`). Mantenha as demais como `pending`. Confirmar uma classificação também exige esse registro.

```powershell
python -m backend.evaluation.question_quality --catalog docs/avaliacao_acuracia/catalogo_68_v5.json --output-prefix experimentos/qualidade_perguntas_v5_nova --review experimentos/qualidade_perguntas_v5_nova.review.json
```

São gerados `.reviewed.json` e `.reviewed.md` sem chamar a LLM; a avaliação preliminar permanece no arquivo original. Use os mesmos argumentos de catálogo, modelo, contexto e campo da execução original. As contagens de revisadas não significam revisão independente: o tipo e o responsável ficam registrados.

## Fundamentação e limites

Esta é uma rubrica proposta por adaptação, não uma escala validada extraída de uma publicação. Completude e especificidade podem ser discutidas como dimensão e subdimensão com o orientador. A avaliação pelo mesmo modelo usado para gerar SQL pode compartilhar vieses; a revisão humana continua necessária.

- Wang e Strong (1996). Beyond Accuracy: What Data Quality Means to Data Consumers. https://courses.washington.edu/geog482/resource/14_Beyond_Accuracy.pdf — completude e adequação à tarefa, originalmente sobre dados.
- Pipino, Lee e Wang (2002). Data Quality Assessment. https://web.mit.edu/tdqm/www/tdqmpub/PipinoLeeWangCACMApr02.pdf — avaliação contextual de qualidade de dados; adaptação para perguntas.
- Bhaskar et al. (2023). Benchmarking and Improving Text-to-SQL Generation under Ambiguity. https://aclanthology.org/2023.emnlp-main.436/ — ambiguidade em perguntas Text-to-SQL.
- Wang et al. (2023). Know What I don't Know: Handling Ambiguous and Unknown Questions for Text-to-SQL. https://aclanthology.org/2023.findings-acl.352/ — perguntas ambíguas e não respondíveis.
