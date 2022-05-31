from datetime import datetime
from functools import lru_cache

from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import JSONResponse, HTMLResponse

from mapi import auth, coinbase_api, tables, twilio_client
from mapi.config import Settings

app = FastAPI(docs_url="/", redoc_url=None, openapi_url=None)
security = HTTPBasic()


@lru_cache()
def get_settings():
    return Settings()


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api(credentials: HTTPBasicCredentials = Depends(security), ):
    auth.verify_is_admin(credentials)
    return JSONResponse(get_openapi(title="FastAPI", version=str(1), routes=app.routes))


@app.get("/", include_in_schema=False)
async def get_docs(
    credentials: HTTPBasicCredentials = Depends(security),
    settings: Settings = Depends(get_settings),
):
    auth.verify_is_admin(credentials)
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/crypto/summary")
async def crypto_summary(
    credentials: HTTPBasicCredentials = Depends(security),
    settings: Settings = Depends(get_settings),
):
    auth.verify_is_admin(credentials)
    message = _get_message(settings)
    return HTMLResponse(f"<code>{message}</code>")


@app.post("/twilio")
async def send_text_via_twilio(
    credentials: HTTPBasicCredentials = Depends(security),
    settings: Settings = Depends(get_settings),
):
    auth.verify_is_admin(credentials)
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
