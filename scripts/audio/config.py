import os
from typing import TypedDict
from config import getint, getparser


_SECTION = "audio"


class AudioConfig(TypedDict):
    input_index: None | int
    output_index: None | int


def getconfig() -> AudioConfig:
    """Read config file to extract audio config

    Returns:
        AudioConfig: A TypedDict of configuration values
    """
    parser = getparser()
    input_index = getint(parser, _SECTION, "input_index")
    output_index = getint(parser, _SECTION, "output_index")

    return AudioConfig(
        input_index=input_index,
        output_index=output_index)
