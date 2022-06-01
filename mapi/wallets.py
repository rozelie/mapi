from typing import Optional

from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import cached_property

from coinbase.wallet.client import Transaction

from mapi.external_clients import coinbase


@dataclass
class Wallet:
    id: str
    name: str
    balance: float
    transactions: list[Transaction]
    yesterday_spot_price: Optional[float] = None
    current_spot_price: Optional[float] = None

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


@dataclass
class Wallets:
    wallets: list[Wallet]

    def __iter__(self):
        yield from self.wallets

    @property
    def pnl(self) -> float:
        return sum(w.pnl for w in self.wallets)

    @property
    def balance(self) -> float:
        return sum(w.balance for w in self.wallets)


def get_wallets() -> Wallets:
    wallets = []
    coinbase_client = coinbase.CoinbaseClient()
    today = datetime.utcnow()
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
                    transactions=coinbase_client.get_wallet_transactions(wallet.id),
                )
            )

    return Wallets(wallets)
