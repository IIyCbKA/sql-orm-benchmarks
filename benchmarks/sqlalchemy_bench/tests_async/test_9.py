import asyncio
import time
from sqlalchemy import select
from tests_async.db import AsyncSessionLocal
from core.models import Booking


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


async def main() -> None:
    start = time.time()

    try:
        async with AsyncSessionLocal() as session:
            stmt = select(Booking).where(Booking.book_ref == generate_book_ref(1))
            result = await session.scalars(stmt)
            book = result.one_or_none()

            if book:
                await book.tickets
                _ = len(book.tickets)
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy Async. Test 9. Nested find unique\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == "__main__":
    asyncio.run(main())
