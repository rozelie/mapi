from dataclasses import dataclass


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
