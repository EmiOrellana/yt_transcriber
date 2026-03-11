from yt_dlp import YoutubeDL
from src.config.settings import VIDEO_DIR
from src.config.settings import AUDIO_DIR
import os
import subprocess

def download_video(url: str) -> str:
    """
    Download a video from a URL.

    Args:
        url (str): URL of the video.

    Returns:
        str: Path to the downloaded video file.
    """
    # Options
    os.makedirs(VIDEO_DIR, exist_ok=True)

    ydl_opts = {
        "outtmpl": f"{VIDEO_DIR}/%(title)s.%(ext)s",
        "restrictfilenames": True,
        "noplaylist": True,
    }
    
    # Download the video
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_path = ydl.prepare_filename(info_dict)

    # Return the video file path
    return video_path

def extract_audio(video_path: str) -> str:
    """
    Extract audio from a video file.

    Args:
        video_path (str): Path to the video file.

    Returns:
        str: Path to the extracted audio file.
    """
    # Options
    os.makedirs(AUDIO_DIR, exist_ok=True)

    filename = os.path.basename(video_path)
    name, _ = os.path.splitext(filename)
    audio_path = os.path.join(AUDIO_DIR, name + ".wav")

    # Extract audio
    subprocess.run([
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        audio_path
    ], check=True)    

    # Return the audio file path
    return audio_path   