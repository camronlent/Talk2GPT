import threading
import numpy as np


from pyaudio import PyAudio, paInt16
from typing import Callable
from audio.devices import get_input_device_info
from pydub import AudioSegment


class Recorder():
    _chunk: int
    _is_recording: bool
    _frames: list[bytes]
    _thread: threading.Thread

    _channels = 1
    _rate = 44100

    _pyaudio: None | PyAudio = None
    _stream: None | PyAudio.Stream = None

    def __init__(self, chunk: int):
        self._chunk = chunk
        self._is_recording = False
        self._frames = []

    def start(self):
        if (self._is_recording == True):
            return

        input_device_index = get_input_device_info().get('device_index')

        self._pyaudio = PyAudio()
        self._stream = self._pyaudio.open(
            format=paInt16,
            channels=self._channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            input_device_index=input_device_index)

        self._thread = threading.Thread(target=self.record)
        self._thread.start()

    def stop(self):
        if (self._is_recording == False or self._stream == None or self._pyaudio == None):
            return

        self._is_recording = False
        self._thread.join()

        self._stream.stop_stream()
        self._stream.close()
        self._stream = None

        self._pyaudio.terminate()
        self._pyaudio = None

    def to_audio_segment(self) -> AudioSegment:
        audio_data = b''.join(self._frames)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        return AudioSegment(
            audio_array.tobytes(),
            frame_rate=self._rate,
            sample_width=audio_array.dtype.itemsize,
            channels=self._channels)

    def record(self):
        if (self._is_recording == True or self._stream == None or self._pyaudio == None):
            return

        self._frames.clear()
        self._is_recording = True
        while self._is_recording:
            self._frames.append(self._stream.read(self._chunk))


def record_m4a(file: str) -> Callable[[], None]:
    recorder = Recorder(1024)
    recorder.start()

    def finish():
        recorder.stop()
        audio_segment = recorder.to_audio_segment()
        audio_segment.export(file, format='mp4', codec='aac')

    return finish
