"""
Configuration values for the application.

Edit these values to match your local MySQL setup. For production, load
these from environment variables or a secure secrets manager.
"""


class AppConfig:
    """Flask and database configuration container."""

    # Flask secret key for session and flash messages
    SECRET_KEY = "change-this-secret-key"

    # Database connection settings
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "pythondb"


