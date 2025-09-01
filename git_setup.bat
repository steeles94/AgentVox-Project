@echo off
echo Git 저장소 초기화 중...

cd C:\newidea

REM Git 초기화
git init

REM 사용자 정보 설정 (필요시 수정)
git config user.name "Your Name"
git config user.email "your.email@example.com"

REM 모든 파일 추가
git add .

REM .gitignore 생성
echo __pycache__/ > .gitignore
echo *.pyc >> .gitignore
echo .venv/ >> .gitignore
echo venv/ >> .gitignore
echo *.wav >> .gitignore
echo *.mp4 >> .gitignore
echo *.mp3 >> .gitignore
echo temp_* >> .gitignore
echo chunk_* >> .gitignore

REM 첫 번째 커밋
git commit -m "Initial commit: AgentVox project setup"

echo.
echo Git 저장소 설정 완료!
echo.
git status

pause