"""
Database migrations for schema changes.
"""

import mysql.connector as connector
from config import AppConfig


def get_connection():
    """Get database connection for migrations."""
    config = {
        "host": AppConfig.DB_HOST,
        "user": AppConfig.DB_USER,
        "password": AppConfig.DB_PASSWORD,
        "database": AppConfig.DB_NAME,
    }
    return connector.connect(**config)


def create_users_table():
    """Create users table migration."""
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS `users` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(100) NOT NULL,
            `email` VARCHAR(255) NOT NULL UNIQUE,
            `password_hash` VARCHAR(255) NOT NULL,
            `image_path` VARCHAR(500) NULL,
            `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            INDEX `idx_email` (`email`),
            INDEX `idx_created_at` (`created_at`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    connection.commit()
    cursor.close()
    connection.close()


def add_image_path_column():
    """Add image_path column to users table if it doesn't exist."""
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Check if column exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'users' 
            AND COLUMN_NAME = 'image_path'
        """, (AppConfig.DB_NAME,))
        
        if cursor.fetchone()[0] == 0:
            cursor.execute("ALTER TABLE `users` ADD COLUMN `image_path` VARCHAR(500) NULL AFTER `password_hash`")
            connection.commit()
            print("Added image_path column to users table")
        else:
            print("image_path column already exists")
            
    except Exception as e:
        print(f"Error adding image_path column: {e}")
    finally:
        cursor.close()
        connection.close()


# Migration registry
MIGRATIONS = {
    "2025_01_05_000001_create_users_table": create_users_table,
    "2025_01_05_000002_add_image_path_to_users": add_image_path_column,
}
