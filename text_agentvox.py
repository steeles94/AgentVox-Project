#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import pyttsx3
from llama_cpp import Llama

class TextAgentVox:
    def __init__(self, model_path):
        print("=== Text AgentVox 초기화 중 ===")
        
        # TTS 엔진 초기화
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.9)
        
        # LLM 초기화
        print(f"모델 로딩 중: {model_path}")
        print("(첫 로딩은 약 30초-1분 정도 걸립니다...)")
        
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
        print(f"\nAI: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
        
    def generate_response(self, user_input):
        """LLM을 사용하여 응답 생성"""
        # 대화 기록 추가
        self.conversation_history.append(f"사용자: {user_input}")
        
        # 프롬프트 생성
        context = "\n".join(self.conversation_history[-5:])  # 최근 5개 대화만 유지
        prompt = f"""당신은 친절한 AI 비서입니다. 다음 대화에 자연스럽고 도움이 되는 응답을 한국어로 제공하세요.

{context}
AI:"""
        
        print("생각 중...")
        
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
        print("\n" + "="*50)
        print("   Text AgentVox - 텍스트 기반 음성 비서")
        print("="*50)
        
        welcome = "안녕하세요! Text AgentVox 음성 비서입니다. 무엇을 도와드릴까요?"
        self.speak(welcome)
        
        print("\n사용법:")
        print("  - 텍스트를 입력하면 AI가 응답하고 음성으로 읽어줍니다")
        print("  - '종료' 또는 'exit': 프로그램 종료")
        print("  - '초기화' 또는 'reset': 대화 기록 초기화")
        print("  - Ctrl+C: 긴급 종료")
        print("-"*50 + "\n")
        
        while self.is_running:
            try:
                # 사용자 입력 받기
                user_input = input("\n사용자: ").strip()
                
                if not user_input:
                    continue
                
                # 종료 명령 확인
                if user_input.lower() in ['종료', 'exit', '끝', 'quit', 'q']:
                    self.speak("대화를 종료합니다. 안녕히 가세요!")
                    break
                
                # 초기화 명령 확인
                if user_input.lower() in ['초기화', 'reset', '리셋', 'clear']:
                    self.conversation_history = []
                    self.speak("대화 기록을 초기화했습니다.")
                    continue
                
                # AI 응답 생성
                response = self.generate_response(user_input)
                
                # 응답 출력 (텍스트 + 음성)
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n\n프로그램을 종료합니다.")
                break
            except EOFError:
                print("\n\n입력이 종료되었습니다.")
                break
            except Exception as e:
                print(f"\n오류 발생: {e}")
                self.speak("죄송합니다. 오류가 발생했습니다.")

def main():
    model_path = r"C:\Users\SS\.agentvox\models\gemma-3-12b-it-Q4_K_M.gguf"
    
    if not os.path.exists(model_path):
        print(f"모델 파일을 찾을 수 없습니다: {model_path}")
        return
    
    # AgentVox 실행
    try:
        agent = TextAgentVox(model_path)
        agent.run()
    except Exception as e:
        print(f"초기화 실패: {e}")

if __name__ == "__main__":
    main()