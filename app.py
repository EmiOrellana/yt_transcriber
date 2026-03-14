import tempfile
import os
import logging
import streamlit as st


class StreamlitHandler(logging.Handler):

    def __init__(self, container):
        super().__init__() 
        self.container = container
        self.logs = []
    
    def emit(self, record):
        record.exc_info = None
        record.exc_text = None
        msg = self.format(record)
        # Skip traceback lines
        if msg.startswith("Traceback") or msg.startswith("  ") or msg.startswith("    "):
            return
        self.logs.append(msg)
        self.container.code("\n".join(self.logs))


st.title("YouTube Video Transcriber")
st.write("Welcome to the YouTube Transcriber app!")

input_mode = st.radio("Select input source:", ["YouTube URL", "Local File"])

if input_mode == "YouTube URL":
    url = st.text_input("Enter YouTube video URL:")
else:
    file_path = st.file_uploader("Upload audio or video file:")

st.sidebar.subheader("Transcription Settings")

use_api = st.sidebar.checkbox("Use OpenAI API for transcription (instead of local Whisper model)", value=False, help="Requires an OpenAI API key and file lesser than 25MB")

st.sidebar.divider()

if not use_api:    
    model_name = st.sidebar.selectbox(
        "Whisper model",
        ["tiny", "base", "small", "medium", "large", "turbo"],
        index=2,
        help="Choose a smaller model for faster transcription (less accurate), or a larger model for better accuracy or if running on GPU "
    )

if use_api:
    api_key = st.sidebar.text_input(
        "OpenAI API key",
        type="password",
        help="Paste your OpenAI API key here. If empty, falls back to OPENAI_API_KEY in .env"
    )
else:
    api_key = None

st.sidebar.divider()
language = st.sidebar.text_input("Language code", value="en", help="ISO 639-1 code, e.g.. 'en', 'es', 'fr', etc.")

st.sidebar.divider()
st.sidebar.subheader("Output Options")

save_transcript = st.sidebar.checkbox("Save transcript text file", value=True)

if input_mode == "YouTube URL":
    save_audio = st.sidebar.checkbox("Save audio file", value=False, help="if not checked, the audio file will be deleted after transcription")
    save_video = st.sidebar.checkbox("Save video file", value=False, help="if not checked, the video file will not be downloaded")

st.divider()

if st.button("Start", type="primary"):

    st.divider()

    if input_mode == "YouTube URL" and not url:
        st.error("Please enter a YouTube video URL.")

    elif input_mode == "Local File" and not file_path:
        st.error("Please upload an audio or video file.")

    else:
        tmp_file = None
        if input_mode == "Local File":
            # Save the uploaded file to a temporary location
            tmp_dir = tempfile.gettempdir()
            tmp_file = os.path.join(tmp_dir, file_path.name)
            with open(tmp_file, "wb") as f:
                f.write(file_path.read())

        from main import main

        with st.spinner("Processing..."):

            log_container = st.empty()
            handler = StreamlitHandler(log_container)
            handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))

            logging.getLogger().addHandler(handler)

            result = main(
                save_video=save_video if input_mode == "YouTube URL" else False,
                save_audio=save_audio if input_mode == "YouTube URL" else False,
                save_transcript=save_transcript,
                use_api=use_api,
                url=url if input_mode == "YouTube URL" else None,
                file=tmp_file if input_mode == "Local File" else None,
                language=language,
                model_name=model_name if not use_api else None,
                api_key=api_key if api_key else None,
            )

            logging.getLogger().removeHandler(handler)

            if tmp_file:
                os.unlink(tmp_file)

        if result["transcript"] or result["audio"] or result["video"]:
            st.success("Done!")
        else:
            st.error("Something went wrong. Check the logs above for details.")

        if result["transcript"]:
            st.divider()
            st.subheader("Transcript")
            with open(result["transcript"], "r", encoding="utf-8") as f:
                transcript_text = f.read()
            st.text_area("Transcript text", transcript_text, height=300, label_visibility="collapsed") 

        

