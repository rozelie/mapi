from datetime import datetime

from tabulate import tabulate

from mapi import config
from mapi.wallets import Wallets

TILE_FORMAT = "===============\n{name}\n==============="


def get_portfolio_text_message(wallets: Wallets) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = "\n\n".join(
        [
            now,
            _get_portfolio_table(wallets),
            _get_daily_moves_table(wallets),
            _get_monthly_investments_table(),
        ]
    )
    return message


def _get_portfolio_table(wallets: Wallets) -> str:
    total_balance_formatted = f"\nTotal Balance: ${wallets.balance:,.2f}"
    total_pnl_formatted = f"Total Pnl: ${wallets.pnl:,.2f}"
    portfolio = sorted(
        [[w.name, round(w.balance), round(w.cost_basis), round(w.pnl)] for w in wallets],
        key=lambda x: x[3],
        reverse=True,
    )
    portfolio_table = tabulate(portfolio, headers=["W", "B", "CB", "PnL"])
    return "\n".join(
        [
            TILE_FORMAT.format(name="Portfolio"),
            portfolio_table,
            total_balance_formatted,
            total_pnl_formatted,
        ]
    )


def _get_daily_moves_table(wallets: Wallets) -> str:
    daily_moves = sorted(
        [[w.name, round(w.daily_percentage_increase)] for w in wallets],
        key=lambda x: x[1],
        reverse=True,
    )
    daily_moves_table = tabulate(daily_moves, headers=["W", "Daily %"])
    return "\n".join(
        [
            TILE_FORMAT.format(name="Daily Change"),
            daily_moves_table,
        ]
    )


def _get_monthly_investments_table() -> str:
    rows = sorted(
        [[b.coin, round(b.per_month_usd)] for b in config.SCHEDULED_BUYS],
        key=lambda x: x[1],
        reverse=True,
    )
    table = tabulate(rows, headers=["C", "PerMonth"])
    total_monthly_investment_usd = sum(b.per_month_usd for b in config.SCHEDULED_BUYS)
    return "\n".join(
        [
            TILE_FORMAT.format(name="Monthly Investments"),
            table,
            f"\nTotal Monthly Investment: ${total_monthly_investment_usd:,.2f}",
        ]
    )
