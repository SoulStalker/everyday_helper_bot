from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    set_operday: DatabaseConfig


def load_config(path: str | None = None) -> Config:

    env: Env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
        ),
        db=DatabaseConfig(
            database=env('DB_URL'),
            # db_host=env('DB_HOST'),
            # db_user=env('DB_USER'),
            # db_password=env('DB_PASSWORD'),

        ),
        set_operday=DatabaseConfig(
            host=env('HOST'),
            database=env('DB_NAME'),
            user=env('USER'),
            password=env('PASSWORD'),
        )
    )