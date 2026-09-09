# Glossar · Local-First AI

Die Begriffe des Tages, je in einem Satz – und wo sie im Workshop vorkommen. Zum Nachschlagen
und Weitergeben. (Kapitel = die Geschichte von Lea und der Muster Solutions AG.)

## Das Modell

| Begriff | Bedeutung | Wo |
|---|---|---|
| **LLM** (Large Language Model) | Ein Programm aus Milliarden gelernter Zahlen, das zu einem Text das wahrscheinlichste nächste Token rät – immer wieder, bis die Antwort steht. | Kap. 1 |
| **Token** | Die Einheit, in der ein Modell liest und schreibt: ein Wortstück, etwa ¾ Wort. Wird auch abgerechnet. | Kap. 1 |
| **Parameter / Gewichte** | Die gelernten Zahlen im Modell. «9B» = 9 Milliarden. Mehr Parameter = mehr Können, mehr RAM, weniger Tempo. | Kap. 1, 2 |
| **Training** | Das Lernen der Gewichte aus riesigen Textmengen. Braucht tausende GPUs; macht der Hersteller. | Kap. 1 |
| **Pretraining** | Phase 1 des Trainings: nächstes Token raten auf Billionen Tokens Text. Ergebnis ist ein Basismodell, das nur weiterschreiben kann. | Kap. 2 |
| **Instruction-Tuning** | Phase 2: das Basismodell lernt aus Frage-Antwort-Beispielen, als Assistent zu antworten (Rollen system/user/assistant). | Kap. 2 |
| **Tokenizer** | Die feste Tabelle (~150'000 Einträge), die Text in Tokens zerlegt. Häufige Wörter sind ein Token, seltene und Deutsch zerfallen in mehrere. | Kap. 1 |
| **Inferenz** | Das Anwenden eines fertig trainierten Modells. Das, was auf eurem Laptop läuft. | Kap. 1 |
| **Transformer** | Die Architektur fast aller heutigen Sprachmodelle: Embedding → viele Schichten aus Attention + MLP → Ausgabe. | Kap. 2 |
| **Attention** | Der Baustein, mit dem jedes Token auf alle vorherigen «schaut» und sich holt, was für seine Bedeutung wichtig ist («die Bank am Fluss»). | Kap. 2 |
| **MLP** (Feed-Forward-Schicht) | Der Baustein, in dem das Faktenwissen sitzt. Rund zwei Drittel aller Parameter. | Kap. 2 |
| **Kontextfenster** (`num_ctx`) | Wie viele Tokens das Modell gleichzeitig «im Kopf» hat: System-Prompt + Verlauf + Frage + Antwort. Was rausfällt, ist vergessen. | Kap. 3 |
| **KV-Cache** | Zwischenspeicher der Attention für alle bisherigen Tokens. Wächst mit dem Kontext – deshalb kostet Kontext RAM. | Kap. 2, 3 |
| **Dicht** (dense) | Modell, bei dem alle Parameter bei jedem Token rechnen. Qwen 3.5 9B, Llama, Gemma. | Kap. 2 |
| **Mixture of Experts** (MoE) | Modell mit vielen «Experten», von denen pro Token nur einige rechnen. Schnell, aber der RAM muss alle halten. DeepSeek, GPT-OSS. | Kap. 2 |
| **Thinking / Reasoning-Modus** | Das Modell schreibt vor der Antwort einen (versteckten) Gedankengang. Bessere Ergebnisse beim Schlussfolgern, deutlich langsamer. Bei Qwen 3.5 abschaltbar (`reasoning_effort="none"`). | Kap. 2, 3 |
| **Post-Training / RLHF** | Nachschliff nach dem Vortraining: das Modell lernt aus menschlichem Feedback, hilfreich und im richtigen Ton zu antworten. Hier unterscheiden sich Cloud-Modelle am meisten. | Kap. 2 |
| **Multimodal / VLM** | Modell, das neben Text auch Bilder versteht: ein Vision-Encoder macht aus Bildkacheln Tokens. Qwen 3.5 kann das. | Kap. 4 |

## Grösse und Tempo

| Begriff | Bedeutung | Wo |
|---|---|---|
| **Quantisierung** | Gewichte gröber speichern (16 Bit → 4 Bit) – ein Viertel des Speichers, kaum Qualitätsverlust. «JPEG für Gewichte». | Kap. 2 |
| **Q4_K_M, Q8_0** | Quantisierungsstufen. Q4_K_M = 4 Bit mit genaueren wichtigen Schichten, der Ollama-Standard. Q8 = fast verlustfrei, doppelt so gross. | Kap. 2 |
| **GGUF** | Das Dateiformat für quantisierte Modelle bei llama.cpp und Ollama. Eine Datei, läuft auf CPU und GPU. | Kap. 2 |
| **Perplexity** | Messwert für Modellqualität: wie «überrascht» das Modell von echtem Text ist. Kleiner = besser. Damit misst man Quantisierungsverlust. | Kap. 2 |
| **Speicherbandbreite** | Wie schnell Daten zwischen RAM und Rechenwerk fliessen. Bestimmt die Token pro Sekunde: Bandbreite ÷ Modellgrösse. | Kap. 2 |
| **Unified Memory** | Apple Silicon: CPU und GPU teilen sich denselben schnellen Speicher. Deshalb laufen grosse Modelle auf MacBooks gut. | Kap. 2 |
| **Prefill** | Erste Phase eines Aufrufs: der ganze Prompt wird parallel verarbeitet. Bestimmt die Pause vor dem ersten Token. | Kap. 2 |
| **Decode** | Zweite Phase: Token für Token generieren. Seriell, bandbreitenlimitiert. Bestimmt die Token pro Sekunde. | Kap. 2 |
| **Time to first token / Token pro Sekunde** | Die zwei Tempo-Masse: Wartezeit bis zur ersten Ausgabe, und Geschwindigkeit danach. | Kap. 2 |

## Betrieb

| Begriff | Bedeutung | Wo |
|---|---|---|
| **Runtime** | Das Programm, das ein Modell lädt und ausführt: Tokenizer, Prefill, Decode, Sampling. | Kap. 2 |
| **Ollama** | Die einfachste Runtime: ein Server auf Port 11434 mit CLI, Modell-Registry und OpenAI-kompatibler API. Nutzt llama.cpp oder MLX. | Kap. 2 |
| **llama.cpp** | Die C++-Bibliothek unter Ollama. Direkt nutzen, wenn man Threads, Offloading, Kontext selbst steuern will. | Kap. 2 |
| **MLX** | Apples Framework für Modelle auf Apple Silicon. In Ollama als `-mlx`-Tags. | Kap. 2 |
| **vLLM** | Runtime für GPU-Server: bedient viele Nutzer gleichzeitig («Continuous Batching»). Auf dem Laptop nutzlos. | Kap. 2, 8 |
| **Modell-Tag** | Name plus Version, z. B. `qwen3.5:9b`. Immer pinnen, nie `latest` – ein Modellwechsel ist ein Release. | Kap. 2, 8 |
| **`keep_alive`** | Wie lange Ollama ein Modell nach dem letzten Aufruf im RAM behält (Default 5 min). | Kap. 2 |
| **Mirror** | Ein Rechner, der Modelle im lokalen Netz bereitstellt (`OLLAMA_HOST=0.0.0.0`) – das Rezept für die Verteilung im Team. | Kap. 8 |
| **Eval-Set** | Eine feste Sammlung echter Aufgaben mit richtigen Antworten. Jedes neue Modell muss sie bestehen, bevor es ausgerollt wird. | Kap. 7, 8 |

## Prompt und API

| Begriff | Bedeutung | Wo |
|---|---|---|
| **Client / Server** | Der Client fragt (euer Skript, der Browser, das Terminal), der Server antwortet (Ollama, wartet im Hintergrund). | Kap. 3 |
| **localhost / Port** | `localhost` = dieser Laptop. Der Port ist die Türnummer, hinter der ein Server wartet: Ollama 11434, Backend 8000, Frontend 5173. | Kap. 3 |
| **API / Endpoint** | Die Schnittstelle: welche Adressen es gibt und wie Anfrage und Antwort aussehen. Ein Endpoint ist eine dieser Adressen, z. B. `/v1/chat/completions`. | Kap. 3 |
| **JSON** | Das Textformat, in dem Programme Daten austauschen: `{"schlüssel": "wert"}`. Lesbar für Mensch und Maschine. | Kap. 3, 4 |
| **Prompt** | Alles, was ihr dem Modell schickt: Anweisung, Verlauf, Frage. | Kap. 3 |
| **Rollen** (`system`, `user`, `assistant`) | Die drei Nachrichtentypen jeder Chat-API. `system` = die Stellenbeschreibung, `user`/`assistant` = das Protokoll. | Kap. 3 |
| **System-Prompt** | Die Anweisung, die immer zuerst kommt: Ton, Regeln, Wissen. Hier steckt der grösste Teil der Qualität – und bei RAG der Kontext. | Kap. 3, 5 |
| **Zustandslos** | Das Modell merkt sich nichts zwischen Aufrufen. «Gedächtnis» heisst: der Verlauf wird jedes Mal mitgeschickt. | Kap. 3, 6 |
| **Chat-Template** | Wie Runtime und Modell die Rollen intern in einen Text mit Sondermarkierungen packen. Macht Ollama für euch. | Kap. 3 |
| **Sampling** | Die Auswahl des nächsten Tokens aus den Wahrscheinlichkeiten: der «Würfel». | Kap. 3 |
| **`temperature`** | Wie stark gewürfelt wird. 0 = immer das wahrscheinlichste Token (reproduzierbar), 1.5 = kreativ bis wirr. | Kap. 3 |
| **`top_p`, `top_k`** | Begrenzen, aus wie vielen Kandidaten gewürfelt wird. Feintuning, selten nötig. | Kap. 3 |
| **`max_tokens`** | Obergrenze für die Länge der Antwort. Schützt vor endlosen Antworten und Wartezeiten – und deckelt in der Cloud die Kosten. | Kap. 3 |
| **`reasoning_effort`** | Der Schalter für den Thinking-Modus über die OpenAI-kompatible API: `extra_body={"reasoning_effort": "none"}` schaltet das Denken bei Qwen 3.5 aus. Für Erkennen und Extrahieren aus, für Rechenaufgaben an. | Kap. 3 |
| **Streaming** | Tokens sofort weiterreichen, statt auf die fertige Antwort zu warten. Gefühlte Geschwindigkeit. | Kap. 3, 6 |
| **OpenAI-kompatible API** | Der de-facto-Standard für Chat-APIs. Ollama spricht ihn: `base_url` ändern, und bestehender Code läuft lokal. | Kap. 3 |
| **`base_url`** | Die eine Zeile: Adresse des Servers, an den der OpenAI-Client schickt. `http://localhost:11434/v1` = euer Laptop. | Kap. 3 |
| **Halluzination** | Eine flüssig formulierte, aber erfundene Antwort. Gegenmittel: Kontext geben (RAG), Quelle verlangen, «sag, wenn du es nicht weisst». | Kap. 4, 5 |

## Audio und Bild

| Begriff | Bedeutung | Wo |
|---|---|---|
| **Whisper / whisper.cpp** | OpenAIs offenes Transkriptionsmodell und seine C++-Umsetzung. Läuft auf CPU, kennt 99 Sprachen. | Kap. 4 |
| **Spektrogramm** | Ton als Bild: Frequenz über Zeit. Das, was Whisper tatsächlich «liest». | Kap. 4 |
| **Encoder / Decoder** | Encoder «versteht» den Input (Ton, Bild) sprachunabhängig; Decoder schreibt daraus Text, Token für Token – ein kleines Sprachmodell. | Kap. 4 |
| **large-v3-turbo** | Whisper-Variante mit gekürztem Decoder: Qualität von large, sechsmal schneller. | Kap. 4 |
| **Vision-Encoder / Patches** | Das Bild wird in Kacheln zerlegt, jede Kachel wird ein Vektor, ein «Projektor» macht daraus Tokens fürs Sprachmodell. | Kap. 4 |
| **OCR** | Texterkennung aus Bildern. Vision-Modelle können es «nebenbei», Spezialisten (`glm-ocr`) genauer. | Kap. 4 |

## Suche und Wissen

| Begriff | Bedeutung | Wo |
|---|---|---|
| **Embedding** | Ein Text als Punkt im «Bedeutungsraum»: ein Vektor mit ein paar hundert Zahlen. Ähnliche Bedeutung = nahe Punkte. | Kap. 5 |
| **Embedding-Modell** | Ein Sprachmodell ohne Textausgabe: liest Text, gibt den Vektor zurück. Mehrsprachig wählen (`embeddinggemma`)! | Kap. 5 |
| **Cosine-Similarity** | Ähnlichkeitsmass zweier Vektoren = Winkel zwischen ihnen. 1.0 = gleiche Richtung. | Kap. 5 |
| **Semantische Suche** | Suche nach Bedeutung statt Buchstaben: «Urlaub» findet «Ferien». | Kap. 5 |
| **RAG** (Retrieval-Augmented Generation) | Passende Textstücke suchen (Retrieval) und dem Modell in den Prompt geben (Generation). Wissen ohne Training. | Kap. 5 |
| **Index** | Die einmal berechneten Embeddings aller Dokumente, im Speicher oder in einer Vektor-Datenbank. | Kap. 5 |
| **Chunking** | Lange Dokumente in Absätze (Chunks, 200–500 Tokens, leicht überlappend) schneiden und jeden einzeln embedden. Der wichtigste Hebel für RAG-Qualität. | Kap. 5 |
| **Top-k** | Wie viele Treffer die Suche in den Prompt gibt. Im Workshop 3. Mehr = mehr Kontext, längeres Prefill, Modell verliert die Mitte. | Kap. 5 |
| **Vektor-Datenbank** | Speichert Embeddings und findet schnell die nächsten Nachbarn. Für 12 Dokumente reicht numpy; ab Millionen braucht man sie. | Kap. 5 |
| **Fine-Tuning** | Ein Modell mit eigenen Daten nachtrainieren. Lernt Stil und Format, aber keine Fakten zuverlässig. Selten die Antwort. | Kap. 5 |

## Der Stack

| Begriff | Bedeutung | Wo |
|---|---|---|
| **Router** | Die Logik, die pro Anfrage entscheidet: lokal oder Cloud. Regel: privat schlägt alles. | Kap. 6 |
| **Privacy-Grenze** | Die Linie in der Architektur, links davon verlässt nichts das Haus. Code, nicht Policy. | Kap. 6 |
| **Klassifikator** | Ein Modell (oder eine Regel), das eine Eingabe in Kategorien einordnet. Im Router: «privat» / «öffentlich». Muss selbst lokal laufen. | Kap. 6 |
| **Feature-Flag** | Ein Schalter in der Konfiguration, der Funktionen ein-/ausblendet (`ENABLE_UPLOADS`). | Kap. 6 |
| **Checkpoint** | Git-Tag mit dem Stand nach einem Block. `git checkout checkpoint-3` = weiter, ohne hängen zu bleiben. | alle |

## Bewerten und Entscheiden

| Begriff | Bedeutung | Wo |
|---|---|---|
| **Erkennen / Umformen / Schlussfolgern** | Die drei Aufgabenarten. Erkennen (Klassifikation, Extraktion) und Umformen (Zusammenfassen) gehen lokal gut; Schlussfolgern gewinnt die Cloud. | Kap. 7 |
| **Blind-Test** | Gleiche Aufgabe, zwei Antworten, Herkunft verdeckt. Misst, was ihr wirklich braucht – nicht, was Hersteller messen. | Kap. 7 |
| **Benchmark** | Standardisierter Aufgabensatz zum Vergleichen von Modellen. Hersteller-Benchmarks messen meist Schlussfolgern. | Kap. 7 |
| **Latenz** | Wartezeit bis zur Antwort. Lokal: kein Netz, aber langsameres Decode. Cloud: schneller Decode, plus Netz. | Kap. 7 |
| **TCO** (Total Cost of Ownership) | Alle Kosten über die Laufzeit: Hardware, Strom, und die Person, die es betreut – nicht nur der API-Preis. | Kap. 7 |
