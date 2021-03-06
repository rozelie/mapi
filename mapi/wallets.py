from typing import Optional

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import cached_property

import pytz
from coinbase.wallet.client import Transaction
from funcy import log_durations

from mapi import persistence
from mapi.config import settings
from mapi.external_clients import coinbase

logger = logging.getLogger(__name__)


@dataclass
class Wallet:
    id: str
    name: str
    balance: float
    transactions: list[Transaction]
    yesterday_spot_price: Optional[float] = None
    one_hour_ago_spot_price: Optional[float] = None
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
    def percentage_gain(self) -> float:
        try:
            return (self.balance - self.cost_basis) / self.cost_basis * 100
        except ZeroDivisionError:
            return 0.0

    @cached_property
    def daily_percentage_increase(self) -> float:
        return _get_percentage_increase(self.current_spot_price, self.yesterday_spot_price)

    @cached_property
    def one_hour_percentage_increase(self) -> float:
        return _get_percentage_increase(self.current_spot_price, self.one_hour_ago_spot_price)


@dataclass
class Wallets:
    wallets: list[Wallet]

    def __post_init__(self):
        self.last_updated = datetime.now(tz=pytz.timezone("US/Central"))

    def __iter__(self):
        yield from self.wallets

    @property
    def pnl(self) -> float:
        return sum(w.pnl for w in self.wallets)

    @property
    def balance(self) -> float:
        return sum(w.balance for w in self.wallets)


@log_durations(logger.info)
def get_wallets(from_cache: bool) -> Wallets:
    if from_cache:
        try:
            return persistence.load_pickle(settings.wallets_pickle_path)
        except FileNotFoundError:
            logger.info(
                f"File not found at {settings.wallets_pickle_path} - will reload wallet data"
            )
            pass

    wallets = []
    coinbase_client = coinbase.CoinbaseClient()
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    one_hour_ago = today - timedelta(hours=1)
    for wallet in coinbase_client.get_accounts():
        if balance := float(wallet.native_balance.amount):
            wallets.append(
                Wallet(
                    id=wallet.id,
                    name=wallet.currency,
                    balance=balance,
                    yesterday_spot_price=coinbase_client.get_spot_price(wallet.currency, yesterday),
                    one_hour_ago_spot_price=coinbase_client.get_spot_price(
                        wallet.currency, one_hour_ago
                    ),
                    current_spot_price=coinbase_client.get_spot_price(wallet.currency),
                    transactions=coinbase_client.get_wallet_transactions(wallet.id),
                )
            )

    wallets = Wallets(wallets)
    persistence.persist_to_pickle(settings.wallets_pickle_path, wallets)
    return wallets


def _get_percentage_increase(current: float, past: float) -> float:
    if not current or not past:
        return 0.0
    difference = current - past
    return difference / current * 100
