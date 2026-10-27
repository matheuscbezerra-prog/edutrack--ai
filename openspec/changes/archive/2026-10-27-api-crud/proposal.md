# Proposal: Endpoints CRUD com Isolamento de Usuário para `subjects` e `academic_tasks`

## Why

Atualmente, o EduTrack AI possui as tabelas `subjects` e `academic_tasks` definidas na base de dados (`tables/subjects.xs` e `tables/academic_tasks.xs`), mas não disponibiliza endpoints REST para que a aplicação frontend execute operações de criação, leitura, atualização e exclusão (CRUD). Além disso, é requisito fundamental de segurança e privacidade acadêmica que cada usuário acesse e gerencie exclusivamente seus próprios dados (multi-tenancy por usuário), impedindo que qualquer usuário visualize ou manipule disciplinas ou tarefas pertencentes a terceiros.

## What Changes

- Criação dos endpoints CRUD RESTful para a entidade `subjects` (POST, GET, PATCH, DELETE), associando e filtrando registros estritamente pelo `user_id` do usuário autenticado.
- Criação dos endpoints CRUD RESTful para a entidade `academic_tasks` (POST, GET, PATCH, DELETE), garantindo que apenas tarefas vinculadas a disciplinas pertencentes ao usuário autenticado possam ser criadas, listadas, atualizadas ou excluídas.
- Aplicação de autenticação obrigatória (`auth = "user"`) em todos os endpoints, utilizando `$auth.id` como âncora de segurança.

## Capabilities

### Modified Capabilities
- `subjects`: Adição de requisitos para endpoints CRUD com isolamento de dados por usuário autenticado.
- `academic-tasks`: Adição de requisitos para endpoints CRUD com controle de acesso validado através do relacionamento com `subjects`.

## Impact

- Novos arquivos de endpoints XanoScript no diretório `apis/`.
- Isolamento estrito de dados entre usuários em todas as operações de banco de dados.
- Viabilização do consumo direto pela camada frontend (Streamlit).

