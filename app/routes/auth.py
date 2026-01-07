from fastapi import APIRouter, HTTPException, status

from ..auth import create_access_token
from ..logging_config import configure_logging
from ..schemas import LoginRequest, TokenResponse
from ..settings import settings


router = APIRouter(prefix="", tags=["auth"])
logger = configure_logging("api-backend")


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    if body.username != settings.demo_username or body.password != settings.demo_password:
        logger.info("/login failed", extra={"username": body.username})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(body.username)
    logger.info("/login success", extra={"username": body.username})
    return TokenResponse(access_token=access_token)
