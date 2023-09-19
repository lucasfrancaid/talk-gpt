from enum import Enum


class CommandOption(str, Enum):
    API = "api"
    CLI = "cli"
    AUDIO = "cli.audio"
    VOICE = "cli.voice"


class PromptOption(str, Enum):
    GPT = "gpt"
    ENGLISH_TEACHER = "english_teacher"
