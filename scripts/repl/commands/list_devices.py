from audio.devices import DeviceInfo, DeviceType, get_devices


def is_list_devices(input: str) -> bool:
    return input == 'devices'


def list_devices() -> str:
    return "\n".join([_device_to_str(d) for d in get_devices()])


def _device_to_str(device: DeviceInfo) -> str:
    is_default = "DEFAULT" if device.get('default') == True else ''
    if device.get('type') == DeviceType.INPUT:
        return f"INTPUT device ({device.get('device_index')}) '{device.get('name')}' {is_default}"
    elif device.get('type') == DeviceType.OUTPUT:
        return f"OUTPUT device ({device.get('device_index')}) '{device.get('name')}' {is_default}"
    else:
        return f"UNKNOWN device ({device.get('device_index')}) '{device.get('name')}'"
