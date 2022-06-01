from tabulate import tabulate

from mapi import scheduled_buys
from mapi.wallets import Wallets

TILE_FORMAT = "===============\n{name}\n==============="


def get_portfolio(wallets: Wallets, tablefmt: str = "simple") -> str:
    total_balance_formatted = f"\nTotal Balance: ${wallets.balance:,.2f}"
    total_pnl_formatted = f"Total Pnl: ${wallets.pnl:,.2f}"
    portfolio = sorted(
        [[w.name, round(w.balance), round(w.cost_basis), round(w.pnl)] for w in wallets],
        key=lambda x: x[3],
        reverse=True,
    )
    portfolio_table = tabulate(portfolio, headers=["W", "B", "CB", "PnL"], tablefmt=tablefmt)
    return "\n".join(
        [
            TILE_FORMAT.format(name="Portfolio"),
            portfolio_table,
            total_balance_formatted,
            total_pnl_formatted,
        ]
    )


def get_daily_moves(wallets: Wallets, tablefmt: str = "simple") -> str:
    daily_moves = sorted(
        [[w.name, round(w.daily_percentage_increase)] for w in wallets],
        key=lambda x: x[1],
        reverse=True,
    )
    daily_moves_table = tabulate(daily_moves, headers=["W", "Daily %"], tablefmt=tablefmt)
    return "\n".join(
        [
            TILE_FORMAT.format(name="Daily Change"),
            daily_moves_table,
        ]
    )


def get_monthly_investments(tablefmt: str = "simple") -> str:
    rows = sorted(
        [[b.coin, round(b.per_month_usd)] for b in scheduled_buys.SCHEDULED_BUYS],
        key=lambda x: x[1],
        reverse=True,
    )
    table = tabulate(rows, headers=["C", "PerMonth"], tablefmt=tablefmt)
    total_monthly_investment_usd = sum(b.per_month_usd for b in scheduled_buys.SCHEDULED_BUYS)
    return "\n".join(
        [
            TILE_FORMAT.format(name="Monthly Investments"),
            table,
            f"\nTotal Monthly Investment: ${total_monthly_investment_usd:,.2f}",
        ]
    )
