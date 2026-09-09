#!/usr/bin/env bash
# Local-First AI Workshop – Setup-Check
# Gruen = bereit fuer den Workshop. Rot = bitte Hinweis befolgen (oder am Workshop die Modelle vom Instruktor kopieren).
set -u
GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
OK=0; FAIL=0

check() { # $1 label, $2 result(0/1), $3 hint
  if [ "$2" -eq 0 ]; then printf "${GREEN}  ✓ %s${NC}\n" "$1"; OK=$((OK+1));
  else printf "${RED}  ✗ %s${NC}\n    → %s\n" "$1" "$3"; FAIL=$((FAIL+1)); fi
}

echo ""
echo "═══ Local-First AI · Setup-Check ═══"
echo ""

# 1) Ollama installiert?
command -v ollama >/dev/null 2>&1; check "Ollama installiert" $? "https://ollama.com/download"

# 2) Ollama laeuft?
curl -s --max-time 3 http://localhost:11434/api/tags >/dev/null 2>&1
check "Ollama laeuft (Port 11434)" $? "Ollama-App starten oder 'ollama serve' ausfuehren"

# 3) Modelle vorhanden?
if curl -s --max-time 3 http://localhost:11434/api/tags >/dev/null 2>&1; then
  INSTALLED=$(ollama list 2>/dev/null | tail -n +2 | awk '{print $1}')
  while read -r MODEL KIND; do
    [ -z "$MODEL" ] && continue; case "$MODEL" in \#*) continue;; esac
    if echo "$INSTALLED" | grep -q "^${MODEL}"; then
      check "Modell $MODEL" 0 ""
    else
      if [ "$KIND" = "pflicht" ]; then
        check "Modell $MODEL" 1 "ollama pull $MODEL"
      else
        printf "${YELLOW}  ~ Modell %s (nur %s) fehlt – ok${NC}\n" "$MODEL" "$KIND"
      fi
    fi
  done < MODELS.txt
fi

# 4) Python – bevorzugt die venv im Repo (.venv oder backend/.venv), sonst python3 aus dem PATH.
#    So stimmt der Check auch, wenn die venv gerade nicht aktiviert ist.
if [ -x .venv/bin/python ]; then PY=.venv/bin/python; PYWO="(.venv)";
elif [ -x backend/.venv/bin/python ]; then PY=backend/.venv/bin/python; PYWO="(backend/.venv)";
else PY=python3; PYWO="(python3 im PATH – keine .venv gefunden)"; fi
PYV=$($PY -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")' 2>/dev/null || echo "0.0")
$PY -c 'import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)' 2>/dev/null
check "Python >= 3.11 (gefunden: $PYV $PYWO)" $? "python3 -m venv .venv && source .venv/bin/activate  – oder https://docs.astral.sh/uv/"

# 5) Python-Abhaengigkeiten – fehlen sie, legt das Skript die .venv gleich selbst an und installiert sie.
#    (Nur wenn Python >= 3.11 ist; sonst wuerde eine unbrauchbare venv entstehen.)
if ! $PY -c 'import fastapi, openai, numpy, uvicorn' 2>/dev/null && [ "$PYV" != "0.0" ] \
   && python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)' 2>/dev/null; then
  if [ ! -x .venv/bin/python ]; then
    printf "${YELLOW}  ~ keine .venv gefunden – lege .venv an ...${NC}\n"
    if ! python3 -m venv .venv >/dev/null 2>&1; then
      rm -rf .venv
      if command -v uv >/dev/null 2>&1; then uv venv .venv >/dev/null 2>&1;
      else printf "${RED}    'python3 -m venv' schlug fehl (Linux: sudo apt install python3-venv)${NC}\n"; fi
    fi
  fi
  if [ -x .venv/bin/python ]; then
    printf "${YELLOW}  ~ installiere Python-Pakete in .venv (1–2 min, einmalig) ...${NC}\n"
    if ! .venv/bin/python -m pip install -q -r backend/requirements.txt 2>&1 | tail -n 3; then :; fi
    PY=.venv/bin/python
  fi
fi
$PY -c 'import fastapi, openai, numpy, uvicorn' 2>/dev/null
check "Python-Pakete (fastapi, openai, numpy, uvicorn)" $? "python3 -m venv .venv && source .venv/bin/activate && pip install -r backend/requirements.txt"

# 6) Node (optional, fuer das Vue-Frontend)
if command -v node >/dev/null 2>&1; then
  NODEV=$(node --version)
  node -e 'process.exit(parseInt(process.version.slice(1))>=20?0:1)'
  check "Node >= 20 (gefunden: $NODEV)" $? "https://nodejs.org – ohne Node läuft das Frontend als Demo am Beamer"
else
  printf "${YELLOW}  ~ Node nicht gefunden – Frontend-Teil dann als Demo am Beamer (kein Blocker)${NC}\n"
fi

# 6b) Frontend-Abhaengigkeiten (optional) – fehlen sie, laeuft npm install gleich hier.
if command -v node >/dev/null 2>&1; then
  if [ ! -d frontend/node_modules ] && command -v npm >/dev/null 2>&1; then
    printf "${YELLOW}  ~ frontend/node_modules fehlt – npm install (1 min, einmalig) ...${NC}\n"
    (cd frontend && npm install --no-audit --no-fund --loglevel=error 2>&1 | tail -n 3)
  fi
  if [ -d frontend/node_modules ]; then check "Frontend-Pakete (frontend/node_modules)" 0 "";
  else printf "${YELLOW}  ~ frontend/node_modules fehlt – cd frontend && npm install (sonst am Workshop)${NC}\n"; fi
fi

# 6c) whisper.cpp (optional – Vorbereitungs-Mail Schritt 5: Mac per brew, Linux als ~/whisper/whisper-cli)
if command -v whisper-cli >/dev/null 2>&1; then check "whisper-cli installiert" 0 "";
elif [ -x "$HOME/whisper/whisper-cli" ]; then check "whisper-cli (~/whisper/whisper-cli)" 0 "";
else printf "${YELLOW}  ~ whisper-cli nicht gefunden – Vorbereitungs-Mail Schritt 5 (Mac: brew install whisper-cpp, Linux: Archiv nach ~/whisper)${NC}\n"; fi
for WM in ggml-small.bin ggml-large-v3-turbo.bin; do
  if [ -f "$HOME/whisper/$WM" ]; then check "Whisper-Modell ~/whisper/$WM" 0 "";
  else printf "${YELLOW}  ~ ~/whisper/%s fehlt – curl-Zeilen in der Vorbereitungs-Mail, Schritt 5${NC}\n" "$WM"; fi
done

# 7) RAM-Hinweis
if [ "$(uname)" = "Darwin" ]; then RAM_GB=$(( $(sysctl -n hw.memsize) / 1073741824 ));
else RAM_GB=$(( $(grep MemTotal /proc/meminfo | awk '{print $2}') / 1048576 )); fi
if [ "$RAM_GB" -ge 16 ]; then check "RAM: ${RAM_GB} GB" 0 "";
else printf "${YELLOW}  ~ RAM: ${RAM_GB} GB – bitte die Fallback-Modelle (qwen3.5:4b) zusaetzlich pullen${NC}\n"; fi

echo ""
if [ "$FAIL" -eq 0 ]; then
  printf "${GREEN}═══ Alles bestens – los geht's! ═══${NC}\n"
else
  printf "${RED}═══ $FAIL Punkt(e) offen – Hinweise oben befolgen. Klemmt etwas? Einfach melden. ═══${NC}\n"
fi
echo ""
exit $FAIL
