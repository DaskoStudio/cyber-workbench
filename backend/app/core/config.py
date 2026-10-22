from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CW_")
    app_name: str = "Cyber Workbench"
    environment: str = "development"


settings = Settings()
