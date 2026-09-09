# BLOCK 4 · Whisper & Vision

## A) Transkription mit whisper.cpp

### Direkt im Terminal (so machen wir's zuerst)
```bash
cd exercises/kapitel4_whisper_vision

# Das Programm – aus Schritt 5 der Vorbereitungs-Mail:
WHISPER=whisper-cli                    # macOS (brew install whisper-cpp)
# Linux:               WHISPER=~/whisper/whisper-cli
# Windows PowerShell:  $WHISPER = "$HOME\whisper\whisper-cli.exe"

# Die zwei Modelle:
SMALL=~/whisper/ggml-small.bin
LARGE=~/whisper/ggml-large-v3-turbo.bin

# Beide auf dieselbe Aufnahme – das kleine ist schnell, das grosse genau:
$WHISPER -m $SMALL -l de -f testaudio_1.wav
$WHISPER -m $LARGE -l de -f testaudio_1.wav
```
Laufen beide durch und der Satz von der Montagssitzung erscheint? Dann ist Whisper bereit.
Achte auf «Dicket» und «Feierwoll» beim kleinen Modell – das grosse schreibt Ticket und Firewall.

Modelle fehlen? Einmalig laden (0.5 + 1.6 GB):
```bash
mkdir -p ~/whisper && cd ~/whisper
curl -LO https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin
curl -LO https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
```

### Aufgaben
1. `testaudio_1.wav` mit beiden Modellen: Welche Wörter unterscheiden sich? Welche Version
   würdest du Nina als Protokoll geben?
2. Nimm mit dem Handy 20 Sekunden eigenen Text auf (Sprachmemo, als .m4a oder .wav
   hierher kopieren) – inkl. einem Dialektwort deiner Wahl. Was macht Whisper daraus?
3. `testaudio_2.wav` (mit Hintergrundgeräusch) mit `time $WHISPER ...` davor: Wie viel
   langsamer ist `large-v3-turbo`, und lohnt sich das für eine Stunde Sitzung?

## B) Vision

```bash
python vision_beschreiben.py mein_foto.jpg
python vision_rechnung.py rechnung.png
```

### Aufgaben
1. Fotografiere etwas auf deinem Tisch, lass es beschreiben.
2. `rechnung.png` → strukturiertes JSON. Stimmen alle Felder? Wo halluziniert es?
3. Bonus: eigene Rechnung/Quittung fotografieren und extrahieren.

> `rechnung.png` ist eine fiktive Muster-Rechnung (generiert). `testaudio_1.wav` ist
> eine saubere Aufnahme (Montagssitzung bei Muster Solutions), `testaudio_2.wav` hat
> Hintergrundgeraeusch – absichtlich. Beide sind mit der macOS-Sprachausgabe erzeugt;
> die eigene Handy-Aufnahme in Aufgabe 2 ist der ehrlichere Test.
