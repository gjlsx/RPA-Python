@echo off
chcp 65001 >nul
echo Chrome批量启动器
echo ================

set /p start_num="请输入起始Chrome编号 (默认11): "
if "%start_num%"=="" set start_num=11

set /p end_num="请输入结束Chrome编号 (默认20): "
if "%end_num%"=="" set end_num=20

set /p delay="请输入启动间隔秒数 (默认3): "
if "%delay%"=="" set delay=3

echo.
echo 准备启动 Chrome_%start_num% 到 Chrome_%end_num%
echo 启动间隔: %delay% 秒
echo.
pause

python batch_chrome_launcher.py %start_num% %end_num% -d %delay%

echo.
echo 批量启动完成！
pause