from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    title : str
    version : str
    descrption : str

    jwt_access_time : int
    jwt_algorithm : str
    jwt_secret_key : str

    redis_url : str | None
    db_url : str | None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

@lru_cache(1024)
async def get_settings() :
    return Settings()