# Local-First AI Workshop – Setup-Check (Windows PowerShell)
$ok = 0; $fail = 0
function Check($label, $result, $hint) {
    if ($result) { Write-Host "  OK  $label" -ForegroundColor Green; $script:ok++ }
    else { Write-Host "  FEHLT  $label" -ForegroundColor Red; Write-Host "    -> $hint"; $script:fail++ }
}
Write-Host "`n=== Local-First AI - Setup-Check ===`n"

Check "Ollama installiert" ([bool](Get-Command ollama -ErrorAction SilentlyContinue)) "https://ollama.com/download"

$running = $false
try { Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -TimeoutSec 3 | Out-Null; $running = $true } catch {}
Check "Ollama laeuft (Port 11434)" $running "Ollama-App starten"

if ($running) {
    $installed = (ollama list | Select-Object -Skip 1 | ForEach-Object { ($_ -split "\s+")[0] })
    Get-Content MODELS.txt | ForEach-Object {
        if ($_ -match "^#" -or $_ -eq "") { return }
        $parts = $_ -split " "; $model = $parts[0]; $kind = $parts[1]
        $has = $installed | Where-Object { $_ -like "$model*" }
        if ($has) { Check "Modell $model" $true "" }
        elseif ($kind -eq "pflicht") { Check "Modell $model" $false "ollama pull $model" }
        else { Write-Host "  ~  Modell $model (nur $kind) fehlt - ok" -ForegroundColor Yellow }
    }
}

# Python - bevorzugt die venv im Repo (.venv oder backend\.venv), sonst "python" aus dem PATH.
# So stimmt der Check auch, wenn die venv gerade nicht aktiviert ist.
$py = "python"; $pywo = "(python im PATH - keine .venv gefunden)"
if (Test-Path ".venv\Scripts\python.exe") { $py = ".venv\Scripts\python.exe"; $pywo = "(.venv)" }
elseif (Test-Path "backend\.venv\Scripts\python.exe") { $py = "backend\.venv\Scripts\python.exe"; $pywo = "(backend\.venv)" }

$pyok = $false
try { $v = & $py -c "import sys; print(sys.version_info >= (3,11))"; $pyok = ($v -eq "True") } catch {}
Check "Python >= 3.11 $pywo" $pyok "https://www.python.org/downloads/ (Haken bei 'Add to PATH'!)"

# Python-Pakete - fehlen sie, legt das Skript die .venv gleich selbst an und installiert sie (nur bei Python >= 3.11).
$deps = $false
try { & $py -c "import fastapi, openai, numpy, uvicorn" 2>$null; $deps = ($LASTEXITCODE -eq 0) } catch {}
if (-not $deps -and $pyok) {
    if (-not (Test-Path ".venv\Scripts\python.exe")) {
        Write-Host "  ~  keine .venv gefunden - lege .venv an ..." -ForegroundColor Yellow
        try { python -m venv .venv 2>$null | Out-Null } catch {}
    }
    if (Test-Path ".venv\Scripts\python.exe") {
        Write-Host "  ~  installiere Python-Pakete in .venv (1-2 min, einmalig) ..." -ForegroundColor Yellow
        try { & ".venv\Scripts\python.exe" -m pip install -q -r backend\requirements.txt 2>&1 | Select-Object -Last 3 } catch {}
        $py = ".venv\Scripts\python.exe"
        try { & $py -c "import fastapi, openai, numpy, uvicorn" 2>$null; $deps = ($LASTEXITCODE -eq 0) } catch {}
    }
}
Check "Python-Pakete (fastapi, openai, numpy, uvicorn)" $deps "python -m venv .venv; .venv\Scripts\activate; pip install -r backend\requirements.txt"

$nodeok = [bool](Get-Command node -ErrorAction SilentlyContinue)
if ($nodeok) { Check "Node installiert" $true "" }
else { Write-Host "  ~  Node nicht gefunden - Frontend dann als Demo am Beamer (kein Blocker)" -ForegroundColor Yellow }

# Frontend-Pakete - fehlen sie, laeuft npm install gleich hier.
if ($nodeok) {
    if (-not (Test-Path "frontend\node_modules") -and (Get-Command npm -ErrorAction SilentlyContinue)) {
        Write-Host "  ~  frontend\node_modules fehlt - npm install (1 min, einmalig) ..." -ForegroundColor Yellow
        try { Push-Location frontend; npm install --no-audit --no-fund --loglevel=error 2>&1 | Select-Object -Last 3; Pop-Location } catch { Pop-Location }
    }
    if (Test-Path "frontend\node_modules") { Check "Frontend-Pakete (frontend\node_modules)" $true "" }
    else { Write-Host "  ~  frontend\node_modules fehlt - cd frontend; npm install (sonst am Workshop)" -ForegroundColor Yellow }
}

$whisperDir = Join-Path $HOME "whisper"
if (Test-Path (Join-Path $whisperDir "whisper-cli.exe")) { Check "whisper-cli ($whisperDir)" $true "" }
else { Write-Host "  ~  whisper-cli.exe fehlt in $whisperDir - Vorbereitungs-Mail Schritt 5 (Windows-Zeilen)" -ForegroundColor Yellow }
foreach ($wm in "ggml-small.bin", "ggml-large-v3-turbo.bin") {
    if (Test-Path (Join-Path $whisperDir $wm)) { Check "Whisper-Modell $wm" $true "" }
    else { Write-Host "  ~  $whisperDir\$wm fehlt - curl.exe-Zeilen in der Vorbereitungs-Mail, Schritt 5" -ForegroundColor Yellow }
}

$ram = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB)
if ($ram -ge 16) { Check "RAM: $ram GB" $true "" }
else { Write-Host "  ~  RAM: $ram GB - bitte Fallback-Modelle (qwen3.5:4b) zusaetzlich pullen" -ForegroundColor Yellow }

Write-Host ""
if ($fail -eq 0) { Write-Host "=== Alles bestens - los geht's! ===" -ForegroundColor Green }
else { Write-Host "=== $fail Punkt(e) offen - Hinweise oben befolgen. ===" -ForegroundColor Red }
