from typing import Optional

from dataclasses import dataclass
from enum import Enum

from pydantic import BaseSettings


class Env(Enum):
    LOCAL = "local"
    PROD = "prod"


class Settings(BaseSettings):
    env: Env = Env.LOCAL
    admin_password: Optional[str] = None
    secret_key: Optional[str] = None
    port: int = 8000

    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_virtual_phone_number: Optional[str] = None
    twilio_my_phone_number: Optional[str] = None

    coinbase_api_key: Optional[str] = None
    coinbase_api_secret: Optional[str] = None

    class Config:
        env_file = "../.env"

    @property
    def is_prod(self) -> bool:
        return self.env == Env.PROD

    @property
    def is_local(self) -> bool:
        return self.env == Env.LOCAL


settings = Settings()


@dataclass
class ScheduledBuy:
    coin: str
    per_day_usd: float

    @property
    def per_month_usd(self) -> float:
        return self.per_day_usd * 30


SCHEDULED_BUYS = [
    ScheduledBuy("DOT", 50 / 7),
    ScheduledBuy("BTC", 20 / 7),
    ScheduledBuy("SOL", 20 / 7),
    ScheduledBuy("ETH", 20 / 7),
]
