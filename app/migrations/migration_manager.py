"""
Migration Manager for handling database schema changes.
"""

import os
import mysql.connector as connector
from mysql.connector import errorcode
from config import AppConfig


class MigrationManager:
    """Manages database migrations and schema changes."""
    
    def __init__(self):
        self.config = {
            "host": AppConfig.DB_HOST,
            "user": AppConfig.DB_USER,
            "password": AppConfig.DB_PASSWORD,
            "database": AppConfig.DB_NAME,
        }
        self.migrations_table = "migrations"
    
    def get_connection(self):
        """Get database connection."""
        try:
            connection = connector.connect(**self.config)
            return connection
        except connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                raise RuntimeError("Database does not exist and could not be created.") from err
            raise
    
    def ensure_database_exists(self):
        """Create the database if it does not exist."""
        config_without_db = {
            "host": self.config["host"],
            "user": self.config["user"],
            "password": self.config["password"],
        }
        
        connection = connector.connect(**config_without_db)
        cursor = connection.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{self.config['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        )
        cursor.close()
        connection.close()
    
    def create_migrations_table(self):
        """Create migrations tracking table."""
        connection = self.get_connection()
        cursor = connection.cursor()
        
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS `{self.migrations_table}` (
                `id` INT NOT NULL AUTO_INCREMENT,
                `migration` VARCHAR(255) NOT NULL UNIQUE,
                `batch` INT NOT NULL,
                `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
    
    def get_ran_migrations(self):
        """Get list of already run migrations."""
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute(f"SELECT migration FROM `{self.migrations_table}` ORDER BY id")
            migrations = [row[0] for row in cursor.fetchall()]
            return migrations
        except connector.Error:
            return []
        finally:
            cursor.close()
            connection.close()
    
    def record_migration(self, migration_name, batch):
        """Record a migration as run."""
        connection = self.get_connection()
        cursor = connection.cursor()
        
        cursor.execute(
            f"INSERT INTO `{self.migrations_table}` (migration, batch) VALUES (%s, %s)",
            (migration_name, batch)
        )
        
        connection.commit()
        cursor.close()
        connection.close()
    
    def get_next_batch(self):
        """Get the next batch number."""
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute(f"SELECT MAX(batch) FROM `{self.migrations_table}`")
            result = cursor.fetchone()
            return (result[0] or 0) + 1
        except connector.Error:
            return 1
        finally:
            cursor.close()
            connection.close()
    
    def run_migrations(self):
        """Run all pending migrations."""
        self.ensure_database_exists()
        self.create_migrations_table()
        
        # Import migrations
        from .migrations import MIGRATIONS
        
        ran_migrations = self.get_ran_migrations()
        batch = self.get_next_batch()
        
        for migration_name, migration_func in MIGRATIONS.items():
            if migration_name not in ran_migrations:
                print(f"Running migration: {migration_name}")
                migration_func()
                self.record_migration(migration_name, batch)
                print(f"✓ {migration_name} completed")
        
        print("All migrations completed!")
