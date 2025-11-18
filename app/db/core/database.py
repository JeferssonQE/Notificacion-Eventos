from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Motor de la BD
# engine = create_engine(settings.database_url, echo=True)
# Supabase
engine = create_engine(
    "postgresql://postgres:1htfHV5dyNw6YBaM@db.talzmqegmmrilxypoztr.supabase.co:5432/postgres",
    echo=True,
)
print("url:", settings.supabase_database_url)

# Sesión (cada request obtiene su propia)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para heredar en modelos
Base = declarative_base()


def get_db():
    """
    Dependency para obtener una sesión de base de datos.
    Se usa con FastAPI Depends() para inyección de dependencias.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Crea todas las tablas definidas en los modelos.
    """
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """
    Elimina todas las tablas (usar con precaución).
    """
    Base.metadata.drop_all(bind=engine)
