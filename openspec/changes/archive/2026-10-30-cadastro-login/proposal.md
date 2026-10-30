# Proposal: Cadastro e Login de Usuários na Página de Perfil

## Why

Atualmente, a página `pages/3_👤_Perfil.py` possui apenas texto estático de apresentação ("Meu Perfil") sem mecanismos reais de autenticação ou visualização de dados de usuário. Para que os estudantes possam acessar a plataforma de forma segura e personalizada, é necessário fornecer interface de cadastro e login integrada aos endpoints do Xano (`auth/signup`, `auth/login` e `auth/me`), persistindo dados cadastrais na tabela `user` e isolando as configurações de URL em arquivo de ambiente `.env`.

## What Changes

- Definição da variável de ambiente `BASE_URL` no arquivo `.env` na raiz do projeto com o endereço base da API de autenticação do Xano.
- Implementação de interface interativa em Streamlit na página `pages/3_👤_Perfil.py` contemplando:
  - Cadastro de novos usuários via endpoint POST `auth/signup`, salvando dados na tabela `user`.
  - Login de usuários existentes via endpoint POST `auth/login`, armazenando o token retornado no `st.session_state`.
  - Exibição de dados do usuário autenticado obtidos via endpoint GET `auth/me` com autenticação Bearer Token.

## Capabilities

### New Capabilities
- `user-auth`: Fluxo de cadastro, autenticação e obtenção de dados do perfil do usuário na interface Streamlit integrado aos endpoints do Xano.

### Modified Capabilities
- None.

## Impact

- Atualização/criação do arquivo `.env` na raiz do projeto.
- Modificação do arquivo `pages/3_👤_Perfil.py` com lógica em Python e componentes Streamlit (sem impacto em esquemas de banco de dados ou endpoints backend já existentes).

