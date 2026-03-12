# Youtube Video Transcriber

Extracts, transcribes, and translates audio from YouTube videos using a modular Python pipeline.
Also supports video and audio downloading. Future GUI/WebApp in development.

## Status
Project initialization.

---

# Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

# Overview

Brief explanation of what the project does.

Example:

This application allows users to download audio from online media and process it for transcription.

Main features:

- Download audio from video sources
- Convert media using FFmpeg
- Prepare audio files for transcription
- CLI interface
- Future GUI support

---

# Quick Start

Clone the repository and install the required dependencies.

```bash
git clone https://github.com/yourusername/project-name.git
cd project-name
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Run the CLI tool:

```bash
python main.py <video_url>
```

Example:

```bash
python main.py https://youtube.com/example_video
```

---

# Requirements

Before running the application, make sure the following dependencies are installed and available in your system.

---

## Node.js

This project requires **Node.js** to run some components used by the application.

### Installation

Download Node.js from the official website:

https://nodejs.org

Install the **LTS version**, recommended for most users.

During installation, ensure that **Node.js is added to your system PATH**.

### Verify installation

Run the following command in your terminal:

```bash
node -v
```

You should see a version number similar to:

```
v20.x.x
```

If the command is not recognized, make sure Node.js was correctly added to the system PATH.

---

## FFmpeg

The application requires **FFmpeg** for audio processing and media conversion.

It is used to:

- Extract audio from downloaded media
- Convert audio formats
- Prepare audio for transcription

### Installation

Download FFmpeg from the official website:

https://ffmpeg.org/download.html

After downloading:

1. Extract the files
2. Add the **`bin` directory** to your system PATH

Example path:

```
C:\ffmpeg\bin
```

### Verify installation

Run the following command:

```bash
ffmpeg -version
```

If correctly installed, you should see information about the FFmpeg build and version.

---

## Troubleshooting

If the commands `node` or `ffmpeg` are not recognized:

1. Verify they are installed.
2. Check that their directories are included in your system **PATH environment variable**.
3. Restart your terminal after modifying the PATH.

---

# Installation

Installation instructions will be added here.

Example steps that will likely appear here:

```
git clone <repository>
cd project
pip install -r requirements.txt
```

---

# Usage

Instructions on how to use the application will be documented here.

Example:

```
python main.py <video_url>
```

---

# Roadmap

Planned features for future development.

- CLI tool
- Browser cookie selection
- GUI interface
- Batch transcription
- API support

---

# Contributing

Guidelines for contributing will be added here.

---

# License

License information will be added here.