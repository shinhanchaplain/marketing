@echo off
setlocal
title Figma Desktop Launcher

:: 윈도우 환경에서 Electron 샌드박스 충돌 없이 데스크톱 앱을 확실하게 띄우는 실행 인자
start "" "%LOCALAPPDATA%\Figma\app-126.10.7\Figma.exe" --no-sandbox --disable-gpu-process-crash-limit
exit
