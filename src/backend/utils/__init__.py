# src/backend/utils/__init__.py
"""
Utility functions and classes.
Provides OCR functionality and other helper tools.
"""

from .paddle_ocr import PaddleOCR, call_ocr

__all__ = [
    "PaddleOCR",
    "call_ocr",
]
