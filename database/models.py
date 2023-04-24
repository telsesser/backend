from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, SMALLINT, DECIMAL
from sqlalchemy.orm import relationship
from .config import Base, session_db

# relaciones:
# https://vegibit.com/sqlalchemy-orm-relationships-one-to-many-many-to-one-many-to-many/


class data(Base):
    __tablename__ = "data"
    id = Column(INTEGER, primary_key=True)
    id_monitor = Column(INTEGER, ForeignKey("monitores.id"))
    rssi = Column(TINYINT)
    temperatura = Column(TINYINT)
    aperturas = Column(SMALLINT(unsigned=True))

    # Relaciones
    monitor = relationship("monitores", back_populates="data")

    # funciones
    def get(id):
        return session_db.query(data).get(id)


class monitores(Base):
    __tablename__ = "monitores"
    id = Column(INTEGER, primary_key=True)
    name = Column(String(length=32))

    # datos dinamicos
    ultimo_dato = Column(DateTime)
    bateria = Column(TINYINT)
    aperturas = Column(INTEGER(unsigned=True))
    rssi = Column(TINYINT)

    # datos identificación
    id_gateway = Column(INTEGER, ForeignKey("gateways.id"))
    id_heladera = Column(INTEGER, ForeignKey("heladeras.id"))
    id_empresa = Column(INTEGER, ForeignKey("empresas.id"))

    # relaciones
    data = relationship("data", back_populates="monitor")
    gateway = relationship("gateways", back_populates="monitores")
    heladera = relationship("heladeras", back_populates="monitor")
    empresa = relationship("empresas", back_populates="monitores")


class heladeras(Base):
    __tablename__ = "heladeras"
    id = Column(INTEGER, primary_key=True)
    id_empresa = Column(INTEGER, ForeignKey("empresas.id"))

    name = Column(String(length=64))
    temp_min = Column(TINYINT)
    temp_max = Column(TINYINT)
    modelo_heladera = Column(String(length=32))
    antiguedad = Column(TINYINT)
    ubicacion = Column(String(length=32))
    categoria = Column(String(length=32))
    ploteo = Column(String(length=32))

    # relaciones
    empresa = relationship("empresas", back_populates="heladeras")
    monitor = relationship("monitores", back_populates="heladera")


class gateways(Base):
    __tablename__ = "gateways"
    id = Column(INTEGER, primary_key=True)
    name = Column(String(length=64))
    id_sucursal = Column(INTEGER, ForeignKey("sucursales.id"))

    # relaciones
    monitores = relationship("monitores", back_populates="gateway")
    sucursal = relationship("sucursales", back_populates="gateways")


class users(Base):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True, index=True)
    email = Column(String(length=254), unique=True, index=True)
    hashed_password = Column(String(length=64))
    is_active = Column(Boolean, default=True)
    id_empresa = Column(INTEGER, ForeignKey("empresas.id"))


class empresas(Base):
    __tablename__ = "empresas"

    id = Column(INTEGER, primary_key=True, index=True)
    name = Column(String(length=64))

    # relaciones
    sucursales = relationship("sucursales", back_populates="empresa")
    heladeras = relationship("heladeras", back_populates="empresa")
    monitores = relationship("monitores", back_populates="empresa")


class sucursales(Base):
    __tablename__ = "sucursales"

    id = Column(INTEGER, primary_key=True, index=True)
    name = Column(String(length=64))
    id_empresa = Column(INTEGER, ForeignKey("empresas.id"))
    tipo_local = Column(String(length=32))
    canal = Column(String(length=32))
    provincia = Column(String(length=32))
    direccion = Column(String(length=32))
    # coordenadas = agregar después
    barrio = Column(String(length=32))

    # relaciones
    gateways = relationship("gateways", back_populates="sucursal")
    empresa = relationship("empresas", back_populates="sucursales")
