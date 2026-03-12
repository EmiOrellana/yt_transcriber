import logging
from src.video.extractor import download_audio, download_video
from src.transcription.transcriber import transcribe
from src.audio.cleaner import cleanup_audio_file


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
    url: str = "https://www.youtube.com/watch?v=kSv6qlPtvR0",
    browser: str = "firefox",
    video_format: str = "bestvideo+bestaudio",
    audio_format: str = "bestaudio/best",
    codec: str = "wav",
    language: str = "es",
    model_name: str = "small"
):
    try:
        if save_video:
            logger.info("Downloading video...")
            video_path = download_video(url, format=video_format, browser=browser)
            logger.info(f"Video saved to {video_path}.")

        if save_transcript or save_audio:
            logger.info("Downloading audio...")
            audio_path = download_audio(url, format=audio_format, codec=codec, browser=browser)
            logger.info(f"Audio saved to {audio_path}.")

            if save_transcript:
                logger.info("Transcribing audio...")
                transcription = transcribe(audio_path, language=language, model_name=model_name)
                logger.info(f"Transcript saved to {transcription[0]}")
                logger.info(f"Segments saved to {transcription[1]}")

            if not save_audio:
                logger.info("Cleaning up audio file...")
                cleanup_audio_file(audio_path=audio_path)

    except Exception as e:
        logger.exception("An error occurred: {e}")

if __name__ == "__main__":
    main()