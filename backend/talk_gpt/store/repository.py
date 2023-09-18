from typing import Protocol

from talk_gpt.gpt.chat import Message


class Repository(Protocol):
    def save(self, *, messages: list[Message]) -> None:
        raise NotImplementedError

    def read(self) -> list[Message]:
        raise NotImplementedError
