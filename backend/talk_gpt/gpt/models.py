from enum import Enum

from pydantic import BaseModel

from talk_gpt.config.settings import settings


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    role: Role = Role.USER
    content: str

    def role_to_str(self) -> str:
        match self.role:
            case Role.USER:
                return settings.USER_NAME
            case Role.ASSISTANT:
                return settings.AI_ASSISTANT_NAME
            case Role.SYSTEM:
                return Role.SYSTEM.value
