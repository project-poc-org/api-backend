from fastapi import APIRouter

from ..logging_config import configure_logging
from ..settings import settings


router = APIRouter()
logger = configure_logging("api-backend")


@router.get("/health")
def health_check():
    logger.info("/health called")
    return {"status": "ok"}


@router.get("/version")
def version():
    logger.info("/version called", extra={"version": settings.api_version})
    return {"version": settings.api_version}
