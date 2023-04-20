import openai
from typing import Literal, TypedDict, Tuple
from config import getparser, getstr


_OPENAPI_SECTION = "openai"
_AGENT_SECTION = "agent"


class PromptInfo(TypedDict):
    role: Literal["user", "system", "assistant"]
    content: str


def _get_api_key() -> str:
    return getstr(getparser(), _OPENAPI_SECTION, "api_key")


def _get_names() -> Tuple[str, str]:
    parser = getparser()
    return (
        getstr(parser, _AGENT_SECTION, "agent_name"),
        getstr(parser, _AGENT_SECTION, "user_name"))


def _system_prompt() -> PromptInfo:
    (agent_name, user_name) = _get_names()
    return PromptInfo(role="system",
                      content=' '.join([
                          f"You are {agent_name}, a large language model trained by OpenAI.",
                          "Answer as concisely as possible.",
                          "Try to keep responses under 128 tokens."
                          f"Refer to user as {user_name}.",
                      ]))


_HISTORY: list[PromptInfo] = [
    _system_prompt()
]


def answer(prompt: str) -> str:
    _HISTORY.append(PromptInfo(role="user", content=prompt))

    api_key = _get_api_key()

    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # model="gpt-4",
        max_tokens=256,
        messages=_HISTORY,
        api_key=api_key
    )

    message = result['choices'][0]['message']

    _HISTORY.append(PromptInfo(
        role=message["role"],
        content=message["content"]))

    return message['content']
