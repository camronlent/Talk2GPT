from typing import Callable
from repl.commands import CommandType, to_command_type
from repl.commands.list_devices import list_devices
from repl.commands.record import start_recording, stop_recording
from audio.playback import play_mp3
from services.chatgpt import answer
from services.whisper import transcribe
from services.eleven import text_to_speach


def send_message(prompt: str) -> str:
    print(f"prompt: {prompt}")
    reply = answer(prompt)
    # reply = prompt
    print(f"reply: {reply}")

    # text-to-speach & play result
    text_to_speach(reply, "./.speech.mp3")
    play_mp3("./.speech.mp3")


def repl_main():
    print("Welcome to Talk2GPT!\n")

    # loop
    # _stop_recording: None | Callable[[], None] = None
    _cleanup_list: list[Callable[[], None]] = []
    try:
        while True:
            # read
            user_input = input("> ")
            command_type = to_command_type(user_input)

            # eval
            # TODO: handle commands better
            prompt = None
            if (command_type == CommandType.EXIT):
                break
            elif (command_type == CommandType.LIST_DEVICES):
                print(list_devices())
                continue
            elif (command_type == CommandType.RECORD):
                file = "./.recording.m4a"
                finish = start_recording(file)
                _cleanup_list.append(finish)
                input("recording...")
                _cleanup_list.remove(finish)
                stop_recording(finish)
                print("transcribing")
                prompt = transcribe(file).get("text")
            else:
                prompt = user_input

            # process prompt
            if (prompt != None):
                send_message(prompt)

    except KeyboardInterrupt as e:
        pass

    finally:
        for cleanup in _cleanup_list:
            cleanup()
        print("goodbye!")
