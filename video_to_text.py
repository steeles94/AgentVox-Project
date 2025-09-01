#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
동영상/오디오 파일에서 음성을 추출하고 텍스트로 변환하는 스크립트
"""

import os
import sys
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks

def extract_audio_from_video(video_path, audio_path="temp_audio.wav"):
    """동영상에서 오디오 추출"""
    print(f"동영상에서 오디오 추출 중: {video_path}")
    
    # ffmpeg 명령어 사용
    cmd = f'ffmpeg -i "{video_path}" -ab 160k -ac 2 -ar 44100 -vn "{audio_path}" -y'
    os.system(cmd)
    
    if os.path.exists(audio_path):
        print(f"오디오 추출 완료: {audio_path}")
        return audio_path
    else:
        print("오디오 추출 실패")
        return None

def transcribe_audio(audio_path, language="ko-KR", chunk_length_ms=30000):
    """오디오 파일을 텍스트로 변환 (긴 파일도 처리)"""
    
    recognizer = sr.Recognizer()
    
    # 오디오 파일 로드
    print(f"오디오 파일 로딩: {audio_path}")
    audio = AudioSegment.from_wav(audio_path)
    
    # 30초 단위로 나누기
    chunks = make_chunks(audio, chunk_length_ms)
    
    full_text = []
    
    for i, chunk in enumerate(chunks):
        print(f"처리 중: {i+1}/{len(chunks)} 부분")
        
        # 임시 파일로 저장
        chunk_name = f"chunk_{i}.wav"
        chunk.export(chunk_name, format="wav")
        
        # 음성 인식
        try:
            with sr.AudioFile(chunk_name) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language=language)
                full_text.append(text)
                print(f"  인식됨: {text[:50]}...")
        except sr.UnknownValueError:
            print(f"  {i+1}번째 부분 인식 실패")
        except sr.RequestError as e:
            print(f"  API 오류: {e}")
        finally:
            # 임시 파일 삭제
            if os.path.exists(chunk_name):
                os.remove(chunk_name)
    
    return " ".join(full_text)

def process_video_or_audio(file_path, output_text_file="transcript.txt"):
    """동영상 또는 오디오 파일 처리"""
    
    # 파일 확장자 확인
    ext = os.path.splitext(file_path)[1].lower()
    
    # 동영상인 경우 오디오 추출
    if ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']:
        audio_path = extract_audio_from_video(file_path)
        if not audio_path:
            return None
    elif ext in ['.wav', '.mp3', '.m4a', '.aac']:
        audio_path = file_path
    else:
        print(f"지원하지 않는 형식: {ext}")
        return None
    
    # 음성 인식
    print("\n음성 인식 시작...")
    transcript = transcribe_audio(audio_path)
    
    # 결과 저장
    if transcript:
        with open(output_text_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"\n변환 완료! 결과가 {output_text_file}에 저장되었습니다.")
        print("\n=== 변환된 텍스트 ===")
        print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
        return transcript
    else:
        print("음성 인식 실패")
        return None

# 사용 예시
if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        process_video_or_audio(file_path)
    else:
        print("사용법: python video_to_text.py [동영상/오디오 파일 경로]")
        print("예시: python video_to_text.py video.mp4")