# Design: Esquema da Tabela `subjects`

## Architecture & Data Model

A tabela `subjects` é projetada seguindo a sintaxe e as convenções do XanoScript e as diretrizes do [AGENTS.md](../../AGENTS.md) e do agente especializado **Xano Table Designer** (`.cursor/agents/xano-db.md`).

### Estrutura do Esquema XanoScript

```xs
// Stores subjects and academic courses associated with users
table subjects {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }

    text name filters=trim
    text teacher filters=trim
    int hours filters=min:0

    // Reference to the user owning/enrolled in this subject
    int user_id {
      table = "user"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  tags = ["edutrack", "subjects"]
}
```

### Justificativas de Design

1. **`id` (int)**:
   - Identificador primário numérico auto-incremental padrão em tabelas Xano, indexado como chave primária (`primary`).
2. **`created_at` (timestamp?=now)**:
   - Campo padrão para auditoria temporal de criação, com visibilidade interna/privada e índice btree descendente para ordenação de consultas recentes.
3. **`name` e `teacher` (text filters=trim)**:
   - Filtro `trim` aplicado na camada de banco de dados para evitar espaços em branco acidentais nas pontas.
4. **`hours` (int filters=min:0)**:
   - Representação em horas inteiras com restrição mínima de valor (`min:0`) para garantir que cargas horárias não sejam negativas.
5. **`user_id` (int com `table = "user"`)**:
   - Foreign Key referenciando a tabela de autenticação embutida `user` (`tables/759418_user.xs`), permitindo integridade referencial e suporte a addons e consultas relacionais no Xano.
   - Índice `btree` criado para acelerar filtros por usuário (`WHERE user_id = ?`).

## Governança e Orquestração (AGENTS.md)

Conforme a regra crítica do **AGENTS.md**:
- O agente orquestrador **não escreve diretamente o arquivo de código XanoScript (`.xs`)** no projeto.
- A fase de implementação (`apply`) deve ser delegada ao agente especializado **Xano Table Designer**, responsável por gerar o arquivo físico em `tables/` e executar o push para o ambiente Xano.
