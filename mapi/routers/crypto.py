from fastapi import APIRouter
from starlette.responses import HTMLResponse

from mapi import templates, wallets

router = APIRouter(prefix="/crypto", tags=["crypto"])


@router.get("/summary")
async def get_summary():
    wallets_ = wallets.get_wallets(from_cache=True)
    html = templates.render_template("crypto_summary.jinja2", wallets=wallets_)
    return HTMLResponse(html)
