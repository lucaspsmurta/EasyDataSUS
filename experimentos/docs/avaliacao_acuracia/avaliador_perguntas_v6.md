# Avaliador de perguntas v6

Este documento descreve o protocolo aplicado aos enunciados do catálogo v4 nos diagnósticos preservados. O catálogo atual de novas perguntas é o v5.

A rubrica e a referência assistida permanecem iguais. O protocolo mudou, portanto use um novo prefixo; não reutilize checkpoints v5.1.

Mudanças:
- Verificação explícita de necessidade de contexto, completude da operação e interpretações alternativas, registrada no JSON e Markdown.
- Esquema restringe combinações de status com verificação/limitação; validação local também rejeita contradições se o servidor não cumprir o esquema.
- Conectividade usa o inventário de relacionamentos: uma única base não exige integração. Ausência de relacionamento não permite concluir impossibilidade.
- Incompatibilidade de metadados exige evidência de campo mapeado.
- Mapeamento usa a entrada completa em trechos, sem repetir fatos extraídos como requisitos separados. Os fatos continuam disponíveis na avaliação da formulação.

Não há regras por ID, notas copiadas da referência nem promoção de pendências a aprovação. O modelo ainda pode errar a interpretação ou a pertinência de campos. Nenhum ganho de acurácia ou de tempo foi medido nesta alteração; os 23 testes locais usam respostas simuladas quando necessário e não executam inferência real.

Executar o diagnóstico:

```powershell
python -m backend.evaluation.question_quality --catalog docs/avaliacao_acuracia/catalogo_68_v4.json --output-prefix experimentos/qualidade_perguntas_v4_avaliador_v6_nova --ids 12 65 68 --resume --timeout 600
```

Comparar o relatório novo:

```powershell
python -m backend.evaluation.question_quality_compare --reference backend/evaluation/references/question_quality_12_65_68.json --report experimentos/qualidade_perguntas_v4_avaliador_v6_nova.json --output-prefix experimentos/comparacao_referencia_v6_nova
```

Esses três casos são diagnósticos conhecidos. Antes de ampliar o uso, revisar também casos novos com critérios definidos independentemente das respostas do modelo. A concordância de rótulos não valida as justificativas.
