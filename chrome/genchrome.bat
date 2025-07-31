@echo off
cd /d "%~dp0"

if "%1"=="" goto usage
if "%2"=="" goto usage

echo Chrome Shortcut Generator
echo Starting number: %1
echo Count: %2
echo.

python chrome_shortcut_generator.py %1 %2

if %errorlevel% equ 0 (
    echo.
    echo Success! Generated %2 shortcuts starting from %1
) else (
    echo.
    echo Error occurred!
)
goto end

:usage
echo Usage: genchrome.bat start_number count
echo Example: genchrome.bat 11 10
goto end

:end
echo.
pause
