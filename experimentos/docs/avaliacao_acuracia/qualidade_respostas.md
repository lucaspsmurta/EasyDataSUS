# Avaliação da qualidade das respostas por dimensão

O módulo `backend.evaluation.quality` analisa uma execução de acurácia já finalizada. Não altera o sistema, não chama LLM/ClickHouse e não reclassifica a acurácia anterior. A avaliação da qualidade das perguntas é uma etapa separada e não foi implementada aqui.

Os resultados utilizados na dissertação já estão no [relatório consolidado v5/r2](../../qualidade_respostas_v5_r2_revisada_ia.md). Os comandos abaixo geram novas saídas, sem substituir esse registro.

## Uso

Na raiz do projeto:

```powershell
python -m backend.evaluation.quality --results experimentos/acuracia_qwen_catalogo_v5_r2.json --references experimentos/referencias_68_catalogo_v5.json --output-prefix experimentos/qualidade_respostas_v5_r2_nova
```

São gerados três arquivos: `.json` com todas as classificações/evidências, `.md` com a matriz e os indicadores e `.review.json` com as fichas qualitativas pendentes. Para repetir, use outro prefixo. Os arquivos de entrada e saídas anteriores não são sobrescritos. A análise confere a integridade da referência, sua associação à execução, os IDs e os enunciados e exige execução finalizada com assinatura de dados inalterada. Preserva a indicação de referências em rascunho.

## O que é automático

Seleção exata de bases e relacionamentos, SQL final aprovado, sucesso operacional, equivalência estrita registrada contra referência, quantidade de linhas/colunas e reconhecimento de limitações previstas. Essas dimensões têm critérios objetivos e seus resultados não certificam o significado analítico da consulta. O relatório preserva a precisão, recall e F1 anteriores em `original_summary`; seleção exata por pergunta é um indicador diferente de recall por item.

## O que precisa ser revisado

| Dimensão | Aprovação | Exemplo de reprovação ou parcial |
|---|---|---|
| Filtros | Todas as restrições solicitadas e relevantes estão presentes, sem restrições indevidas. | Omitir exclusão de coordenadas zero: reprovação. |
| Unidade e agregação | Entidade, DISTINCT, agrupamentos, denominadores e junções correspondem à pergunta. | Agrupar UBS por nome da unidade quando se pede município: reprovação. |
| Dimensões e identificadores | Campos, códigos e unidades de saída identificam o objeto solicitado. | Nome de município quando se pede código: parcial se a identidade puder ser confirmada; justificar a correspondência. |
| Informação principal | Todas as medidas e entidades centrais estão corretas. | Informação extra não reprova por si só esta dimensão. Uma parcela correta de pedido composto pode ser parcial. |
| Completude e escopo | Todos os grupos/medidas solicitados, com limites e extremos corretos. | Ranking inteiro quando se pede somente extremos: reprovação de escopo. |
| Formato da saída | Colunas, ordem exigida e representação correspondem ao contrato. | Coluna extra: reprovação nesta dimensão, independentemente do valor principal. |
| Fidelidade do texto | Texto corresponde à tabela e aos limites dos dados. | Inventar valor ou inferir cobertura nacional de um recorte local: reprovação. |

Use `pass` quando todo o critério for atendido, `fail` quando a falha comprometer o critério e `partial` somente quando uma parte identificável estiver atendida e outra não, com ambas descritas na evidência. `partial` não vale meio ponto nem entra como aprovação. Use `not_applicable` apenas com justificativa quando a operação realmente não se aplica (por exemplo, ausência de filtros pedidos), nunca para ocultar falha ou ausência de resposta. Ambiguidade que impeça julgamento deve permanecer `pending` com discussão no protocolo; não invente referência.

O avaliador não marca automaticamente como qualitativamente correta uma resposta que coincidiu com a referência. SQLs incorretos podem coincidir em um recorte. Também não marca como correta uma explicação só por ter sido gerada no modo `llm_grounded`.

## Preenchimento e consolidação

O arquivo `.review.json` contém uma entrada por dimensão elegível. Inspecione a pergunta, o SQL e a resposta no JSON de resultados, e o SQL/tabela esperados no pacote de referência. Preencha, por exemplo:

```json
{
  "id": 6,
  "dimension": "output_contract",
  "status": "fail",
  "evidence": "A referência solicita categoria e percentual; a resposta contém também uma coluna de contagem.",
  "reviewer": "Nome real de quem realizou a revisão",
  "reviewed_at": "2026-09-24",
  "review_kind": "human"
}
```

Use `human` para uma revisão efetivamente realizada por pessoa; use `ai_assisted` para um parecer assistido ainda não assumido por revisor humano, identificando corretamente sua procedência. O script separa as contagens por método no JSON; não certifica as declarações de autoria. Não substitua esses campos por nomes ou datas fictícias. É possível consolidar uma revisão parcial; as demais dimensões permanecem pendentes.

```powershell
python -m backend.evaluation.quality --results experimentos/acuracia_qwen_catalogo_v5_r2.json --references experimentos/referencias_68_catalogo_v5.json --review experimentos/qualidade_respostas_v5_r2_nova.review.json --output-prefix experimentos/qualidade_respostas_v5_r2_nova_revisada
```

## Denominadores

- `applicable`: casos em que a dimensão se aplica, incluindo pendências e respostas impossíveis de avaliar.
- `evaluated`: somente `pass`, `partial` e `fail`.
- Aprovação/reprovação/parcial: contagem da categoria dividida por `evaluated`.
- Cobertura: `evaluated / applicable`. Sempre mostrar junto ao percentual de aprovação.
- `pending`: existe material para avaliação, mas a classificação ainda não foi concluída.
- `not_assessable`: não há resposta analítica final, texto ou metadado suficiente para avaliar a dimensão.
- `not_applicable`: dimensão não se aplica ao caso. As quatro limitações previstas são analisadas separadamente.

As falhas técnicas permanecem como não acertos na métrica estrita e como falhas operacionais; não viram aprovações qualitativas pela ausência de resultado. As dimensões se sobrepõem: uma pergunta pode falhar em filtro, valor e completude simultaneamente. Não some percentuais entre dimensões. Não conclua que 94% passaram qualitativamente porque 6% receberam uma classificação de erro.

Para um percentual sobre todas as 64 perguntas, use a contagem da classificação sobre 64 e mantenha visíveis os não avaliados. Não apresente uma aprovação entre os poucos revisados como se cobrisse o conjunto inteiro. Os resultados continuam sendo avaliação de desenvolvimento e não medem qualidade das perguntas, utilidade clínica ou generalização.
