# PocketSmart AI

A complete FastAPI + Jinja2 + SQLite + Gemini recommendation assistant for Home Interior, Party, and Jewelry budget planning.

## Source-document alignment

The project documentation specifies a modular FastAPI backend, Gemini-powered recommendation generation, the `/generate-home`, `/generate-party`, and `/generate-jewelry` planner endpoints, authentication/session endpoints, history, responsive Jinja2 pages, optional jewelry image input, and fallback recommendations.

This implementation includes those capabilities. Marketplace integrations use safe search URLs rather than scraping or claiming live inventory. Replace `app/services/catalog.py` with licensed APIs/affiliate feeds when credentials are available.

## Gemini model

The document names Gemini 1.5 Flash Pro. Model availability changes over time, so this project makes the model configurable with `GEMINI_MODEL`. The default is `gemini-2.5-flash`. If your Google AI account exposes another supported model, set that model name in `.env`.

Without `GEMINI_API_KEY`, the application automatically uses deterministic fallback recommendations so authentication, UI, database, and API testing still work.

## Setup in VS Code

### Windows PowerShell

```powershell
cd PocketSmartAI
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and add your Gemini API key.

### macOS/Linux

```bash
cd PocketSmartAI
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` and `http://127.0.0.1:8000/docs`.

## Test

```bash
pytest -q
```

## Main routes

Auth:
- POST `/register`
- POST `/login`
- POST `/logout`
- POST `/token`
- GET `/session-info`
- GET `/session-data`

Planning:
- POST `/generate-home`
- POST `/generate-party`
- POST `/generate-jewelry`
- GET `/recommendations-details/{recommendation_id}`
- GET `/history`

System:
- GET `/health`
- GET `/startup`

## Project tree

```text
PocketSmartAI/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── pages.py
│   │   └── recommendations.py
│   └── services/
│       ├── catalog.py
│       ├── gemini_service.py
│       ├── prompts.py
│       └── recommendation_service.py
├── static/css/style.css
├── static/js/app.js
├── templates/
├── tests/
├── docs/
├── .env.example
├── requirements.txt
└── README.md
```

## Production hardening

Use PostgreSQL, HTTPS, a secret manager, rate limiting, logging/observability, licensed marketplace APIs, and stronger file validation before public deployment.
