from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/routes")


@router.get("/ping", response_class=PlainTextResponse)
def health_check() -> str:
    """Simple health check endpoint used for the route app."""
    return "pong"
