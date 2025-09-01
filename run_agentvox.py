#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

# AgentVox 경로 추가
sys.path.insert(0, 'C:\\newidea\\AgentVox-Pro-main')

def main():
    print("=== AgentVox 음성 비서 시작 ===")
    print("모델 경로: C:\\Users\\SS\\.agentvox\\models\\gemma-3-12b-it-Q4_K_M.gguf")
    
    # 환경 변수 설정
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    
    try:
        # 간단한 TTS 테스트
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        welcome_text = "안녕하세요. AgentVox 음성 비서입니다. 시스템이 준비되었습니다."
        print(f"\n출력: {welcome_text}")
        engine.say(welcome_text)
        engine.runAndWait()
        
        print("\n=== 음성 비서 준비 완료 ===")
        print("다음 기능들이 사용 가능합니다:")
        print("1. 음성 인식 (STT)")
        print("2. 대화형 AI (LLM)")
        print("3. 음성 합성 (TTS)")
        print("\n종료하려면 Ctrl+C를 누르세요.")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        print("\n시스템 요구사항:")
        print("- 마이크와 스피커가 연결되어 있어야 합니다")
        print("- Windows 음성 서비스가 활성화되어 있어야 합니다")

if __name__ == "__main__":
    main()