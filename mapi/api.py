from datetime import datetime
from functools import lru_cache

from fastapi import Depends, FastAPI

from mapi import coinbase_api, tables, twilio_client
from mapi.config import Settings

app = FastAPI(docs_url="/")


@lru_cache()
def get_settings():
    return Settings()


@app.post("/twilio")
async def send_text_via_twilio(settings: Settings = Depends(get_settings)):
    message = _get_message(settings)
    _send_sms(message, settings=settings)
    return {"message": message}


def _get_message(settings: Settings):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wallets = coinbase_api.get_wallets(settings)
    message = "\n\n".join(
        [
            now,
            tables.get_portfolio(wallets),
            tables.get_daily_moves(wallets),
            tables.get_monthly_investments(),
        ]
    )
    print(message)
    return message


def _send_sms(message: str, settings: Settings) -> None:
    twilio_client.send_message(body=message, settings=settings)
