@echo off
cd /d "%~dp0"

echo ========================================
echo    Chrome自动化套件 v2.0
echo ========================================
echo.

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查依赖包
echo 🔍 检查依赖包...
python -c "import selenium, psutil" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  正在安装必需的依赖包...
    pip install selenium psutil pywin32
    if errorlevel 1 (
        echo ❌ 安装依赖包失败
        pause
        exit /b 1
    )
)

echo ✅ 环境检查完成
echo.

REM 显示菜单
:menu
echo 🎮 请选择操作:
echo   1. 显示系统状态
echo   2. 启动Chrome实例 (11-15)
echo   3. 关闭Chrome实例
echo   4. 运行示例任务
echo   5. 进入交互模式
echo   6. 退出
echo.

set /p choice="请输入选择 (1-6): "

if "%choice%"=="1" goto status
if "%choice%"=="2" goto launch
if "%choice%"=="3" goto close
if "%choice%"=="4" goto sample
if "%choice%"=="5" goto interactive
if "%choice%"=="6" goto exit
goto menu

:status
echo.
python chrome_automation_suite.py --status
pause
goto menu

:launch
echo.
python chrome_automation_suite.py --launch 11 15
pause
goto menu

:close
echo.
set /p nums="请输入要关闭的Chrome实例编号 (用空格分隔): "
python chrome_automation_suite.py --close %nums%
pause
goto menu

:sample
echo.
python chrome_automation_suite.py --batch sample_tasks.json
pause
goto menu

:interactive
echo.
python chrome_automation_suite.py --interactive
goto menu

:exit
echo.
echo 👋 感谢使用Chrome自动化套件！
pause
