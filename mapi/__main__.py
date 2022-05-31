import uvicorn

from mapi.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=80,
        reload=True if settings.is_local else False,
        debug=True if settings.is_local else False,
        workers=1 if settings.is_local else 4,
    )
