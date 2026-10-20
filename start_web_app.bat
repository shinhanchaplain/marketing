@echo off
chcp 65001 > nul
title AI 마케팅 스튜디오 - 웹 대시보드 실행기
echo ========================================================
echo   ⚡ AI 마케팅 자동화 스튜디오 (독립 웹 애플리케이션)
echo ========================================================
echo.
echo [1/2] 필수 패키지 점검 및 설치 확인...
python -m pip install -r requirements.txt --quiet

echo.
echo [2/2] 웹브라우저 대시보드 서버 가동 중...
echo * 로컬 접속 주소: http://localhost:8501
echo * 브라우저가 자동으로 열립니다. 종료하려면 이 창에서 Ctrl+C를 누르세요.
echo.

python -m streamlit run app.py --server.port=8501 --server.headless=false
pause
