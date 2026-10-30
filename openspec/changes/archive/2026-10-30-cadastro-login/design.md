# Design: Autenticação e Perfil de Usuário

## Context

A aplicação EduTrack AI é construída com frontend Streamlit e backend Xano. Os endpoints de autenticação (`auth/signup`, `auth/login`, `auth/me`) já se encontram implementados no grupo `Authentication` do Xano com canonical `rkQbZi0C`. A tabela de banco de dados `user` armazena os registros com nome, email, senha criptografada e identificadores.

A página `pages/3_👤_Perfil.py` precisa ser enriquecida para atuar como o ponto central de identidade do usuário:
1. Usuário não autenticado: visualiza abas de Login e Cadastro.
2. Usuário autenticado: visualiza suas informações de perfil (carregadas via `auth/me`) e opção de desconectar (logout).

## Goals / Non-Goals

**Goals:**
- Configurar e utilizar a variável `BASE_URL` no arquivo `.env` na raiz do projeto.
- Implementar formulário de cadastro com envio para POST `auth/signup`, gravando o usuário na tabela `user`.
- Implementar formulário de login com envio para POST `auth/login`, persistindo o `authToken` retornado no `st.session_state`.
- Implementar chamada autenticada a GET `auth/me` para exibir informações do usuário logado na interface Streamlit.
- Fornecer feedback visual adequado (mensagens de sucesso/erro com `st.success` e `st.error`).

**Non-Goals:**
- Alterar as tabelas ou endpoints existentes no Xano.
- Alterar outras páginas do Streamlit nesta tarefa.
- Realizar operações de deploy ou sincronização com a nuvem do Xano.

## Decisions

1. **Gestão de Ambiente (.env)**:
   - Utilizar a biblioteca `requests` para requisições HTTP e carregar `BASE_URL` do `.env` na raiz.
   - Tratar ausência da variável de ambiente com mensagem clara ao desenvolvedor/usuário.
2. **Gerenciamento de Sessão (Streamlit)**:
   - Utilizar `st.session_state` (`auth_token`, `user_data`) para manter o estado de login durante a navegação entre páginas.
3. **Estrutura Visual da Página `Perfil.py`**:
   - Se o usuário não estiver logado: exibir abas `Entrar` (Login) e `Cadastrar` (Signup).
   - Se o usuário estiver logado: exibir os dados do perfil obtidos de `auth/me` (Nome, E-mail, ID, Papel/Role) e botão de Logout que limpa a sessão.

## Risks / Trade-offs

- **Persistência de Sessão**: No Streamlit, a sessão reside em memória por conexão de navegador. Recarregar a página (F5) reinicia o `session_state`.
  - *Mitigação*: Manter o fluxo simples e limpo, permitindo login rápido e mensagens informativas.
- **Falhas de Conexão ou Credenciais Inválidas**: Endpoints do Xano retornam códigos 400/403 em caso de erro.
  - *Mitigação*: Tratar exceções de rede e respostas HTTP não-200 com blocos `try/except` exibindo mensagens amigáveis via `st.error`.

## Migration Plan

1. Verificar e garantir a configuração da variável `BASE_URL` no arquivo `.env`.
2. Implementar a lógica em `pages/3_👤_Perfil.py`.
3. Testar localmente a interface Streamlit simulando cadastro, login e visualização de perfil.

