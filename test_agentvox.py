#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# AgentVox 디렉토리를 Python 경로에 추가
sys.path.insert(0, 'C:\\newidea\\AgentVox-Pro-main')

from agentvox import ModelConfig, AudioConfig

def main():
    print("=== AgentVox 테스트 시작 ===")
    
    # 기본 설정
    model_config = ModelConfig(
        stt_model="tiny",  # 작은 모델로 시작
        llm_temperature=0.7,
        tts_speed=1.0
    )
    
    audio_config = AudioConfig()
    
    print("설정 완료!")
    print(f"STT 모델: {model_config.stt_model}")
    print(f"LLM 온도: {model_config.llm_temperature}")
    print(f"TTS 속도: {model_config.tts_speed}")
    
    # LLM 모듈 테스트
    try:
        from agentvox.voice_assistant import LLMModule
        print("\n=== LLM 모듈 테스트 ===")
        llm = LLMModule(model_config)
        
        # 간단한 질문 테스트
        test_prompt = "안녕하세요. 당신은 누구입니까?"
        print(f"질문: {test_prompt}")
        
        # 모델이 없을 경우를 대비한 예외 처리
        try:
            response = llm.generate_response(test_prompt)
            print(f"응답: {response}")
        except Exception as e:
            print(f"LLM 응답 생성 중 오류: {e}")
            print("모델 파일이 없을 수 있습니다. 모델을 다운로드해야 합니다.")
            
    except ImportError as e:
        print(f"LLM 모듈 로드 실패: {e}")
    
    # STT 모듈 테스트 (로드만)
    try:
        from agentvox.voice_assistant import STTModule
        print("\n=== STT 모듈 로드 성공 ===")
    except ImportError as e:
        print(f"STT 모듈 로드 실패: {e}")
    
    # TTS 모듈 테스트 (로드만)
    try:
        from agentvox.voice_assistant import TTSModule
        print("=== TTS 모듈 로드 성공 ===")
    except ImportError as e:
        print(f"TTS 모듈 로드 실패: {e}")

if __name__ == "__main__":
    main()