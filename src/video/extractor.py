import os
import logging
from yt_dlp import YoutubeDL
from src.config.settings import VIDEO_DIR
from src.config.settings import AUDIO_DIR


logger = logging.getLogger(__name__)


# Video download function with retry mechanism for bot detection 
def download_video(url: str, format: str, browser: str) -> str:

    """
    Download a video from a URL.
    First tries without cookies (works in most cases).
    If it fails due to bot detection, retries using browser cookies.

    Args:
        url (str): URL of the video.
        format (str): Format of the video to download. Default is "bestvideo+bestaudio" (best quality).
        browser (str): Browser to use for downloading (for cookies). Default is "firefox".

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
            "quiet": True,
            "js_runtimes": {
                "node": {
                    "node": {}
                }
            },
            "remote_components": [
                "ejs:github"
            ],
            "format": format,
        }

        if use_cookies:
            ydl_opts["cookiesfrombrowser"] = (browser, None, None, None)
        
        # Download the video
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_path = ydl.prepare_filename(info_dict)

        if not os.path.exists(video_path):
            with YoutubeDL(ydl_opts) as ydl:
                logger.info("Downloading video...")
                ydl.download([url])
            logger.info(f"Downloaded video saved to {video_path}.")
            return video_path

        logger.info(f"Video already exists at {video_path}, skipping download.")
        return video_path

    # First attempt without cookies
    try:
        logger.info("Downloading video without cookies...")
        return _download(use_cookies=False)
    
    # If it fails, retry with cookies
    except Exception as e:
        logger.exception("Download without cookies failed")
        logger.warning("First attempt failed, retrying with cookies...")
        return _download(use_cookies=True)


# Audio download function with retry mechanism for bot detection
def download_audio(url: str, format: str, codec: str, browser: str) -> str:

    """
    Download audio from a video URL and convert it to the desired codec.

    First tries without cookies (works in most cases).
    If it fails due to bot detection, retries using browser cookies.

    Args:
        url (str): URL of the video.
        format (str): Format of the audio to download. Default is "bestaudio/best" (best quality).
        codec (str): Audio codec to convert to. Default is "wav".
        browser (str): Browser to use for downloading (for cookies). Default is "firefox
    
    Returns:
        str: Path to the downloaded audio file.
    """

    os.makedirs(AUDIO_DIR, exist_ok=True)

    def _download(use_cookies: bool) -> str:
        # Options
        ydl_opts = {
            "outtmpl": f"{AUDIO_DIR}/%(title)s.%(ext)s",
            "restrictfilenames": True,
            "noplaylist": True, 
            "quiet": True,
            "js_runtimes": {
                "node": {
                    "node": {"node": "node"}
                }
            },
            "remote_components": [
                "ejs:github"
            ],
            "format": format,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": codec,
            }],
            
        }

        if use_cookies:
            ydl_opts["cookiesfrombrowser"] = (browser, None, None, None)

        # Download the audio
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_path = ydl.prepare_filename(info)
            audio_path = os.path.splitext(audio_path)[0] + f".{codec}"

        if not os.path.exists(audio_path):
            with YoutubeDL(ydl_opts) as ydl:
                logger.info("Downloading audio...")
                ydl.download([url])
            logger.info(f"Downloaded audio {codec} saved to {audio_path}.")
            return audio_path

        logger.info(f"Audio {codec} already exists at {audio_path}, skipping download.")
        return audio_path

    # First attempt without cookies
    try:    
        logger.info("Downloading audio without cookies...")
        return _download(use_cookies=False)
    
    # If it fails, retry with cookies
    except Exception as e:
        logger.exception("Download without cookies failed")
        logger.warning("First attempt failed, retrying with cookies...")        
        return _download(use_cookies=True)