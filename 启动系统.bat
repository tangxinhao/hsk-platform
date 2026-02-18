@echo off
chcp 65001 >nul
echo ============================================================
echo HSK学习平台 - 一键启动
echo ============================================================
echo.

echo [1/3] 启动后端服务...
start "HSK后端" cmd /k "cd /d %~dp0backend && python manage.py runserver"
timeout /t 3 /nobreak >nul

echo [2/3] 启动用户前端...
start "HSK用户端" cmd /k "cd /d %~dp0frontend-user && npm run dev"
timeout /t 3 /nobreak >nul

echo [3/3] 启动管理前端...
start "HSK管理端" cmd /k "cd /d %~dp0frontend-admin && npm run dev"

echo.
echo ============================================================
echo ✓ 所有服务正在启动中...
echo ============================================================
echo.
echo 请等待几秒钟，然后访问以下地址：
echo.
echo 用户端: http://localhost:5173/ 或 http://localhost:5174/
echo 管理端: http://localhost:5173/
echo 后端API: http://localhost:8000/api/
echo.
echo 按任意键关闭本窗口...
pause >nul
