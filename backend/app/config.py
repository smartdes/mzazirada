from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    AT_USERNAME: str = "sandbox"
    AT_API_KEY: str = ""
    AT_SHORTCODE: str = "*384*73355#"
    WEBHOOK_SECRET: str = "change_me_to_a_secure_random_string"

    model_config = SettingsConfigDict(
        env_file=(".env", "backend/.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
