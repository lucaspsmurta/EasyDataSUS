# Auditoria do piloto v5 — Q12, Q65 e Q68

## Qwen 2.5 Coder 7B

Execução local de 28/09/2026, relatório
`experimentos/qualidade_perguntas_v4_avaliador_v5.json`.
As tentativas exploratórias anteriores (`v5_piloto` e `v5_piloto2`) foram
interrompidas para corrigir o protocolo e não entram nesta comparação.

| Medida | v4 | v5 |
|---|---:|---:|
| Chamadas registradas | 11 | 14 |
| Tempo acumulado nas chamadas | 1.685,81 s | 1.063,80 s |
| Tokens de entrada registrados pelo Ollama | 46.955 | 21.934 |
| Dimensões aceitas tecnicamente, dentre 15 | 8 | 14 |
| Dimensões pendentes | 7 | 1 |

O tempo caiu aproximadamente 37% e os tokens de entrada, 53%. São medições locais
de duas execuções, não um benchmark controlado; carga da máquina e cache podem variar.
Aceitação técnica não mede acurácia semântica.

## Achados da revisão assistida

- Q12: o mapeamento final utiliza apenas o campo de fabricante da base de vacinação.
  Empates e apresentação não aparecem mais como requisitos separados. O suporte de
  implementação foi aceito sem inventar uma integração com UBS. Disponibilidade
  permaneceu pendente por contradição entre status e limitação.
  A justificativa de especificidade ainda confunde fabricante com unidade contada;
  a contagem é de registros. A penalização contextual continua genérica.
- Q65: o modelo encontrou `UTI_TOTAL_SUS` e `UF` na base de leitos. Porém associou
  `SG_UF` à UF de notificação, embora o schema descreva UF de residência;
  `SG_UF_NOT` corresponde à notificação. A ausência de integração cadastrada pode
  limitar suporte de implementação, mas não demonstra ausência dos campos.
  O julgamento de ausência de ambiguidade não examina quantos estados compõem
  o ranking solicitado por “maior número”.
- Q68: o modelo encontrou campos de leitos, mas aprovou ausência de ambiguidade
  sem definir “alto número” e “baixa disponibilidade”. Isso é uma falha semântica
  central. Também usou código de município como se identificasse UBS, sem distinguir
  agrupamento de estabelecimento, e misturou disponibilidade com integração.

## Conclusão deste piloto

A v5 reduziu custo e respostas estruturalmente inválidas. O Qwen 2.5 Coder 7B ainda
não demonstrou qualidade suficiente para avaliar automaticamente as 68 perguntas.
O relatório continua preliminar; não converter a melhora de conclusão técnica em
alegação de melhora equivalente de acurácia. Os testes de código não substituem esta
auditoria. Uma comparação com outro modelo deve manter o mesmo protocolo e registrar
separadamente seus resultados, sem sobrescrever este relatório.

## Comparação exploratória com Llama 3.1 8B

Foi aplicado o mesmo protocolo a Q68, no relatório separado
`experimentos/qualidade_perguntas_v4_avaliador_v5_llama_piloto.json`.
O modelo marcou ambiguidade como `fail`, mas sua justificativa sugeriu que muitos
casos e UBS poderiam implicar poucos leitos, em vez de explicar limites alternativos
para “alto” e “baixo”. A mudança do rótulo, portanto, não demonstra acerto do julgamento.

A extração omitiu o requisito de disponibilidade de leitos. Como o mapeamento depende
dos fatos extraídos, essa omissão é um risco de perda de requisitos nas etapas seguintes.
A primeira tentativa de formulação também alegou ausência de população apesar de
extrair “municípios”; a nova verificação rejeitou essa contradição e exigiu correção.
Esse exemplo comprova o funcionamento de uma barreira estrutural, mas não a correção
semântica da resposta final. O teste isolado não sustenta recomendar troca de modelo.

O teste levou 435,99 s e terminou com quatro dimensões aceitas e uma pendente.
Disponibilidade recebeu `pass` com evidência de código de município, sem comprovar
leitos. Esse falso positivo motivou a v5.1: além dos fatos extraídos, o mapeamento
recebe obrigatoriamente passagens que cobrem todo o enunciado e o contexto. A lista
de requisitos deixa de depender exclusivamente da completude da extração.

O teste direcionado dessa correção fica em
`experimentos/diagnostico_mapeamento_v5_1.json`. Ele reutiliza explicitamente os fatos
incompletos do piloto Llama para reproduzir o defeito; executa apenas mapeamento e
suporte. Não é uma avaliação completa nova nem deve ser somado à comparação v4/v5.

Nesse diagnóstico, o mapeamento recuperou `field:leitos:LEITOS_EXISTENTES` e
`field:leitos:LEITOS_SUS` a partir do enunciado completo, apesar de os fatos herdados
omitirem leitos. A etapa levou aproximadamente 247 s. Isso confirma a recuperação dessa omissão
específica; não comprova a completude de qualquer extração nem a acurácia dos rótulos.

O diagnóstico completo consumiu 329,28 s em três chamadas. As duas classificações
de suporte passaram pela validação estrutural, mas a revisão ainda encontrou
justificativas insuficientes: disponibilidade citou apenas campos de municípios e
notificação, e implementação recebeu `fail` por relacionamento “não configurado
corretamente”, sem demonstrar incompatibilidade. Não se recomenda ampliar a execução
automática às 68 perguntas com esses modelos com base apenas nesse resultado.

O código final é v5.1; 16 testes automatizados passaram, incluindo preservação do
enunciado quando a extração omite requisitos. A execução completa de três perguntas
foi feita na v5; a última correção foi validada no diagnóstico direcionado acima.
