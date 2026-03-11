# Youtube Video Transcriptor

Extracts, transcribes, and translates audio from YouTube videos using a modular Python pipeline.


## Status
Project initialization.

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
