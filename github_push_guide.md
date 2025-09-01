# GitHub 푸시 가이드

## 1. GitHub에서 새 저장소 생성

1. [GitHub.com](https://github.com) 로그인
2. 우측 상단 "+" 클릭 → "New repository"
3. 저장소 설정:
   - Repository name: `AgentVox-Project`
   - Description: "음성 비서 프로젝트 - Gemma LLM 기반"
   - Public 또는 Private 선택
   - **"Initialize repository with:"는 모두 체크 해제** (이미 로컬에 파일이 있으므로)
4. "Create repository" 클릭

## 2. 로컬 저장소와 GitHub 연결

### WSL에서 (현재 백업 위치)
```bash
cd /tmp/newidea_backup

# 원격 저장소 추가 (YOUR_USERNAME을 실제 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/AgentVox-Project.git

# 브랜치 이름을 main으로 변경 (선택사항)
git branch -M main

# GitHub에 푸시
git push -u origin main
```

### Windows에서 (원본 폴더)
```cmd
cd C:\newidea

# Git 초기화
git init

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: AgentVox 음성 비서 프로젝트"

# 원격 저장소 추가
git remote add origin https://github.com/YOUR_USERNAME/AgentVox-Project.git

# 브랜치 이름 변경
git branch -M main

# 푸시
git push -u origin main
```

## 3. 인증 설정

### HTTPS 사용 시
- GitHub 사용자명과 Personal Access Token 입력
- Token 생성: GitHub Settings → Developer settings → Personal access tokens

### SSH 사용 시
```bash
# SSH 키 생성 (없는 경우)
ssh-keygen -t ed25519 -C "your_email@example.com"

# 공개 키 복사
cat ~/.ssh/id_ed25519.pub

# GitHub Settings → SSH and GPG keys → New SSH key에 추가

# 원격 URL을 SSH로 변경
git remote set-url origin git@github.com:YOUR_USERNAME/AgentVox-Project.git
```

## 4. 푸시 명령어

### 첫 푸시
```bash
git push -u origin main
```

### 이후 푸시
```bash
git push
```

## 5. .gitignore 파일 추가
```bash
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv
build/
dist/
*.egg-info/

# 모델 파일
*.gguf
*.bin
*.pt
*.pth

# 오디오/비디오
*.wav
*.mp3
*.mp4
*.avi

# 임시 파일
temp_*
chunk_*
*.tmp
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo
```

## 6. 유용한 Git 명령어

```bash
# 상태 확인
git status

# 변경 사항 보기
git diff

# 커밋 기록
git log --oneline

# 브랜치 확인
git branch

# 파일 제외
git rm --cached <file>

# 태그 추가
git tag -a v0.1.0 -m "Initial release"
git push origin v0.1.0
```

## 7. GitHub Actions (자동화)

`.github/workflows/python-app.yml` 파일 생성:
```yaml
name: Python application

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Test
      run: |
        python -m pytest tests/ || true
```

---
*작성일: 2025-09-01*