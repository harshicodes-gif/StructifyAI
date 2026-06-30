import json
import sqlite3
from pathlib import Path
from typing import Any

from backend.utils.constants import DATABASE_PATH
from backend.utils.logger import get_logger

logger = get_logger(__name__)


def initialize_database() -> None:
    """Create SQLite database if it does not exist."""

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = _connect()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT,

            file_path TEXT,

            document_type TEXT,

            extracted_json TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );
        """)

    _ensure_column(cursor, "documents", "file_path", "TEXT")

    connection.commit()

    connection.close()

    logger.info("Database initialized.")


def save_document(
    filename: str,
    file_path: str | Path,
    structured_json: dict[str, Any],
) -> int:
    """Persist processed document metadata and structured extraction output."""

    initialize_database()

    document_type = _clean_text(structured_json.get("document_type"))
    extracted_json = json.dumps(structured_json, ensure_ascii=False)

    connection = _connect()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO documents (filename, file_path, document_type, extracted_json)
        VALUES (?, ?, ?, ?)
        """,
        (filename, str(file_path), document_type, extracted_json),
    )

    document_id = int(cursor.lastrowid)

    connection.commit()
    connection.close()

    return document_id


def list_documents() -> list[dict[str, Any]]:
    """Return processed documents, newest first."""

    initialize_database()

    connection = _connect()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, filename, file_path, document_type, extracted_json, created_at
        FROM documents
        ORDER BY datetime(created_at) DESC, id DESC
        """
    )

    documents = [_row_to_document(row) for row in cursor.fetchall()]

    connection.close()

    return documents


def get_document(document_id: int) -> dict[str, Any] | None:
    """Return one processed document by id."""

    initialize_database()

    connection = _connect()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, filename, file_path, document_type, extracted_json, created_at
        FROM documents
        WHERE id = ?
        """,
        (document_id,),
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return None

    return _row_to_document(row)


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE_PATH)


def _ensure_column(
    cursor: sqlite3.Cursor,
    table_name: str,
    column_name: str,
    column_type: str,
) -> None:
    cursor.execute(f"PRAGMA table_info({table_name})")
    existing_columns = {row[1] for row in cursor.fetchall()}

    if column_name not in existing_columns:
        cursor.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
        )


def _row_to_document(row: tuple[Any, ...]) -> dict[str, Any]:
    structured_json = _load_structured_json(row[4])

    return {
        "id": row[0],
        "filename": row[1] or "",
        "file_path": row[2] or "",
        "document_type": row[3] or _clean_text(structured_json.get("document_type")),
        "structured_json": structured_json,
        "created_at": row[5] or "",
    }


def _load_structured_json(value: str | None) -> dict[str, Any]:
    if not value:
        return {}

    try:
        loaded = json.loads(value)
    except json.JSONDecodeError:
        return {}

    if isinstance(loaded, dict):
        return loaded

    return {}


def _clean_text(value: Any) -> str:
    if value is None:
        return "Unknown"

    if isinstance(value, str):
        value = value.strip()
        return value if value else "Unknown"

    return str(value)
