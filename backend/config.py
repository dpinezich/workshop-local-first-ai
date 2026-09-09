"""Zentrale Konfiguration – alles per Umgebungsvariable uebersteuerbar."""
import os

# Lokale Runtime (Ollama). Kann auf ein Ollama auf einem anderen Rechner zeigen:
#   export OLLAMA_BASE_URL=http://<rechner>:11434/v1
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

# qwen3.5 ist multimodal: EIN Modell fuer Chat und Vision. Bei 8 GB RAM: qwen3.5:4b
LOCAL_CHAT_MODEL = os.getenv("LOCAL_CHAT_MODEL", "qwen3.5:9b")
# Embeddings: embeddinggemma ist mehrsprachig trainiert. nomic-embed-text (englisch) findet
# auf Deutsch die Frage "Urlaub" -> Dokument "Ferien" NICHT (live getestet, Rang 8 von 12).
LOCAL_EMBED_MODEL = os.getenv("LOCAL_EMBED_MODEL", "embeddinggemma")
# embeddinggemma will wissen, ob es eine Suchanfrage oder ein Dokument embeddet ("Task-Praefix").
# Ohne Praefix: 3/4 Testfragen richtig, mit Praefix: 4/4. Andere Modelle: leer lassen.
EMBED_QUERY_PREFIX = os.getenv("EMBED_QUERY_PREFIX", "task: search result | query: ")
EMBED_DOC_PREFIX = os.getenv("EMBED_DOC_PREFIX", "title: none | text: ")
LOCAL_VISION_MODEL = os.getenv("LOCAL_VISION_MODEL", LOCAL_CHAT_MODEL)

# Qwen 3.5 "denkt" standardmaessig vor der Antwort (Thinking-Modus) – und zwar lange:
# live gemessen 2'400 Denk-Tokens fuer eine Zwei-Satz-Frage, 2.5 Minuten. Fuer den Workshop
# schalten wir das aus. ACHTUNG: Im OpenAI-kompatiblen Endpoint von Ollama (0.33) wirkt
# NUR reasoning_effort="none"; das Feld "think" wird dort ignoriert (nur native API / CLI).
# LOCAL_THINK=1 setzen, wenn ihr das Denken sehen wollt (dann Geduld mitbringen).
LOCAL_THINK = os.getenv("LOCAL_THINK", "0") == "1"
LOCAL_EXTRA_BODY = {} if LOCAL_THINK else {"reasoning_effort": "none"}

# Bremse (Kapitel 3: max_tokens): Auf «Analysiere … und begründe …» schreibt qwen3.5 sonst einen
# 2'400-Zeichen-Aufsatz – bei 20 Token/s eine Minute, im UI fuehlt sich das wie Haengen an.
# 600 Tokens sind rund eine Bildschirmseite. LOCAL_MAX_TOKENS=0 hebt die Grenze auf.
LOCAL_MAX_TOKENS = int(os.getenv("LOCAL_MAX_TOKENS", "600"))

# System-Prompt = die "Stellenbeschreibung" (Kapitel 3). Ohne ihn weiss ein Modell nicht, wer es
# ist: qwen3.5 antwortet auf "Wer bist du?" mal mit Qwen, mal mit "ein Modell von Google" – die
# Identitaet steht nirgends im Modell, sie kommt aus den Trainingsdaten (live gesehen, 7.9.).
# {model} und {ort} fuellt main.py pro Anfrage: das tatsaechlich benutzte Modell, lokal oder Cloud.
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT",
    "Du bist der Assistent der Muster Solutions AG in Muri AG. Du bist das Sprachmodell {model} "
    "und läufst {ort}. Antworte auf Deutsch in Schweizer Schreibweise (ss statt ß), knapp und konkret.")

# Cloud (nur der Veranstalter setzt den Key – Teilnehmer brauchen keinen!)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLOUD_MODEL = os.getenv("CLOUD_MODEL", "claude-opus-5")   # Preise: 5 USD / 25 USD pro Mio Tokens (in/out)

# whisper.cpp Binary + Modell (Block 4). Leer lassen = Transkription deaktiviert.
WHISPER_BIN = os.getenv("WHISPER_BIN", "")          # z.B. /opt/whisper.cpp/build/bin/whisper-cli
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "")      # z.B. /opt/whisper.cpp/models/ggml-large-v3-turbo.bin

# Dokumentordner fuer RAG (Kapitel 5). Leer = die 12 Wiki-Seiten aus exercises/kapitel5_embeddings/docs.
# Challenge C3: RAG_DOCS_DIR=/pfad/zu/eigenen/texten uvicorn main:app --reload --port 8000
RAG_DOCS_DIR = os.getenv("RAG_DOCS_DIR", "")

# Feature-Flags (Block 6: Uploads erst dann aktivieren)
ENABLE_UPLOADS = os.getenv("ENABLE_UPLOADS", "0") == "1"
