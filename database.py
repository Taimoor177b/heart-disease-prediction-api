# database file
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

url = "sqlite:///./heart_disease.db"

engine = create_engine(url,connect_args={"check_same_thread":False})
session_Local = sessionmaker(bind=engine,autocommit=False)
base = declarative_base()

def get_db():
    db=session_Local()
    try:
        yield db
    finally:
        db.close()
