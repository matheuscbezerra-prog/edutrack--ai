# Proposal: Cálculo de Progresso de Disciplinas Baseado em Tarefas

## Why

Para que o EduTrack AI forneça métricas de acompanhamento acadêmico, é necessário calcular o percentual de conclusão das tarefas vinculadas a cada disciplina. Atualmente, os endpoints CRUD permitem criar e consultar as tarefas acadêmicas (`academic_tasks`), mas não há um módulo ou script utilitário responsável por agregar esses dados e produzir indicadores de progresso consolidados em formato JSON para consumo do sistema.

## What Changes

- Planejamento e especificação de um script Python em `scripts/calculate_progress.py`.
- Implementação de função para consultar as tarefas de uma disciplina específica através do endpoint CRUD `GET /academic_tasks` (com filtro por `subject_id` e autenticação via Bearer token).
- Cálculo das métricas de progresso: total de tarefas, tarefas concluídas, tarefas pendentes e percentual de conclusão (`concluídas / total * 100`).
- Retorno estruturado em formato JSON com os indicadores calculados e tratamento de divisões por zero quando não houver tarefas cadastradas.

## Capabilities

### New Capabilities
- `progress-calculation`: Lógica utilitária de agregação e cálculo percentual de progresso de disciplinas a partir de tarefas acadêmicas obtidas via endpoints CRUD.

### Modified Capabilities
- None.

## Impact

- Criação de novo script em `scripts/calculate_progress.py`.
- Consumo dos endpoints CRUD existentes de `academic_tasks` sem alterações em esquemas de banco de dados ou endpoints backend.
