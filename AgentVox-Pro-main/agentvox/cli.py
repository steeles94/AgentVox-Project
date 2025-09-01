"""
Command-line interface for agentvox
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from .voice_assistant import ModelConfig, AudioConfig


    

def main():
    # Required for multiprocessing on macOS/Windows
    import multiprocessing
    try:
        multiprocessing.set_start_method('spawn', force=True)
    except RuntimeError:
        pass  # Already set
    
    parser = argparse.ArgumentParser(description="AgentVox - Voice Assistant")
    parser.add_argument("--model", type=str, default="mlx-community/gemma-3-12b-it-4bit",
                       help="MLX model identifier (default: mlx-community/gemma-3-12b-it-4bit)")
    parser.add_argument("--stt-model", type=str, default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size for STT")
    parser.add_argument("--device", type=str, default=None,
                       choices=["cpu", "cuda", "mps", "auto"],
                       help="Device to use for inference (default: auto-detect)")
    parser.add_argument("--voice", type=str, default="multilingual",
                       help="TTS voice preset (male/female/multilingual) - for compatibility")
    parser.add_argument("--tts-engine", type=str, default="coqui",
                       choices=["coqui"],
                       help="TTS engine to use (default: coqui)")
    parser.add_argument("--speaker-wav", type=str, default=None,
                       help="Speaker voice sample file for voice cloning (Coqui only)")
    parser.add_argument("--list-voices", action="store_true",
                       help="[Deprecated] List voices - not supported with Coqui engine")
    parser.add_argument("--list-tts-models", action="store_true",
                       help="List all available Coqui TTS models")
    parser.add_argument("--record-speaker", action="store_true",
                       help="Record speaker voice sample for TTS voice cloning")
    
    # STT 파라미터
    parser.add_argument("--stt-language", type=str, default="ko",
                       help="STT language (default: ko)")
    parser.add_argument("--stt-beam-size", type=int, default=5,
                       help="STT beam size for decoding (default: 5)")
    parser.add_argument("--stt-temperature", type=float, default=0.0,
                       help="STT temperature for sampling (default: 0.0)")
    parser.add_argument("--stt-vad-threshold", type=float, default=0.5,
                       help="STT VAD threshold (default: 0.5)")
    parser.add_argument("--stt-vad-min-speech-duration", type=int, default=250,
                       help="Minimum speech duration in ms (default: 250)")
    parser.add_argument("--stt-vad-min-silence-duration", type=int, default=1000,
                       help="Minimum silence duration in ms before cutting off (default: 1000)")
    
    # TTS 파라미터
    parser.add_argument("--tts-speed", type=float, default=1.0,
                       help="TTS speed (1.0 is normal, higher is faster, default: 1.3)")
    
    # LLM 파라미터
    parser.add_argument("--llm-max-tokens", type=int, default=512,
                       help="Maximum tokens for LLM response (default: 512)")
    parser.add_argument("--llm-temperature", type=float, default=0.7,
                       help="LLM temperature for sampling (default: 0.7)")
    parser.add_argument("--llm-top-p", type=float, default=0.95,
                       help="LLM top-p for nucleus sampling (default: 0.95)")
    parser.add_argument("--llm-context-size", type=int, default=4096,
                       help="LLM context window size (default: 4096)")
    
    args = parser.parse_args()
    
    
    if args.list_tts_models:
        print("\nCoqui TTS models available:")
        print("=" * 80)
        print("\nThe default model used is: tts_models/multilingual/multi-dataset/xtts_v2")
        print("\nThis model supports:")
        print("  - Multiple languages (Korean, English, Japanese, Chinese, etc.)")
        print("  - Voice cloning with a speaker WAV file")
        print("\nUsage example:")
        print("  agentvox --speaker-wav path/to/voice_sample.wav")
        print("=" * 80)
        sys.exit(0)
    
    if args.list_voices:
        print("\n[Deprecated] --list-voices is not supported with Coqui engine")
        print("\nCoqui TTS uses voice cloning instead of preset voices.")
        print("To use a specific voice, record or provide a speaker WAV file:")
        print("  agentvox --record-speaker")
        print("  agentvox --speaker-wav path/to/voice_sample.wav")
        sys.exit(0)
    
    if args.record_speaker:
        # Import the recording module
        from .record_speaker_wav import main as record_main
        
        # Pass the stt_language to the recorder
        original_argv = sys.argv
        sys.argv = ["record_speaker_wav", "--language", args.stt_language]
        
        # Add output path if speaker_wav is specified
        if args.speaker_wav:
            sys.argv.extend(["--output", args.speaker_wav])
        
        try:
            record_main()
        finally:
            sys.argv = original_argv
        sys.exit(0)
    
    # Create configurations
    
    # Voice presets are for compatibility only - Coqui uses voice cloning
    stt_language = args.stt_language
    
    # Set device (auto-detection will happen in ModelConfig.__post_init__)
    device = args.device if args.device else "auto"
    
    # Use MLX model (always)
    llm_model = args.model
    
    model_config = ModelConfig(
        stt_model=args.stt_model,
        llm_model=llm_model,
        device=device,
        # STT parameters
        stt_language=stt_language,
        stt_beam_size=args.stt_beam_size,
        stt_temperature=args.stt_temperature,
        stt_vad_threshold=args.stt_vad_threshold,
        stt_vad_min_speech_duration_ms=args.stt_vad_min_speech_duration,
        stt_vad_min_silence_duration_ms=args.stt_vad_min_silence_duration,
        # TTS parameters
        tts_engine=args.tts_engine,
        speaker_wav=args.speaker_wav,
        tts_speed=args.tts_speed,
        # LLM parameters
        llm_max_tokens=args.llm_max_tokens,
        llm_temperature=args.llm_temperature,
        llm_top_p=args.llm_top_p,
        llm_context_size=args.llm_context_size
    )
    
    audio_config = AudioConfig()
    
    # Run the voice assistant
    try:
        # Import and create voice assistant with configurations
        from .voice_assistant import VoiceAssistant
        
        assistant = VoiceAssistant(model_config, audio_config)
        
        # Run conversation loop
        assistant.run_conversation_loop()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()