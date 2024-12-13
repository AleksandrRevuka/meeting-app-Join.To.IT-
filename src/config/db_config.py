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
    DATABASE_DIALECT: Dialect = Dialect.sqlite

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
        if self.DATABASE_DIALECT == Dialect.sqlite:
            database_url = (
                f"{self.DATABASE_DIALECT}+{Driver.aiosqlite}:///{self.DATABASE_NAME}"
            )
        else:
            database_url = (
                f"{self.DATABASE_DIALECT}+{Driver.asyncpg}://"
                f"{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@"
                f"{self.DATABASE_HOST}:{self.DATABASE_PORT}/"
                f"{self.DATABASE_NAME}"
            )
        return database_url


database_config: DatabaseConfig = DatabaseConfig()
