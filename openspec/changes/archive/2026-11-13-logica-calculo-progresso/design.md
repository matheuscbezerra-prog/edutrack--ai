# Design: Cálculo de Progresso de Disciplinas em Python

## Context

O EduTrack AI possui endpoints RESTful desenvolvidos em XanoScript para gerenciamento de tarefas acadêmicas (`GET /academic_tasks` em `apis/matheuss_workspace/academic_tasks_GET.xs`). Cada tarefa possui atributos como `id`, `title`, `status` e `subject_id`.

Para apoiar funcionalidades de relatórios, acompanhamento e visualização acadêmica, é necessário disponibilizar um script utilitário em Python (`scripts/calculate_progress.py`) que consuma a API CRUD de tarefas, calcule a taxa de conclusão de uma matéria e forneça a saída em formato JSON padronizado.

## Goals / Non-Goals

**Goals:**
- Criar o script Python em `scripts/calculate_progress.py`.
- Implementar função de integração com o endpoint CRUD `GET /academic_tasks` utilizando autenticação Bearer token.
- Filtrar e analisar o status de cada tarefa associada à disciplina informada (`subject_id`).
- Calcular as métricas:
  - `total_tasks`: contagem de tarefas da disciplina;
  - `completed_tasks`: tarefas com status de conclusão (ex: `"completed"`, `"concluida"`, `"concluída"`);
  - `pending_tasks`: contagem de tarefas não concluídas;
  - `progress_percentage`: porcentagem formatada com precisão decimal (`completed / total * 100.0`), com fallback seguro para `0.0` caso `total == 0`.
- Retornar o resultado estruturado em JSON.
- Permitir execução tanto como módulo importável (função reutilizável) quanto via linha de comando (CLI) via `argparse`.

**Non-Goals:**
- Criar novos endpoints no backend Xano ou modificar tabelas do banco de dados.
- Alterar páginas de visualização do Streamlit nesta tarefa.
- Executar comandos de deploy ou push para o Xano (em conformidade com a Regra nº 2 do projeto).

## Decisions

1. **Localização e Estrutura do Script**:
   - O arquivo será posicionado em `scripts/calculate_progress.py`.
   - Utilizará a biblioteca padrão `requests` (já presente no ambiente) para requisições HTTP e `json` para formatação da resposta.
2. **Resolução de URL Base**:
   - Obter a URL base da API a partir de variável de ambiente ou do arquivo `.env`, permitindo também passagem explícita como argumento opcional na função.
3. **Critério de Status Concluído**:
   - Para suportar variações usuais de status, tarefas com status normalizado (minúsculas, sem espaços extras) correspondentes a `"completed"`, `"concluida"`, `"concluída"` ou `"done"` serão contabilizadas como concluídas.
4. **Tratamento de Exceções**:
   - Utilização de blocos `try/except` para capturar falhas de rede (`requests.exceptions.RequestException`), erros de autenticação (HTTP 401/403) ou dados malformados, retornando um JSON com detalhes do erro e código de status correspondente.

## Risks / Trade-offs

- **Disciplina sem tarefas cadastradas**:
  - *Risco*: Erro de divisão por zero (`ZeroDivisionError`).
  - *Mitigação*: Verificação explícita `if total_tasks == 0: progress_percentage = 0.0`.
- **Credenciais ou Token Inválidos**:
  - *Risco*: Resposta com erro de autenticação ao consultar o endpoint CRUD.
  - *Mitigação*: Tratar códigos HTTP não-200 e retornar mensagem de erro estruturada em JSON informando falha de autorização.

## Migration Plan

1. Criar o diretório `scripts/` se ainda não existir.
2. Implementar a função e interface de linha de comando em `scripts/calculate_progress.py` durante a fase de aplicação (`/opsx:apply`).
3. Validar a sintaxe e testes de unidade/chamada do script.
