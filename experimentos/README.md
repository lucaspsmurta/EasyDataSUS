# Experimentos da dissertação

Esta pasta pode ser versionada no Git. Os resultados e as referências permanecem nos caminhos usados pelos scripts e pela dissertação; a subpasta `docs/` reúne os catálogos e a documentação necessários para sua consulta e reprodução.

O pacote histórico reúne 37 arquivos de evidência e 19 arquivos de documentação, além do índice e do manifesto original. A revisão manual posterior possui pasta e manifesto próprios, descritos abaixo. Nem todos são resultados principais: as seções abaixo distinguem resultados, referências e diagnósticos de apoio.

As assinaturas dos arquivos estão no [manifesto do pacote](MANIFESTO.json). Os resultados foram preservados sem reclassificação. A limpeza retirou checkpoints parciais, arquivos deprecated, diagnósticos substituídos e resultados de catálogos anteriores que não sustentam a análise atual.

## Resultados principais

| Material | Papel na dissertação |
|---|---|
| `test_results_68_questoes_{deepseek,qwen,llama}_v{1,2,3}.json` (9 arquivos) | Três execuções de cada modelo no experimento operacional. |
| [Acurácia v5/r2](acuracia_qwen_catalogo_v5_r2.json) | Rodada apresentada: 52/64 correspondências, 56/64 sucessos operacionais e quatro limitações reconhecidas. |
| [Referências v5](referencias_68_catalogo_v5.json) | Resultados candidatos e assinatura do recorte utilizados nas rodadas v5. |
| [Acurácia v5/r1](acuracia_qwen_catalogo_v5_r1.json) | Outra execução completa do mesmo catálogo, mantida para rastreabilidade; não foi agregada aos resultados da r2. |
| [Qualidade das respostas](qualidade_respostas_v5_r2_revisada_ia.md) e [JSON consolidado](qualidade_respostas_v5_r2_revisada_ia.json) | Sete dimensões aplicadas às 56 respostas finais disponíveis. |
| [Fichas assistidas](qualidade_respostas_v5_r2.revisao_ia.json), [parecer](parecer_qualidade_respostas_v5_r2.md) e [evidência de metadados](qualidade_respostas_v5_r2.evidencia_metadados.json) | Origem e justificativas dos 392 julgamentos iniciais. |
| [Relatório automático](qualidade_respostas_v5_r2.md) e [JSON automático](qualidade_respostas_v5_r2.json) | Estado anterior à incorporação dos julgamentos, citado no parecer. |
| [Ficha pendente de revisão](qualidade_respostas_v5_r2.review.json) | Instrumento para registrar a revisão posterior pelo autor, separado da origem assistida. Sua existência não comprova preenchimento ou aprovação. |

## Referências históricas necessárias

O [pacote v3](referencias_68_catalogo_v3.json) permanece porque é entrada do [recálculo em Python](docs/avaliacao_acuracia/conferencia_referencias_v3.py) e da [revisão técnica](docs/avaliacao_acuracia/revisao_tecnica_referencias_68_v3.md) descritos no capítulo 4. Os catálogos v3, v4 e v5 estão em `docs/avaliacao_acuracia/`; os dois anteriores sustentam a rastreabilidade e dependências dos scripts. Antigo não significa dispensável.

## Qualidade das perguntas: evidência exploratória

Foram mantidos 16 arquivos para conferir os diagnósticos descritos no texto e nos pareceres:

- Relatórios JSON dos avaliadores v4, v5, v5.1 e v6 sobre perguntas do catálogo v4, além do piloto Llama e do diagnóstico de mapeamento v5.1.
- Comparações v5.1 e v6 com a referência assistida, em JSON e Markdown.
- Relatório legível do avaliador v6.
- Diagnósticos isolados Qwen e Llama, em JSON e Markdown, e seu resumo.

Veja a [auditoria dos pilotos](docs/avaliacao_acuracia/auditoria_perguntas_v5.md), o [diagnóstico isolado](docs/avaliacao_acuracia/diagnostico_isolado_v1.md) e o [guia atual](docs/avaliacao_acuracia/qualidade_perguntas.md). Esses registros sustentam a constatação de inconsistências; não certificam a qualidade das 68 perguntas nem equivalem a uma avaliação dos novos enunciados v5.

## Reprodução e estado metodológico

