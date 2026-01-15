# JARVIS Quick Start Script
# Run: .\start_jarvis.ps1

param(
    [switch]$Dashboard,
    [switch]$Voice,
    [switch]$Both
)

$ErrorActionPreference = "Stop"
$projectRoot = $PSScriptRoot

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "        JARVIS STARTUP                 " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (-not (Test-Path "$projectRoot\.venv")) {
    Write-Host "Virtual environment not found. Run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "$projectRoot\.venv\Scripts\Activate.ps1"

# Check Ollama
Write-Host "Checking Ollama..." -ForegroundColor Yellow
try {
    $ollamaStatus = ollama list 2>&1
    Write-Host "  Ollama is running" -ForegroundColor Green
} catch {
    Write-Host "  WARNING: Ollama not running. Start with: ollama serve" -ForegroundColor Yellow
}

# Determine what to start
if ($Both) {
    $Dashboard = $true
    $Voice = $true
}

if (-not $Dashboard -and -not $Voice) {
    # Default: start voice pipeline
    $Voice = $true
}

# Start dashboard in background if requested
if ($Dashboard) {
    Write-Host ""
    Write-Host "Starting Dashboard..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$projectRoot\.venv\Scripts\Activate.ps1'; python -m src.dashboard"
    Write-Host "  Dashboard running at http://localhost:5000" -ForegroundColor Green
    Start-Sleep -Seconds 2
}

# Start voice pipeline
if ($Voice) {
    Write-Host ""
    Write-Host "Starting Voice Pipeline..." -ForegroundColor Yellow
    Write-Host "  Press F9 to talk, Ctrl+C to exit" -ForegroundColor White
    Write-Host ""
    python -m src.voice_pipeline
}

Write-Host ""
Write-Host "JARVIS shutdown complete." -ForegroundColor Cyan
