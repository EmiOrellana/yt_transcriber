import os
import logging
import whisper
import torch
from src.config.settings import TRANSCRIPTION_DIR
from src.config.settings import SUBTITLE_DIR



logger = logging.getLogger(__name__)
device = "cuda" if torch.cuda.is_available() else "cpu"
model_instance = None
loaded_model = None


# Lazy loading of the model to avoid unnecessary memory usage if transcription is not needed
def get_model(model_name:str) -> whisper.Whisper:

    global model_instance, loaded_model

    if model_instance is None or loaded_model != model_name:
        logger.info(f"Loading Whisper model...{model_name}")
        model_instance = whisper.load_model(model_name, download_root="models", device=device)
        loaded_model = model_name
        logger.info(f"Whisper running on {device}")

    return model_instance


# Transcription function
def transcribe(audio_path: str, language: str, model_name: str) -> tuple[str, str]:

    """
    Transcribe an audio file using the Whisper model.

    Args:
        audio_path (str): The path to the audio file to be transcribed.
        language (str): The language of the audio. Default is "en" (English).
        model_name (str): The name of the Whisper model to use. Default is "small" (available models: tiny, base, small, medium, large, turbo).

    Returns:
        tuple[str, str]: A tuple containing the paths to the saved transcript and timestamps text files.
    """

    model = get_model(model_name)

    result = model.transcribe(audio_path, language=language)
    filename = os.path.splitext(os.path.basename(audio_path))[0]

    transcript_path = _save_transcript(result, filename)
    segments_path = _save_segments(result, filename)

    return (transcript_path, segments_path)


# Helper function to save the transcript to a text file
def _save_transcript(result: dict, filename: str) -> str:

    """Save the full transcript to a text file."""

    os.makedirs(TRANSCRIPTION_DIR, exist_ok=True)

    path = os.path.join(TRANSCRIPTION_DIR, f"{filename}_transcript.txt")
    transcript = result["text"]

    with open(path, "w", encoding="utf-8") as f:
        f.write(transcript)

    return path


# Helper function to save the segments with timestamps to a text file
def _save_segments(result: dict, filename: str) -> str:

    """Save the full transcript with timestamps to a text file."""

    os.makedirs(SUBTITLE_DIR, exist_ok=True)

    path = os.path.join(SUBTITLE_DIR, f"{filename}_segments.srt")
    segments  = result["segments"]

    def _format_timestamp(seconds: float) -> str:

        total_seconds = int(seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        millis = int((seconds - total_seconds) * 1000)

        return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

    def _segments_to_srt(segments):
        srt = []

        for i, seg in enumerate(segments, start=1):
            start = _format_timestamp(seg["start"])
            end = _format_timestamp(seg["end"])
            text = " ".join(seg["text"].split()).replace("-->", "→")

            srt.append(f"{i}")
            srt.append(f"{start} --> {end}")
            srt.append(text)
            srt.append("")

        return "\n".join(srt)

    with open(path, "w", encoding="utf-8") as f:
        f.write(_segments_to_srt(segments))

    return path


