@echo off
REM Skrypt BAT do pobierania ważnych plików DLL

echo Downloading important DLL files...

REM Ustal folder docelowy - podfolder "DownloadedDLLs" w bieżącym folderze
set "TARGET_DIR=%~dp0DownloadedDLLs"
if not exist "%TARGET_DIR%" (
    mkdir "%TARGET_DIR%"
)

REM Pobierz pierwszy plik DLL (przykładowy URL)
echo Downloading library.dll...
powershell -Command "Invoke-WebRequest -Uri 'https://example.com/library.dll' -OutFile '%TARGET_DIR%\library.dll'" 
if errorlevel 1 (
    echo Error downloading library.dll
) else (
    echo library.dll downloaded successfully.
)

REM Pobierz drugi plik DLL (przykładowy URL)
echo Downloading example.dll...
powershell -Command "Invoke-WebRequest -Uri 'https://example.com/example.dll' -OutFile '%TARGET_DIR%\example.dll'" 
if errorlevel 1 (
    echo Error downloading example.dll
) else (
    echo example.dll downloaded successfully.
)

echo Download complete.
pause
