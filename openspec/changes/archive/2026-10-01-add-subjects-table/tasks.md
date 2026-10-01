# Implementation Tasks

- [x] 1. Delegar ao agente especializado **Xano Table Designer** conforme definido no [AGENTS.md](../../AGENTS.md) <!-- id: 1 -->
- [x] 2. Criar o arquivo `tables/subjects.xs` contendo o schema com os campos: `id`, `created_at`, `name`, `teacher`, `hours` e `user_id` <!-- id: 2 -->
- [x] 3. Configurar a relação de chave estrangeira em `user_id` apontando para a tabela `user` <!-- id: 3 -->
- [x] 4. Definir os índices da tabela (`primary` em `id`, `btree` em `user_id`, `btree` em `created_at`) <!-- id: 4 -->
- [x] 5. Sincronizar as alterações com o backend Xano via `push_all_changes_to_xano` <!-- id: 5 -->
