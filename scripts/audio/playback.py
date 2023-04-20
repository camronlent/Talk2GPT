from pyaudio import PyAudio, paInt16
from pydub import AudioSegment
from pydub.utils import make_chunks
from audio.devices import get_output_device_info
# from io import BytesIO


def play_mp3(file) -> None:
    """Play a mp3 file

    Args:
        file (str): The path to the m4a file.
    """
    _play_audio_segment(AudioSegment.from_file(file, format="mp3"))


def play_m4a(file) -> None:
    """Play a m4a file

    Args:
        file (str): The path to the m4a file.
    """
    _play_audio_segment(AudioSegment.from_file(file, format="m4a"))


def _play_audio_segment(audio: AudioSegment) -> None:
    audio = audio.set_channels(1).set_sample_width(2).set_frame_rate(44100)
    p = PyAudio()

    output_device_index = get_output_device_info().get('device_index')
    # print(f"output_device_index: {output_device_index}")
    stream = p.open(format=paInt16, channels=1, rate=44100,
                    output=True, output_device_index=output_device_index)

    chunk_size = 1024
    for chunk in make_chunks(audio, chunk_size):
        stream.write(chunk._data)

    stream.stop_stream()
    stream.close()

    p.terminate()
