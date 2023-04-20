from elevenlabslib import ElevenLabsUser
from audio.devices import get_output_device_info
from config import getparser, getstr


_SECTION = "elevenlabs"


def _get_api_key() -> str:
    return getstr(getparser(), _SECTION, "api_key")


def _get_voice_id() -> str:
    return getstr(getparser(), _SECTION, "voice_id")


def text_to_speach(text: str, file: str):
    eleven = ElevenLabsUser(_get_api_key())
    voice = eleven.get_voice_by_ID(_get_voice_id())
    stability = 0.75
    similarity_boost = 0.75
    audio = voice.generate_audio_bytes(text, stability, similarity_boost)
    with open(file, "wb") as f:
        f.write(audio)
