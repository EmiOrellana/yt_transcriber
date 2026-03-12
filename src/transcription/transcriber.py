import whisper
import os
from src.config.settings import TRANSCRIPTION_DIR
from src.config.settings import SUBTITLE_DIR

model = whisper.load_model("small", download_root="models")


def transcribe(audio_path: str, language: str = "en") -> dict:

    """
    Transcribe an audio file using the Whisper model.

    Args:
        audio_path (str): The path to the audio file to be transcribed.
        language (str): The language of the audio. Default is "en" (English).

    Returns:
        dict: The transcription result from the Whisper model.
    """

    result = model.transcribe(audio_path, language=language)

    save_transcript(result, audio_path)
    save_timestamps(result, audio_path)

    return result
    

def save_transcript(result: dict, audio_path: str) -> str:

    """
    Save the full transcript to a text file.

    Args:
        result (dict): The transcription result from the Whisper model.
        audio_path (str): The path to the audio file that was transcribed.

    Returns:
        str: The path to the saved transcript text file.
    """

    filename = os.path.splitext(os.path.basename(audio_path))[0]
    os.makedirs(TRANSCRIPTION_DIR, exist_ok=True)

    transcript = result["text"]

    with open(os.path.join(TRANSCRIPTION_DIR, f"{filename}_transcript.txt"), "w") as f:
        f.write(transcript)

    return os.path.join(TRANSCRIPTION_DIR, f"{filename}_transcript.txt")

    
def save_timestamps(result: dict, audio_path: str) -> str:

    """
    Save the full transcript with timestamps to a text file.

    Args:
        result (dict): The transcription result from the Whisper model.
        audio_path (str): The path to the audio file that was transcribed.

    Returns:
        str: The path to the saved timestamps text file.
    """

    filename = os.path.splitext(os.path.basename(audio_path))[0]
    os.makedirs(SUBTITLE_DIR, exist_ok=True)

    segments  = result["segments"]

    with open(os.path.join(SUBTITLE_DIR, f"{filename}_timestamps.txt"), "w") as f:
        for segment in segments:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            f.write(f"[{start:.2f} - {end:.2f}] {text}\n")

    return os.path.join(SUBTITLE_DIR, f"{filename}_timestamps.txt")     