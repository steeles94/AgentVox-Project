@echo off
echo =======================================
echo    GitHub 안전 푸시 스크립트
echo =======================================
echo.
echo 주의: 토큰을 직접 입력하지 마세요!
echo.

cd C:\newidea

echo Git Credential Manager를 사용합니다...
git config --global credential.helper manager-core

echo.
echo GitHub 인증 창이 열립니다.
echo 브라우저에서 로그인하거나 토큰을 입력하세요.
echo.

git push -u origin main

echo.
echo 푸시 완료!
pause