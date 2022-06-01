from typing import Optional

from datetime import date

import coinbase.wallet.error
from coinbase.wallet.client import Client as CoinbaseClient_

from mapi.config import Settings

PAGINATION_MAX_LIMIT = 300


class CoinbaseClient:
    def __init__(self, settings: Settings):
        self.client = CoinbaseClient_(settings.coinbase_api_key, settings.coinbase_api_secret)

    def get_wallet_transactions(self, wallet_id: str):
        return self.client.get_transactions(wallet_id, limit=PAGINATION_MAX_LIMIT).data

    def get_accounts(self):
        return self.client.get_accounts(limit=PAGINATION_MAX_LIMIT).data[2:]

    def get_spot_price(self, coin: str, date_: date = None) -> Optional[float]:
        kwargs = {"currency_pair": f"{coin}-USD"}
        if date_:
            kwargs["date"] = date_.strftime("%Y-%m-%d")

        try:
            return float(self.client.get_spot_price(**kwargs).amount)
        except (AttributeError, coinbase.wallet.error.NotFoundError):
            return None
