from typing import Callable
from audio.recording import record_m4a


def is_record(input: str) -> bool:
    return input == ''


def start_recording(file: str) -> Callable[[], None]:
    return record_m4a(file)


def stop_recording(finish: Callable[[], None]) -> None:
    return finish()
