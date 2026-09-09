# Vorlage Vorbereitungs-Mail (Versand: T-7, Reminder: T-2)

**Betreff:** Workshop «Local-First AI» am 8.9. – 20 Minuten Vorbereitung nötig

Hallo zusammen

Ich freue mich auf den Workshop am **Dienstag, 8. September, 9:00, Raum K91**!
Damit wir keine Minute mit Downloads verlieren, bitte ich euch um ~20 Minuten
Vorbereitung – **am besten heute, die Modelle sind rund 7 GB gross:**

**1. Kurze Antwort auf diese Mail** mit eurer Hardware:
Mac (Apple Silicon / Intel) oder Windows (mit / ohne Nvidia-GPU) oder Linux – plus RAM-Grösse.

**2. Ollama installieren:** https://ollama.com/download

**3. Modelle laden** (Terminal, Copy-Paste):
```
ollama pull qwen3.5:9b
ollama pull embeddinggemma
```
Bei 8 GB RAM oder ohne Grafikkarte zusätzlich: `ollama pull qwen3.5:4b`

**4. Repo klonen + Setup prüfen:**
```
git clone https://github.com/dpinezich/workshop-local-first-ai local-first-ai
cd local-first-ai
python3 -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..
./verify-setup.sh
```
(Windows in PowerShell: `python -m venv .venv`, `.venv\Scripts\activate`, dann `pip install -r backend\requirements.txt` und `.\verify-setup.ps1`)

**5. Whisper (Transkription) – 5 Minuten, 2 GB Download:**
Whisper ist kein Ollama-Modell, sondern ein eigenes kleines Programm (`whisper-cli`)
plus zwei Modelldateien. Alles kommt in den Ordner `whisper` in eurem Home-Verzeichnis.

*Mac:*
```
brew install whisper-cpp
mkdir -p ~/whisper && cd ~/whisper
curl -LO https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin
curl -LO https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
whisper-cli --help
```

*Windows (PowerShell):*
```
mkdir $HOME\whisper; cd $HOME\whisper
curl.exe -LO https://github.com/ggml-org/whisper.cpp/releases/latest/download/whisper-bin-x64.zip
Expand-Archive whisper-bin-x64.zip -DestinationPath .
Move-Item Release\* .
curl.exe -LO https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin
curl.exe -LO https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
.\whisper-cli.exe --help
```
(Bitte wirklich `curl.exe` mit `.exe` tippen – ohne ist es in PowerShell ein anderes Kommando.)

*Linux:*
```
mkdir -p ~/whisper && cd ~/whisper
curl -LO https://github.com/ggml-org/whisper.cpp/releases/latest/download/whisper-bin-ubuntu-x64.tar.gz
tar xzf whisper-bin-ubuntu-x64.tar.gz --strip-components=1
curl -LO https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin
curl -LO https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
./whisper-cli --help
```
(ARM-Rechner: `ubuntu-arm64` statt `ubuntu-x64`. Meldet `./whisper-cli` einen GLIBC-Fehler, ist
die Distribution älter als 2022 – dann selbst bauen, dauert 2 Minuten:
`sudo apt install build-essential cmake git`, `git clone https://github.com/ggml-org/whisper.cpp`,
`cd whisper.cpp && cmake -B build -DBUILD_SHARED_LIBS=OFF && cmake --build build -j --config Release`,
`cp build/bin/whisper-cli ~/whisper/`.)

Zum Schluss `./verify-setup.sh` bzw. `verify-setup.ps1` nochmals laufen lassen – Whisper und beide
Modelle sollten jetzt grün sein.

**6. Alles grün?** Dann seid ihr bereit. Den Check schauen wir am Dienstag zu Beginn gemeinsam an – wer rot hat, meldet sich einfach vorher.

Keine Sorge, falls etwas rot bleibt oder klemmt: kurz melden, oder am Workshop
gibt es die Modelle von mir per AirDrop oder USB-Stick. Ihr müsst keine Python-Profis sein – alles im Workshop
ist Copy-Paste-fähig, wir bauen Schritt für Schritt.

Was euch erwartet: ein kompletter AI-Stack auf eurem eigenen Laptop – Chat,
Transkription, Bildverarbeitung, semantische Suche, eigenes UI. Und ein
Blind-Quiz, bei dem ihr raten dürft, ob die Antwort vom Laptop oder aus der
Cloud kam. Es gibt Schoggi zu gewinnen.

Bis Dienstag!

---

## Reminder (T-2)

**Betreff:** Reminder Workshop Dienstag – ist dein Setup grün?

Hallo zusammen

Kurzer Reminder für Dienstag 9:00, Raum K91. Wer den `verify-setup`-Check
noch nicht gemacht hat: bitte heute noch nachholen
(Anleitung in der letzten Mail, dauert 20 Minuten, Download rund 7 GB plus 2 GB Whisper).

Bitte mitbringen: Laptop **mit Ladekabel**, Kopfhörer (für die Whisper-Übung),
und ein Handy zum Fotografieren. Wer Windows ohne Nvidia-Grafikkarte hat:
zusätzlich `ollama pull qwen3.5:4b` – dann läuft alles, nur etwas gemütlicher.

Bis Dienstag!
