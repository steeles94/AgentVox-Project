#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib.request
from pathlib import Path

def download_model():
    """Gemma 모델 다운로드"""
    
    # 모델 저장 경로
    model_dir = Path.home() / ".agentvox" / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    
    model_name = "gemma-3-12b-it-Q4_K_M.gguf"
    model_path = model_dir / model_name
    
    if model_path.exists():
        print(f"모델이 이미 존재합니다: {model_path}")
        return str(model_path)
    
    # 모델 URL
    model_url = "https://huggingface.co/tgisaturday/Docsray/resolve/main/gemma-3-12b-it-GGUF/gemma-3-12b-it-Q4_K_M.gguf"
    
    print(f"모델 다운로드 시작: {model_name}")
    print(f"다운로드 위치: {model_path}")
    print("파일 크기: 약 7GB - 시간이 걸릴 수 있습니다...")
    
    try:
        # 다운로드 진행상황 표시
        def download_hook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(downloaded * 100 / total_size, 100)
            print(f"진행률: {percent:.1f}%", end='\r')
        
        urllib.request.urlretrieve(model_url, model_path, reporthook=download_hook)
        print("\n모델 다운로드 완료!")
        return str(model_path)
        
    except Exception as e:
        print(f"다운로드 실패: {e}")
        if model_path.exists():
            model_path.unlink()
        return None

if __name__ == "__main__":
    model_path = download_model()
    if model_path:
        print(f"\n모델 경로: {model_path}")
        print("\n이제 다음 명령으로 AgentVox를 실행할 수 있습니다:")
        print(f'python -m agentvox.cli --model "{model_path}"')