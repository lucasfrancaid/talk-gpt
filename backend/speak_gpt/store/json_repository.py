import json
from datetime import datetime
from pathlib import Path
from typing import Final

from speak_gpt.config.settings import ROOT_DIR
from speak_gpt.gpt.chat import Message
from speak_gpt.store.repository import Repository


class JsonRepository(Repository):
    _STORE_FILENAME: Final[str] = f"{ROOT_DIR}/etc/_bkp/database_{datetime.now().strftime('%d%m%Y')}.json"

    def __init__(self) -> None:
        filename = Path(self._STORE_FILENAME)
        filename.touch(exist_ok=True)

    def save(self, *, messages: list[Message]) -> None:
        with open(self._STORE_FILENAME, "w") as file:
            dict_messages = [message.dict() for message in messages]
            file.write(json.dumps(dict_messages))

    def read(self) -> list[Message]:
        with open(self._STORE_FILENAME, "r") as file:
            if data_messages := file.read():
                data_messages = json.loads(data_messages)
            messages = [Message(**message) for message in data_messages or []]
            return messages
