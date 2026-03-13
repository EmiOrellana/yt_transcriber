from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

VIDEO_DIR = "tmp/video"
AUDIO_DIR = "tmp/audio"
TRANSCRIPTION_DIR = "tmp/transcript"
SEGMENTS_DIR = "tmp/subtitles"