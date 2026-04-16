import os

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in .env")
url = "https://api.openai.com/v1/audio/transcriptions"

file_to_transcribe = "0.mp3"
file_location = "/Users/diego/coding/transcripcion/"+file_to_transcribe

with open(file_location, "rb") as f:
    files = {"file": (file_to_transcribe, f, "audio/mpeg")}
    data = {"model": "whisper-1", "response_format": "json", "language": "es"}
    headers = {"Authorization": f"Bearer {api_key}"}
    r = requests.post(url, headers=headers, files=files, data=data, timeout=600)
    print(r.json())