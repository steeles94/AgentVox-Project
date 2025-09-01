#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import threading
import queue
import pyttsx3
import speech_recognition as sr
from llama_cpp import Llama

class SimpleAgentVox:
    def __init__(self, model_path):
        print("=== Simple AgentVox 초기화 중 ===")
        
        # TTS 엔진 초기화
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.9)
        
        # 한국어 음성 설정 시도
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            if 'korean' in voice.name.lower() or 'ko' in voice.id.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        
        # STT 엔진 초기화
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # LLM 초기화
        print(f"모델 로딩 중: {model_path}")
        print("(첫 로딩은 시간이 걸릴 수 있습니다...)")
        
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,  # 컨텍스트 크기
            n_threads=4,  # CPU 스레드 수
            n_gpu_layers=0,  # GPU 레이어 (0 = CPU만 사용)
            verbose=False
        )
        
        print("모델 로딩 완료!")
        
        self.conversation_history = []
        self.is_running = True
        
    def speak(self, text):
        """텍스트를 음성으로 출력"""
        print(f"AI: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
        
    def listen(self):
        """마이크로부터 음성을 듣고 텍스트로 변환"""
        try:
            with self.microphone as source:
                print("\n듣는 중... (말씀해 주세요)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            print("인식 중...")
            text = self.recognizer.recognize_google(audio, language='ko-KR')
            print(f"사용자: {text}")
            return text
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("음성을 인식할 수 없습니다.")
            return None
        except sr.RequestError as e:
            print(f"음성 인식 서비스 오류: {e}")
            return None
        except Exception as e:
            print(f"오류: {e}")
            return None
    
    def generate_response(self, user_input):
        """LLM을 사용하여 응답 생성"""
        # 대화 기록 추가
        self.conversation_history.append(f"사용자: {user_input}")
        
        # 프롬프트 생성
        context = "\n".join(self.conversation_history[-5:])  # 최근 5개 대화만 유지
        prompt = f"""당신은 친절한 AI 비서입니다. 다음 대화에 자연스럽고 도움이 되는 응답을 한국어로 제공하세요.

{context}
AI:"""
        
        # LLM 응답 생성
        response = self.llm(
            prompt,
            max_tokens=256,
            temperature=0.7,
            stop=["사용자:", "\n\n"],
            echo=False
        )
        
        ai_response = response['choices'][0]['text'].strip()
        self.conversation_history.append(f"AI: {ai_response}")
        
        return ai_response
    
    def run(self):
        """메인 대화 루프"""
        # 시작 인사
        welcome = "안녕하세요! Simple AgentVox 음성 비서입니다. 무엇을 도와드릴까요?"
        self.speak(welcome)
        
        print("\n=== 명령어 ===")
        print("- '종료', 'exit': 프로그램 종료")
        print("- '초기화', 'reset': 대화 기록 초기화")
        print("- Ctrl+C: 긴급 종료\n")
        
        while self.is_running:
            try:
                # 사용자 음성 듣기
                user_input = self.listen()
                
                if user_input is None:
                    continue
                
                # 종료 명령 확인
                if user_input.lower() in ['종료', 'exit', '끝', 'quit']:
                    self.speak("대화를 종료합니다. 안녕히 가세요!")
                    break
                
                # 초기화 명령 확인
                if user_input.lower() in ['초기화', 'reset', '리셋']:
                    self.conversation_history = []
                    self.speak("대화 기록을 초기화했습니다.")
                    continue
                
                # AI 응답 생성
                print("응답 생성 중...")
                response = self.generate_response(user_input)
                
                # 응답 출력
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n\n프로그램을 종료합니다.")
                break
            except Exception as e:
                print(f"오류 발생: {e}")
                self.speak("죄송합니다. 오류가 발생했습니다.")

def main():
    model_path = r"C:\Users\SS\.agentvox\models\gemma-3-12b-it-Q4_K_M.gguf"
    
    if not os.path.exists(model_path):
        print(f"모델 파일을 찾을 수 없습니다: {model_path}")
        return
    
    # AgentVox 실행
    agent = SimpleAgentVox(model_path)
    agent.run()

if __name__ == "__main__":
    main()