Os comandos atualizados estão no [guia de avaliação](docs/avaliacao_acuracia/README.md). Use novos nomes para novas saídas. O pacote utilizado continua sem aprovação formal registrada das referências. As fichas iniciais de qualidade das respostas mantêm sua origem assistida por IA; a revisão posterior do autor é uma etapa diferente.

Este pacote contém as evidências selecionadas para a dissertação. O backend e os testes permanecem na raiz do repositório; os dados brutos não fazem parte deste pacote. Consulte as [instruções de reprodução](#reanalisar-os-resultados-sem-banco-ou-llm) e o [manifesto](MANIFESTO.json).

## Reanalisar os resultados sem banco ou LLM

Na raiz do repositório, com as dependências Python do backend instaladas:

```powershell
python -m backend.evaluation.quality --results experimentos/acuracia_qwen_catalogo_v5_r2.json --references experimentos/referencias_68_catalogo_v5.json --review experimentos/qualidade_respostas_v5_r2.revisao_ia.json --output-prefix experimentos/reconsolidacao_v1
```

Esse comando reconsolida as classificações preservadas, sem nova avaliação humana, execução SQL ou chamada à LLM. Use um prefixo ainda inexistente para cada saída.

## Executar uma nova avaliação

É necessário configurar o backend, iniciar ClickHouse e Ollama, disponibilizar o modelo e carregar as bases. Os CSVs brutos e arquivos `.env` não são incluídos neste pacote. A carga deve corresponder à assinatura do pacote de referências para utilizar os valores esperados preservados.

```powershell
python -m backend.evaluation.accuracy run --references experimentos/referencias_68_catalogo_v5.json --model qwen2.5-coder:7b --generation-strategy llm_first --allow-draft --output experimentos/acuracia_nova.json
```

`--allow-draft` permite um ensaio com referências candidatas; não registra aprovação. Para preparar referências em outro recorte, indique explicitamente o catálogo e um novo arquivo de saída:

```powershell
python -m backend.evaluation.accuracy prepare --catalog experimentos/docs/avaliacao_acuracia/catalogo_68_v5.json --output experimentos/referencias_novas.json
```

Uma mudança nos dados ou nas referências produz outra condição de avaliação. Os arquivos históricos permanecem associados ao recorte e às regras originais. O commit informado no manifesto identifica o código observado no empacotamento, não certifica a versão de código utilizada em cada execução histórica.


## Entradas dos scripts históricos

Alguns scripts e testes usam os catálogos em `docs/` na raiz do projeto. Em um clone novo, sem essa pasta local, restaure as entradas publicadas antes de usar esses scripts:

```powershell
Copy-Item -LiteralPath experimentos/docs -Destination . -Recurse
```

Os resultados já estão em seus caminhos originais. A documentação local em `/docs/` continua ignorada pelo Git. Para novas execuções, use nomes novos e selecione para commit somente os resultados que pretende preservar. O arquivo local `manifesto_dissertacao.json` registra a limpeza anterior e permanece ignorado; o manifesto público é [MANIFESTO.json](MANIFESTO.json).

## Revisão manual dos dois perfis

A pasta [avaliacao_manual](avaliacao_manual/README.md) reúne a ficha preenchida, o template sem julgamentos e a consolidação das rodadas uniformes r1. Esses materiais são citados nos capítulos 4 e 6 e não modificam os indicadores automáticos nem o manifesto histórico.

## Novas execuções dos dois perfis

As rodadas uniformes r2 preservam novas execuções completas de 68 casos por perfil, com Qwen2.5-Coder 7B e estratégia `llm_first`.

| Execução | Correspondência com referências | Sucesso operacional | Limitações reconhecidas |
|---|---|---|---|
| [Perfil de usuário, r2](acuracia_qwen_usuario_uniforme_r2.json) | 46/64 (71,88%) | 62/64 (96,88%) | 4/4 |
| [Perfil técnico, r2](acuracia_qwen_tecnico_uniforme_r2.json) | 55/64 (85,94%) | 61/64 (95,31%) | 4/4 |

Os totais coincidem com os das rodadas r1, mas os registros individuais das execuções são distintos. Os arquivos preservam os metadados originais, inclusive os indicadores de referências em rascunho. A revisão manual documentada da r1 não é transferida automaticamente para estas rodadas. Estes resultados complementares não substituem os arquivos analisados na dissertação nem alteram o manifesto histórico.
