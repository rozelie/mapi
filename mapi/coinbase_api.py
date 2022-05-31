"""
https://docs.cloud.coinbase.com/sign-in-with-coinbase/docs/api-transactions
https://github.com/coinbase/coinbase-python/blob/master/coinbase/wallet/client.py
https://medium.com/@samhagin/check-your-balance-on-coinbase-using-python-5641ff769f91
"""
from typing import Optional

from dataclasses import dataclass
from datetime import date, timedelta
from functools import cached_property

import coinbase.wallet.error
from coinbase.wallet.client import Client as CoinbaseClient_
from coinbase.wallet.client import Transaction

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


@dataclass
class Wallet:
    id: str
    name: str
    balance: float
    settings: Settings
    coinbase_client: CoinbaseClient
    yesterday_spot_price: Optional[float] = None
    current_spot_price: Optional[float] = None

    @cached_property
    def transactions(self) -> list[Transaction]:
        return self.coinbase_client.get_wallet_transactions(self.id)

    @cached_property
    def earned_transactions(self) -> list[Transaction]:
        return [
            t
            for t in self.transactions
            if t.type in {"buy", "advanced_trade_fill", "Coinbase Earn", "fiat_deposit"}
        ]

    @cached_property
    def sells(self) -> list[Transaction]:
        return [t for t in self.transactions if t.type == "sell"]

    @cached_property
    def cost_basis(self) -> float:
        return sum([float(t.native_amount.amount) for t in self.earned_transactions]) - sum(
            [float(t.native_amount.amount) for t in self.sells]
        )

    @cached_property
    def pnl(self) -> float:
        return self.balance - self.cost_basis

    @cached_property
    def daily_percentage_increase(self) -> float:
        if not self.current_spot_price or not self.yesterday_spot_price:
            return 0
        daily_difference = self.current_spot_price - self.yesterday_spot_price
        return daily_difference / self.current_spot_price * 100


def get_wallets(settings: Settings) -> list[Wallet]:
    wallets = []
    coinbase_client = CoinbaseClient(settings)
    today = date.today()
    yesterday = today - timedelta(days=1)
    for wallet in coinbase_client.get_accounts():
        if balance := float(wallet.native_balance.amount):
            wallets.append(
                Wallet(
                    id=wallet.id,
                    name=wallet.currency,
                    balance=balance,
                    yesterday_spot_price=coinbase_client.get_spot_price(wallet.currency, yesterday),
                    current_spot_price=coinbase_client.get_spot_price(wallet.currency),
                    settings=settings,
                    coinbase_client=coinbase_client,
                )
            )

    return wallets
