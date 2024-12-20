from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str = "secret key"
    algorithm: str = "HS256"

    mail_username: str = "example@meta.ua"
    mail_password: SecretStr = ""
    mail_from: str = "example@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.meta.ua"

    model_config = SettingsConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")

settings = Settings()
