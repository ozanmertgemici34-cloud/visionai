$ErrorActionPreference = "Stop"

Write-Host "[1/3] venv oluşturuluyor"
python -m venv .venv
.\.venv\Scripts\Activate.ps1

Write-Host "[2/3] bağımlılıklar kuruluyor"
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

Write-Host "[3/3] EXE oluşturuluyor"
pyinstaller --clean --noconfirm build/windows/jarvis.spec

Write-Host "Bitti. EXE yolu: dist/JarvisAssistant.exe"
