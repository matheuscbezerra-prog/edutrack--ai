# subjects Specification

## Purpose

Define the database structure and CRUD REST API endpoints for managing academic subjects in EduTrack AI with strict user data isolation.

## Requirements

### Requirement 1: Definição da Entidade `subjects`
O sistema DEVE possuir uma tabela chamada `subjects` no diretório `tables/` configurada para armazenar disciplinas acadêmicas.
- O atributo `auth` DEVE ser `false` (autenticação permanece restrita à tabela `user`).
- A tabela DEVE conter um identificador primário auto-incremental `id` do tipo `int`.
- A tabela DEVE conter o campo padrão de auditoria `created_at` do tipo `timestamp?=now` com visibilidade `private`.

#### Scenario 1: Cadastro de nova disciplina
- **WHEN** uma nova disciplina for inserida com `name = "Estrutura de Dados"`, `teacher = "Prof. Silva"`, `hours = 80`, `user_id = 1`
- **THEN** o registro deve ser persistido com `id` gerado automaticamente e associado ao usuário 1.

### Requirement 2: Atributos da Disciplina
A tabela DEVE conter os seguintes campos informativos:
1. `name`: tipo `text`, com filtro `trim`, obrigatório, representando o nome da matéria/disciplina.
2. `teacher`: tipo `text`, com filtro `trim`, obrigatório, representando o nome do professor.
3. `hours`: tipo `int`, com filtro `min:0`, representando a carga horária em horas.

### Requirement 3: Vínculo com Usuário Autenticado
A tabela DEVE registrar a posse/associação do registro com o usuário:
- Campo `user_id`: tipo `int`, referenciando explicitamente a tabela `user` (`table = "user"`).

#### Scenario 2: Isolamento e integridade
- **WHEN** o usuário busca suas disciplinas
- **THEN** a consulta deve utilizar o índice em `user_id` retornando apenas os registros vinculados àquele usuário.

### Requirement 4: Indexação
A tabela DEVE definir os seguintes índices para integridade e performance:
- Índice `primary` no campo `id`.
- Índice `btree` no campo `user_id` para busca eficiente de disciplinas por usuário.
- Índice `btree` no campo `created_at` (ordenação `desc`) para listagens cronológicas.

### Requirement: Authenticated user creates subject
The system SHALL provide a POST `/subjects` endpoint allowing authenticated users to create a subject associated with their authenticated `user_id`.

#### Scenario: Successfully create a subject
- **WHEN** an authenticated user sends a POST request to `/subjects` with valid subject fields (`name`, `teacher`, `hours`)
- **THEN** the system stores the record with `user_id` set to the authenticated user's ID and returns the created subject

#### Scenario: Unauthenticated request is rejected
- **WHEN** an unauthenticated client sends a POST request to `/subjects`
- **THEN** the system rejects the request with an authentication error

### Requirement: Authenticated user lists their subjects
The system SHALL provide a GET `/subjects` endpoint returning only the subjects belonging to the authenticated user.

#### Scenario: Query own subjects
- **WHEN** an authenticated user sends a GET request to `/subjects`
- **THEN** the system returns only the subjects where `user_id` matches the authenticated user's ID

### Requirement: Authenticated user updates their subject
The system SHALL provide a PATCH `/subjects/{id}` endpoint allowing authenticated users to update only subjects they own.

#### Scenario: Successfully update owned subject
- **WHEN** an authenticated user sends a PATCH request to `/subjects/{id}` with valid update data for a subject they own
- **THEN** the system updates the subject record and returns the updated subject

#### Scenario: Attempt to update another user's subject
- **WHEN** an authenticated user sends a PATCH request to `/subjects/{id}` for a subject owned by another user
- **THEN** the system denies the operation and preserves existing data

### Requirement: Authenticated user deletes their subject
The system SHALL provide a DELETE `/subjects/{id}` endpoint allowing authenticated users to delete only subjects they own.

#### Scenario: Successfully delete owned subject
- **WHEN** an authenticated user sends a DELETE request to `/subjects/{id}` for a subject they own
- **THEN** the system removes the subject record and returns a success response

#### Scenario: Attempt to delete another user's subject
- **WHEN** an authenticated user sends a DELETE request to `/subjects/{id}` for a subject owned by another user
- **THEN** the system denies the operation and does not delete the record
