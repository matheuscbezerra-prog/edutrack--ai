# Proposal: Geração de Relatório de Desempenho em PDF e Endpoint de Download

## Why

Estudantes e professores necessitam de um documento consolidado e exportável que resuma o progresso e o rendimento acadêmico ao longo do período letivo. Atualmente, o EduTrack AI dispõe de tabelas e endpoints para disciplinas e tarefas, bem como cálculo de progresso via script, mas não possui mecanismo para gerar um documento PDF formatado contendo o histórico de desempenho do estudante nem um endpoint no Xano para que o aluno baixe esse relatório de forma segura e autenticada.

## What Changes

- Planejamento e especificação de um script Python (`scripts/generate_performance_report_pdf.py`) responsável por estruturar os dados acadêmicos do aluno (disciplinas cursadas, tarefas concluídas, percentuais de progresso) e gerar um arquivo PDF formatado.
- Planejamento e especificação de um endpoint RESTful no Xano (`apis/matheuss_workspace/student_performance_report_pdf_GET.xs` ou rota `reports/performance_pdf`) protegido por autenticação (`auth = "user"`), que disponibiliza o download do arquivo PDF com os devidos cabeçalhos HTTP (`Content-Type: application/pdf` e `Content-Disposition: attachment`).

## Capabilities

### New Capabilities
- `performance-report-pdf`: Geração de relatório de desempenho acadêmico em formato PDF via script Python e disponibilização para download através de endpoint autenticado no Xano.

### Modified Capabilities
- None.

## Impact

- Novo script Python no diretório `scripts/`.
- Novo arquivo de endpoint XanoScript no diretório `apis/matheuss_workspace/`.
- Sem impactos negativos ou alterações estruturais nas tabelas já existentes no banco de dados.
