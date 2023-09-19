from talk_gpt.store.chat.json import ChatRepositoryJSON
from talk_gpt.store.chat.repository import ChatRepository


class ChatRepositoryFactory:
    @staticmethod
    def factory() -> ChatRepository:
        return ChatRepositoryJSON()
