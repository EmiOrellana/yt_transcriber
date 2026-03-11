from yt_dlp import YoutubeDL
from src.config.settings import VIDEO_DIR
from src.config.settings import AUDIO_DIR
import os

def download_video(url: str, format: str = "bestvideo+bestaudio") -> str:

    """
    Download a video from a URL.

    Args:
        url (str): URL of the video.

    Returns:
        str: Path to the downloaded video file.
    """

    os.makedirs(VIDEO_DIR, exist_ok=True)

    def _download(use_cookies: bool) -> str:
        # Options
        ydl_opts = {
            "outtmpl": f"{VIDEO_DIR}/%(title)s.%(ext)s",
            "restrictfilenames": True,
            "noplaylist": True,
            "format": format,
        }

        if use_cookies:
            ydl_opts["cookiefile"] = "cookies.txt"
        
        # Download the video
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info_dict)

    try:
        print("Downloading without cookies...")
        video_path = _download(use_cookies=False)
    except Exception as e:
        print("First attempt failed, retrying with cookies...")
        print(e)
        video_path = _download(use_cookies=True)

    # Return the video file path
    return video_path


def download_audio(url: str, codec: str = "wav") -> str:

    """
    Download audio from a video URL and convert it to the desired codec.

    First tries without cookies (works in most cases).
    If it fails due to bot detection, retries using browser cookies.
    """

    os.makedirs(AUDIO_DIR, exist_ok=True)

    def _download(use_cookies: bool) -> str:
        # Options
        ydl_opts = {
            "outtmpl": f"{AUDIO_DIR}/%(title)s.%(ext)s",
            "restrictfilenames": True,
            "noplaylist": True, 
            "quiet": False,
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": codec,
            }],
        }

        if use_cookies:
            ydl_opts["cookiefile"] = "cookies.txt"

        # Download the audio
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            path = ydl.prepare_filename(info)

        return os.path.splitext(path)[0] + f".{codec}"

    # First attempt without cookies
    try:
        print("Downloading without cookies...")
        return _download(use_cookies=False)
    
    # If it fails, retry with cookies
    except Exception as e:
        print("First attempt failed, retrying with cookies...")
        print(e)
        return _download(use_cookies=True)
    
 