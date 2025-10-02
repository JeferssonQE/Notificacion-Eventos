from sqlalchemy import Column, Integer, String, Date, Time, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Evento(Base):
    __tablename__ = "eventos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    numero = Column(String)  
    nombre = Column(String, nullable=False)
    title = Column(String)
    body = Column(String)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class RecordatorioDolar(Base):
    __tablename__ = "recordatorios_dolar"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    numero = Column(String)
    nombre = Column(String, nullable=False)        # {{1}}
    movimiento = Column(String, nullable=False)    # {{2}} #[subio, bajo]
    porcentaje = Column(Float, nullable=False)    # {{3}} # 10.0
    valor = Column(String, nullable=False)         # {{4}}
    #fecha = Column(String, nullable=False)         # {{5}}
    created_at = Column(DateTime, default=datetime.utcnow)


class Dolar(Base):
    __tablename__ = "dolar"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    origen = Column(String, nullable=False)        # Ej: SBS, BCRP
    fecha = Column(Date, nullable=False)
    precio_venta = Column(Float, nullable=False)
    precio_compra = Column(Float, nullable=False)
    scraped_at = Column(DateTime, default=datetime.utcnow)
