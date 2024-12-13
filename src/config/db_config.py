from enum import StrEnum

from pydantic_settings import BaseSettings


class Dialect(StrEnum):
    postgresql: str = "postgresql"
    sqlite: str = "sqlite"


class Driver(StrEnum):
    asyncpg: str = "asyncpg"
    psycopg2: str = "psycopg2"
    aiosqlite: str = "aiosqlite"


class DatabaseConfig(BaseSettings):
    DATABASE_DIALECT: Dialect = Dialect.postgresql

    DATABASE_HOST: str = ""
    DATABASE_PORT: int = 5432
    DATABASE_USER: str = ""
    DATABASE_PASSWORD: str = ""
    DATABASE_NAME: str = ""

    DATABASE_ECHO: bool = False
    DATABASE_AUTO_FLUSH: bool = False
    DATABASE_AUTO_COMMIT: bool = False
    DATABASE_EXPIRE_ON_COMMIT: bool = False

    @property
    def GET_ASYNC_DB_URL(self) -> str:
        database_url = f"{database_config.DATABASE_DIALECT}+{Driver.asyncpg}://{database_config.DATABASE_USER}:{database_config.DATABASE_PASSWORD}@{database_config.DATABASE_HOST}:{database_config.DATABASE_PORT}/{database_config.DATABASE_NAME}"
        return database_url


database_config: DatabaseConfig = DatabaseConfig()
