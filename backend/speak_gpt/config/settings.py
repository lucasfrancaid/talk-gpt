from pathlib import Path
from typing import Any

import openai
from pydantic import BaseSettings, validator

APP_DIR = Path(__file__).parent.parent
ROOT_DIR = APP_DIR.parent


class Settings(BaseSettings):
    def __init__(self, env_file: str | None = None) -> None:
        super().__init__(_env_file=env_file)

    APP_NAME: str = "Speak GPT"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = True
    GPT_MODEL: str = "gpt-3.5-turbo"
    OPENAI_API_KEY: str = ""
    OPENAI_ORGANIZATION: str = ""

    class Config:
        case_sensitive = True

    @validator('OPENAI_API_KEY')
    def openai_api_key(cls, key: str, values: dict[str, Any]) -> str:
        openai.api_key = key
        return key

    @validator('OPENAI_ORGANIZATION')
    def openai_organization(cls, org: str, values: dict[str, Any]) -> str:
        openai.organization = org
        return org


settings = Settings()
