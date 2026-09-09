# Modelle im September 2026 · Landkarte für den Laptop

Stand: 7. September 2026. Tags, Download-Grössen und Kontextfenster stammen aus der
Ollama-Library (ollama.com/library). Die Spalte **Stärke** ist eine Einschätzung des
Veranstalters aus eigener Nutzung, kein Benchmark – Hersteller-Benchmarks messen vor allem
Schlussfolgern, nicht deine Aufgabe (Kapitel 7). In drei Monaten selbst nachschauen.

**So liest du die Tabellen:** Grösse = Download bei Q4_K_M (Ollama-Default ohne Suffix).
RAM-Bedarf ≈ Grösse + 1–2 GB für den Kontext. Faustregel: 8 GB Laptop → Modelle bis 4 GB,
16 GB → bis 10 GB, 32 GB → bis 20 GB, darüber Server. Kontext = wie viel Text pro Anfrage
(256K ≈ 600 Seiten), aber jedes Token Kontext kostet RAM und Prefill-Zeit (Kapitel 2).

## Chat und Alltag (Text, meist auch Bild)

| Ollama-Tag | Von | Grösse | Kontext | Kann | Stärke | Lizenz |
|---|---|---|---|---|---|---|
| `qwen3.5:4b` | Alibaba | 3.4 GB | 256K | Text, Bild, Denken | Der Kleine für 8 GB und CPU-only. Erstaunlich gutes Deutsch, Bilder inklusive. | Apache 2.0 |
| `qwen3.5:9b` | Alibaba | 6.6 GB | 256K | Text, Bild, Denken | **Das Workshop-Modell.** Bester Allrounder für 16 GB: Erkennen, Extrahieren, Zusammenfassen, Bilder – ein Download. | Apache 2.0 |
| `qwen3.5:27b` | Alibaba | 17 GB | 256K | Text, Bild, Denken | Ab 32 GB. Spürbar sorgfältiger beim Schlussfolgern, gleiche Familie, gleiche Prompts. | Apache 2.0 |
| `qwen3.6:27b` · `qwen3.8:27b` | Alibaba | 17–18 GB | 256K | Text, Bild, Denken | Die neueren 27b-Generationen (3.8 ist der neuste Stand). 3.6 hat eine `-coding`-Variante. Wer 32 GB hat, nimmt hier das Aktuellste. | Apache 2.0 |
| `qwen3.6:35b-a3b` | Alibaba | 23 GB | 256K | Text, Bild, Denken | Mixture of Experts: 35B gespeichert, 3B rechnen pro Token → schnell wie ein Kleiner, weiss wie ein Grosser. Braucht aber den RAM für alles. | Apache 2.0 |
| `gemma4:e4b-it-qat` | Google | 6.1 GB | 128K | Text, Bild, Denken | Googles Antwort für 16 GB. QAT = beim Quantisieren mittrainiert, weniger Verlust als nachträgliches Q4. Sehr sauberes Deutsch. | Gemma-Lizenz |
| `gemma4:12b` (`12b-it-qat` 7.2 GB) | Google | 7.6 GB | 256K | Text, Bild, Denken | Viel Qualität pro Gigabyte, passt noch in 16 GB. Gute Alternative zu qwen3.5:9b, wenn dir dessen Ton nicht gefällt. | Gemma-Lizenz |
| `gemma4:26b` · `gemma4:31b` | Google | 19–20 GB | 256K | Text, Bild, Denken | Die Grossen der Familie für 32 GB und mehr. | Gemma-Lizenz |
| `gpt-oss:20b` | OpenAI | 14 GB | 128K | Text, Denken, Tools | OpenAIs erstes offenes Modell seit GPT-2, Mixture of Experts. Stark beim Schlussfolgern und bei Tool-Aufrufen, kein Bild. 16 GB ist knapp, 24 GB entspannt. | Apache 2.0 |
| `mistral-small3.2:24b` | Mistral, Paris | 15 GB | 128K | Text, Bild, Tools | Der Europäer. Hält sich genau an Anweisungen, gut für strukturierte Ausgaben. Das Argument, wenn jemand «EU» sagt. | Apache 2.0 |
| `ministral-3:3b` · `:8b` · `:14b` | Mistral, Paris | 3–9 GB | 256K | Text, Bild, Tools | Mistrals Kleine, alle mit Bild. Der 8b ist eine echte Alternative zu qwen3.5:9b. | Apache 2.0 (prüfen) |
| `magistral:24b` | Mistral, Paris | 14 GB | 39K | Text, Denken | Mistrals Denk-Modell. Kurzer Kontext, dafür nachvollziehbare Zwischenschritte. | Apache 2.0 |
| `phi4:14b` | Microsoft | 9.1 GB | 16K | Text | Auf Lehrbuch-Daten trainiert: stark bei Logik und Mathe, schwach bei Weltwissen, kurzer Kontext. `phi4-reasoning` (11 GB) denkt dazu. | MIT |
| `deepseek-r1:8b` · `:14b` · `:32b` | DeepSeek | 5–20 GB | 128K | Text, Denken | Das Denken von R1, in kleine Qwen-/Llama-Modelle destilliert. Gut für Aufgaben mit Zwischenschritten, langsam, weil es viele Denk-Tokens schreibt. Kein Bild. | MIT |
| `llama3.3:70b` · `llama4:scout` | Meta | 43 / 67 GB | 128K / 10M | Text (Llama 4: Bild) | Der Klassiker mit der grössten Community, heute eher Server-Klasse. Llama 4 Scout: 16 Experten, riesiger Kontext, 67 GB. | Llama-Lizenz |
| `granite4:3b` · `:1b-h` | IBM | 1.6–2.1 GB | 128K–1M | Text, Tools | Winzig, sehr langer Kontext, gemacht für Tool-Aufrufe in Firmen-Workflows. Kein Chat-Star, aber ein guter Arbeiter. | Apache 2.0 |

