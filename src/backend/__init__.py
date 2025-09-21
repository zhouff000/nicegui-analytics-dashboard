# src/backend/__init__.py
"""
Backend module for zh-llm project.
Provides core functionality including character comprehension, database operations, and utilities.
"""

from .core import llm_character_response
from .database import DatabaseManager, db_manager
from .utils import PaddleOCR, call_ocr

__version__ = "0.1.0"

__all__ = [
    # Core functionality
    "llm_character_response",
    # Database
    "DatabaseManager",
    "db_manager",
    # Utils
    "PaddleOCR",
    "call_ocr",
]
