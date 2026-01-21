from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    save_dir: str = "outputs/person_detector/"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

settings = Config()