import asyncio
import os
import time
from sqlalchemy import select
from tests_async.db import AsyncSessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


async def main() -> None:
    start = time.time()

    try:
        async with AsyncSessionLocal() as session:
            for i in range(COUNT):
                stmt = select(Booking).where(Booking.book_ref == generate_book_ref(i))
                result = await session.scalars(stmt)
                booking = result.first()
                if booking:
                    await session.delete(booking)
            await session.commit()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy Async. Test 14. Batch delete. {COUNT} entries\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == "__main__":
    asyncio.run(main())
