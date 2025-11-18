from sqlalchemy.orm import Session
from app.db.core.database import SessionLocal
from typing import Generator


def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager para manejo seguro de sesiones de base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db_session_manual() -> Session:
    """
    Obtiene una sesión manual (recordar cerrarla).
    """
    return SessionLocal()


class DatabaseManager:
    """
    Clase para manejo avanzado de transacciones de base de datos.
    """

    def __init__(self):
        self.db = None

    def __enter__(self):
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db.rollback()
        else:
            self.db.commit()
        self.db.close()
