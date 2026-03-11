from yt_dlp import YoutubeDL
from src.config.settings import VIDEO_DIR
import os

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

    # Extract audio

    # Return the audio file path