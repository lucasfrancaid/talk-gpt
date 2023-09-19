from typing import Protocol

from talk_gpt.gpt.chat import Message


class ChatRepository(Protocol):
    def save(self, *, chat_id: str, messages: list[Message]) -> None:
        raise NotImplementedError

    def read(self, *, chat_id: str) -> list[Message]:
        raise NotImplementedError
