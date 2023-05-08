from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, SMALLINT, DECIMAL, BIGINT
from sqlalchemy.orm import relationship
from .config import Base, session_db

# relaciones:
# https://vegibit.com/sqlalchemy-orm-relationships-one-to-many-many-to-one-many-to-many/


class data(Base):
    __tablename__ = "data"
    id = Column(INTEGER, primary_key=True)
    id_monitor = Column(INTEGER, ForeignKey("monitors.id"))
    rssi = Column(TINYINT)
    temp = Column(DECIMAL(4, 2))
    openings = Column(SMALLINT(unsigned=True))
    timestmp = Column(DateTime)

    # Relaciones
    monitor = relationship("monitors", back_populates="data")

    # funciones
    def get(id):
        return session_db.query(data).get(id)


class monitors(Base):
    __tablename__ = "monitors"
    id = Column(INTEGER, primary_key=True)
    mac_address = Column(BIGINT(unsigned=True))
    name = Column(String(length=32))

    # datos dinamicos
    last_data = Column(DateTime)
    batery = Column(TINYINT)
    openings = Column(INTEGER(unsigned=True))
    rssi = Column(TINYINT)

    # datos identificación
    id_gateway = Column(INTEGER, ForeignKey("gateways.id"))
    id_refrigerator = Column(INTEGER, ForeignKey("refrigerators.id"))
    id_company = Column(INTEGER, ForeignKey("companies.id"))

    # relaciones
    data = relationship("data", back_populates="monitor")
    gateway = relationship("gateways", back_populates="monitors")
    refrigerator = relationship("refrigerators", back_populates="monitor")
    company = relationship("companies", back_populates="monitors")


class refrigerators(Base):
    __tablename__ = "refrigerators"
    id = Column(INTEGER, primary_key=True)
    id_company = Column(INTEGER, ForeignKey("companies.id"))

    name = Column(String(length=64))
    temp_min = Column(TINYINT)
    temp_max = Column(TINYINT)
    refrigerator_model = Column(String(length=32))
    age = Column(TINYINT)
    ubication = Column(String(length=32))
    category = Column(String(length=32))
    plotting = Column(String(length=32))

    # relaciones
    company = relationship("companies", back_populates="refrigerators")
    monitor = relationship("monitors", back_populates="refrigerator")


class gateways(Base):
    __tablename__ = "gateways"
    id = Column(INTEGER, primary_key=True)
    name = Column(String(length=64))
    id_branch = Column(INTEGER, ForeignKey("branches.id"))

    # relaciones
    monitors = relationship("monitors", back_populates="gateway")
    branch = relationship("branches", back_populates="gateways")


class users(Base):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True, index=True)
    email = Column(String(length=254), unique=True, index=True)
    hashed_password = Column(String(length=64))
    is_active = Column(Boolean, default=True)
    id_company = Column(INTEGER, ForeignKey("companies.id"))


class companies(Base):
    __tablename__ = "companies"

    id = Column(INTEGER, primary_key=True, index=True)
    name = Column(String(length=64))

    # relaciones
    branches = relationship("branches", back_populates="company")
    refrigerators = relationship("refrigerators", back_populates="company")
    monitors = relationship("monitors", back_populates="company")


class branches(Base):
    __tablename__ = "branches"

    id = Column(INTEGER, primary_key=True, index=True)
    name = Column(String(length=64))
    id_company = Column(INTEGER, ForeignKey("companies.id"))
    local_type = Column(String(length=32))
    canal = Column(String(length=32))
    provincia = Column(String(length=32))
    address = Column(String(length=32))
    # coordenadas = agregar después
    neighborhood = Column(String(length=32))

    # relaciones
    gateways = relationship("gateways", back_populates="branch")
    company = relationship("companies", back_populates="branches")
