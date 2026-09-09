# Local-First AI · Cheat-Sheet (Take-Home)

## Modell-Empfehlungen nach Hardware (Stand September 2026 – danach selbst prüfen!)

| Hardware | Chat + Vision | Embeddings | Whisper |
|---|---|---|---|
| 8 GB RAM / CPU-only | `qwen3.5:4b` (3.4 GB) | `embeddinggemma` | `small` |
| 16 GB (Apple Silicon / GPU) | `qwen3.5:9b` (6.6 GB), `gemma4:e4b-it-qat` | `embeddinggemma` | `large-v3-turbo` |
| 32 GB+ | `qwen3.5:27b`, `gemma4:12b-it-qat`, `qwen3.6:27b` | `embeddinggemma` oder `bge-m3` | `large-v3-turbo` |

Die Qwen-3.5-Familie ist multimodal: ein Modell für Chat **und** Bilder.
Embeddings auf Deutsch: **mehrsprachiges Modell nehmen** (`embeddinggemma`, `bge-m3`). Das populäre
`nomic-embed-text` ist englisch trainiert und findet «Urlaub» → «Ferien» nicht.
Spezialisten, wenn's drauf ankommt: `glm-ocr` (Dokumente/OCR), `qwen3-coder`
(Code), `moondream` (Vision auf winziger Hardware).

## Die Befehle, die du wirklich brauchst

```bash
ollama pull <modell>        # Modell holen
ollama list                 # Was ist installiert?
ollama ps                   # Was läuft gerade + RAM-Verbrauch
ollama run <modell>         # Chat im Terminal (/bye zum Verlassen)
ollama rm <modell>          # Platz schaffen
OLLAMA_HOST=0.0.0.0 ollama serve   # Für andere im Netz freigeben
```

## Der Eine-Zeile-Trick

```python
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
# Rest deines OpenAI-Codes: unverändert.
```

## Entscheidungsmatrix lokal vs. Cloud

| Aufgabe | Empfehlung |
|---|---|
| Klassifikation, Extraktion, Tagging | **lokal** – schnell, gratis, gut genug |
| Einfache Zusammenfassung, Umformulierung | **lokal** |
| Code-Completion, kleine Snippets | **lokal** |
| Transkription, Bild → Text | **lokal** – Whisper und Vision-Modelle sind reif |
| Private/regulierte Daten (immer!) | **lokal** – nicht verhandelbar |
| Komplexes Reasoning, Mehrschritt-Analysen | **cloud** |
| Sehr lange Kontexte (>32k sinnvoll genutzt) | **cloud** |
| Kreatives Schreiben mit Anspruch | **cloud** |
| Hohes Volumen einfacher Tasks | **lokal** – hier explodieren API-Kosten |

## Quantisierung in einem Satz
Q4 ≈ JPEG 80 %: ein Viertel der Grösse, kaum sichtbarer Verlust – im Zweifel
`Q4_K_M` nehmen (das ist der Ollama-Default ohne Suffix).

## Runtimes in einem Satz
**Ollama** für 95 % der Fälle · **llama.cpp** wenn du Kontrolle willst ·
**MLX** als Apple-Silicon-Bonus (`-mlx`-Tags in Ollama) · **vLLM** erst mit Server.

## Modelle im Team verteilen
1. Ein Rechner als Mirror: `OLLAMA_HOST=0.0.0.0 ollama serve`
2. Oder `~/.ollama/models` auf SSD/Netzlaufwerk kopieren
3. Modellversion pinnen (Tag wie `qwen3.5:9b`, nie `latest`) und Updates bewusst ausrollen

## Begriffe nachschlagen
`docs/glossar.md` – Token, Quantisierung, KV-Cache, Embedding, RAG, Router … je in einem Satz.

## Mehr Modelle
`docs/modelle-2026.md` – rund 30 offene Modelle mit Grösse, Kontext, Stärke und Lizenz (Stand September 2026), plus die Adressen für aktuelle Ranglisten.

## Probier morgen als Erstes
Nimm EINEN wiederkehrenden Task aus deinem Alltag (E-Mail-Kategorisierung,
Ticket-Tagging, Protokoll-Zusammenfassung) und lass ihn eine Woche lokal
laufen. Miss: Qualität ok? Dann hast du deinen Business Case.
