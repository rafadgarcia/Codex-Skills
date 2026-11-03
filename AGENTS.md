# Preferências globais de execução

## Roteamento de skills

Ative a menor combinação de skills que cubra o pedido. Use uma skill de domínio como principal e acrescente outra apenas quando ela tratar de uma necessidade concreta.

- **Interface e produto visual:** `$frontend-design` para implementar ou polir interfaces; `$ui-ux-pro-max` para pesquisa de padrões e recomendações de design; `$site-recreation` para reconstruir um site com referências locais; `$ui-responsive-audit` para auditoria de breakpoints; `$playwright-interactive` para depuração interativa no navegador/Electron.
- **Next.js e deploy:** `$nextjs-16-modern` para Next.js 16+ App Router; `$docker-caddy-vps` para Docker, Compose, Caddy ou deploy VPS.
- **Dados e APIs:** `$restful-api` para contratos HTTP/REST; `$typescript-engineering` para tipos, validação runtime e toolchain TypeScript; `$postgres-best-practices` para projeto e desempenho PostgreSQL; use `$prisma-client-api` para queries/transações, `$prisma-database-setup` para configuração de banco, `$prisma-cli` para comandos ORM/CLI e `$prisma-upgrade-v7` para migração v6→v7. `$prisma-postgres` cobre provisionamento Prisma Postgres.
- **Cloudflare:** `$cloudflare` para escolha de produtos/arquitetura; `$workers-best-practices` para código/configuração de Workers; `$wrangler` antes de comandos Wrangler; `$turnstile-spin` para Turnstile.
- **Integrações e auditoria:** `$webhook-handler-patterns` para receivers de webhook; `$audit-logging` para trilhas de alterações sensíveis, não para logs comuns.
- **Engenharia reversa (REA):** `$reverse-engineer-anything` para análise de artefatos/runtime; `$rea-tool-design` para contratos e ferramentas REA; `$rea-changelog-update` para changelogs/releases REA.

Ao usar `$rea-tool-design` ou `$rea-changelog-update`, os guias do projeto REA podem não estar instalados localmente; abra os links GitHub dessas skills como fonte de orientação.

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
