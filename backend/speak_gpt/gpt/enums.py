from enum import Enum


class SpeakGPTCommandOptions(str, Enum):
    API = "api"
    CLI = "cli"
    AUDIO = "audio"
    VOICE = "voice"
