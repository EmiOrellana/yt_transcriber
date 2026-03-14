import os
import logging

logger = logging.getLogger(__name__)

SUPPORTED_AUDIO = [".mp3", ".wav", ".flac", ".ogg", ".m4a"]
SUPPORTED_VIDEO = [".mp4", ".mkv", ".webm", ".avi", ".mov"]
SUPPORTED_EXTENSIONS = SUPPORTED_AUDIO + SUPPORTED_VIDEO


def prepare_audio(file_path: str) -> str:

    """
    Validates the file and extracts audio if it's a video. Returns the audio path.
    
    Args:
        file_path (str): The path to the input file (audio or video).
        
    Returns:
        str: The path to the audio file ready for transcription.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file format is not supported.
    """
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file format: {ext}. Supported formats: {SUPPORTED_EXTENSIONS}")
    
    if ext in SUPPORTED_VIDEO:
        logger.info(f"Video file detected, extracting audio...")
        return _extract_audio(file_path)
    
    return file_path


def _extract_audio(video_path: str) -> str:

    """Extracts audio from a video file using FFmpeg. Returns the audio path."""

    audio_path = os.path.splitext(video_path)[0] + ".wav"
    
    if os.path.exists(audio_path):
        logger.info(f"Audio already exists, skipping extraction: {audio_path}")
        return audio_path
    
    os.system(f'ffmpeg -loglevel quiet -y -i "{video_path}" -q:a 2 "{audio_path}"')
    logger.info(f"Audio extracted to {audio_path}")
    return audio_path