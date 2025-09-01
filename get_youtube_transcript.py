#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
YouTube 자막 추출 스크립트
처음 3분간의 자막만 가져옵니다
"""

# 먼저 설치: pip install youtube-transcript-api

from youtube_transcript_api import YouTubeTranscriptApi

def get_first_3min_transcript(video_id):
    try:
        # 자막 목록 가져오기
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # 사용 가능한 자막 출력
        print("Available transcripts:")
        for transcript in transcript_list:
            print(f"- {transcript.language} ({'generated' if transcript.is_generated else 'manual'})")
        print("-" * 50)
        
        # 영어 자막 가져오기 (자동 생성 포함)
        try:
            transcript = transcript_list.find_transcript(['en'])
        except:
            transcript = transcript_list.find_generated_transcript(['en'])
        
        # 자막 데이터 가져오기
        transcript_data = transcript.fetch()
        
        # 처음 3분(180초)까지만 필터링
        first_3min = []
        for entry in transcript_data:
            if entry['start'] <= 180:  # 3분 = 180초
                first_3min.append(f"[{entry['start']:.1f}s] {entry['text']}")
            else:
                break
        
        return '\n'.join(first_3min)
    
    except Exception as e:
        return f"Error: {e}"

# 사용 예시
video_id = "KmDYXaaT9sA"
print(f"Video ID: {video_id}")
print("=" * 50)
print(get_first_3min_transcript(video_id))