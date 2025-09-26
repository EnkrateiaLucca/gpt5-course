#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = ["openai"]
# ///

import sys
from openai import OpenAI


def transcribe_audio(file_path):
    """Transcribe audio file using OpenAI's Whisper model."""
    client = OpenAI()
    
    try:
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        return transcription
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error transcribing audio: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run transcribe.py <audio_file_path>", file=sys.stderr)
        sys.exit(1)
    
    input_audio_file = sys.argv[1]
    transcription = transcribe_audio(input_audio_file)
    print(f"Transcription:\n\n{transcription}")