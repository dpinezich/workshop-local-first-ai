# Kapitel 3 · Übung 4: Dein Copilot läuft offline (Demo am Beamer, 5–10 Min)

Lokale Modelle können auch Code-Assistenz – direkt in VS Code, ohne dass eine Zeile
Code den Laptop verlässt. Der Instruktor zeigt es am Beamer; wer schnell ist, macht mit.

## Was zu konfigurieren ist – genau drei Dinge

| # | Was | Wo |
|---|---|---|
| 1 | Extension **Continue** installieren | VS Code → Extensions (Mac ⇧⌘X · Windows/Linux Ctrl+Shift+X) → «Continue» → Install |
| 2 | Continue sagen, dass es Ollama nehmen soll | Datei `~/.continue/config.yaml` (Windows: `%USERPROFILE%\.continue\config.yaml`) |
| 3 | Das Modell im Chat auswählen | Continue-Seitenleiste → Dropdown über dem Eingabefeld → «qwen3.5:9b lokal» |

Sonst nichts. Kein Account, kein API-Key, keine Cloud.

## Schritt 2 im Detail: die Config

Continue-Seitenleiste öffnen (Icon links, oder ⌘L · Windows/Linux Ctrl+L) → Zahnrad unten rechts → **Open config file**.
Alles ersetzen durch:

```yaml
name: Local-First AI
version: 1.0.0
schema: v1

models:
  # Chat, Erklären, Umschreiben – das Workshop-Modell
  - name: qwen3.5:9b lokal
    provider: ollama
    model: qwen3.5:9b
    roles: [chat, edit, apply]

  # Suche im eigenen Code (@codebase) – dasselbe Embedding-Modell wie in Kapitel 5
  - name: embeddinggemma lokal
    provider: ollama
    model: embeddinggemma
    roles: [embed]
```

Die drei Zeilen, die zählen: `provider: ollama` (nicht openai, nicht anthropic),
`model:` exakt der Name aus `ollama list`, und `roles:` – ohne `chat` erscheint das
Modell nicht im Dropdown.

Speichern reicht, Continue lädt die Config sofort neu. Erscheint das Modell nicht:
läuft Ollama? (`ollama ps` oder http://localhost:11434 im Browser → «Ollama is running»).

## Check: Ist es wirklich lokal?

1. WLAN ausschalten. Ernsthaft. 😎
2. Im Continue-Chat fragen: «Was macht diese Datei?» und dabei `backend/main.py` mit `@` anhängen.
3. Antwortet es? Dann läuft dein Copilot offline. Terminal daneben: `ollama ps` zeigt das Modell mit 100 % GPU.

Qwen 3.5 denkt vor jeder Antwort – die erste Antwort kann 30–60 s dauern. Das ist der
Thinking-Modus aus Übung 1, und Continue lässt ihn eingeschaltet. Wer das nicht mag:
`ollama pull qwen2.5-coder:7b` (4.7 GB, reines Code-Modell, denkt nicht) und in der
Config als zweites Modell eintragen.

## Ausprobieren

Tasten: Mac ⌘ · Windows/Linux Ctrl. ⌘L = Chat mit Markierung, ⌘I = Änderung direkt im Code.

- Eine Funktion in `backend/rag.py` markieren → ⌘L (Ctrl+L) → «Erkläre diese Funktion»
- Markieren → ⌘I (Ctrl+I) → «Schreib einen Docstring dazu» → Diff anschauen, annehmen oder verwerfen
- Chat: «Schreibe einen Pytest für die Funktion cosine() in @backend/solutions/rag.py»

## Ehrlicher Vergleich

Wo ist es gut genug? Wo merkst du den Unterschied zu Copilot oder Claude?
Ein Beispiel pro Richtung notieren – wir sammeln sie im Reality-Check (Kapitel 7).
Erfahrungswert: Docstrings, Tests und Erklärungen bestehen, grössere Umbauten über
mehrere Dateien nicht.
