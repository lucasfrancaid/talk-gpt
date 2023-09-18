from enum import Enum


class TalkGPTCommandOptions(str, Enum):
    API = "api"
    CLI = "cli"
    AUDIO = "audio"
    VOICE = "voice"
