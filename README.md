# YouTube Video Transcriber

A modular Python CLI tool to download and transcribe YouTube videos.
Generates both plain text transcripts and `.srt` subtitle files, 
using either a local Whisper model or the OpenAI Whisper API.
Users may choose to download the video, audio, or just the transcript.

## Status
Active development — CLI fully functional. GUI in planning stage.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

yt-transcriber is a command-line tool built with Python that automates the process of downloading and transcribing YouTube videos. It uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloading and [OpenAI Whisper](https://github.com/openai/whisper) for transcription.

The tool supports two transcription modes:
- **Local**: runs Whisper locally, no API key required, GPU recommended
- **API**: uses the OpenAI Whisper API, faster and no GPU needed, requires an API key

---

## Features

- Download YouTube videos and/or audio
- Transcribe audio using a local Whisper model (offline, no API key needed)
- Transcribe audio using the OpenAI Whisper API (faster, no GPU needed)
- Generate plain text transcripts and `.srt` subtitle files
- Automatic audio conversion to MP3 if file exceeds API size limit
- Skips downloading or transcribing if files already exist (no redundant processing)
- Lazy loading of the Whisper model (only loaded when needed, saves memory)
- Local files support for transcription (audio and video formats)
- Modular dependencies — install only what you need (video/audio download, local transcription, API transcription)

---

## Requirements

- Python 3.8+
- GPU recommended for local transcription (CUDA-compatible)
- OpenAI API key (only if using `--use-api`)

### FFmpeg
Required for audio extraction and conversion.
```bash
sudo apt install ffmpeg    # Linux

brew install ffmpeg        # Mac
```

**Windows**: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) and add the `bin` folder to your PATH. Verify with `ffmpeg -version`.

### Node.js
Required for yt-dlp JavaScript runtime support. **Version 22.6+ required.**

Download the LTS version from [nodejs.org](https://nodejs.org) and ensure it's added to your PATH. Verify with `node -v`.

---

## Installation
```bash
# Clone the repository
git clone https://github.com/tuusuario/yt-transcriber.git
cd yt-transcriber

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Linux/Mac

# Install dependencies

# For audio and video download only
pip install -e .

# With local transcription (CPU)
pip install -e ".[local]"

# With local transcription (GPU - recommended)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install -e ".[local]"

# With OpenAI API transcription
pip install -e ".[api]"

# Everything
pip install -e ".[all]"

# Transcribe a video
yt-transcriber -u "https://www.youtube.com/watch?v=..." -t

# See all options
yt-transcriber --help
```

### Set up environment variables (Add OpenAI API key if using API mode)
```bash
cp .env.example .env
```

---

## Usage
```bash
yt-transcriber -u "VIDEO_URL" [options]
```

### Options

| Flag | Long | Description |
|------|------|-------------|
| `-u` | `--url` | YouTube video URL |
| `-t` | `--save-transcript` | Generate transcript and .srt file |
| `-v` | `--save-video` | Download and save the video |
| `-a` | `--save-audio` | Save the extracted audio file |
| `-api` | `--use-api` | Use OpenAI Whisper API instead of local model |
| `-l` | `--language` | Language code (default: en) |
| `-m` | `--model-name` | Whisper model size (default: small) |
| `-b` | `--browser` | Browser for cookie extraction (default: firefox) |
| `-f` | `--file` | Path to a local audio/video file |

### Examples
```bash
# Transcribe a video
yt-transcriber -u "https://youtube.com/..." -t

# Download video and transcribe
yt-transcriber -u "https://youtube.com/..." -v -t

# Transcribe keeping audio file
yt-transcriber -u "https://youtube.com/..." -t -a

# Transcribe using OpenAI API
yt-transcriber -u "https://youtube.com/..." -t -api

# Transcribe in Spanish with medium model
yt-transcriber -u "https://youtube.com/..." -t -l es -m medium

# Transcribe a local file
yt-transcriber -f "path/to/file.mp4" -t
```

---

## Roadmap

- [x] Local file support (audio/video)
- [ ] Streamlit GUI
- [ ] Unit tests

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.