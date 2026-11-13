# Design: Geração de Relatório de Desempenho em PDF e Endpoint no Xano

## Context

O EduTrack AI armazena dados acadêmicos divididos entre disciplinas (`subjects`) e tarefas acadêmicas (`academic_tasks`), com autenticação e isolamento multi-tenant por usuário no backend Xano. Já existe uma lógica em Python (`scripts/calculate_progress.py`) para mensurar a taxa de conclusão das tarefas de cada disciplina.

Para atender à necessidade de exportação formal de relatórios de desempenho, este design articula duas frentes complementares:
1. Um script Python em `scripts/generate_performance_report_pdf.py` capaz de gerar um documento PDF estruturado com o histórico acadêmico do aluno;
2. Um endpoint RESTful autenticado no Xano (`apis/matheuss_workspace/`) configurado para fornecer o download do relatório diretamente pelo navegador ou cliente HTTP, com cabeçalhos apropriados de anexo (`Content-Disposition: attachment`).

## Goals / Non-Goals

**Goals:**
- Implementar script Python em `scripts/generate_performance_report_pdf.py` para gerar arquivos PDF com layout legível e estruturado:
  - Cabeçalho institucional (EduTrack AI, data de emissão, identificação do estudante);
  - Resumo geral de rendimento (total de matérias, total de tarefas, tarefas concluídas, percentual global de conclusão);
  - Tabela detalhada por matéria com professor, carga horária e percentual individual de tarefas concluídas.
- Implementar endpoint XanoScript `GET "reports/performance_pdf"` em `apis/matheuss_workspace/`:
  - Autenticação obrigatória (`auth = "user"`);
  - Coleta segura dos dados daquele aluno (`$auth.id`);
  - Configuração de cabeçalhos HTTP (`Content-Type: application/pdf` e `Content-Disposition: attachment; filename="relatorio_desempenho.pdf"`);
  - Retorno do arquivo PDF para download.

**Non-Goals:**
- Alterar as tabelas ou campos do banco de dados existente.
- Modificar páginas do frontend Streamlit nesta etapa.
- Realizar deploy ou push para os servidores do Xano (em obediência à Regra nº 2 do AGENTS.md).

## Decisions

1. **Geração de PDF em Python (Independência de Dependências Complexas)**:
   - O gerador Python criará um documento no formato padrão `%PDF-1.4` de forma direta ou via módulo utilitário limpo, evitando problemas de compatibilidade com pacotes externos que exijam compiladores C/C++ ou bibliotecas de sistema ausentes.
2. **Isolamento de Dados no Endpoint Xano**:
   - O endpoint no Xano utilizará `auth = "user"` e filtrará exclusivamente registros onde `user_id == $auth.id`, garantindo que nenhum aluno consiga baixar o relatório de outro estudante.
3. **Cabeçalhos de Download**:
   - Utilização da instrução `util.set_header` para definir `Content-Type: application/pdf` e `Content-Disposition: attachment; filename="..."`, instruindo o cliente a efetuar o download automático do arquivo.

## Risks / Trade-offs

- **Formatos e Encoding de Caracteres no PDF**:
  - *Risco*: Nomes de disciplinas ou de alunos com caracteres acentuados podem apresentar falhas em visualizadores de PDF que usem fontes padrão limitadas.
  - *Mitigação*: Normalização de texto e suporte adequado a fontes padrão PDF (WinAnsiEncoding / Latin-1) ou escape de sequências de texto.
- **Tamanho do Arquivo e Performance no Xano**:
  - *Risco*: Relatórios de alunos com centenas de tarefas podem gerar respostas pesadas.
  - *Mitigação*: Estruturação enxuta e focada nos resumos consolidados de disciplinas e tarefas.

## Migration Plan

1. Definir e revisar os arquivos de especificação da change.
2. Durante a execução (`/opsx:apply`), criar o script Python em `scripts/generate_performance_report_pdf.py` e o endpoint em `apis/matheuss_workspace/`.
3. Validar a sintaxe dos arquivos gerados.
