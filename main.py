from src.video.extractor import download_audio
from src.video.extractor import download_video
from src.transcription.transcriber import transcribe

def main():
    print("Downloading audio...")
    url = "https://www.youtube.com/watch?v=kSv6qlPtvR0"
    path = download_audio(url)

    print("Transcribing audio...")
    transcription = transcribe(path, "es")
    print(transcription)
    print(path)

if __name__ == "__main__":
    main()