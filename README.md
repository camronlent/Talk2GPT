# Talk2GPT

This project uses APIs from OpenAI and ElevenLabs to allow you to talk directly
to ChatGPT

## Configuration

Before you can run the project, you will need to have an API key from both OpenAI and ElevenLabs.
The configuration itself is stored in a file called config.ini, to create this file.

1. Rename `config.ini.example` to `config.ini`
1. Update the `api_key` values in the `openai` and `elevenlabs` section.

## Setup

Required Libraries:

```bash
$ pip install -r requirements.txt
```

## Run

```bash
$ python scripts/main.py
```

## Commands

### Exit
You use the `exit` command to exit the application.

```
> exit
```

### List Devices
The `devices` command is for situations when you need to play or record from a specific audio device.

```
> devices
```

To identify the index for audio devices on the system run this command.
Then modify the `[audio]` configuration within the `config.ini` file to reflect the appropriate index-to-device configuration.

### Transcribe Voice
Simply press enter and begin speaking, then press enter again when you are finished. This will transcribe your voice and send it into ChatGPT.

```
> 
recording...
```

### Chat

This is the normal chat behavior, simply type your message directly.

```
> How do you make a cappuccino?
```
