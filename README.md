
A robust FastAPI application for managing users and posts with secure authentication, efficient database usage, and comprehensive validation. 
Designed for maintainability, security, and clarity, with a clean MVC structure and extensive documentation.

---

## 🚀 Features

- **User Management:** Register, login, and manage users with secure password hashing.
- **Post Management:** CRUD operations for posts, with in-memory caching to minimize DB load.
- **JWT Authentication:** Secure, stateless authentication for all protected endpoints.
- **Environment-based Configuration:** All sensitive/configurable values managed via `.env`.
- **Payload Size Limiter:** Middleware to prevent large payload attacks.
- **Comprehensive Validation:** Pydantic and SQLAlchemy models with strict type and field validation.
- **MVC Structure:** Clear separation of models, controllers, services, and repositories.
- **Extensive Documentation:** Every function, model, and endpoint is fully documented.

---

## 🗂️ Project Structure

```
lucid-financials-app/
├── app/
│   ├── config/           # Pydantic settings and environment management
│   ├── controllers/      # FastAPI route handlers (views/controllers)
│   ├── middleware/       # Custom middleware (e.g., payload size limiter)
│   ├── models/          # SQLAlchemy ORM models
│   ├── repositories/     # Database abstraction layer
│   ├── schemas/          # Pydantic models (request/response validation)
│   ├── services/         # Business logic (e.g., PostService, AuthService)
│   └── utils/            # Utility functions (e.g., auth helpers)
├── migrations/          # Alembic database migrations
├── tests/                # Test files (unit tests)
├── .env                  # Environment variables
├── README.md            
├── main.py              # FastAPI app entry point
├── pyproject.toml       # Project metadata and configuration
├── uv.lock              # Python dependency lock file
└── .gitignore          
```

---

## 🛠️ Tech Stack & Packages

- **Python 3.10+**
- **FastAPI** (web framework)
- **SQLAlchemy** (ORM)
- **Pydantic** (data validation & settings)
- **bcrypt** (password hashing)
- **python-jose** (JWT handling)
- **uvicorn** (ASGI server)
- **python-dotenv** (env var loading)
- **pytest** (testing)
- **ruff** (linter/formatter)
- **Other:** threading, typing, standard libraries

---

## ⚙️ Environment Variables

All configuration is managed via `.env` (example keys):

```
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CACHE_EXPIRE_MINUTES=10
MAX_PAYLOAD_SIZE_MB=1
BCRYPT_ROUNDS=12
DEBUG=True
```

---

## 📦 Installation

> **Note:** This project uses [uv](https://github.com/astral-sh/uv) for Python packaging and environment management. To install uv, follow the instructions at [https://github.com/astral-sh/uv#installation](https://github.com/astral-sh/uv#installation) or run:
>
> ```bash
> curl -Ls https://astral.sh/uv/install.sh | sh
> ```

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zxenonx/lucid-financials-app.git
   cd lucid-financials-app
   ```

2. **Create and activate a virtual environment (using uv):**
   ```bash
   uv venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies (using uv):**
   ```bash
   uv sync
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and edit as needed.

5. **Run database migrations (if using Alembic):**
   ```bash
   alembic upgrade head
   ```

6. **Run the application (development mode):**
   ```bash
   fastapi dev main.py
   ```

---

## 🧪 Running Tests

```bash
pytest
```

---

## 🧹 Code Style & Linting

To automatically check and fix code formatting and lint issues, run:

```bash
ruff check . --fix
```

This will apply `ruff`'s recommended fixes to the entire codebase.

---

## 📖 API Documentation

- **Interactive Docs (local):**  
  http://localhost:8000/docs

- **ReDoc (local):**  
  http://localhost:8000/redoc

- **Deployed API Docs:**  
  https://lucid-financials-app.onrender.com/docs

---

## 🔒 Security Notes

- All secrets and sensitive config are managed via `.env` and never hardcoded.
- Passwords are hashed using bcrypt with configurable rounds.
- JWT secret and algorithm are configurable.
- Payload size limiting middleware protects against large payload attacks.

---

## 🤝 Contributing

Pull requests are welcome! Please ensure code is well-documented and tested. For major changes, open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the terms of the LICENSE file in this repo.

---

## 📚 Code Style & Documentation

This project follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) for code style and docstring formatting. All functions, classes, and modules include Google-style docstrings for consistency and maintainability.

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JWT (python-jose)](https://python-jose.readthedocs.io/en/latest/)
- [Google Python Style Guide - Docstrings](https://google.github.io/styleguide/pyguide.html#s3.8.1-comments-in-doc-strings)
