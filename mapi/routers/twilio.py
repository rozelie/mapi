from fastapi import APIRouter

from mapi import text_messages, wallets
from mapi.external_clients import twilio

router = APIRouter(prefix="/twilio", tags=["twilio"])


@router.post("/send_portfolio_test")
async def send_portfolio_test():
    wallets_ = wallets.get_wallets()
    message = text_messages.get_portfolio_text_message(wallets_)
    twilio.send_message(body=message)
    return {"message": message}
