# Proposal: Criação da Tabela de Disciplinas (`subjects`)

## Why
O sistema EduTrack necessita de uma entidade central para gerenciamento de matérias e disciplinas acadêmicas (`subjects`). Atualmente, existem tabelas de autenticação (`user`), contas (`account`), logs (`event_log`), clientes e papéis, mas não há estrutura para persistir os componentes pedagógicos/acadêmicos vinculados aos usuários do sistema.

## What
Definir o esquema da nova tabela `subjects` no XanoScript para armazenar as disciplinas cursadas/lecionadas, contemplando:
- Identificador único (`id`);
- Nome da disciplina (`name`);
- Nome ou identificação do professor/instrutor (`teacher`);
- Carga horária em horas (`hours`);
- Associação direta com o usuário autenticado (`user_id` com chave estrangeira referenciando a tabela `user`).

## Scope & Impact
- **Novo componente**: Tabela `subjects` a ser criada no diretório `tables/`.
- **Relacionamento**: Chave estrangeira (`user_id`) referenciando a tabela de autenticação `user` (`tables/759418_user.xs`).
- **Orquestração**: Conforme estipulado no [AGENTS.md](../../AGENTS.md), este planejamento estabelece a especificação e delega a criação e manipulação direta do XanoScript ao agente especializado **Xano Table Designer**.
