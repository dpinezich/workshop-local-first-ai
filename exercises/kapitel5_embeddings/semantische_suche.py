"""
BLOCK 5 · Uebung: Semantische Suche von Hand
============================================
Bevor wir RAG ins Backend bauen, einmal das nackte Prinzip:

  Schritt 1: Woerter vergleichen  ->  python semantische_suche.py woerter
  Schritt 2: Dokumente suchen     ->  python semantische_suche.py "Wie viele Tage Urlaub habe ich?"

DER Test: Das Wort "Urlaub" kommt in KEINEM Dokument vor (wir sagen "Ferien").
Findet die Suche die Ferienregelung trotzdem?
"""
import sys
from pathlib import Path
import numpy as np
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
EMBED_MODEL = "embeddinggemma"     # mehrsprachig! nomic-embed-text findet "Urlaub" auf Deutsch nicht
DOCS = Path(__file__).parent / "docs"

# embeddinggemma will wissen, ob es eine Frage oder ein Dokument sieht ("Task-Praefix").
# Das Modell wurde mit genau solchen Frage/Dokument-Paaren trainiert.
PREFIX = {"query": "task: search result | query: ", "document": "title: none | text: "}


def embed(text: str, kind: str = "document") -> np.ndarray:
    r = client.embeddings.create(model=EMBED_MODEL, input=PREFIX[kind] + text)
    return np.array(r.data[0].embedding)


def cosine(a, b) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def demo_woerter():
    woerter = ["Hund", "Katze", "Kartoffel", "Ferien", "Urlaub", "Vacances"]
    vecs = {w: embed(w, "query") for w in woerter}
    print(f"{'':12}" + "".join(f"{w:>12}" for w in woerter))
    for w1 in woerter:
        zeile = f"{w1:12}"
        for w2 in woerter:
            zeile += f"{cosine(vecs[w1], vecs[w2]):>12.3f}"
        print(zeile)
    print("\nBeobachtung: Hund<->Katze nah, Kartoffel weit weg."
          "\nUnd: Ferien<->Urlaub<->Vacances – drei Sprachen, ein Konzept!")


def suche(frage: str):
    print(f"Frage: {frage}\n")
    qvec = embed(frage, "query")
    treffer = []
    for f in sorted(DOCS.glob("*.txt")):
        score = cosine(qvec, embed(f.read_text(encoding="utf-8")))
        treffer.append((score, f.stem))
    for score, name in sorted(treffer, reverse=True)[:5]:
        balken = "█" * int(score * 40)
        print(f"  {score:.3f}  {balken}  {name}")


if __name__ == "__main__":
    arg = " ".join(sys.argv[1:]) or "woerter"
    if arg == "woerter":
        demo_woerter()
    else:
        suche(arg)
