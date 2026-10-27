# Tasks

## 1. Endpoints CRUD para `subjects`

- [x] 1.1 Criar endpoint POST `/subjects` para cadastro de disciplina vinculado ao usuário autenticado (`user_id = $auth.id`)
- [x] 1.2 Criar endpoint GET `/subjects` para listagem de disciplinas filtradas por `user_id == $auth.id`
- [x] 1.3 Criar endpoint PATCH `/subjects/{id}` para atualização de disciplina pertencente ao usuário autenticado
- [x] 1.4 Criar endpoint DELETE `/subjects/{id}` para exclusão de disciplina pertencente ao usuário autenticado

## 2. Endpoints CRUD para `academic_tasks`

- [x] 2.1 Criar endpoint POST `/academic_tasks` para criação de tarefa acadêmica com validação de que `subject_id` pertence ao usuário autenticado
- [x] 2.2 Criar endpoint GET `/academic_tasks` para listagem de tarefas acadêmicas vinculadas a disciplinas do usuário autenticado
- [x] 2.3 Criar endpoint PATCH `/academic_tasks/{id}` para atualização de tarefa acadêmica pertencente a disciplina do usuário autenticado
- [x] 2.4 Criar endpoint DELETE `/academic_tasks/{id}` para exclusão de tarefa acadêmica pertencente a disciplina do usuário autenticado