## Bilder und Dokumente

| Ollama-Tag | Von | Grösse | Kontext | Stärke | Lizenz |
|---|---|---|---|---|---|
| `qwen3.5:*` | Alibaba | s. oben | 256K | Alle Qwen-3.5-Grössen sehen Bilder. Für Rechnungen, Screenshots, Fotos reicht das Chat-Modell – kein zweites nötig. | Apache 2.0 |
| `qwen3-vl:4b` · `:8b` | Alibaba | 3.3 / 6.1 GB | 256K | Reine Vision-Spezialisten. Wenn Bilder der Hauptjob sind: etwas genauer beim Lesen von Tabellen und Diagrammen. | Apache 2.0 |
| `glm-ocr` | Zhipu | 2.2 GB | 128K | OCR für Dokumente: Tabellen, Formulare, gescannte Briefe → Text oder Markdown. Klein und schnell. | MIT (prüfen) |
| `moondream` | Moondream | 1.7 GB | 2K | Vision auf Mini-Hardware (Raspberry Pi, alte Laptops). Englisch, kurze Beschreibungen. | Apache 2.0 |
| `translategemma:4b` · `:12b` · `:27b` | Google | 3.3–17 GB | 128K | Übersetzungs-Spezialist, auch Text in Bildern. | Gemma-Lizenz |

## Code

| Ollama-Tag | Von | Grösse | Kontext | Stärke | Lizenz |
|---|---|---|---|---|---|
| `qwen2.5-coder:7b` · `:14b` | Alibaba | 4.7 / 9 GB | 32K | Der Klassiker für Autocomplete und «erklär mir diese Funktion» auf 16 GB. Gut in Continue / VS Code. | Apache 2.0 |
| `qwen3-coder:30b` | Alibaba | 19 GB | 256K | Mixture of Experts (3B aktiv): schnell trotz Grösse, ganzer Repo-Kontext. Braucht 32 GB. | Apache 2.0 |
| `qwen3.6:27b-coding` | Alibaba | 18 GB | 256K | Chat-Modell mit Code-Feinschliff, wenn du nur ein 27b-Modell halten willst. | Apache 2.0 |
| `qwen3-coder-next` | Alibaba | 52 GB | 256K | Server-Klasse für Agenten, die selbständig Code ändern. | Apache 2.0 |

## Embeddings (Suche und RAG)

| Ollama-Tag | Von | Grösse | Kontext | Stärke | Lizenz |
|---|---|---|---|---|---|
| `embeddinggemma` | Google | 622 MB | 2K | **Das Workshop-Modell.** Mehrsprachig, winzig, findet «Urlaub» bei «Ferien». | Gemma-Lizenz |
| `bge-m3` | BAAI | 1.2 GB | 8K | Mehrsprachig, längere Abschnitte pro Vektor, stark auf Deutsch. Erste Wahl, wenn embeddinggemma zu kurz greift. | MIT |
| `qwen3-embedding:0.6b` · `:4b` · `:8b` | Alibaba | 0.6–4.7 GB | 32–40K | Mehrsprachig, grösser = genauer. Der 4b ist der beste Kompromiss. | Apache 2.0 |
| `nomic-embed-text` | Nomic | 274 MB | 2K | Sehr beliebt, aber englisch trainiert: findet auf Deutsch «Urlaub» nicht (Rang 8 von 12 im Test). Nicht für deutsche Texte. | Apache 2.0 |

## Nur Server oder Cloud

`gpt-oss:120b` (65 GB), `qwen3.5:122b` (81 GB), `deepseek-r1:671b` (404 GB), `llama4:maverick`
(245 GB), `qwen3-coder:480b` (290 GB): das sind Rechenzentrums-Modelle. Für 50 Leute
gleichzeitig: vLLM statt Ollama, ein Server mit GPU (Kapitel 8). Claude, GPT und Gemini
bleiben Cloud – dort liegt der Vorsprung beim Schlussfolgern, nicht beim Erkennen.

## Wo du aktuelle Zahlen findest

- **ollama.com/library** – was es gibt, Tags, Grössen, Kontext. Nach «popular» sortieren.
- **lmarena.ai** – Menschen vergleichen zwei Antworten blind und stimmen ab. Dasselbe wie unser Quiz, mit Millionen Stimmen.
- **artificialanalysis.ai** – Qualität, Tempo und Preis nebeneinander, auch für offene Modelle.
- **huggingface.co/spaces/open-llm-leaderboard** – akademische Benchmarks der offenen Modelle.
- **Dein eigenes Eval-Set** (Kapitel 7) schlägt jede Rangliste: zwanzig echte Aufgaben aus
  deinem Alltag mit richtigen Antworten, und jedes neue Modell muss sie bestehen.

## Faustregeln

1. **Ein Modell, das Bilder kann, spart ein zweites.** Qwen 3.5, Gemma 4, Ministral 3.
2. **Denken einschalten kostet Zeit.** Für Erkennen und Extrahieren aus, für Schlussfolgern an.
3. **Mixture of Experts = schnell, aber RAM-hungrig.** Alle Experten müssen geladen sein.
4. **Embeddings auf Deutsch: mehrsprachiges Modell.** Sonst findet die Suche nichts.
5. **Version pinnen.** `qwen3.5:9b`, nie `latest`. Update = Eval-Set neu laufen lassen.
6. **Lizenzen lesen, bevor es produktiv geht.** Apache 2.0 und MIT sind frei, Gemma und Llama haben eigene Bedingungen.
