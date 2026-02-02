from pydantic_settings import BaseSettings , SettingsConfigDict


class BaseSettings (BaseSettings):






	model_config = SettingsConfigDict(env_file='.env')