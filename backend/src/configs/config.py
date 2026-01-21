from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    save_dir: str = "outputs/person_detector/"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    postgres_host: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int = 5432

    postgresql_detection_results_table: str = "detection_results"

settings = Config()