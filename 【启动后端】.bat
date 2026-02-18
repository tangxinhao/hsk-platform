@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   启动HSK后端服务
echo ========================================
echo.
echo 正在启动，请稍候...
echo.
cd backend
python manage.py runserver 0.0.0.0:8000
echo.
echo 如果看到错误，请检查Python是否已安装
echo.
pause
