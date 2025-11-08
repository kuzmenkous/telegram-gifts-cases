from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic.networks import PostgresDsn
from pydantic_settings import BaseSettings

from src.core.pydantic_types import TimezoneInfo


class AppSettings(BaseSettings, env_prefix="app_"):
    name: str = "Telegram Gifts Cases API"
    version: int = 1
    secret_key: str
    domain: str = "localhost:8000"
    protocol: str = "http"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    @property
    def base_url(self) -> str:
        return f"{self.protocol}://{self.domain}"


class CorsSettings(BaseSettings, env_prefix="cors_"):
    origins: list[str]


class DatabaseSettings(BaseSettings, env_prefix="postgres_"):
    db: str
    user: str
    password: str
    host: str
    port: int

    @property
    def url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.db,
            )
        )


class JWTSettings(BaseSettings, env_prefix="jwt_"):
    algorithm: str
    access_token_expire: int
    refresh_token_expire: int


class Settings(BaseSettings):
    debug: bool
    timezone: TimezoneInfo

    # App
    app: AppSettings = Field(default_factory=AppSettings)
    # Cors
    cors: CorsSettings = Field(default_factory=CorsSettings)
    # Database
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    # JWT
    jwt: JWTSettings = Field(default_factory=JWTSettings)


@lru_cache
def get_settings() -> Settings:
    load_dotenv()
    return Settings()


settings: Settings = get_settings()
