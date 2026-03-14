import logging
import torch
import yt_dlp
from src.video.extractor import download_audio, download_video
from src.transcription.transcriber import transcribe
from src.transcription.api_transcriber import transcribe_api
from src.audio.cleaner import cleanup_audio_file
from src.cli.parser import parse_args


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


# PIPELINE
def main(
    save_video: bool = False, 
    save_audio: bool = False, 
    save_transcript: bool = True,
    use_api: bool = False, 
    url: str = "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    browser: str = "firefox",
    video_format: str = "bestvideo+bestaudio/best",
    audio_format: str = "bestaudio/best",
    codec: str = "wav",
    language: str = "en",
    model_name: str = "small"
):
    try:
        if save_video:
            download_video(url, format=video_format, browser=browser)

        if save_transcript or save_audio:
            audio_path = download_audio(url, format=audio_format, codec=codec, browser=browser)

            if save_transcript:
                if use_api:
                    transcribe_api(audio_path, language=language) # transcribe_api returns a tuple with the paths to the transcript and segments files
                else:
                    transcribe(audio_path, language=language, model_name=model_name) # transcribe returns a tuple with the paths to the transcript and segments files

            if not save_audio:
                logger.info("Cleaning up audio file...")
                cleanup_audio_file(audio_path=audio_path)

    except yt_dlp.utils.DownloadError as e:
        logger.error(f"Download error (invalid URL, private or unavailable video): {e}")

    except torch.cuda.OutOfMemoryError as e:    
        logger.error(f"GPU out of memory. Try using a smaller Whisper model: {e}")

    except RuntimeError as e:
        logger.error(f"Whisper model error: {e}")

    except FileNotFoundError as e:
        logger.error(f"File not found, the download may have failed: {e}")

    except PermissionError as e:
        logger.error(f"Permission denied when writing to the output directory: {e}")

    except ValueError as e:
        logger.error(f"Invalid parameter, check the language code or model name: {e}")
        
    except Exception as e:
        # Fallback error handling for any other unexpected exceptions
        logger.exception(f"Unexpected error: {e}")

if __name__ == "__main__":
    args = parse_args()
    main(
        save_video = args.save_video,
        save_audio = args.save_audio,
        save_transcript = args.save_transcript,
        use_api = args.use_api,
        url = args.url,
        browser= args.browser,
        video_format = args.video_format,        
        audio_format = args.audio_format,
        codec = args.codec,
        language = args.language,
        model_name = args.model_name
    )