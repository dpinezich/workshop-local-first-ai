# Aufräumen · Was der Workshop auf deinem Laptop hinterlässt

Alles, was du für den Workshop installiert hast, an einem Ort – mit Grösse und dem Befehl,
der es wieder entfernt. Nichts davon läuft im Hintergrund weiter, ausser der Ollama-App,
solange sie in der Menüleiste steht.

**Empfehlung vorweg:** Behalte Ollama und ein Modell. Das sind 7 GB, und damit hast du
zuhause alles, um einen eigenen Task eine Woche lokal laufen zu lassen (Take-Home-Folie).
Den Rest kannst du gefahrlos löschen.

## Was wo liegt

| Was | Wo | Grösse | Behalten? |
|---|---|---|---|
| Modelle | `~/.ollama/models` (Windows: `%USERPROFILE%\.ollama\models`) | 10–20 GB | mindestens `qwen3.5:9b` |
| Ollama-App | `/Applications/Ollama.app` · Windows: Apps · Linux: `/usr/local/bin/ollama` | 1 GB | ja, wenn du weitermachst |
| Whisper | Mac: `brew` · Windows/Linux: `~/whisper` (Modelle immer in `~/whisper`) | 2 GB | nur für Transkription |
| Repo | der Ordner `local-first-ai` mit `.venv` und `frontend/node_modules` | 1 GB | Lösungen sind auf GitHub, Branch `loesung` |
| Continue (VS Code) | Extension + `~/.continue` | 200 MB | nur, wenn du den Offline-Copilot nutzt |

Python, Node, Homebrew, Git und VS Code waren vermutlich schon vorher da – die lassen wir in Ruhe.

## Schritt für Schritt

### 1. Modelle löschen (der grosse Brocken)

```bash
ollama list                                   # was ist da?
ollama rm qwen3.5:4b                          # einzeln …
ollama rm qwen3.5:9b embeddinggemma           # … oder mehrere auf einmal
```

Wer alles auf einmal weg will: Ollama beenden (Menüleiste → Quit), dann den Ordner löschen:

```bash
rm -rf ~/.ollama                              # Mac / Linux
```
```powershell
Remove-Item -Recurse -Force $HOME\.ollama    # Windows PowerShell
```

### 2. Ollama-App deinstallieren (optional)

- **Mac:** Ollama in der Menüleiste beenden, `Ollama.app` aus `/Applications` in den Papierkorb, dann `rm -rf ~/.ollama`.
- **Windows:** Einstellungen → Apps → Ollama → Deinstallieren, dann `%USERPROFILE%\.ollama` löschen.
- **Linux:** `sudo systemctl stop ollama && sudo systemctl disable ollama`, dann `sudo rm /etc/systemd/system/ollama.service /usr/local/bin/ollama` und `sudo rm -rf /usr/share/ollama`.

### 3. Whisper

```bash
brew uninstall whisper-cpp                    # Mac (falls per brew installiert)
rm -rf ~/whisper                              # Mac / Linux: Modelle und ggf. whisper-cli
```
```powershell
Remove-Item -Recurse -Force $HOME\whisper    # Windows
```

### 4. Repo

Den Ordner `local-first-ai` löschen. Er enthält alles Weitere (`.venv`, `frontend/node_modules`,
deine gelösten Übungen). Nichts liegt ausserhalb. Wenn du deine Lösungen behalten willst:
`backend/rag.py` und `backend/router.py` vorher kopieren.

### 5. Continue in VS Code

Extensions → Continue → Uninstall, dann `rm -rf ~/.continue` (Windows: `%USERPROFILE%\.continue`).

## Kontrolle

```bash
ollama list          # leer oder «command not found»
du -sh ~/.ollama ~/whisper ~/.continue 2>/dev/null    # nichts mehr da
```

## Und wer alles behält?

Dann nur eines: `ollama rm qwen3.5:9b-q8_0`, falls du das Vergleichsmodell aus der
Quantisierungs-Demo geladen hast – 11 GB, die niemand braucht. Alles andere ist der Stack,
mit dem du morgen weitermachst.
