from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic.networks import AmqpDsn, PostgresDsn
from pydantic_settings import BaseSettings

from src.core.pydantic_types import TimezoneInfo


class AppSettings(BaseSettings, env_prefix="app_"):
    name: str = "Telegram Gifts Cases API"
    version: int = 1
    session_token_expire: int
    secret_key: str
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"


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


class TelegramSettings(BaseSettings, env_prefix="telegram_"):
    api_id: int
    api_hash: str
    bot_token: str
    client_session: str
    init_data_expire: int


class RabbitSettings(BaseSettings, env_prefix="rabbitmq_"):
    user: str
    password: str
    host: str

    @property
    def url(self) -> str:
        return str(
            AmqpDsn.build(
                scheme="amqp",
                username=self.user,
                password=self.password,
                host=self.host,
            )
        )


class PortalsAPISettings(BaseSettings, env_prefix="portals_api_"):
    url: str


class Settings(BaseSettings):
    debug: bool
    timezone: TimezoneInfo

    # App
    app: AppSettings = Field(default_factory=AppSettings)
    # Cors
    cors: CorsSettings = Field(default_factory=CorsSettings)
    # Database
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    # Telegram
    telegram: TelegramSettings = Field(default_factory=TelegramSettings)
    # RabbitMQ
    rabbit: RabbitSettings = Field(default_factory=RabbitSettings)
    # Portals API
    portals_api: PortalsAPISettings = Field(default_factory=PortalsAPISettings)


@lru_cache
def get_settings() -> Settings:
    load_dotenv()
    return Settings()


settings: Settings = get_settings()
