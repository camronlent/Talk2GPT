from repl.commands.exit import is_exit
from repl.commands.record import is_record
from repl.commands.list_devices import is_list_devices
from enum import Enum


class CommandType(Enum):
    MESSAGE = "message",
    EXIT = "exit",
    RECORD = "record",
    LIST_DEVICES = "list_devices",


def to_command_type(input: str) -> CommandType:
    lower = input.strip().lower()

    if (is_record(input)):
        return CommandType.RECORD

    if (is_exit(lower)):
        return CommandType.EXIT

    if (is_list_devices(lower)):
        return CommandType.LIST_DEVICES

    return CommandType.MESSAGE
