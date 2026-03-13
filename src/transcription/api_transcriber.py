import os
import logging
from openai import OpenAI
from src.config.settings import OPENAI_API_KEY, TRANSCRIPTION_DIR, SEGMENTS_DIR


logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = None


# Avoid unnecessary initialization if transcription is not needed
def _get_client() -> OpenAI:
    global client
    if client is None:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set. Add it to your .env file.")
        client = OpenAI(api_key=OPENAI_API_KEY)
    return client


# Helper function to convert audio files to MP3 format using ffmpeg (for files larger than 25MB)
def _convert_to_mp3(audio_path: str) -> str:
    base = os.path.splitext(audio_path)[0]
    mp3_path = f"{base}.mp3"
    os.system(f'ffmpeg -i "{audio_path}" -q:a 2 "{mp3_path}"')
    return mp3_path


# Helper function to format timestamps in SRT format (HH:MM:SS,mmm)
def _format_timestamp(seconds: float) -> str:

    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int((seconds - total_seconds) * 1000)
    
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


# Helper function to save the segments with timestamps to a text file in SRT format
def _segments_to_srt(segments) -> str:

    srt = []
    for i, seg in enumerate(segments, start=1):
        start = _format_timestamp(seg.start)
        end = _format_timestamp(seg.end)
        text = " ".join(seg.text.split())
        srt.append(f"{i}")
        srt.append(f"{start} --> {end}")
        srt.append(text)
        srt.append("")

    return "\n".join(srt)


# Helper function to save the transcript to a text file
def _save_transcript(text: str, path: str) -> None:

    os.makedirs(TRANSCRIPTION_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


# Helper function to save the segments with timestamps to a text file
def _save_segments(segments, path: str) -> None:

    os.makedirs(SEGMENTS_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(_segments_to_srt(segments))


# Transcription function using OpenAI API
def transcribe_api(audio_path: str, language: str) -> tuple[str, str]:

    """
    Transcribe an audio file using the Whisper model from OpenAI API.
    
    Args:
        audio_path (str): The path to the audio file.
        language (str): The language of the audio file.

    Returns:
        tuple[str, str]: The transcription text and the segment file path.
    """

    filename = os.path.splitext(os.path.basename(audio_path))[0]

    transcript_path = os.path.join(TRANSCRIPTION_DIR, f"{filename}_transcript.txt")
    segments_path = os.path.join(SEGMENTS_DIR, f"{filename}_segments.srt")

    if os.path.exists(transcript_path) and os.path.exists(segments_path):
        logger.info(f"Transcription for this video already exists: {filename}")
        return (transcript_path, segments_path)
    
    client = _get_client()
    file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    MAX_SIZE_MB = 25

    original_audio_path = audio_path

    if file_size_mb > MAX_SIZE_MB and not audio_path.endswith(".mp3"):
        logger.info(f"Audio file is too large for the API ({file_size_mb:.1f}MB), converting to MP3...")
        audio_path = _convert_to_mp3(audio_path)
        mp3_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
        if mp3_size_mb > MAX_SIZE_MB:
            os.remove(audio_path)  
            raise ValueError(f"Audio file too large even after MP3 conversion ({mp3_size_mb:.1f}MB). Max is {MAX_SIZE_MB}MB.")
        logger.info(f"Converted to MP3: {audio_path}")

    logger.info(f"Transcribing {filename} via OpenAI API...")

    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language=language,
            response_format="verbose_json"
        )

    logger.info(f"Transcription completed")

    if audio_path != original_audio_path:
        os.remove(audio_path)
        logger.info(f"Removed temporary MP3: {audio_path}")

    _save_transcript(result.text, transcript_path)
    _save_segments(result.segments, segments_path)

    logger.info(f"Transcription saved to {transcript_path}")
    logger.info(f"Segments saved to {segments_path}")

    return (transcript_path, segments_path)
