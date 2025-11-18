# crea_tablas.py
from app.db.database import engine, Base
from app.db.models import *

print("Creando tablas...")
Base.metadata.create_all(bind=engine)
print("Tablas creadas")
