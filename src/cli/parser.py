import argparse


def parse_args():

    parser = argparse.ArgumentParser(
        description="YouTube Transcriber CLI"
    )

    parser.add_argument(
        "-v", "--save-video",
        action="store_true",
        help="Download and save the video"
    )

    parser.add_argument(
        "-a", "--save-audio",
        action="store_true",
        help="Save the extracted audio file"
    )

    parser.add_argument(
        "-t", "--save-transcript",
        action="store_true",
        help="Generate and save transcript and .srt files"
    )

    parser.add_argument(
        "-api", "--use-api",
        action="store_true",
        help="Use OpenAI Whisper API instead of local model. Requires OPENAI_API_KEY in .env"
    )

    parser.add_argument(
        "-u", "--url",
        type=str,
        default="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        help="YouTube video URL to download and/or transcribe (default: find out)",
        metavar=""
    )

    parser.add_argument(
        "-b", "--browser",
        type=str,
        default="firefox",
        help="Browser to use for downloading (e.g., 'firefox', 'chrome') (default: firefox)",
        metavar=""
    )

    parser.add_argument(
        "--video-format",
        type=str,
        default="bestvideo+bestaudio/best",
        help="yt-dlp video format string (default: bestvideo+bestaudio/best)",
        metavar=""
    )

    parser.add_argument(
        "--audio-format",
        type=str,
        default="bestaudio/best",
        help="yt-dlp audio format string (default: bestaudio/best)",
        metavar=""
    )

    parser.add_argument(
        "--codec",
        type=str,
        default="wav",
        help="Audio codec for conversion (default: wav)",
        metavar=""
    )

    parser.add_argument(
        "-l", "--language",
        type=str,
        default="en",
        help="ISO 639-1 language code for transcription (e.g., 'en', 'es', 'fr') (default: en)",
        metavar=""
    )

    parser.add_argument(
        "-m", "--model-name",
        type=str,
        default="small",
        help="Whisper model size to use for transcription (e.g., 'tiny', 'base', 'small', 'medium', 'large') (default: small)",
        metavar=""
    )

    return parser.parse_args()