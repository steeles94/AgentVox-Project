# AgentVox 프로젝트 설정 및 실행 가이드

## 📅 작업 일자
2025년 9월 1일 월요일

## 🎯 프로젝트 개요
AgentVox-Pro - Edge 기반 음성 비서 시스템 구축
- 실시간 음성 인식 (STT)
- 대화형 AI (LLM - Gemma 3 12B)
- 음성 합성 (TTS)
- 완전한 오프라인 작동

## 📁 폴더 구조
```
C:\newidea\
├── AgentVox-Pro-main\      # 메인 프로젝트
│   ├── agentvox\           # 소스 코드
│   ├── README.md
│   └── requirements.txt
├── text_agentvox.py        # 텍스트 기반 음성 비서
├── simple_agentvox.py      # 간단한 음성 비서
├── simple_voice_test.py    # TTS 테스트
└── video_to_text.py        # 동영상→텍스트 변환

C:\Users\SS\.agentvox\models\
└── gemma-3-12b-it-Q4_K_M.gguf  # 6.8GB LLM 모델
```

## ✅ 완료된 작업

### 1. 환경 설정
- [x] C:\newidea 작업 폴더 생성
- [x] AgentVox-Pro 프로젝트 다운로드 및 압축 해제
- [x] Python 3.13 환경 구성

### 2. 패키지 설치
```bash
# 설치된 주요 패키지
- numpy
- torch
- llama-cpp-python
- pyttsx3 (TTS)
- speechrecognition (STT)
- RealtimeSTT
- RealtimeTTS
```

### 3. 모델 다운로드
- [x] Gemma 3 12B 모델 다운로드 (6.8GB)
- 위치: `C:\Users\SS\.agentvox\models\gemma-3-12b-it-Q4_K_M.gguf`

### 4. 구현된 기능
- [x] TTS (텍스트→음성) 기능 테스트 완료
- [x] 텍스트 기반 대화형 AI 구현
- [x] 한국어/영어 음성 출력 지원
- [x] YouTube 자막 추출 시도
- [x] 동영상 처리 스크립트 작성

## 🔧 실행 방법

### 1. 간단한 TTS 테스트
```bash
python simple_voice_test.py
```

### 2. 텍스트 기반 음성 비서 실행
```bash
python text_agentvox.py
```
- 텍스트 입력 → AI 응답 → 음성 출력
- 명령어: '종료', '초기화'

### 3. 음성 출력 예제
```python
import pyttsx3
engine = pyttsx3.init()
engine.say("안녕하세요")
engine.runAndWait()
```

## ⚠️ 알려진 문제점

### 1. Python 3.13 호환성
- TTS/coqui-tts: Python 3.13 미지원
- 일부 패키지 버전 제한

### 2. 인코딩 문제
- Windows CP949 vs UTF-8 충돌
- 한글 출력 시 인코딩 오류 발생 가능

### 3. 마이크 설정
- 기본 입력 장치 없음 오류
- 텍스트 입력으로 대체 구현

## 💡 추가 작업 제안

### 1. 음성 인식 개선
```bash
# 마이크 설정 확인
python -c "import pyaudio; p=pyaudio.PyAudio(); print(p.get_default_input_device_info())"
```

### 2. 모델 최적화
- GPU 가속 설정 (CUDA)
- 컨텍스트 크기 조정
- 응답 속도 개선

### 3. UI 개발
- 웹 인터페이스 (Flask/Gradio)
- 데스크톱 앱 (Tkinter/PyQt)

## 📚 참고 자료
- [AgentVox GitHub](https://github.com/InnoventixInc/AgentVox-Pro)
- [Gemma Model](https://huggingface.co/tgisaturday/Docsray)
- [llama.cpp](https://github.com/ggerganov/llama.cpp)

## 🎤 사용 가능한 음성
- 한국어: Microsoft Heami Desktop
- 영어: Microsoft Zira Desktop

## 📝 메모
- 모델 로딩 시간: 약 30초-1분
- 메모리 사용량: 약 8GB 이상
- CPU 추론 모드로 실행 중 (GPU 미사용)

---
*생성일: 2025-09-01*
*작성: Claude + AgentVox 프로젝트*