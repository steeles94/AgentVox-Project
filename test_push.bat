@echo off
echo GitHub Push 테스트
echo.
echo 토큰을 입력하세요 (ghp_로 시작):
set /p token=

echo.
echo 푸시 시도 중...
git push https://steeles94:%token%@github.com/steeles94/AgentVox-Project.git main

echo.
echo 완료!
pause