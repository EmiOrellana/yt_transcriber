from src.video.extractor import download_video

def main():
    url = "https://www.youtube.com/watch?v=RgpAc7U29BA"
    path = download_video(url)
    print(path)

if __name__ == "__main__":
    main()