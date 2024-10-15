from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, join
import asyncio
import bible
from bible import Verse, Book

# Create an asynchronous engine
engine = create_async_engine("postgresql+asyncpg://anthropos:humanity@localhost:5432/logosdb")
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def load_verse_text(reference: bible.BibleReference, session: AsyncSession):
    try:
        # Fetch the verse based on the reference
        statement = (
            select(Verse)
            .join(Book, Verse.book_id == Book.id)
            .where(
                Book.name == reference.book,
                Verse.chapter == reference.chapter,
                Verse.verse == reference.verse
            )
        )
        result = await session.execute(statement)
        verse_record = result.scalar_one_or_none()

        if verse_record is None:
            raise ValueError("Verse not found in the database.")
        
        await verse_record.fetch_text(session)
        print(verse_record.text)  # Now it should return the fetched text
    except ValueError as e:
        print(f"Error: {e}")

async def main():
    async with AsyncSessionLocal() as session:
        reference = bible.BibleReference(book="Bereshit", chapter=1, verse=1)
        await load_verse_text(reference, session)

# Run the main function
asyncio.run(main())