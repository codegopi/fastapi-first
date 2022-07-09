from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#include username, password, url and database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:maran.28@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

#to connect to database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#dependencies will open and close everytime we get a request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()