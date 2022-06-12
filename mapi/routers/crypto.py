from fastapi import APIRouter
from starlette.responses import HTMLResponse

from mapi import config, templates, wallets

router = APIRouter(prefix="/crypto", tags=["crypto"])


@router.get("/summary")
async def get_summary():
    wallets_ = wallets.get_wallets()
    html = templates.render_template(
        "crypto_summary.jinja2", wallets=wallets_, scheduled_buys=config.SCHEDULED_BUYS
    )
    return HTMLResponse(html)
