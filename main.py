from src.video.extractor import download_video
from src.video.extractor import extract_audio

def main():
    print("Downloading video...")
    url = "https://www.youtube.com/watch?v=RgpAc7U29BA"
    path = download_video(url)
    print(path)

    print("Extracting audio...")
    audio_path = extract_audio(path)
    print(audio_path)

if __name__ == "__main__":
    main()