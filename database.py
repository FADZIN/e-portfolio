import certifi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Gunakan Connection String TiDB anda di sini
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://HTMXbv8inEVYUPx.root:OkWgShAjYRS49S1p@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/test?ssl_ca=" + certifi.where()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"ssl": {"ca": certifi.where()}}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

