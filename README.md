# Local-First AI – Alles läuft auf deinem Laptop

Starter-Repo zum Workshop vom **8. September 2026** (Raum K91).
Ein kompletter AI-Stack ohne Cloud: Chat, Embeddings/RAG, Transkription,
Bildverarbeitung – plus ein Python-Backend mit intelligentem Routing
und einer Vue-Oberfläche.

## Setup in 5 Schritten (VOR dem Workshop!)

1. **Ollama installieren:** https://ollama.com/download
2. **Modelle pullen** (rund 7 GB – heute machen, nicht am Workshop!):
   ```bash
   ollama pull qwen3.5:9b          # Chat UND Bilder – ein Modell für beides
   ollama pull embeddinggemma    # Embeddings für die semantische Suche (mehrsprachig)
   # Nur bei 8 GB RAM oder ohne GPU zusätzlich:
   ollama pull qwen3.5:4b
   ```
3. **Repo klonen und Python-Abhängigkeiten installieren:**
   ```bash
   git clone https://github.com/dpinezich/workshop-local-first-ai local-first-ai
   cd local-first-ai
   python3 -m venv .venv && source .venv/bin/activate   # Windows: python -m venv .venv; .venv\Scripts\activate
   pip install -r backend/requirements.txt              # oder: uv venv && uv pip install -r backend/requirements.txt
   ```
   Die venv ist Pflicht: Homebrew- und Linux-Python verweigern `pip install` ohne venv («externally managed»).
   `verify-setup` findet die `.venv` im Repo-Ordner auch dann, wenn sie gerade nicht aktiviert ist –
   und legt sie samt Paketen selbst an, falls sie noch fehlt. Dasselbe gilt für `frontend/node_modules`.
4. **Frontend vorbereiten** (Node 20+, optional aber empfohlen):
   ```bash
   cd ../frontend && npm install
   ```
5. **Setup prüfen:**
   ```bash
   ./verify-setup.sh        # macOS / Linux
   .\verify-setup.ps1     # Windows PowerShell
   ```
   → Alles grün? Dann bist du bereit. Den Check schauen wir am Kursstart gemeinsam nochmals an.

## Am Workshop: Stack starten

```bash
# Terminal 1 – Backend
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2 – Frontend
cd frontend && npm run dev        # → http://localhost:5173  (☀️/🌙 oben rechts oder Taste T: hell/dunkel)
```

## Struktur

| Pfad | Was | Wann |
|---|---|---|
| `exercises/kapitel3_api/` | Erste API-Calls, Streaming, Code-Assistent | Block 3 |
| `exercises/kapitel4_whisper_vision/` | Transkription & Bildverarbeitung | Block 4 |
| `exercises/kapitel5_embeddings/` | Semantische Suche von Hand + Doku-Set | Block 5 |
| `backend/rag.py` | **Deine Übung:** Mini-RAG (TODOs) | Block 5 |
| `backend/router.py` | **Deine Übung:** lokal/cloud-Router (TODOs) | Block 6 |
| `backend/solutions/` | Lösungen, falls du hängst – kein Stolz, nur Fortschritt | – |
| `exercises/challenges/` | Für die Schnellen | jederzeit |
| `docs/cheatsheet.md` | Take-Home: Befehle, Modell-Empfehlungen, Entscheidungsmatrix | danach |
| `docs/glossar.md` | Take-Home: alle Begriffe des Tages in je einem Satz | danach |
| `docs/modelle-2026.md` | Take-Home: Landkarte der offenen Modelle (Stand September 2026) mit Grösse, Kontext, Stärke, Lizenz | danach |
| `docs/aufraeumen.md` | Was der Workshop auf dem Laptop hinterlässt – mit Grösse und Löschbefehl, falls du den Platz zurückwillst | danach |
| `docs/local-first-ai-folien.pdf` | Alle Folien des Tages, eine Seite pro Folie (dunkel). Zum Nachlesen | danach |
| `docs/local-first-ai-folien-hell.pdf` | Dieselben Folien auf weissem Grund – zum Ausdrucken | danach |

## Checkpoints

Hängen geblieben? Kein Problem:
```bash
git checkout checkpoint-3   # Stand nach Block 3 (analog 1–5)
git checkout loesung        # kompletter Stack, alles gelöst
```

## Kein/zu wenig RAM? Konferenz-WLAN tot?

Fehlt ein Modell, bekommst du es am Workshop **vom Instruktor per AirDrop oder USB-Stick**:
Ordner nach `~/.ollama/models` kopieren, Ollama neu starten, `ollama list`.

## Wichtige Umgebungsvariablen (Backend)

| Variable | Default | Zweck |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | Kann auf ein Ollama auf einem anderen Rechner zeigen |
| `LOCAL_CHAT_MODEL` | `qwen3.5:9b` | Bei 8 GB RAM: `qwen3.5:4b` |
| `LOCAL_VISION_MODEL` | `qwen3.5:9b` | Dasselbe Modell, es kann sehen |
| `LOCAL_EMBED_MODEL` | `embeddinggemma` | Embeddings für RAG (mehrsprachig, mit Task-Präfix) |
| `ANTHROPIC_API_KEY` | – | Nur der Veranstalter setzt ihn |
| `ENABLE_UPLOADS` | `0` | Block 6: auf `1` → Audio/Bild im UI |
| `LOCAL_MAX_TOKENS` | `600` | Obergrenze pro lokaler Chat-Antwort (Bremse). `0` = keine Grenze |
| `WHISPER_BIN` / `WHISPER_MODEL` | – | Pfade zu whisper.cpp |
