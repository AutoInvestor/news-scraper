from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.logger import get_logger

logger = get_logger(__name__)


class HttpExceptionHandler:
    def __init__(self, app: FastAPI):
        self.app = app
        self._register_handlers()

    def _register_handlers(self):
        @self.app.exception_handler(Exception)
        async def internal_error(request: Request, exc: Exception):
            logger.warning("Internal server error for %s", exc)
            return JSONResponse(
                status_code=500, content={"detail": "Internal server error"}
            )
