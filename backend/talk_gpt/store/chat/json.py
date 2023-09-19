import json
from pathlib import Path
from typing import Final

from talk_gpt.config.settings import ROOT_DIR
from talk_gpt.gpt.chat import Message
from talk_gpt.store.chat.repository import ChatRepository


class ChatRepositoryJSON(ChatRepository):
    _STORE_FILENAME: Final[str] = f"{ROOT_DIR}/etc/_bkp/db_{{chat_id}}.json"

    def _initialize(self, chat_id: str) -> None:
        filename = Path(self._STORE_FILENAME.format(chat_id=chat_id))
        filename.touch(exist_ok=True)

    def save(self, *, chat_id: str, messages: list[Message]) -> None:
        self._initialize(chat_id=chat_id)
        with open(self._STORE_FILENAME.format(chat_id=chat_id), "w") as file:
            dict_messages = [message.dict() for message in messages]
            file.write(json.dumps(dict_messages))

    def read(self, *, chat_id: str) -> list[Message]:
        self._initialize(chat_id=chat_id)
        with open(self._STORE_FILENAME.format(chat_id=chat_id)) as file:
            if data_messages := file.read():
                data_messages = json.loads(data_messages)
            messages = [Message(**message) for message in data_messages or []]
            return messages
