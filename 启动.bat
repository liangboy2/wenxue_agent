@echo off
chcp 65001 >nul
title 文思 Agent 一键启动（网页版）
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (set "PY=py") else (set "PY=python")

%PY% -c "import sys; assert sys.version_info >= (3, 9)" >nul 2>nul
if errorlevel 1 (
    echo [错误] 未检测到 Python 3.9 及以上版本。
    echo 请先安装 Python（安装时勾选 Add Python to PATH），再重新双击本脚本。
    pause
    exit /b 1
)

%PY% -c "import requests, flask" >nul 2>nul
if errorlevel 1 (
    echo 首次运行，正在安装依赖（仅需一次）...
    %PY% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败，请检查网络后重试。
        pause
        exit /b 1
    )
)

%PY% -c "import config; assert config.API_KEY and config.MODEL" >nul 2>nul
if errorlevel 1 (
    echo [提示] 尚未配置 LLM。
    echo 将打开 config.py，请填写 API_KEY 和 MODEL 两行，保存后重新双击本脚本。
    start notepad config.py
    pause
    exit /b 1
)

echo 正在启动网页版，浏览器将自动打开...
echo 提示：关闭本窗口即停止服务。地址：http://127.0.0.1:8000
%PY% web.py --open
pause
