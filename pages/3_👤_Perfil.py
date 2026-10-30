import os
from pathlib import Path
from datetime import datetime
import requests
import streamlit as st

st.set_page_config(page_title="Perfil", page_icon="👤", layout="wide")


def get_base_url() -> str:
    """Retrieve BASE_URL from environment variable or .env file."""
    base_url = os.getenv("BASE_URL")
    if base_url:
        return base_url.strip().rstrip("/")

    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        try:
            with open(env_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        if key.strip() == "BASE_URL":
                            return val.strip().strip("'\"").rstrip("/")
        except Exception as error:
            st.error(f"Error loading .env file: {error}")

    return ""


def signup_user(base_url: str, name: str, email: str, password: str) -> dict:
    """Call Xano auth/signup endpoint to register a new user in the user table."""
    url = f"{base_url}/auth/signup"
    payload = {
        "name": name.strip(),
        "email": email.strip().lower(),
        "password": password,
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json() if response.content else {}
        if response.status_code == 200 and "authToken" in data:
            return {"success": True, "data": data}

        error_message = data.get("message") or data.get("error") or "Erro ao realizar cadastro."
        return {"success": False, "error": error_message}
    except requests.exceptions.RequestException as error:
        return {"success": False, "error": f"Erro de conexão com o servidor: {error}"}
    except Exception as error:
        return {"success": False, "error": f"Erro inesperado: {error}"}


def login_user(base_url: str, email: str, password: str) -> dict:
    """Call Xano auth/login endpoint to authenticate user credentials."""
    url = f"{base_url}/auth/login"
    payload = {
        "email": email.strip().lower(),
        "password": password,
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json() if response.content else {}
        if response.status_code == 200 and "authToken" in data:
            return {"success": True, "data": data}

        error_message = data.get("message") or data.get("error") or "Credenciais inválidas."
        return {"success": False, "error": error_message}
    except requests.exceptions.RequestException as error:
        return {"success": False, "error": f"Erro de conexão com o servidor: {error}"}
    except Exception as error:
        return {"success": False, "error": f"Erro inesperado: {error}"}


def get_user_profile(base_url: str, token: str) -> dict:
    """Call Xano auth/me endpoint with Bearer token to get current user details."""
    url = f"{base_url}/auth/me"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json() if response.content else {}
        if response.status_code == 200:
            return {"success": True, "data": data}

        error_message = data.get("message") or data.get("error") or "Sessão expirada ou inválida."
        return {"success": False, "error": error_message}
    except requests.exceptions.RequestException as error:
        return {"success": False, "error": f"Erro de conexão: {error}"}
    except Exception as error:
        return {"success": False, "error": f"Erro inesperado: {error}"}


# Initialize Session State
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None

base_url = get_base_url()

if not base_url:
    st.error("Configuração de BASE_URL não encontrada no arquivo .env na raiz do projeto.")
    st.stop()

st.title("👤 Meu Perfil")

# Display Profile View if Authenticated
if st.session_state["auth_token"]:
    profile_result = get_user_profile(base_url, st.session_state["auth_token"])

    if profile_result["success"]:
        user = profile_result["data"]
        st.session_state["user_info"] = user

        st.success(f"Conectado como **{user.get('name', 'Estudante')}**")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📋 Dados Pessoais")
            st.write(f"**Nome:** {user.get('name', 'Não informado')}")
            st.write(f"**E-mail:** {user.get('email', 'Não informado')}")
            st.write(f"**ID do Usuário:** {user.get('id', '-')}")

        with col2:
            st.markdown("### ⚙️ Informações da Conta")
            st.write(f"**Perfil / Papel:** {user.get('role', 'member')}")
            created_timestamp = user.get("created_at")
            if created_timestamp:
                try:
                    formatted_date = datetime.fromtimestamp(created_timestamp / 1000).strftime("%d/%m/%Y %H:%M")
                except Exception:
                    formatted_date = str(created_timestamp)
                st.write(f"**Cadastrado em:** {formatted_date}")

        st.divider()
        if st.button("🚪 Sair da Conta (Logout)", type="secondary"):
            st.session_state["auth_token"] = None
            st.session_state["user_info"] = None
            st.rerun()

    else:
        st.warning("Sua sessão expirou ou o token é inválido. Por favor, faça login novamente.")
        st.session_state["auth_token"] = None
        st.session_state["user_info"] = None
        st.rerun()

# Display Login / Signup Tabs if Not Authenticated
else:
    st.write("Faça login ou crie uma conta para acessar a plataforma.")

    tab_login, tab_signup = st.tabs(["🔑 Entrar", "📝 Criar Conta"])

    with tab_login:
        st.subheader("Login na Plataforma")
        with st.form("form_login"):
            login_email = st.text_input("E-mail", placeholder="seu.email@exemplo.com")
            login_password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            login_submitted = st.form_submit_button("Entrar", use_container_width=True)

            if login_submitted:
                if not login_email or not login_password:
                    st.warning("Por favor, preencha o e-mail e a senha.")
                else:
                    with st.spinner("Autenticando..."):
                        result = login_user(base_url, login_email, login_password)

                    if result["success"]:
                        st.session_state["auth_token"] = result["data"]["authToken"]
                        st.success("Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error(result["error"])

    with tab_signup:
        st.subheader("Cadastro de Novo Estudante")
        with st.form("form_signup"):
            signup_name = st.text_input("Nome Completo", placeholder="Seu nome")
            signup_email = st.text_input("E-mail", placeholder="seu.email@exemplo.com")
            signup_password = st.text_input(
                "Senha",
                type="password",
                placeholder="Mínimo 8 caracteres, com letras e números",
                help="A senha deve ter pelo menos 8 caracteres, contendo letras e dígitos.",
            )
            signup_submitted = st.form_submit_button("Cadastrar", use_container_width=True)

            if signup_submitted:
                if not signup_name or not signup_email or not signup_password:
                    st.warning("Por favor, preencha todos os campos.")
                elif len(signup_password) < 8:
                    st.warning("A senha deve possuir pelo menos 8 caracteres.")
                else:
                    with st.spinner("Criando conta..."):
                        result = signup_user(base_url, signup_name, signup_email, signup_password)

                    if result["success"]:
                        st.session_state["auth_token"] = result["data"]["authToken"]
                        st.success("Conta criada com sucesso!")
                        st.rerun()
                    else:
                        st.error(result["error"])
