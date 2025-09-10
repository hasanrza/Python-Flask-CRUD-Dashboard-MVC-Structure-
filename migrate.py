"""
Migration command script.
Run this to execute database migrations.
"""

from app.migrations.migration_manager import MigrationManager

if __name__ == "__main__":
    print("Running database migrations...")
    migration_manager = MigrationManager()
    migration_manager.run_migrations()
    print("Migrations completed!")
