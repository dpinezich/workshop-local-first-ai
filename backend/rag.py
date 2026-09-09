"""
BLOCK 5 · UEBUNG: Mini-RAG in ~60 Zeilen
========================================
Kein Vektor-DB-Framework. Absichtlich. Ihr sollt das PRINZIP sehen:

    1. Dokumente -> Embeddings (einmalig)
    2. Frage -> Embedding
    3. Cosine-Similarity -> beste Dokumente
    4. Dokumente + Frage -> Chat-Modell -> Antwort

Test danach:  Frage nach "Urlaub" – findet es die Seite ueber "Ferien"?

Haengst du fest?  ->  backend/solutions/rag.py
"""
from pathlib import Path
import numpy as np
from openai import OpenAI
import config

client = OpenAI(base_url=config.OLLAMA_BASE_URL, api_key="ollama")
DOCS_DIR = Path(config.RAG_DOCS_DIR) if config.RAG_DOCS_DIR else Path(__file__).parent.parent / "exercises" / "kapitel5_embeddings" / "docs"

_index: list[dict] = []   # [{"name": ..., "text": ..., "vec": np.array}, ...]


def embed(text: str, kind: str = "document") -> np.ndarray:
    """Text -> Vektor, via lokalem Embeddings-Modell.

    kind = "document" beim Indexieren, "query" fuer die Frage. embeddinggemma bekommt
    dafuer ein kurzes Praefix (config.EMBED_DOC_PREFIX / EMBED_QUERY_PREFIX) – es wurde
    mit genau solchen Paaren trainiert und findet so deutlich besser.
    """
    # TODO 1: prefix = config.EMBED_QUERY_PREFIX if kind == "query" else config.EMBED_DOC_PREFIX
    #         resp = client.embeddings.create(model=config.LOCAL_EMBED_MODEL, input=prefix + text)
    #         Rueckgabe: np.array(resp.data[0].embedding)
    raise NotImplementedError("TODO 1: embed implementieren")


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Wie aehnlich sind zwei Vektoren? 1.0 = identische Richtung."""
    # TODO 2: np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    raise NotImplementedError("TODO 2: cosine implementieren")


def build_index() -> int:
    """Alle .txt aus DOCS_DIR embedden und im Speicher halten."""
    _index.clear()
    for f in sorted(DOCS_DIR.glob("*.txt")):
        text = f.read_text(encoding="utf-8")
        # TODO 3: Vektor berechnen und dict an _index anhaengen
        raise NotImplementedError("TODO 3: build_index vervollstaendigen")
    return len(_index)


def search(question: str, top_k: int = 3) -> list[dict]:
    """Die top_k aehnlichsten Dokumente zur Frage."""
    # TODO 4: Frage embedden (kind="query"!), Cosine zu jedem Dokument, absteigend sortieren
    raise NotImplementedError("TODO 4: search implementieren")


def answer(question: str) -> dict:
    """RAG: Suche + Kontext in den Prompt + lokales Chat-Modell."""
    if not _index:
        build_index()
    hits = search(question)
    context = "\n\n---\n\n".join(f"[{h['name']}]\n{h['text']}" for h in hits)
    resp = client.chat.completions.create(
        model=config.LOCAL_CHAT_MODEL, extra_body=config.LOCAL_EXTRA_BODY,
        messages=[
            {"role": "system", "content":
             "Beantworte die Frage NUR anhand der folgenden internen Dokumente. "
             "Nenne das Dokument, aus dem die Antwort stammt. "
             "Steht die Antwort nicht in den Dokumenten, sag das ehrlich.\n\n" + context},
            {"role": "user", "content": question},
        ],
    )
    return {"answer": resp.choices[0].message.content,
            "sources": [{"name": h["name"], "score": round(h["score"], 3)} for h in hits]}
