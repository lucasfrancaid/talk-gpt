from talk_gpt.store.json_repository import JsonRepository
from talk_gpt.store.repository import Repository


class RepositoryFactory:
    @staticmethod
    def factory() -> Repository:
        return JsonRepository()
