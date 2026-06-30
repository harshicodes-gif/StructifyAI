import sqlite3

from backend.utils.constants import DATABASE_PATH
from backend.utils.logger import get_logger

logger = get_logger(__name__)


def initialize_database() -> None:
    """Create SQLite database if it does not exist."""

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT,

            document_type TEXT,

            extracted_json TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );
        """
    )

    connection.commit()

    connection.close()

    logger.info("Database initialized.")
