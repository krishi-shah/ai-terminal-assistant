# Quick setup script for AI Terminal Assistant (Windows PowerShell)
# Run: powershell -ExecutionPolicy Bypass -File setup.ps1

Write-Host "Setting up AI Terminal Assistant..." -ForegroundColor Cyan
Write-Host ""

# Install dependencies
Write-Host "Installing Python packages..." -ForegroundColor Yellow
pip install openai python-dotenv colorama

if ($LASTEXITCODE -ne 0) {
    Write-Host "Trying with pip3..." -ForegroundColor Yellow
    pip3 install openai python-dotenv colorama
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "Trying with --user flag..." -ForegroundColor Yellow
    pip install --user openai python-dotenv colorama
}

# Check if .env exists
$envFile = Join-Path $PSScriptRoot ".env"
$envExample = Join-Path $PSScriptRoot ".env.example"

if (-not (Test-Path $envFile)) {
    Write-Host ""
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    
    if (Test-Path $envExample) {
        Copy-Item $envExample $envFile
        Write-Host "Created .env file from .env.example" -ForegroundColor Green
    } else {
        # Create default .env file
        @"
# OpenAI API Key Configuration
# Add your actual API key below

OPENAI_API_KEY=your-api-key-here

# Get your API key from:
# https://platform.openai.com/api-keys
"@ | Out-File -FilePath $envFile -Encoding utf8
        Write-Host "Created new .env file" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "WARNING: Please edit .env and add your OpenAI API key" -ForegroundColor Red
    Write-Host "Get your key from: https://platform.openai.com/api-keys" -ForegroundColor Cyan
} else {
    Write-Host ".env file already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "   1. Edit .env and add your API key"
Write-Host "   2. Run: python ai-terminal.py"
Write-Host ""

