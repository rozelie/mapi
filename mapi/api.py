from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.responses import FileResponse, HTMLResponse, JSONResponse

import mapi.routers.crypto
import mapi.routers.twilio
from mapi import auth

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    dependencies=[Depends(auth.verify_is_admin)],
)
for router in [
    mapi.routers.twilio.router,
    mapi.routers.crypto.router,
]:
    app.include_router(router)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(Path(__file__).parent.parent / "assets" / "favicon.ico")


@app.get("/", include_in_schema=False)
async def index():
    # @TODO: add github source code link
    return HTMLResponse("hi")


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api():
    return JSONResponse(get_openapi(title="FastAPI", version=str(1), routes=app.routes))


@app.get("/docs", include_in_schema=False)
async def get_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
