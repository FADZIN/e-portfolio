from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Format: mysql+pymysql://username:password@localhost:3306/db_name
# Use an empty password if you haven't set one: "root:@"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/e_portfolio"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()