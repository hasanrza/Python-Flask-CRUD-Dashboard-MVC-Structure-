"""
Migration system for database schema management.
"""

from .migration_manager import MigrationManager
from .migrations import create_users_table, add_image_path_column

__all__ = ['MigrationManager', 'create_users_table', 'add_image_path_column']
