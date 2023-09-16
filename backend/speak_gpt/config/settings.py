from pathlib import Path

from pydantic import BaseSettings

APP_DIR = Path(__file__).parent.parent
ROOT_DIR = APP_DIR.parent


class Settings(BaseSettings):
    APP_NAME: str = "Speak GPT"
    GPT_MODEL: str = "gpt-3.5-turbo"
    OPENAI_KEY: str = ""
    OPENAI_ORG: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
