@echo off
echo GitHub 푸시 스크립트
echo.

cd C:\newidea

REM Git 초기화 확인
if not exist .git (
    git init
    git add .
    git commit -m "Initial commit: AgentVox 음성 비서 프로젝트"
)

REM 원격 저장소 추가 (이미 있으면 무시)
git remote add origin https://github.com/steeles94/AgentVox-Project.git 2>nul

REM 브랜치 이름을 main으로 변경
git branch -M main

echo.
echo GitHub에 푸시 중...
echo 사용자명과 Personal Access Token을 입력하세요.
echo.

REM 푸시
git push -u origin main

echo.
echo 푸시 완료!
pause