# Avaliações utilizadas na dissertação

Este guia preserva os caminhos de trabalho originais. Para utilizar as entradas diretamente desta pasta ou restaurar a estrutura local em um clone novo, consulte o [README do pacote](../../README.md).

O catálogo atual é o [v5](catalogo_68_v5.json), com [versão legível](catalogo_68_v5.md). Ele contém 68 IDs: 64 perguntas analíticas e quatro limitações previstas. Há quatro pares repetidos, totalizando 64 enunciados distintos. Os enunciados foram reformulados; não são idênticos aos do experimento operacional original.

## Evidências mantidas

O [índice dos experimentos](../../README.md) identifica as evidências e seus papéis. Os arquivos brutos preservam conteúdo, autoria, datas e assinaturas originais.

| Avaliação | Arquivos principais |
|---|---|
| Operacional, três modelos e três execuções | `experimentos/test_results_68_questoes_<modelo>_v<execucao>.json` |
| Acurácia apresentada na dissertação | [v5, rodada 2](../../acuracia_qwen_catalogo_v5_r2.json) e [referências v5](../../referencias_68_catalogo_v5.json) |
| Outra rodada completa do mesmo catálogo | [v5, rodada 1](../../acuracia_qwen_catalogo_v5_r1.json), preservada separadamente |
| Qualidade das respostas | [Relatório consolidado](../../qualidade_respostas_v5_r2_revisada_ia.md), [fichas iniciais assistidas](../../qualidade_respostas_v5_r2.revisao_ia.json) e [parecer](../../parecer_qualidade_respostas_v5_r2.md) |
| Conferência das referências | [Revisão técnica v3](revisao_tecnica_referencias_68_v3.md), [recálculo](conferencia_referencias_v3.py) e [resultados](conferencia_referencias_v3_resultado.json) |
| Qualidade das perguntas, exploratória | [Auditoria do piloto](auditoria_perguntas_v5.md), [diagnóstico isolado](diagnostico_isolado_v1.md) e [referência assistida de três casos](referencia_perguntas_12_65_68.md) |

Na v5/r2, houve 52/64 correspondências com referências candidatas (81,25%), 56/64 sucessos operacionais (87,5%), quatro divergências e oito falhas técnicas. As quatro limitações previstas foram reconhecidas. As sete dimensões qualitativas examinam as 56 respostas finais disponíveis; seus percentuais não devem ser somados.

## Estado das referências e dos julgamentos

As referências do pacote utilizado continuam sem aprovação formal registrada (`reference_reviewed=false`, `valid_for_claims=false`). Executar SQL sem erro ou obter concordância com um recálculo não aprova automaticamente sua interpretação. A comparação mede equivalência de resultados no recorte, não identidade textual do SQL nem equivalência em qualquer base.

A inspeção inicial das respostas foi assistida por IA, com procedência preservada nas fichas. A dissertação registra a revisão posterior pelo autor; a ficha pendente mantida permite documentar suas confirmações ou alterações separadamente. Não foi medida concordância entre revisores independentes.

O avaliador de perguntas usa Ollama, apresentou inconsistências e permanece exploratório. Seus diagnósticos históricos usam o catálogo v4; não representam uma avaliação concluída dos novos enunciados v5.

## Executar uma nova rodada de acurácia

Na raiz do projeto, com as dependências do backend, ClickHouse e Ollama disponíveis, use o pacote existente somente se os dados carregados ainda coincidirem com sua assinatura. Não recarregue as tabelas durante uma execução. Use um nome de saída ainda inexistente:

```powershell
python -m backend.evaluation.accuracy run --references experimentos/referencias_68_catalogo_v5.json --model qwen2.5-coder:7b --generation-strategy llm_first --allow-draft --output experimentos/acuracia_qwen_catalogo_v5_r3.json
```

`--allow-draft` permite o ensaio com referências candidatas; não registra aprovação humana. O script chama o mesmo fluxo do endpoint diretamente, sem exigir que o servidor Swagger esteja aberto. Não executa três repetições implicitamente.

Após revisar o catálogo ou mudar os dados, prepare um pacote novo, informando o catálogo explicitamente:

```powershell
python -m backend.evaluation.accuracy prepare --catalog docs/avaliacao_acuracia/catalogo_68_v5.json --output experimentos/referencias_68_catalogo_v5_nova_preparacao.json
```

A preparação executa as consultas de referência no ClickHouse, sem LLM, e registra resultados e assinatura dos dados. Depois use o novo pacote no comando `run`. Não edite o pacote congelado. Mudanças nos enunciados, SQLs ou comparação exigem versionamento; execuções antigas não devem ser renomeadas como se usassem as entradas novas.

Quando a revisão de uma ficha for efetivamente realizada, registre no catálogo `review_status`, `reviewer` e `reviewed_at`, com responsável e data reais, antes de preparar outro pacote. Esses campos registram a decisão, não substituem a revisão. Após aprovação de todas as fichas, a execução pode dispensar `--allow-draft`.

## Analisar as respostas por dimensões

O [guia de qualidade das respostas](qualidade_respostas.md) explica rubrica, denominadores e revisão. Para reconsolidar as fichas assistidas existentes, sem chamar o banco ou a LLM:

```powershell
python -m backend.evaluation.quality --results experimentos/acuracia_qwen_catalogo_v5_r2.json --references experimentos/referencias_68_catalogo_v5.json --review experimentos/qualidade_respostas_v5_r2.revisao_ia.json --output-prefix experimentos/qualidade_respostas_v5_r2_reconsolidada
```

Use novo prefixo em cada consolidação. Para uma nova rodada do sistema, forneça seu resultado e as referências correspondentes; as fichas da rodada antiga são vinculadas à sua origem e não devem ser reaproveitadas como julgamentos da nova.

## Qualidade das perguntas e versões históricas necessárias

Veja o [guia das perguntas](qualidade_perguntas.md). O catálogo v5 orienta novas avaliações. Os catálogos [v3](catalogo_68_v3.json) e [v4](catalogo_68_v4.json) foram preservados porque sustentam, respectivamente, a conferência das referências e a origem da reformulação v5, testes locais e diagnósticos exploratórios. O pacote v3 é entrada da conferência em Python.

Resultados antigos de desenvolvimento, checkpoints parciais, duplicatas e materiais deprecated foram retirados. A limpeza e os hashes das evidências mantidas constam no [manifesto](../../MANIFESTO.json).
