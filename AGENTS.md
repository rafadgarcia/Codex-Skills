# Preferências globais de execução

## Preferência de execução para tarefas complexas

Ao receber uma tarefa, priorize qualidade, completude e confiabilidade, não a tentativa de fazer tudo monoliticamente.

- Se a tarefa for simples ou couber confortavelmente em uma única execução, faça-a diretamente, sem criar etapas artificiais.
- Se a complexidade, quantidade de requisitos, tamanho do código ou necessidade de validação puder prejudicar a qualidade, decomponha a tarefa em etapas menores e coerentes.
- Faça essa decomposição por conta própria. O usuário não precisa pedir explicitamente que a tarefa seja dividida.
- Execute as etapas sequencialmente e de forma autônoma, sem parar para pedir confirmação entre elas, salvo quando faltar uma informação realmente indispensável ou existir uma decisão importante que não possa ser inferida com segurança.
- Sempre que possível, valide o resultado de cada etapa antes de avançar, usando testes, build, lint, type-check, inspeção do resultado ou outro método apropriado.
- Não sacrifique requisitos, simplifique silenciosamente, deixe TODOs ou finja concluir partes apenas para conseguir terminar tudo em uma única passagem.
- Se perceber durante a execução que a tarefa ficou maior ou mais complexa do que parecia inicialmente, pode reorganizar o plano e subdividi-la mais.
- O objetivo é concluir o pedido inteiro, mesmo que internamente sejam necessárias várias etapas.

Em resumo: decomponha quando isso aumentar a confiabilidade; não decomponha apenas por conveniência. Planeje internamente, execute autonomamente e não omita requisitos para caber tudo de uma vez.

## Verificação em tarefas de programação

Antes de considerar o trabalho concluído, verifique o estado real do projeto. Quando aplicável, rode testes, lint, type-check e build e corrija problemas introduzidos pelas alterações. Preserve o comportamento existente que não foi solicitado alterar.
