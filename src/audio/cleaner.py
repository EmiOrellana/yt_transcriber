import os
import logging


logger = logging.getLogger(__name__)


# Clean up function for audio files 
def cleanup_audio_file(audio_path: str) -> None:

    """Clean up audio temporary files created after audio transcription."""

    try:
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
            logger.info(f"Removed file: {audio_path}")
    except Exception as e:
        logger.error(f"Error removing {audio_path}: {e}")



