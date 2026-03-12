import whisper
import os
from src.config.settings import TRANSCRIPTION_DIR
from src.config.settings import SUBTITLE_DIR
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("small", download_root="models", device=device)


def transcribe(audio_path: str, language: str = "en") -> tuple[str, str]:

    """
    Transcribe an audio file using the Whisper model.

    Args:
        audio_path (str): The path to the audio file to be transcribed.
        language (str): The language of the audio. Default is "en" (English).

    Returns:
        tuple[str, str]: A tuple containing the paths to the saved transcript and timestamps text files.
    """

    print(f"Whisper running on: {device}")
    
    result = model.transcribe(audio_path, language=language)
    filename = os.path.splitext(os.path.basename(audio_path))[0]

    transcript_path = save_transcript(result, filename)
    segments_path = save_segments(result, filename)

    return (transcript_path, segments_path)


def save_transcript(result: dict, filename: str) -> str:

    """
    Save the full transcript to a text file.

    Args:
        result (dict): The transcription result from the Whisper model.
        audio_path (str): The path to the audio file that was transcribed.

    Returns:
        str: The path to the saved transcript text file.
    """

    os.makedirs(TRANSCRIPTION_DIR, exist_ok=True)
    path = os.path.join(TRANSCRIPTION_DIR, f"{filename}_transcript.txt")

    transcript = result["text"]

    with open(path, "w", encoding="utf-8") as f:
        f.write(transcript)

    return path

def save_segments(result: dict, filename: str) -> str:

    """
    Save the full transcript with timestamps to a text file.

    Args:
        result (dict): The transcription result from the Whisper model.
        audio_path (str): The path to the audio file that was transcribed.

    Returns:
        str: The path to the saved timestamps text file.
    """

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
            text = seg["text"].strip()

            srt.append(f"{i}")
            srt.append(f"{start} --> {end}")
            srt.append(text)
            srt.append("")

        return "\n".join(srt)

    with open(path, "w", encoding="utf-8") as f:
        f.write(_segments_to_srt(segments))

    return path


