# VSCode Claude Dev 설정 가이드

## 설치 방법

### 1. VSCode에서 직접 설치
```bash
# VSCode 명령 팔레트 (Ctrl+Shift+P)
ext install saoudrizwan.claude-dev
```

### 2. 명령줄 설치
```bash
code --install-extension saoudrizwan.claude-dev
```

## API 키 설정

### 1. Anthropic API 키 받기
1. [console.anthropic.com](https://console.anthropic.com) 접속
2. 계정 생성/로그인
3. API Keys 섹션에서 새 키 생성
4. 키 복사 (sk-ant-...)

### 2. VSCode에서 설정
1. **Ctrl+Shift+P** → "Claude Dev: Set API Key"
2. API 키 붙여넣기
3. Enter 눌러 저장

## 사용 방법

### 기본 명령어
- **Ctrl+Shift+P** → Claude Dev 명령들 확인
- **우클릭** → "Ask Claude" 메뉴

### 주요 기능

#### 1. 코드 생성
```
선택: 빈 파일 또는 주석
명령: "Claude: Generate Code"
입력: "Python으로 피보나치 함수 만들어줘"
```

#### 2. 코드 설명
```
선택: 이해하고 싶은 코드
명령: "Claude: Explain Code"
```

#### 3. 버그 수정
```
선택: 문제가 있는 코드
명령: "Claude: Fix Bug"
```

#### 4. 리팩토링
```
선택: 개선하고 싶은 코드
명령: "Claude: Refactor Code"
```

#### 5. 테스트 생성
```
선택: 함수나 클래스
명령: "Claude: Generate Tests"
```

## 단축키 설정

### keybindings.json에 추가
```json
{
  "key": "ctrl+alt+c",
  "command": "claude-dev.askClaude"
},
{
  "key": "ctrl+alt+e",
  "command": "claude-dev.explainCode"
},
{
  "key": "ctrl+alt+f",
  "command": "claude-dev.fixCode"
}
```

## 설정 최적화

### settings.json
```json
{
  "claude-dev.apiKey": "your-api-key",
  "claude-dev.model": "claude-3-opus-20240229",
  "claude-dev.maxTokens": 4096,
  "claude-dev.temperature": 0.7,
  "claude-dev.streamResponse": true,
  "claude-dev.showCodeActions": true
}
```

## 유용한 프롬프트 예시

### 1. 함수 문서화
```
"이 함수에 대한 docstring을 작성해줘. 파라미터, 반환값, 예시 포함"
```

### 2. 코드 최적화
```
"이 코드의 시간 복잡도를 개선해줘"
```

### 3. 에러 처리
```
"적절한 에러 처리와 로깅을 추가해줘"
```

### 4. 타입 힌트
```
"Python 타입 힌트를 추가해줘"
```

### 5. 디자인 패턴
```
"이 코드를 싱글톤 패턴으로 리팩토링해줘"
```

## 문제 해결

### API 키 오류
```bash
# Windows
set ANTHROPIC_API_KEY=sk-ant-...

# Linux/Mac
export ANTHROPIC_API_KEY=sk-ant-...
```

### 응답 없음
1. API 키 확인
2. 인터넷 연결 확인
3. API 사용량 한도 확인

### 느린 응답
1. 모델을 claude-3-haiku로 변경 (더 빠름)
2. maxTokens 줄이기
3. 선택한 코드 양 줄이기

## 대안 확장 프로그램

### 1. Continue
- 여러 AI 모델 지원
- 로컬 모델도 가능
- 더 많은 커스터마이징

### 2. Codeium
- 무료 사용 가능
- 자동 완성 특화
- Claude는 미지원

### 3. GitHub Copilot
- 유료 구독
- 깊은 VSCode 통합
- GPT 기반

## 팁과 트릭

1. **컨텍스트 제공**: 관련 코드를 함께 선택하면 더 정확한 답변
2. **명확한 지시**: 구체적인 요구사항 명시
3. **단계별 접근**: 큰 작업은 작은 단위로 나누어 요청
4. **피드백 제공**: 생성된 코드가 맞지 않으면 수정 요청

---
*작성일: 2025-09-01*
*Claude VSCode 통합 가이드*