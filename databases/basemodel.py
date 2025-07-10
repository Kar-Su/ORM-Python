from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from contextlib import contextmanager
load_dotenv()


HOST= os.getenv('HOST_DB')
PORT = os.getenv('PORT_DB')
USER = os.getenv('USER_DB')
PASSWORD = os.getenv('USER_DB_PASSWORD')
DATABASE = os.getenv('DATABASE_NAME')

DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(DATABASE_URL)
local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()

@contextmanager
def ConnectDB():
    db = local()
    try:
        yield db
    finally:
        db.close()
