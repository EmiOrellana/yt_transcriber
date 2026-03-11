from src.video.extractor import download_audio
from src.video.extractor import download_video

def main():
    print("Downloading audio...")
    url = "https://www.youtube.com/watch?v=RgpAc7U29BA"
    path = download_audio(url)
    print(path)

if __name__ == "__main__":
    main()