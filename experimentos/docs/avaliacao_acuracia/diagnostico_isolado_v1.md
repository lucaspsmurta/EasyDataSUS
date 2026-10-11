# Auditoria do diagnóstico isolado — 29/09/2026

## Conclusão

O protocolo simplificado e a troca entre os dois modelos locais testados não produziram justificativas suficientemente confiáveis para avaliação autônoma. O Llama obteve mais concordâncias de rótulos, mas manteve erros concretos e uma resposta inválida. Não foi alterado o modelo padrão nem o avaliador oficial.

## Desenho do teste

Foram executadas oito chamadas por modelo: formulação e suporte separados para Q12, Q65 e Q68, mais dois controles sintéticos de formulação. Os controles usam o mesmo enunciado sobre lojas com vendas altas, com e sem uma definição explícita do corte no contexto. As expectativas dos controles não foram enviadas ao modelo.

Qwen2.5-coder:7b e Llama3.1:8b receberam exatamente as mesmas entradas, prompts, esquema e opções. Temperatura 0, seed 42, contexto 4096 e teto de 900 tokens. Uma tentativa por chamada, sem retentativa ou promoção de respostas inválidas. Justificativas não são cortadas pelo programa nem por limites de caracteres no esquema; saídas truncadas por tokens ou justificativas vazias são rejeitadas.

A formulação recebeu somente pergunta/contexto. O suporte recebeu campos deduplicados do mapeamento v6 e inventário compacto dos relacionamentos. Essa seleção é parcial e pode conter erros; o teste isola o julgamento sobre ela, não mede extração/mapeamento completos. Não foram fornecidos gabaritos, notas anteriores, referência assistida ou respostas SQL. A referência só foi usada após as execuções para contar concordâncias.

O endpoint mudou após a ativação dos contêineres. Confirmou-se o Qwen disponível antes dos testes; nenhum DeepSeek foi executado e nenhum modelo foi baixado. O Ollama informou size_vram=0 durante a execução do Qwen.

## Resultados

| Modelo/protocolo | Células com resposta válida | Concordâncias estritas | Tempo Q12/Q65/Q68 | Controles de ambiguidade |
|---|---:|---:|---:|---:|
| Qwen v6 anterior | 14/15 | 6/14 | 21,6 min | Não executados |
| qwen2.5-coder:7b isolado | 15/15 | 4/15 | 3.86 min | 1/2 |
| llama3.1:8b isolado | 13/15 | 8/13 | 4.13 min | 2/2 |

Os dois diagnósticos, incluindo controles, levaram 4,62 e 5,04 minutos, respectivamente. O menor tempo não é ganho equivalente de desempenho: foram retiradas extração e mapeamento, reduzidos contexto, formato e verificações. Houve uma execução por configuração, sem estimar variabilidade. Classificações not_assessable contam como rótulos válidos estruturalmente, não como julgamentos substantivos.

## Inspeção das justificativas

- Qwen, Q12: exige fonte/contexto sem demonstrar necessidade; confunde fabricante com unidade contada; exige coluna total para COUNT; reprova suporte por relações irrelevantes a uma consulta de uma base.
- Qwen, Q65: responde com regras gerais de COUNT/SUM, sem analisar o campo UTI_TOTAL_SUS fornecido.
- Qwen, Q68: afirma que só existe geocódigo para leitos, embora LEITOS_SUS tenha sido enviado; também exige coluna total para contar registros.
- Llama, Q12: reconhece contagem de registros, mas inventa uma leitura contraditória de fabricante não vazio e alega falta de relação quando uma base basta.
- Llama, Q65: reconhece seleção indefinida, porém devolve suporte sem justificativa. A chamada inteira de suporte foi rejeitada neste diagnóstico, deixando duas células sem resposta aceita.
- Llama, Q68: aprova especificidade sem resolver alto/baixa; a justificativa de disponibilidade apenas repete instruções gerais.
- Controle definido: ambos aprovam ausência de ambiguidade. O Llama ainda confunde unidade e medida na justificativa de especificidade.
- Controle indefinido: Qwen responde não avaliável; Llama reprova ambiguidade, mas sua explicação é menos direta que a lacuna explícita do corte. Concordância de rótulo não basta para validar raciocínio.

## Decisão e próximos passos

Não promover o diagnóstico para produção nem ampliar automaticamente a avaliação. Não substituir notas pelo conteúdo da referência. Os resultados não justificam considerar qualquer dos dois modelos validado.

Para avançar metodologicamente: obter revisão humana da rubrica e dos exemplos; registrar a qualidade das justificativas, além dos rótulos; preparar casos adicionais antes de testar outra configuração. Verificações de campos e conectividade podem ser calculadas pelo programa como fatos auxiliares, mas não devem converter um mapeamento falível automaticamente em aprovação.

## Reproduzir

Use prefixo novo; o diagnóstico recusa sobrescrever arquivos existentes.

```powershell
python -m backend.evaluation.question_quality_diagnostic --report experimentos/qualidade_perguntas_v4_avaliador_v6.json --output-prefix experimentos/diagnostico_isolado_qwen_v2 --model qwen2.5-coder:7b
```

Para repetir com Llama, altere o modelo para llama3.1:8b e o prefixo. Não é necessário repetir agora; as duas execuções já foram concluídas.

Código validado por 25 testes locais, incluindo isolamento das entradas e rejeição de justificativas inválidas. Esses testes não demonstram qualidade semântica das respostas dos modelos.
