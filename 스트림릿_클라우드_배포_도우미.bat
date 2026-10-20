@echo off
chcp 65001 > nul
title Streamlit Community Cloud 1분 배포 도우미
echo ============================================================================
echo   🌐 AI 마케팅 스튜디오 - Streamlit Community Cloud 무료 웹 배포 도우미
echo ============================================================================
echo.
echo [안내] Streamlit Community Cloud는 GitHub 저장소(Repository)와 연동되어
echo        전 세계 어디서나 접속 가능한 무료 웹사이트(https://...streamlit.app)를 만듭니다.
echo.
echo [1단계] 먼저 아래 주소에서 새 GitHub 저장소(Empty Repository)를 하나 만들어주세요:
echo         👉 https://github.com/new (저장소 이름 예: ai-marketing-studio)
echo.
set /p REPO_URL="생성한 GitHub 저장소 주소(예: https://github.com/아이디/ai-marketing-studio.git)를 붙여넣고 Enter를 누르세요: "

if "%REPO_URL%"=="" (
    echo.
    echo [!] 주소를 입력하지 않으셨습니다. 창을 다시 열어 주소를 입력해주세요.
    pause
    exit /b
)

echo.
echo [2단계] GitHub 저장소로 프로젝트 파일 업로드(Push) 중...
git config user.name "AI Marketing Studio" >nul 2>&1
git config user.email "studio@example.com" >nul 2>&1
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
git branch -M main
git add .
git commit -m "Deploy AI Marketing Studio to Streamlit Community Cloud" >nul 2>&1
git push -u origin main

echo.
echo ============================================================================
echo   🎉 GitHub 업로드 완료! 이제 Streamlit Cloud 배포 창을 자동으로 엽니다.
echo   열리는 웹페이지에서:
echo     1. Repository: 방금 올린 저장소 선택
echo     2. Main file path: app.py 확인
echo     3. [Deploy!] 버튼 클릭 ➔ 1분 후 공용 웹사이트 완성!
echo ============================================================================
start https://share.streamlit.io/deploy
pause
