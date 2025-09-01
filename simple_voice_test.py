#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyttsx3
import speech_recognition as sr

def test_tts():
    """TTS 테스트 - 텍스트를 음성으로 변환"""
    print("=== TTS 테스트 ===")
    
    # TTS 엔진 초기화
    engine = pyttsx3.init()
    
    # 음성 속성 설정
    engine.setProperty('rate', 150)    # 속도
    engine.setProperty('volume', 0.9)  # 볼륨
    
    # 테스트 메시지
    text = "안녕하세요. AgentVox 음성 테스트입니다."
    print(f"출력할 텍스트: {text}")
    
    # 음성 출력
    engine.say(text)
    engine.runAndWait()
    
    print("TTS 테스트 완료!")

def test_stt():
    """STT 테스트 - 음성을 텍스트로 변환"""
    print("\n=== STT 테스트 ===")
    
    # 음성 인식기 초기화
    recognizer = sr.Recognizer()
    
    try:
        # 마이크 사용
        with sr.Microphone() as source:
            print("마이크 준비 중...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("말씀해 주세요 (5초 동안 녹음)...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            print("음성 인식 중...")
            # Google Web Speech API 사용
            text = recognizer.recognize_google(audio, language='ko-KR')
            print(f"인식된 텍스트: {text}")
            
    except sr.WaitTimeoutError:
        print("시간 초과: 음성이 감지되지 않았습니다.")
    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        print(f"음성 인식 서비스 오류: {e}")
    except Exception as e:
        print(f"오류 발생: {e}")

def main():
    print("=== 음성 시스템 테스트 ===\n")
    
    # TTS 테스트
    try:
        test_tts()
    except Exception as e:
        print(f"TTS 오류: {e}")
    
    # STT 테스트 (옵션)
    user_input = input("\nSTT 테스트를 하시겠습니까? (y/n): ")
    if user_input.lower() == 'y':
        try:
            test_stt()
        except Exception as e:
            print(f"STT 오류: {e}")
    
    print("\n테스트 완료!")

if __name__ == "__main__":
    main()