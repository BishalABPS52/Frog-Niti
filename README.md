# Niti-Agent (Frogtoberfest)
Conversational guide for Nepali administrative procedures: where to go, online vs in-person,
steps, required and optional documents, with sources and last-verified dates.

## Structure
- `backend/`  FastAPI API + knowledge base loader + baseline (no-AI) bot
- `frontend/` Next.js (App Router) chat UI (create it: see below)
- `data/procedures/` verified procedure records (JSON, validated by schema)
- `data/sources/`    raw collected documents (not committed)
- `eval/`     benchmark questions + results
- `notebooks/` Colab notebooks (bake-off, extraction, fine-tuning)

## Run backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate    Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
# open http://localhost:8000/docs
```

## Create frontend
```bash
npx create-next-app@latest frontend
# suggested answers: TypeScript Yes, ESLint Yes, Tailwind Yes, src/ directory Yes, App Router Yes
cd frontend && npm run dev     # http://localhost:3000
# put the API address in frontend/.env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Rule
No source, no claim. Every procedure needs at least one source + last_verified date.
