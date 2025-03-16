import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(os.getenv("LOGOSDB_CONNECTION_STRING"))
Session = sessionmaker(bind=engine)

def get_session():
    return Session()