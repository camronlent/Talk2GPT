import openai
from config import getparser, getstr


_SECTION = "openai"


def _get_api_key() -> str:
    return getstr(getparser(), _SECTION, "api_key")


def transcribe(file: str):
    with open(file, "rb") as audio_file:
        return openai.Audio.transcribe(
            "whisper-1", audio_file, api_key=_get_api_key())
