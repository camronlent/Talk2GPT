from pyaudio import PyAudio
from typing import Dict, TypedDict
from enum import Enum
from audio.config import getconfig


class DeviceType(Enum):
    INPUT = "in",
    OUTPUT = "out",
    UNKNOWN = "unknown"


class DeviceInfo(TypedDict):
    default: bool
    host_index: int
    device_index: int
    type: DeviceType
    name: str


def get_devices() -> list[DeviceInfo]:
    """Get a list of device info for the audio devices on the host.

    Returns:
        list[DeviceInfo]: The list of device information.
    """
    p = PyAudio()
    host_info = _get_host_api_info(p, 0)
    info_by_device_index = _generate_info_by_host_api_device_index(p, 0)
    numdevices = host_info.get('deviceCount')
    defaults = [host_info.get('defaultInputDevice'),
                host_info.get('defaultOutputDevice')]

    return [_to_device_info(info_by_device_index(i), defaults) for i in range(0, numdevices)]


def get_input_device_info() -> DeviceInfo:
    """Get the default or configured input device info

    Returns:
        DeviceInfo: The device info for the selected device
    """
    config = getconfig()
    devices = [device for device in get_devices() if device.get('type')
               == DeviceType.INPUT]
    return _get_device_or_default(devices, config.get('input_index'))


def get_output_device_info() -> DeviceInfo:
    """Get the default or configured output device

    Returns:
        DeviceInfo: The device info for the selected device
    """
    config = getconfig()
    devices = [device for device in get_devices() if device.get('type')
               == DeviceType.OUTPUT]
    return _get_device_or_default(devices, config.get('output_index'))


def _to_device_type(info: Dict) -> DeviceType:
    if info.get('maxInputChannels') > 0:
        return DeviceType.INPUT
    elif info.get('maxOutputChannels') > 0:
        return DeviceType.OUTPUT
    else:
        return DeviceType.UNKNOWN


def _to_device_info(info: Dict, defaults: list[int]) -> DeviceInfo:
    device_index = info.get('index')
    return DeviceInfo(
        default=device_index in defaults,
        host_index=info.get('hostApi'),
        device_index=device_index,
        type=_to_device_type(info),
        name=info.get('name')
    )


def _generate_info_by_host_api_device_index(p: PyAudio, host_index: int):
    def device_info_by_index(device_index: int) -> Dict[str, str | int | float]:
        return p.get_device_info_by_host_api_device_index(host_index, device_index)
    return device_info_by_index


def _get_host_api_info(p: PyAudio, i: int) -> Dict:
    return p.get_host_api_info_by_index(i)


def _get_device_or_default(devices: list[DeviceInfo], index: None | int) -> DeviceInfo:
    default_device = None
    for device in devices:
        if device.get('device_index') == index:
            return device
        if (device.get('default')) == True:
            default_device = device
    return default_device
