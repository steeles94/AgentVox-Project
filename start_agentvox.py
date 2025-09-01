#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

# AgentVox 경로 추가
sys.path.insert(0, 'C:\\newidea\\AgentVox-Pro-main')

def main():
    print("=== AgentVox 음성 비서 실행 중 ===")
    
    model_path = "C:\\Users\\SS\\.agentvox\\models\\gemma-3-12b-it-Q4_K_M.gguf"
    
    if not Path(model_path).exists():
        print(f"모델 파일을 찾을 수 없습니다: {model_path}")
        return
    
    # 명령어 구성
    cmd = [
        "python.exe",
        "-m", "agentvox.cli",
        "--model", model_path,
        "--stt-model", "tiny",  # 빠른 시작을 위해 작은 모델 사용
        "--stt-language", "ko",  # 한국어
        "--llm-temperature", "0.7",
        "--tts-speed", "1.3"
    ]
    
    print(f"실행 명령: {' '.join(cmd)}")
    print("\n시작 중... (첫 실행시 추가 모델 다운로드가 있을 수 있습니다)")
    
    # AgentVox 실행
    os.system(' '.join(cmd))

if __name__ == "__main__":
    main()