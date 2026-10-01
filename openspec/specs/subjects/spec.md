# Spec: Tabela `subjects` (Disciplinas)

## Requirements

### Requirement 1: Definição da Entidade `subjects`
O sistema DEVE possuir uma tabela chamada `subjects` no diretório `tables/` configurada para armazenar disciplinas acadêmicas.
- O atributo `auth` DEVE ser `false` (autenticação permanece restrita à tabela `user`).
- A tabela DEVE conter um identificador primário auto-incremental `id` do tipo `int`.
- A tabela DEVE conter o campo padrão de auditoria `created_at` do tipo `timestamp?=now` com visibilidade `private`.

### Requirement 2: Atributos da Disciplina
A tabela DEVE conter os seguintes campos informativos:
1. `name`: tipo `text`, com filtro `trim`, obrigatório, representando o nome da matéria/disciplina.
2. `teacher`: tipo `text`, com filtro `trim`, obrigatório, representando o nome do professor.
3. `hours`: tipo `int`, com filtro `min:0`, representando a carga horária em horas.

### Requirement 3: Vínculo com Usuário Autenticado
A tabela DEVE registrar a posse/associação do registro com o usuário:
- Campo `user_id`: tipo `int`, referenciando explicitamente a tabela `user` (`table = "user"`).

### Requirement 4: Indexação
A tabela DEVE definir os seguintes índices para integridade e performance:
- Índice `primary` no campo `id`.
- Índice `btree` no campo `user_id` para busca eficiente de disciplinas por usuário.
- Índice `btree` no campo `created_at` (ordenação `desc`) para listagens cronológicas.

## Scenarios

### Scenario 1: Cadastro de nova disciplina
- **Given** um usuário existente com `id = 1`
- **When** uma nova disciplina for inserida com `name = "Estrutura de Dados"`, `teacher = "Prof. Silva"`, `hours = 80`, `user_id = 1`
- **Then** o registro deve ser persistido com `id` gerado automaticamente e associado ao usuário 1.

### Scenario 2: Isolamento e integridade
- **Given** consultas à tabela `subjects` filtradas por `user_id`
- **When** o usuário busca suas disciplinas
- **Then** a consulta deve utilizar o índice em `user_id` retornando apenas os registros vinculados àquele usuário.
