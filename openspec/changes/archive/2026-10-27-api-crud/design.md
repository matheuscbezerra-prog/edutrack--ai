# Design: Endpoints CRUD para `subjects` e `academic_tasks`

## Context

O EduTrack AI possui as tabelas `subjects` e `academic_tasks` estruturadas em `tables/subjects.xs` e `tables/academic_tasks.xs`.
- A tabela `subjects` possui a coluna `user_id` vinculada diretamente à tabela `user`.
- A tabela `academic_tasks` possui a coluna `subject_id` vinculada à tabela `subjects`.

Para suportar as operações da interface do usuário (Streamlit) garantindo a privacidade acadêmica e segurança dos dados, é necessário expor endpoints RESTful completos (POST, GET, PATCH, DELETE) com autenticação obrigatória (`auth = "user"`) e validação estrita de isolamento (multi-tenancy por usuário).

## Goals / Non-Goals

**Goals:**
- Fornecer endpoints CRUD completos para a entidade `subjects`:
  - POST `/subjects`: Criação de disciplina associando automaticamente `user_id` ao `$auth.id`.
  - GET `/subjects`: Listagem restrita às disciplinas pertencentes ao `$auth.id`.
  - PATCH `/subjects/{id}`: Atualização de disciplina garantindo que `user_id == $auth.id`.
  - DELETE `/subjects/{id}`: Exclusão de disciplina garantindo que `user_id == $auth.id`.
- Fornecer endpoints CRUD completos para a entidade `academic_tasks`:
  - POST `/academic_tasks`: Criação de tarefa acadêmica validando que a disciplina informada (`subject_id`) pertence ao `$auth.id`.
  - GET `/academic_tasks`: Listagem de tarefas acadêmicas cujas disciplinas pertençam ao `$auth.id`.
  - PATCH `/academic_tasks/{id}`: Atualização de tarefa acadêmica validando a posse da disciplina associada pelo `$auth.id` (e validando novo `subject_id` se fornecido).
  - DELETE `/academic_tasks/{id}`: Exclusão de tarefa acadêmica validando a posse da disciplina associada pelo `$auth.id`.

**Non-Goals:**
- Modificar os esquemas de tabelas existentes em `tables/`.
- Implementar código na camada frontend Streamlit neste momento.
- Executar sincronização, push ou deploy para o Xano (em conformidade estrita com a Regra nº 2 do AGENTS.md).

## Decisions

1. **Roteamento RESTful**:
   - `subjects`: rotas `/subjects` (GET, POST) e `/subjects/{id}` (PATCH, DELETE).
   - `academic_tasks`: rotas `/academic_tasks` (GET, POST) e `/academic_tasks/{id}` (PATCH, DELETE).
2. **Autenticação Obrigatória**:
   - Configuração de `auth = "user"` em todos os endpoints, disponibilizando o identificador `$auth.id`.
3. **Mecanismo de Isolamento**:
   - Em `subjects`: Aplicação direta do filtro `where = $db.subjects.user_id == $auth.id`. No POST, o `user_id` é forçado a partir de `$auth.id`.
   - Em `academic_tasks`: Como a propriedade do dado é relacional via disciplina, cada operação valida que `subject_id` referencia uma linha em `subjects` cujo `user_id == $auth.id`.
4. **Tratamento de Violações de Acesso**:
   - Requisições que tentem manipular dados pertencentes a outro usuário recebem erro de autorização/rejeição, impedindo vazamento de informações.
5. **Divisão de Responsabilidades**:
   - Este artefato estabelece a arquitetura e especificações. A implementação XanoScript em `apis/` será delegada ao agente especializado correspondente.

## Risks / Trade-offs

- **Validação relacional de tarefas**: Como `academic_tasks` referencia `subjects` e não `user` diretamente, cada mutação em tarefas exige verificação do dono da matéria associada.
  - *Mitigação*: Consultar a matéria por `id` e `user_id == $auth.id` na pilha de execução do endpoint antes de efetuar gravação, edição ou remoção.
- **Alteração de disciplina no PATCH**: Um usuário malicioso poderia tentar associar uma tarefa existente à matéria de outro usuário.
  - *Mitigação*: Se `subject_id` for enviado na atualização, verificar se o novo `subject_id` também pertence ao `$auth.id`.

## Migration Plan

1. Criar os arquivos XanoScript correspondentes no diretório `apis/`.
2. Validar a sintaxe dos endpoints contra as diretrizes do projeto.
3. O desenvolvedor humano revisará os arquivos gerados e efetuará o push manual para o ambiente Xano.

