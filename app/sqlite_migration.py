import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, make_transient
from object_models.sqlalchemy_models import Verse, Book, Translation, TranslationBook
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection
postgres_uri = os.getenv("LOGOSDB_CONNECTION_STRING")
postgres_engine = create_engine(postgres_uri)
PostgresSession = sessionmaker(bind=postgres_engine)
postgres_session = PostgresSession()

# SQLite connection
sqlite_uri = os.getenv("SQLITE_CONNECTION_STRING")
sqlite_engine = create_engine(sqlite_uri)
SQLiteSession = sessionmaker(bind=sqlite_engine)
sqlite_session = SQLiteSession()

# Create tables in SQLite
Verse.metadata.create_all(sqlite_engine)
Book.metadata.create_all(sqlite_engine)
Translation.metadata.create_all(sqlite_engine)
TranslationBook.metadata.create_all(sqlite_engine)

def migrate_table(table_class):
    records = postgres_session.query(table_class).all()
    for record in records:
        postgres_session.expunge(record)  # Detach the object from the PostgreSQL session
        make_transient(record)  # Make the object transient
        sqlite_session.merge(record)
    sqlite_session.commit()

def main():
    migrate_table(Verse)
    migrate_table(Book)
    migrate_table(Translation)
    migrate_table(TranslationBook)
    print("Migration completed successfully.")

if __name__ == "__main__":
    main()