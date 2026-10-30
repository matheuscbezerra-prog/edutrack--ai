# user-auth Specification

## Purpose

Define user registration, authentication, and profile viewing workflows in the Streamlit frontend integrated with Xano authentication endpoints.

## ADDED Requirements

### Requirement: User Registration
The system SHALL provide a registration form in `pages/3_👤_Perfil.py` allowing a new user to create an account by calling the POST `auth/signup` endpoint, saving the user record in the `user` table.

#### Scenario: Successful registration
- **WHEN** user submits valid name, email, and password in the registration form
- **THEN** the system calls POST `auth/signup`, saves the record in the `user` table, stores the returned auth token in session state, and confirms account creation

#### Scenario: Registration failure with existing email
- **WHEN** user submits an email that is already registered
- **THEN** the system displays an error message informing that the account is already in use

### Requirement: User Login
The system SHALL provide a login form in `pages/3_👤_Perfil.py` allowing an existing user to authenticate by calling the POST `auth/login` endpoint.

#### Scenario: Successful login
- **WHEN** user submits correct email and password credentials
- **THEN** the system calls POST `auth/login`, receives the auth token, and stores it in session state

#### Scenario: Login failure with invalid credentials
- **WHEN** user submits invalid email or password
- **THEN** the system displays an invalid credentials error message and does not authenticate

### Requirement: Authenticated User Profile
The system SHALL fetch and display authenticated user details in `pages/3_👤_Perfil.py` by calling the GET `auth/me` endpoint using the active authentication token.

#### Scenario: Display profile data
- **WHEN** user is authenticated with a valid token in session state
- **THEN** the system requests GET `auth/me` using the token and displays the user's name, email, and account details

### Requirement: Environment Configuration
The system SHALL load the authentication endpoints base URL from the `BASE_URL` variable stored in the `.env` file at the root of the project.

#### Scenario: Load base URL from environment
- **WHEN** the authentication module executes HTTP requests
- **THEN** the system resolves endpoint URLs using the `BASE_URL` value configured in `.env`

