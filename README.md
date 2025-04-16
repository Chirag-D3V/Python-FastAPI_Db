# SQLite Database Connection and CRUD Operations with FastAPI and Command-Line Interface

FastAPI app with SQLite and SQLAlchemy ORM for user CRUD operations. Includes web routes with Pydantic validation, a CLI for database actions, and automatic table creation with proper session management on startup.

## 🚀 Features

- FastAPI for high-performance APIs
- Modular code structure
- Easy development with hot-reloading
- Dependency management via `requirements.txt`

---

## 📦 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Chirag-D3V/Python-FastAPI_Db.git
```
---

### 2. Create & Activate Virtual Environment

**Using `venv`:**

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the Server

```bash
uvicorn main:app --reload
```

- This assumes your FastAPI app is in `main.py` and the FastAPI instance is named `app`.
- `--reload` enables hot-reloading during development.

---

## 🧪 API Testing

Once the server is running:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
