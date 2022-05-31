import secrets

from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials
from starlette import status

from mapi.config import settings


def verify_is_admin(credentials: HTTPBasicCredentials):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, settings.admin_password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
