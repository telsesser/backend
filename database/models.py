from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, SMALLINT, DECIMAL
from .config import Base, session_db


class data(Base):
    __tablename__ = "data"
    id = Column(INTEGER, primary_key=True)
    id_monitor = Column(INTEGER, ForeignKey("monitores.id"))
    rssi = Column(TINYINT)
    temperatura = Column(TINYINT)
    aperturas = Column(SMALLINT(unsigned=True))

    def get(id):
        return session_db.query(data).get(id)


class monitores(Base):
    __tablename__ = "monitores"
    id = Column(INTEGER, primary_key=True)
    monitor = Column(String(length=32))
    ultimo_dato = Column(DateTime)
    batery = Column(TINYINT)
    aperturas = Column(INTEGER(unsigned=True))
    id_gateway = Column(INTEGER, ForeignKey("broadcasters.id"))
    id_empresa = Column(INTEGER, ForeignKey("empresas.id"))


class gateways(Base):
    __tablename__ = "gateways"
    id = Column(INTEGER, primary_key=True)
    gateway = Column(String(length=64))


class users(Base):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    id_empresa = Column(INTEGER, ForeignKey("empresas.id"))


class empresas(Base):
    __tablename__ = "empresas"

    id = Column(INTEGER, primary_key=True, index=True)
    empresa = Column(String)
