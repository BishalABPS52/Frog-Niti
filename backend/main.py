from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import kb as kb_module, baseline
from app.schemas import AskRequest, AskResponse

app = FastAPI(title="Niti-Agent API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Next.js, Vite
    allow_methods=["*"],
    allow_headers=["*"],
)

KB = kb_module.load_all()


@app.get("/health")
def health():
    return {"status": "ok", "procedures_loaded": len(KB)}


@app.get("/procedures")
def procedures():
    return [{"id": p.id, "title_en": p.title_en, "municipality": p.municipality} for p in KB.values()]


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    # Step 1 baseline (no AI). Later: replace with the AI router + RAG + composer.
    return baseline.answer(req.question, KB)
