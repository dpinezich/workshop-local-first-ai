"""
Local-First AI Workshop – Backend
=================================
Fertiges Geruest. Die Teilnehmer implementieren nur:
  - rag.py    (Block 5)
  - router.py (Block 6)

Start:  uvicorn main:app --reload --port 8000
"""
import base64
import subprocess
import tempfile
import time
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI

import config
import router
import rag

app = FastAPI(title="Local-First AI Stack")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

local_client = OpenAI(base_url=config.OLLAMA_BASE_URL, api_key="ollama")


# ── Chat mit intelligentem Routing (Block 3 + 6) ─────────────────────────────
class ChatRequest(BaseModel):
    messages: list[dict]
    force_backend: str | None = None   # "local" | "cloud" | None = Router entscheidet


@app.post("/api/chat")
def chat(req: ChatRequest):
    try:
        backend = req.force_backend or router.choose_backend(req.messages)
    except NotImplementedError:
        backend = "local"   # Bis Block 6: Router noch nicht gebaut -> alles lokal

    def system_prompt(model: str, ort: str) -> str:
        # Eigener system-Prompt im Request gewinnt, sonst die Stellenbeschreibung aus config.py
        own = " ".join(m["content"] for m in req.messages if m["role"] == "system")
        return own or config.SYSTEM_PROMPT.format(model=model, ort=ort)

    def stream_local():
        msgs = [{"role": "system", "content": system_prompt(config.LOCAL_CHAT_MODEL, "lokal per Ollama auf diesem Laptop, ohne Internet")}]
        msgs += [m for m in req.messages if m["role"] != "system"]
        s = local_client.chat.completions.create(
            model=config.LOCAL_CHAT_MODEL, messages=msgs, stream=True,
            max_tokens=config.LOCAL_MAX_TOKENS or None,
            extra_body=config.LOCAL_EXTRA_BODY)
        for chunk in s:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    def stream_cloud():
        if not config.ANTHROPIC_API_KEY:
            yield "[Cloud nicht konfiguriert – ANTHROPIC_API_KEY fehlt. Antworte lokal:]\n\n"
            yield from stream_local()
            return
        import anthropic
        c = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        msgs = [m for m in req.messages if m["role"] != "system"]
        with c.messages.stream(model=config.CLOUD_MODEL, max_tokens=4096,
                               system=system_prompt(config.CLOUD_MODEL, "in der Cloud bei Anthropic"),
                               messages=msgs) as s:
            for text in s.text_stream:
                yield text

    gen = stream_local() if backend == "local" else stream_cloud()
    return StreamingResponse(gen, media_type="text/plain",
                             headers={"X-Backend": backend})


# ── RAG (Block 5) ────────────────────────────────────────────────────────────
class RagRequest(BaseModel):
    question: str


@app.post("/api/rag/query")
def rag_query(req: RagRequest):
    try:
        return rag.answer(req.question)
    except NotImplementedError as e:
        raise HTTPException(501, f"Noch nicht implementiert: {e} – siehe rag.py")


@app.post("/api/rag/reindex")
def rag_reindex():
    try:
        n = rag.build_index()
        return {"indexed": n}
    except NotImplementedError as e:
        raise HTTPException(501, f"Noch nicht implementiert: {e} – siehe rag.py")


# ── Transkription via whisper.cpp (Block 4) ─────────────────────────────────
@app.post("/api/transcribe")
def transcribe(file: UploadFile = File(...)):
    if not config.ENABLE_UPLOADS:
        raise HTTPException(403, "Uploads sind noch deaktiviert (ENABLE_UPLOADS=1 setzen – Block 6!)")
    if not config.WHISPER_BIN or not config.WHISPER_MODEL:
        raise HTTPException(501, "WHISPER_BIN / WHISPER_MODEL nicht gesetzt – siehe README")
    with tempfile.NamedTemporaryFile(suffix=Path(file.filename).suffix, delete=False) as tmp:
        tmp.write(file.file.read())
        audio_path = tmp.name
    t0 = time.time()
    result = subprocess.run(
        [config.WHISPER_BIN, "-m", config.WHISPER_MODEL, "-l", "de",
         "--no-timestamps", "-f", audio_path],
        capture_output=True, text=True, timeout=300)
    return {"text": result.stdout.strip(), "seconds": round(time.time() - t0, 1)}


# ── Vision (Block 4) ─────────────────────────────────────────────────────────
@app.post("/api/vision")
def vision(file: UploadFile = File(...),
           prompt: str = "Beschreibe dieses Bild auf Deutsch in maximal fünf Sätzen. Bei Dokumenten: Absender, Datum, Betrag."):
    if not config.ENABLE_UPLOADS:
        raise HTTPException(403, "Uploads sind noch deaktiviert (ENABLE_UPLOADS=1 setzen – Block 6!)")
    b64 = base64.b64encode(file.file.read()).decode()
    resp = local_client.chat.completions.create(
        model=config.LOCAL_VISION_MODEL, extra_body=config.LOCAL_EXTRA_BODY,
        messages=[{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
        ]}])
    return {"description": resp.choices[0].message.content}


# ── Feature-Flags & Health ───────────────────────────────────────────────────
@app.get("/api/features")
def features():
    return {"uploads": config.ENABLE_UPLOADS,
            "cloud": bool(config.ANTHROPIC_API_KEY),
            "local_model": config.LOCAL_CHAT_MODEL}


@app.get("/api/health")
def health():
    try:
        local_client.models.list()
        return {"ollama": "ok"}
    except Exception as e:
        return {"ollama": f"nicht erreichbar: {e}"}
