import sqlite3
import os
from pathlib import Path
from typing import Optional, Dict
from app.logger import get_logger

logger = get_logger()

# Database path
DB_DIR = Path(__file__).parent.parent / 'data'
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / 'document_mappings.db'

def init_db():
    """Initialize the database and create tables if they don't exist"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create document_mappings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_mappings (
                document_name TEXT PRIMARY KEY,
                original_filename TEXT NOT NULL,
                file_id TEXT,
                store_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {DB_PATH}")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}", exc_info=True)
        raise

def save_mapping(document_name: str, original_filename: str, file_id: Optional[str] = None, store_name: Optional[str] = None) -> bool:
    """
    Save document name to original filename mapping

    Args:
        document_name: Full document name (e.g., 'fileSearchStores/xxx/documents/yyy')
        original_filename: Original file name
        file_id: Optional file ID from Files API
        store_name: Optional store name

    Returns:
        True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO document_mappings
            (document_name, original_filename, file_id, store_name)
            VALUES (?, ?, ?, ?)
        ''', (document_name, original_filename, file_id, store_name))

        conn.commit()
        conn.close()
        logger.info(f"Saved mapping: {document_name} -> {original_filename}")
        return True
    except Exception as e:
        logger.error(f"Error saving mapping: {str(e)}", exc_info=True)
        return False

def get_mapping(document_name: str) -> Optional[str]:
    """
    Get original filename for a document name

    Args:
        document_name: Full document name

    Returns:
        Original filename if found, None otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT original_filename FROM document_mappings
            WHERE document_name = ?
        ''', (document_name,))

        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        return None
    except Exception as e:
        logger.error(f"Error getting mapping: {str(e)}", exc_info=True)
        return None

def delete_mapping(document_name: str) -> bool:
    """
    Delete mapping for a document

    Args:
        document_name: Full document name

    Returns:
        True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM document_mappings
            WHERE document_name = ?
        ''', (document_name,))

        conn.commit()
        conn.close()
        logger.info(f"Deleted mapping: {document_name}")
        return True
    except Exception as e:
        logger.error(f"Error deleting mapping: {str(e)}", exc_info=True)
        return False

def get_all_mappings() -> Dict[str, str]:
    """
    Get all document mappings

    Returns:
        Dictionary of document_name -> original_filename
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('SELECT document_name, original_filename FROM document_mappings')
        results = cursor.fetchall()
        conn.close()

        return {doc_name: filename for doc_name, filename in results}
    except Exception as e:
        logger.error(f"Error getting all mappings: {str(e)}", exc_info=True)
        return {}

# Initialize database on module import
init_db()
