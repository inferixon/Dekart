@echo off

:: Dekart Builder
:: Creates standalone EXE using PyInstaller

:: Step 1: Check if pyinstaller is installed
where pyinstaller >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

:: Step 2: Build
pyinstaller --noconfirm --onefile --windowed --name=DEKART dekart.py

:: Step 3: Copy resources
if exist dist\dekart.exe (
    echo Copying resources...
    copy ord.txt dist\ord.txt
    copy chart.png dist\chart.png
)

:: Step 4: Clean temporary files
rd /s /q build
rd /s /q __pycache__
del dekart.spec

echo.
echo Build finished!
echo Your EXE is located in the "dist" folder.
pause
