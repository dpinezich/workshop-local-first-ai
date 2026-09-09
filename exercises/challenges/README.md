# Challenges – fuer die Schnellen

Fertig vor allen anderen? Hier entlang. Reihenfolge frei.

## C1 (nach Kapitel 3): Modell-Battle
Schreibe ein Skript, das dieselbe Frage an ZWEI lokale Modelle schickt
(z.B. qwen3.5:9b vs. qwen3.5:4b) und Antwort + Latenz nebeneinander ausgibt.

## C2 (nach Kapitel 4): Meeting-Protokoll-Pipeline
Kette: Audio -> whisper.cpp -> Transkript -> lokales Chat-Modell fasst
zusammen und extrahiert Action Items als JSON. Zwei subprocess-Aufrufe
und ein Prompt – mehr braucht es nicht.

## C3 (nach Kapitel 5): Eigene Dokumente – und warum lange Dateien brechen

Unser RAG kennt 12 kurze Wiki-Seiten. Jetzt deine eigenen Texte: ein Reglement, ein
Vertrag, eine Anleitung. Du brauchst kein neues Python, nur einen Ordner und eine
Umgebungsvariable – und am Schluss eine Funktion zum Einfügen.

### Schritt 1: Ordner mit eigenen Texten (5 Min)
```bash
mkdir -p ~/rag-test
cp irgendein_reglement.txt ~/rag-test/          # .txt reicht, 3–5 Dateien
```
PDF? Einmal in Text umwandeln:
```bash
pip install pypdf
python -c "from pypdf import PdfReader; import sys; print('\n'.join(p.extract_text() or '' for p in PdfReader(sys.argv[1]).pages))" vertrag.pdf > ~/rag-test/vertrag.txt
```

### Schritt 2: Backend auf den Ordner zeigen lassen
```bash
cd backend
RAG_DOCS_DIR=~/rag-test uvicorn main:app --reload --port 8000     # Windows PowerShell: $env:RAG_DOCS_DIR="$HOME\rag-test"
curl -X POST localhost:8000/api/rag/reindex                       # → {"indexed": 4}
```
Dann im UI «📚 Dokumente fragen» – Fragen stellen, deren Antwort du kennst.

### Schritt 3: Beobachten, wo es bricht
Mit kurzen Dateien läuft es wie im Workshop. Mit einem 40-Seiten-Vertrag passieren drei Dinge:

1. **Das Embedding-Modell liest nur den Anfang.** embeddinggemma hat ein Kontextfenster von
   2'048 Tokens, etwa drei Seiten. Der Rest wird stillschweigend abgeschnitten – eine Frage
   zu Seite 30 findet nichts.
2. **Ein Vektor für 40 Seiten ist ein Durchschnitt.** Haftung, Preise, Kündigung, Datenschutz
   in einem Vektor zeigen in keine Richtung mehr; der Score zu jeder konkreten Frage bleibt
   mittelmässig.
3. **Der Treffer sprengt den Prompt.** Landet die Datei in den Top 3, klebt `answer()` alle
   40 Seiten in den system-Prompt: langes Prefill, und bei kleinem Kontextfenster fällt vorne
   etwas raus – ohne Fehlermeldung.

### Schritt 4: Chunking – die Lösung zum Einfügen
Statt «eine Datei = ein Vektor»: jede Datei in Stücke von ~1'500 Zeichen schneiden, mit
200 Zeichen Überlappung, jedes Stück einzeln embedden. In `backend/rag.py`:

```python
def chunks(text: str, size: int = 1500, overlap: int = 200) -> list[str]:
    """Text in ueberlappende Stuecke schneiden. Ueberlappung, damit kein Satz an der Grenze verloren geht."""
    out, start = [], 0
    while start < len(text):
        out.append(text[start:start + size])
        start += size - overlap
    return out
```
und in `build_index()` die eine Zeile aus TODO 3 durch eine Schleife ersetzen:
```python
        for n, part in enumerate(chunks(text), start=1):
            _index.append({"name": f"{f.stem}#{n}", "text": part, "vec": embed(part)})
```
`reindex` zeigt jetzt statt 4 Dateien vielleicht 60 Stücke. Die Quellen im UI heissen
`vertrag#17` – und die Frage zu Seite 30 findet ihren Absatz.

### Was du mitnimmst
Genau das tun LangChain, LlamaIndex und jede Vektor-Datenbank im Kern – plus Persistenz
und Millionen statt 60 Stücke. Die Stellschrauben sind dieselben: Stückgrösse, Überlappung,
Anzahl Treffer (`top_k`).

## C4 (nach Kapitel 6): Router-Upgrade
Ersetze die Keyword-Heuristik in router.py durch einen LLM-Klassifikator:
Das LOKALE Modell entscheidet selbst per Prompt ("Antworte nur mit
PRIVAT oder OEFFENTLICH"), ob die Anfrage lokal bleiben muss.
Achtung Denkfalle: Warum darf diese Klassifikation NIE in der Cloud laufen?

## C5 (Koenigsdisziplin): Structured Output
Zwinge das lokale Modell mit response_format / JSON-Schema zu garantiert
validem JSON fuer die Rechnungs-Extraktion aus Block 4.
