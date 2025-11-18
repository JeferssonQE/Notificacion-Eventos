# Database module - Main entry point
from app.db.core.database import (
    engine,
    SessionLocal,
    Base,
    get_db,
    create_tables,
    drop_tables,
)
from app.db.core.session import get_db_session, get_db_session_manual, DatabaseManager
from app.db.models import Evento, RecordatorioDolar, Dolar

# Re-export everything for backward compatibility
__all__ = [
    "engine",
    "SessionLocal",
    "Base",
    "get_db",
    "create_tables",
    "drop_tables",
    "get_db_session",
    "get_db_session_manual",
    "DatabaseManager",
    "Evento",
    "RecordatorioDolar",
    "Dolar",
]
