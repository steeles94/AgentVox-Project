#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Conan O'Brien 졸업 연설 영상의 첫 3분을 처리하는 스크립트
"""

import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import warnings
warnings.filterwarnings("ignore")

def extract_first_3min_audio(video_path, output_audio="conan_3min.wav"):
    """비디오의 첫 3분 오디오 추출"""
    print("영상에서 첫 3분 오디오 추출 중...")
    
    try:
        # 비디오 로드
        video = VideoFileClip(video_path)
        
        # 첫 3분(180초)만 추출
        duration = min(180, video.duration)
        audio_clip = video.subclip(0, duration).audio
        
        # WAV로 저장
        audio_clip.write_audiofile(output_audio, verbose=False, logger=None)
        
        # 메모리 정리
        audio_clip.close()
        video.close()
        
        print(f"오디오 추출 완료: {duration:.1f}초")
        return output_audio
        
    except Exception as e:
        print(f"오디오 추출 실패: {e}")
        return None

def transcribe_audio_chunks(audio_path, language="en-US"):
    """오디오를 30초 단위로 나누어 텍스트로 변환"""
    print("\n음성을 텍스트로 변환 중...")
    
    recognizer = sr.Recognizer()
    
    # 오디오 로드
    audio = AudioSegment.from_wav(audio_path)
    
    # 30초 단위로 나누기
    chunk_length = 30000  # 30초
    chunks = [audio[i:i+chunk_length] for i in range(0, len(audio), chunk_length)]
    
    transcripts = []
    
    for i, chunk in enumerate(chunks):
        print(f"처리 중: {i+1}/{len(chunks)} 부분 ({i*30}초-{min((i+1)*30, 180)}초)")
        
        # 임시 파일로 저장
        temp_file = f"temp_chunk_{i}.wav"
        chunk.export(temp_file, format="wav")
        
        try:
            with sr.AudioFile(temp_file) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language=language)
                transcripts.append(f"[{i*30:03d}s-{min((i+1)*30, 180):03d}s] {text}")
                print(f"  ✓ 인식 완료")
        except sr.UnknownValueError:
            transcripts.append(f"[{i*30:03d}s-{min((i+1)*30, 180):03d}s] (인식 불가)")
            print(f"  ✗ 인식 실패")
        except Exception as e:
            print(f"  오류: {e}")
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    return "\n\n".join(transcripts)

def main():
    video_path = r"C:\Users\SS\Downloads\Conan O'Brien's 2011 Dartmouth College Commencement Address _ CONAN on TBS.mp4"
    
    if not os.path.exists(video_path):
        print(f"영상 파일을 찾을 수 없습니다: {video_path}")
        return
    
    print("=" * 60)
    print("Conan O'Brien - 2011 Dartmouth College 졸업 연설")
    print("첫 3분 처리 시작")
    print("=" * 60)
    
    # 1. 오디오 추출
    audio_file = extract_first_3min_audio(video_path)
    
    if not audio_file:
        return
    
    # 2. 음성 인식
    transcript = transcribe_audio_chunks(audio_file)
    
    # 3. 결과 저장
    output_file = "conan_transcript_3min.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Conan O'Brien - 2011 Dartmouth College Commencement Address\n")
        f.write("First 3 Minutes Transcript\n")
        f.write("=" * 60 + "\n\n")
        f.write(transcript)
    
    print(f"\n결과가 {output_file}에 저장되었습니다.")
    print("\n=== 변환된 텍스트 (첫 부분) ===")
    print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
    
    # 임시 파일 삭제
    if os.path.exists(audio_file):
        os.remove(audio_file)

if __name__ == "__main__":
    main()