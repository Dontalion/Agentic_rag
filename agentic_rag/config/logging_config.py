"""
Centralized Logging Configuration for Agentic RAG.

All modules should use `get_logger(__name__)` to obtain a logger instance.
Logging is configured once here — format, level, and handlers are managed centrally.

Usage:
    from agentic_rag.config.logging_config import get_logger

    logger = get_logger(__name__)
    logger.info("Something happened")
    logger.warning("Something might be wrong")
    logger.error("Something went wrong", exc_info=True)

Custom per-module logging:
    logger = get_logger(__name__, level="DEBUG")  # Override level for this module
"""
import logging
import sys
from typing import Optional

# ──────────────────────────────────────────────
# Central configuration — change here once
# ──────────────────────────────────────────────
DEFAULT_LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Track whether logging has been configured
_configured = False


def _configure_logging(level: str = DEFAULT_LOG_LEVEL) -> None:
    """
    Configure the root logger with format, level, and handlers.
    Called automatically on first use of `get_logger()`.
    """
    global _configured
    if _configured:
        return

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, level.upper(), logging.INFO))

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    handler.setFormatter(formatter)

    root.addHandler(handler)
    _configured = True


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance for the given module name.

    Args:
        name: Usually `__name__` of the calling module.
        level: Optional override for this specific logger (e.g. "DEBUG").

    Returns:
        A configured logging.Logger instance.
    """
    _configure_logging()

    logger = logging.getLogger(name)
    if level:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    return logger


def set_global_level(level: str) -> None:
    """
    Change the global logging level at runtime.

    Args:
        level: One of "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL".
    """
    logging.getLogger().setLevel(getattr(logging, level.upper(), logging.INFO))
    for handler in logging.getLogger().handlers:
        handler.setLevel(getattr(logging, level.upper(), logging.INFO))
