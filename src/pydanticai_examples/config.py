import os
from functools import lru_cache

from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(os.getenv("DOTENV_FILE", ".env")),
        extra="ignore",
    )

class QdrantConfig(BaseConfig):
    qdrant_url: str
    qdrant_port: int
    qdrant_index_name: str

class OpenAIConfig(BaseConfig):
    openai_api_key: str

class TodoistConfig(BaseConfig):
    todoist_api_key: str
    todoist_project: str


@lru_cache
def get_qdrant_config():
    return QdrantConfig()


@lru_cache
def get_openai_config():
    return OpenAIConfig()

@lru_cache
def get_todoist_config():
    return TodoistConfig()

