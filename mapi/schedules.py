import logging
import time

import schedule
from funcy import log_calls

from mapi import wallets

logger = logging.getLogger(__name__)


@log_calls(logger.info)
def _poll_and_cache_wallets() -> None:
    wallets.get_wallets(from_cache=False)


@log_calls(logger.info)
def start_scheduler():
    schedule.every(30).minutes.do(_poll_and_cache_wallets)
    while True:
        schedule.run_pending()
        time.sleep(1)
