import whisper

model = whisper.load_model("small", download_root="models")

def transcribe(audio_path: str, language:str = "en", timestamps=False) -> str:    
    
    """Transcribe an audio file using the Whisper model. 
    'Small' model is used for a good balance between speed and accuracy

    Args:
        audio_path (str): Path to the audio file to transcribe.
        language (str, optional): Language code for transcription. Defaults to "en" (English).
        timestamps (bool, optional): Whether to include timestamps in the output. Defaults to False.

    Returns:
        str: Transcribed text or list of segments with timestamps.
    """
    
    result = model.transcribe(audio_path, language=language)
    
    if timestamps:
        return result["segments"]
    else:
        return result["text"]
 