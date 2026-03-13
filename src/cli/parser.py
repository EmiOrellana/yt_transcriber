import argparse


def parse_args():

    parser = argparse.ArgumentParser(
        description="YouTube Transcriber CLI"
    )

    parser.add_argument(
        "-v", "--save-video",
        type=bool,
        default=False,
        help="Download and save the video"
    )

    parser.add_argument(
        "-a", "--save-audio",
        type=bool,
        default=False,
        help="Download and save the audio"
    )

    parser.add_argument(
        "-t", "--save-transcript",
        type=bool,
        default=True,
        help="Save transcript and segments files"
    )

    parser.add_argument(
        "-api", "--use-api",
        type=bool,
        default=False,
        help="Use OpenAI API for transcription. You need to set the OPENAI_API_KEY env variable for this to work"
    )

    parser.add_argument(
        "-u", "--url",
        type=str,
        default="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        help="YouTube video URL to download/extract audio/transcribe"
    )

    parser.add_argument(
        "-b", "--browser",
        type=str,
        default="firefox",
        help="Browser to use for downloading (e.g., 'firefox', 'chrome')"
    )

    parser.add_argument(
        "--video-format",
        type=str,
        default="bestvideo+bestaudio",
        help="Video format to download"
    )

    parser.add_argument(
        "--audio-format",
        type=str,
        default="bestaudio/best",
        help="Audio format to download"
    )

    parser.add_argument(
        "--codec",
        type=str,
        default="wav",
        help="Audio codec to use for conversion"
    )

    parser.add_argument(
        "-l", "--language",
        type=str,
        default="en",
        help="Language code for transcription (e.g., 'en' for English)"
    )

    parser.add_argument(
        "-m", "--model-name",
        type=str,
        default="small",
        help="Whisper model size to use for transcription (e.g., 'tiny', 'base', 'small', 'medium', 'large')"
    )

    return parser.parse_args()