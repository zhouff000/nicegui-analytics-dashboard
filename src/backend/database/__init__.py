# src/backend/database/__init__.py
"""
Database operations module.
Provides SQLite database management functionality.
"""

from .sqlite import DatabaseManager, db_manager

__all__ = [
    "DatabaseManager",
    "db_manager",
]
