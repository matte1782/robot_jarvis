# Jarvis Setup Script for Windows
# Run: .\setup.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "       JARVIS SETUP SCRIPT             " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Stop"
$projectRoot = $PSScriptRoot

# Check Python
Write-Host "[1/7] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Python not found. Please install Python 3.11+" -ForegroundColor Red
    Write-Host "  Run: winget install Python.Python.3.11" -ForegroundColor Yellow
    exit 1
}

# Check Git
Write-Host "[2/7] Checking Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>&1
    Write-Host "  Found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "  WARNING: Git not found. Some features won't work." -ForegroundColor Yellow
}

# Check Node.js
Write-Host "[3/7] Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  Found: Node $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  WARNING: Node.js not found. MCP TypeScript servers won't work." -ForegroundColor Yellow
    Write-Host "  Run: winget install OpenJS.NodeJS.LTS" -ForegroundColor Yellow
}

# Create virtual environment
Write-Host "[4/7] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "$projectRoot\.venv") {
    Write-Host "  Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv "$projectRoot\.venv"
    Write-Host "  Created .venv" -ForegroundColor Green
}

# Activate venv and install dependencies
Write-Host "[5/7] Installing Python dependencies..." -ForegroundColor Yellow
& "$projectRoot\.venv\Scripts\Activate.ps1"
pip install --upgrade pip -q
pip install -r "$projectRoot\requirements.txt" -q
Write-Host "  Dependencies installed" -ForegroundColor Green

# Create .env from example
Write-Host "[6/7] Creating configuration..." -ForegroundColor Yellow
if (-not (Test-Path "$projectRoot\.env")) {
    $username = $env:USERNAME
    $envContent = Get-Content "$projectRoot\.env.example" -Raw
    $envContent = $envContent -replace "YOUR_USERNAME", $username
    $envContent | Out-File "$projectRoot\.env" -Encoding utf8
    Write-Host "  Created .env (edit with your settings)" -ForegroundColor Green
} else {
    Write-Host "  .env already exists" -ForegroundColor Green
}

# Check Ollama
Write-Host "[7/7] Checking Ollama..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama --version 2>&1
    Write-Host "  Found: $ollamaVersion" -ForegroundColor Green

    # Check if qwen2.5:7b is installed (matches llm_router.py default)
    $models = ollama list 2>&1
    if ($models -match "qwen2.5") {
        Write-Host "  Model qwen2.5:7b is ready" -ForegroundColor Green
    } else {
        Write-Host "  Downloading qwen2.5:7b (this may take a while)..." -ForegroundColor Yellow
        ollama pull qwen2.5:7b
    }
} catch {
    Write-Host "  WARNING: Ollama not found. Install from https://ollama.com" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "          SETUP COMPLETE!              " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "1. Edit .env with your settings" -ForegroundColor White
Write-Host "2. Copy config\claude_desktop_config.example.json to:" -ForegroundColor White
Write-Host "   $env:APPDATA\Claude\claude_desktop_config.json" -ForegroundColor Yellow
Write-Host "3. Update paths in claude_desktop_config.json" -ForegroundColor White
Write-Host "4. Restart Claude Desktop" -ForegroundColor White
Write-Host "5. Test: Ask Claude to 'list files in workspace'" -ForegroundColor White
Write-Host ""
Write-Host "To start Jarvis voice pipeline:" -ForegroundColor White
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "  python -m src.voice_pipeline" -ForegroundColor Yellow
Write-Host ""
