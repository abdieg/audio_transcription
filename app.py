import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in .env")

SUPPORTED_FORMATS = ["mp3", "mpga", "m4a", "wav", "webm"]
OPENAI_URL = "https://api.openai.com/v1/audio/transcriptions"

LANGUAGES = {
    "Auto-detect": None,
    "Afrikaans": "af",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Belarusian": "be",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Chinese": "zh",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "Galician": "gl",
    "German": "de",
    "Greek": "el",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Kazakh": "kk",
    "Korean": "ko",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Macedonian": "mk",
    "Malay": "ms",
    "Marathi": "mr",
    "Maori": "mi",
    "Nepali": "ne",
    "Norwegian": "no",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "Serbian": "sr",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Spanish": "es",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog": "tl",
    "Tamil": "ta",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Vietnamese": "vi",
    "Welsh": "cy",
}

if "transcriptions" not in st.session_state:
    st.session_state.transcriptions = {}

st.title("Audio Transcription")

uploaded_files = st.file_uploader(
    "Upload audio files",
    type=SUPPORTED_FORMATS,
    accept_multiple_files=True,
)

language_name = st.selectbox("Language", list(LANGUAGES.keys()), index=list(LANGUAGES.keys()).index("Spanish"))
language_code = LANGUAGES[language_name]

MAX_FILE_SIZE_MB = 25
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

if uploaded_files and st.button("Transcribe"):
    for uploaded_file in uploaded_files:
        ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
        if ext not in SUPPORTED_FORMATS:
            st.error(f"**{uploaded_file.name}** — unsupported format `.{ext}`. Allowed: {', '.join(f.upper() for f in SUPPORTED_FORMATS)}")
            continue

        if uploaded_file.size > MAX_FILE_SIZE_BYTES:
            st.error(f"**{uploaded_file.name}** — file is {uploaded_file.size / 1024 / 1024:.1f} MB, exceeds the {MAX_FILE_SIZE_MB} MB limit.")
            continue

        with st.spinner(f"Transcribing {uploaded_file.name}..."):
            uploaded_file.seek(0)
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {
                "model": "whisper-1",
                "response_format": "json",
                **({"language": language_code} if language_code else {}),
            }
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.post(OPENAI_URL, headers=headers, files=files, data=data, timeout=600)

        if response.ok:
            st.session_state.transcriptions[uploaded_file.name] = response.json().get("text", "")
        else:
            st.error(f"**{uploaded_file.name}** — Error {response.status_code}: {response.text}")

for filename, text in st.session_state.transcriptions.items():
    st.subheader(filename)
    st.code(text, language=None)
    st.download_button(
        "Download as .txt",
        data=text,
        file_name=filename + ".txt",
        key=f"dl_{filename}",
    )
