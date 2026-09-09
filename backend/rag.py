"""LOESUNG Block 5 – Mini-RAG komplett."""
from pathlib import Path
import numpy as np
from openai import OpenAI
import config

client = OpenAI(base_url=config.OLLAMA_BASE_URL, api_key="ollama")
DOCS_DIR = Path(config.RAG_DOCS_DIR) if config.RAG_DOCS_DIR else Path(__file__).parent.parent / "exercises" / "kapitel5_embeddings" / "docs"
_index: list[dict] = []


def embed(text: str, kind: str = "document") -> np.ndarray:
    prefix = config.EMBED_QUERY_PREFIX if kind == "query" else config.EMBED_DOC_PREFIX
    resp = client.embeddings.create(model=config.LOCAL_EMBED_MODEL, input=prefix + text)
    return np.array(resp.data[0].embedding)


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def build_index() -> int:
    _index.clear()
    for f in sorted(DOCS_DIR.glob("*.txt")):
        text = f.read_text(encoding="utf-8")
        _index.append({"name": f.stem, "text": text, "vec": embed(text)})
    return len(_index)


def search(question: str, top_k: int = 3) -> list[dict]:
    qvec = embed(question, kind="query")
    scored = [{"name": d["name"], "text": d["text"], "score": cosine(qvec, d["vec"])}
              for d in _index]
    return sorted(scored, key=lambda d: d["score"], reverse=True)[:top_k]


def answer(question: str) -> dict:
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
