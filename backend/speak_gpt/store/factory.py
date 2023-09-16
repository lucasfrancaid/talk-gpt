from speak_gpt.store.json_repository import JsonRepository
from speak_gpt.store.repository import Repository


class RepositoryFactory:
    @staticmethod
    def factory() -> Repository:
        return JsonRepository()
