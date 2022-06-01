from fastapi import APIRouter
from starlette.responses import HTMLResponse

from mapi import jinja, scheduled_buys, wallets

router = APIRouter(prefix="/crypto", tags=["crypto"])


@router.get("/summary")
async def get_summary():
    wallets_ = wallets.get_wallets()
    html = jinja.render_template(
        "crypto_summary.jinja2", wallets=wallets_, scheduled_buys=scheduled_buys.SCHEDULED_BUYS
    )
    return HTMLResponse(html)
