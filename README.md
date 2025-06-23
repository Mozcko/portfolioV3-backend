# FastAPI Portfolio/Blog Backend Template

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

## 🌐 How to Manage Languages (i18n)

The i18n system is designed to be simple and flexible.

### Adding a New Language

1.  Create a new JSON file in the `src/i18n/` directory (e.g., `fr.json` for French).
2.  The new language will automatically be available through the `/i18n/` endpoint.

### Updating Translations

You can update translations in two ways:

1.  **Manually**: Edit the JSON files in the `src/i18n/` directory directly.
2.  **Via the API**: Send a `PUT` request to the `/i18n/{lang_code}` endpoint with the new JSON data in the request body. This requires admin authentication.

