import logging
import sys
from typing import Any, Dict

from loguru import logger

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logging() -> None:
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                "level": "INFO",
            }
        ]
    )

def log_request(request_id: str, method: str, path: str, status_code: int, duration: float) -> None:
    logger.info(
        "Request processed",
        extra={
            "request_id": request_id,
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration": duration,
        }
    )

def log_error(request_id: str, error: Exception, context: Dict[str, Any] = None) -> None:
    logger.error(
        "Error occurred",
        extra={
            "request_id": request_id,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {},
        }
    ) 