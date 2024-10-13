import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

load_dotenv()

uri = os.getenv("LOGOSDB_CONNECTION_STRING")
engine = create_engine(uri)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()