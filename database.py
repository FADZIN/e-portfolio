import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Gantikan URL dengan yang anda dapat tadi, tetapi kita baiki bahagian SSL
# Kita gunakan certifi untuk dapatkan path sijil secara automatik
import certifi

# Masukkan pautan anda di sini
# Nota: Saya telah membuang bahagian <CA_PATH> dan menggantikannya dengan pembolehubah certifi
BASE_URL = "mysql+pymysql://HTMXbv8inEVYUPx.root:OkWgShAjYRS49S1p@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/test"

# Cantumkan dengan konfigurasi SSL yang betul
SQLALCHEMY_DATABASE_URL = f"{BASE_URL}?ssl_ca={certifi.where()}&ssl_verify_cert=true&ssl_verify_identity=true"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"ssl": {"ca": certifi.where()}}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
