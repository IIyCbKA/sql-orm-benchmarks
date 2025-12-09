import asyncio
import time
from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
from tests_async.db import AsyncSessionLocal
from core.models import Booking
import os
from sqlalchemy import select

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def get_new_amount(i: int) -> Decimal:
    return Decimal(i + 100) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


async def main() -> None:
    start = time.time()

    try:
        async with AsyncSessionLocal() as session:
            for i in range(COUNT):
                stmt = select(Booking).where(Booking.book_ref == generate_book_ref(i))
                result = await session.execute(stmt)
                booking = result.first()
                if booking:
                    obj = booking[0]
                    obj.total_amount = get_new_amount(i)
                    obj.book_date = get_curr_date()
            await session.commit()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy Async. Test 11. Batch update. {COUNT} entries\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == "__main__":
    asyncio.run(main())
