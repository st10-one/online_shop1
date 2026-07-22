from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfigApp(BaseSettings):
    SECRET_JWT: str 

    DB_USER:str
    DB_PASSWORD:str
    DB_HOST:str
    DB_PORT:str
    DB_NAME:str

    model_config = SettingsConfigDict(env_file=".env")


settings = BaseConfigApp()


DB_URL = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

