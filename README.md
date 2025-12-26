# FastAPI Portfolio/Blog Backend Template

[English](#english) | [Español](#español)

<a name="english"></a>
## 🇬🇧 English

This is a starter template for a **FastAPI** backend, ideal for a portfolio or blog. It comes with a solid foundation that includes authentication, internationalization (i18n), and a structured project layout to get you up and running quickly.

## ✨ Features

* **Modern Framework**: Built with **FastAPI** for high performance.
* **Database Ready**: Uses **SQLAlchemy** for ORM, configured for SQLite by default.
* **Authentication**: Secure user authentication with JWT tokens using **Passlib** and **python-jose**. The system includes a `/login` route that provides a bearer token.
* **Admin User**: Automatically creates an admin user on startup based on your environment variables.
* **Internationalization (i18n)**:
    * Endpoints to fetch available languages and translation files (`.json`).
    * A secure endpoint for an administrator to update translations.
* **Configuration Management**: Centralized configuration using Pydantic's `BaseSettings`, loaded from a `.env` file.
* **Logging**: Pre-configured logging that outputs to both the console and a rotating log file (`logs/app.log`).
* **Dependency Injection**: Organizes dependencies for database sessions and user authentication, making the code clean and easy to test.

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Prerequisites

* Python 3.8+
* A virtual environment tool (like `venv` or `virtualenv`)

### 2. Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration

Before running the application, you need to create a `.env` file in the root directory. Copy the following variables and fill them in with your own values.

```env
# --- App Settings ---
APP_TITLE="My Portfolio API"
APP_DESCRIPTION="Backend for my awesome portfolio"
APP_VERSION="1.0.0"

# --- Database Settings ---
DATABASE_URL="sqlite:///"
DATABASE_NAME="portfolio.db"

# --- Security Settings ---
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="your_super_secret_password"
SECRET_KEY="a_very_long_and_random_secret_key_for_jwt"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# --- CORS Settings ---
# A comma-separated list of allowed origins.
# Example: 
ALLOWED_HOSTS='["localhost", "127.0.0.1"]'
ALLOWED_METHODS='["GET", "POST", "PUT", "DELETE"]'
ALLOWED_HEADERS='["Content-Type", "Authorization"]'
ALLOWED_EXPOSED_HEADERS='["Content-Type", "Authorization"]'
ALLOWED_CREDENTIALS=true
```

### 4. Running the Application

Once you've set up your `.env` file, run the app with Uvicorn:

```bash
uvicorn src.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

---

## 📁 Project Structure

```
├── logs/
│   └── app.log
├── src/
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   ├── i18n/
│   │   ├── en.json
│   │   └── es.json
│   ├── models/
│   │   └── User.py
│   ├── routes/
│   │   ├── auth.py
│   │   └── i18n.py
│   ├── schemas/
│   │   └── User.py
│   ├── services/
│   │   └── i18n_service.py
│   ├── static/
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   └── utils.py
├── .env
└── requirements.txt
```

---

## ⚙️ API Endpoints

Here are the main API endpoints available in this template:

### Authentication (`/auth`)

* `POST /auth/login`: Authenticates a user and returns a JWT access token. It expects `username` and `password` in a form data payload.
* `GET /auth/me`: A protected endpoint to get the current authenticated user's details. Requires a valid JWT token.

### Internationalization (`/i18n`)

* `GET /i18n/`: Returns a list of available language codes (e.g., `["en", "es"]`).
* `GET /i18n/{lang_code}`: Retrieves the full JSON translation file for a given language code.
* `PUT /i18n/{lang_code}`: Updates a language file with new key-value pairs. This is a **protected endpoint** and requires admin authentication.

### Certificates (`/certificates`)
* `GET /certificates`: Get all certificates.
* `POST /certificates`: Create a certificate (Admin only).
* `GET /certificates/{id}`: Get a certificate.
* `PUT /certificates/{id}`: Update a certificate (Admin only).
* `DELETE /certificates/{id}`: Delete a certificate (Admin only).

### Projects (`/projects`)
* `GET /projects`: Get all projects.
* `POST /projects`: Create a project (Admin only).
* `GET /projects/{id}`: Get a project.
* `PUT /projects/{id}`: Update a project (Admin only).
* `DELETE /projects/{id}`: Delete a project (Admin only).

### Technologies (`/technologies`)
* `GET /technologies`: Get all technologies.
* `POST /technologies`: Create a technology (Admin only).
* `GET /technologies/{id}`: Get a technology.
* `PUT /technologies/{id}`: Update a technology (Admin only).
* `DELETE /technologies/{id}`: Delete a technology (Admin only).

### Jobs (`/jobs`)
* `GET /jobs`: Get all jobs.
* `POST /jobs`: Create a job (Admin only).
* `GET /jobs/{id}`: Get a job.
* `PUT /jobs/{id}`: Update a job (Admin only).
* `DELETE /jobs/{id}`: Delete a job (Admin only).

### Socials (`/socials`)
* `GET /socials`: Get all social links.
* `POST /socials`: Create a social link (Admin only).
* `GET /socials/{id}`: Get a social link.
* `PUT /socials/{id}`: Update a social link (Admin only).
* `DELETE /socials/{id}`: Delete a social link (Admin only).

### CV (`/cv`)
* `GET /cv/download/{lang_code}`: Download CV as PDF.
* `PUT /cv/upload/{lang_code}`: Update CV Markdown file (Admin only).

## 🌐 How to Manage Languages (i18n)

The i18n system is designed to be simple and flexible.

### Adding a New Language

1.  Create a new JSON file in the `src/i18n/` directory (e.g., `fr.json` for French).
2.  The new language will automatically be available through the `/i18n/` endpoint.

### Updating Translations

You can update translations in two ways:

1.  **Manually**: Edit the JSON files in the `src/i18n/` directory directly.
2.  **Via the API**: Send a `PUT` request to the `/i18n/{lang_code}` endpoint with the new JSON data in the request body. This requires admin authentication.

---

<a name="español"></a>
## 🇪🇸 Español

Esta es una plantilla inicial para un backend con **FastAPI**, ideal para un portafolio o blog. Viene con una base sólida que incluye autenticación, internacionalización (i18n) y una estructura de proyecto organizada para que empieces rápidamente.

## ✨ Características

* **Framework Moderno**: Construido con **FastAPI** para un alto rendimiento.
* **Listo para Base de Datos**: Usa **SQLAlchemy** como ORM, configurado para SQLite por defecto.
* **Autenticación**: Autenticación segura de usuarios con tokens JWT usando **Passlib** y **python-jose**. Incluye una ruta `/login`.
* **Usuario Administrador**: Crea automáticamente un usuario administrador al iniciar basándose en tus variables de entorno.
* **Internacionalización (i18n)**:
    * Endpoints para obtener idiomas disponibles y archivos de traducción (`.json`).
    * Endpoint seguro para actualizar traducciones.
* **Gestión de Configuración**: Configuración centralizada usando `BaseSettings` de Pydantic, cargada desde un archivo `.env`.
* **Logging**: Logging preconfigurado que muestra salida en consola y en un archivo rotativo (`logs/app.log`).
* **Inyección de Dependencias**: Organiza dependencias para sesiones de base de datos y autenticación.

---

## 🚀 Comenzando

Sigue estos pasos para configurar y ejecutar el proyecto localmente.

### 1. Prerrequisitos

* Python 3.8+
* Una herramienta de entorno virtual (como `venv` o `virtualenv`)

### 2. Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone <tu-url-del-repositorio>
    cd <nombre-del-repositorio>
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows, usa `venv\Scripts\activate`
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuración

Antes de ejecutar la aplicación, necesitas crear un archivo `.env` en el directorio raíz. Copia las siguientes variables y llénalas con tus propios valores.

```env
# --- Configuración de la App ---
APP_TITLE="Mi API de Portafolio"
APP_DESCRIPTION="Backend para mi increíble portafolio"
APP_VERSION="1.0.0"

# --- Configuración de Base de Datos ---
DATABASE_URL="sqlite:///"
DATABASE_NAME="portfolio.db"

# --- Configuración de Seguridad ---
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="tu_password_super_secreto"
SECRET_KEY="una_clave_secreta_muy_larga_y_aleatoria"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# --- Configuración de CORS ---
ALLOWED_HOSTS='["localhost", "127.0.0.1"]'
ALLOWED_METHODS='["GET", "POST", "PUT", "DELETE"]'
ALLOWED_HEADERS='["Content-Type", "Authorization"]'
ALLOWED_EXPOSED_HEADERS='["Content-Type", "Authorization"]'
ALLOWED_CREDENTIALS=true
```

### 4. Ejecutando la Aplicación

Una vez configurado el archivo `.env`, ejecuta la app con Uvicorn:

```bash
uvicorn src.main:app --reload
```

La aplicación estará disponible en `http://127.0.0.1:8000`. Puedes acceder a la documentación interactiva de la API en `http://127.0.0.1:8000/docs`.

---

## ⚙️ Endpoints de la API

Aquí están los principales endpoints disponibles en esta plantilla:

### Autenticación (`/auth`)

* `POST /auth/login`: Autentica un usuario y devuelve un token de acceso JWT. Espera `username` y `password` en el payload.
* `GET /auth/me`: Endpoint protegido para obtener detalles del usuario autenticado actual.

### Internacionalización (`/i18n`)

* `GET /i18n/`: Devuelve una lista de códigos de idioma disponibles (ej. `["en", "es"]`).
* `GET /i18n/{lang_code}`: Obtiene el archivo de traducción JSON completo para un código de idioma.
* `PUT /i18n/{lang_code}`: Actualiza un archivo de idioma con nuevos pares clave-valor. Requiere autenticación de administrador.

### Certificados (`/certificates`)
* `GET /certificates`: Obtener todos los certificados.
* `POST /certificates`: Crear un certificado (Solo Admin).
* `GET /certificates/{id}`: Obtener un certificado.
* `PUT /certificates/{id}`: Actualizar un certificado (Solo Admin).
* `DELETE /certificates/{id}`: Eliminar un certificado (Solo Admin).

### Proyectos (`/projects`)
* `GET /projects`: Obtener todos los proyectos.
* `POST /projects`: Crear un proyecto (Solo Admin).
* `GET /projects/{id}`: Obtener un proyecto.
* `PUT /projects/{id}`: Actualizar un proyecto (Solo Admin).
* `DELETE /projects/{id}`: Eliminar un proyecto (Solo Admin).

### Tecnologías (`/technologies`)
* `GET /technologies`: Obtener todas las tecnologías.
* `POST /technologies`: Crear una tecnología (Solo Admin).
* `GET /technologies/{id}`: Obtener una tecnología.
* `PUT /technologies/{id}`: Actualizar una tecnología (Solo Admin).
* `DELETE /technologies/{id}`: Eliminar una tecnología (Solo Admin).

### Trabajos (`/jobs`)
* `GET /jobs`: Obtener todos los trabajos.
* `POST /jobs`: Crear un trabajo (Solo Admin).
* `GET /jobs/{id}`: Obtener un trabajo.
* `PUT /jobs/{id}`: Actualizar un trabajo (Solo Admin).
* `DELETE /jobs/{id}`: Eliminar un trabajo (Solo Admin).

### Redes Sociales (`/socials`)
* `GET /socials`: Obtener todas las redes sociales.
* `POST /socials`: Crear una red social (Solo Admin).
* `GET /socials/{id}`: Obtener una red social.
* `PUT /socials/{id}`: Actualizar una red social (Solo Admin).
* `DELETE /socials/{id}`: Eliminar una red social (Solo Admin).

### CV (`/cv`)
* `GET /cv/download/{lang_code}`: Descargar CV en PDF.
* `PUT /cv/upload/{lang_code}`: Actualizar archivo Markdown del CV (Solo Admin).

## 🌐 Cómo gestionar Idiomas (i18n)

El sistema i18n está diseñado para ser simple y flexible.

### Agregar un Nuevo Idioma

1.  Crea un nuevo archivo JSON en el directorio `src/i18n/` (ej. `fr.json` para Francés).
2.  El nuevo idioma estará automáticamente disponible a través del endpoint `/i18n/`.

### Actualizar Traducciones

Puedes actualizar las traducciones de dos formas:

1.  **Manualmente**: Edita los archivos JSON en el directorio `src/i18n/` directamente.
2.  **Vía API**: Envía una petición `PUT` al endpoint `/i18n/{lang_code}` con los nuevos datos JSON. Requiere autenticación de administrador.
