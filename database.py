import os
import certifi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Render akan secara automatik ambil nilai DATABASE_URL yang anda set tadi
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Jika anda mahu test secara lokal, anda boleh letak pautan backup di sini
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:pass@localhost/e_portfolio"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"ssl": {"ca": certifi.where()}}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

