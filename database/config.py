from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DB_IP = "192.168.5.20:3306"
# DB_USER = "server"
DB_USER = "tomas"
DB_IP = "89.117.33.152:3306"
DB_DB = "data"
DB_PSWRD = "Holatomi48."
engine = create_engine(
    f"mariadb+mariadbconnector://{DB_USER}:{DB_PSWRD}@{DB_IP}/{DB_DB}",
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_recycle=3600,
)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session_db = SessionLocal()
