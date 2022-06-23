from typing import Optional

import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from pydantic import BaseSettings

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


class Env(Enum):
    LOCAL = "local"
    PROD = "prod"


class Settings(BaseSettings):
    env: Env = Env.LOCAL
    wallets_pickle_path: Path = Path().absolute() / "wallets.pickle"
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
