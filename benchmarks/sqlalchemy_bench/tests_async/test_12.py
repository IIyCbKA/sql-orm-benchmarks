import asyncio
import time
from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
from sqlalchemy import select
from tests_async.db import AsyncSessionLocal
from core.models import Booking
import os

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
            stmt = select(Booking).where(Booking.book_ref.in_([generate_book_ref(i) for i in range(COUNT)]))
            result = await session.scalars(stmt)
            bookings = result.all()

            for i, booking in enumerate(bookings):
                booking.total_amount = get_new_amount(i)
                booking.book_date = get_curr_date()

            await session.commit()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy Async. Test 12. Single update. {COUNT} entries\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == "__main__":
    asyncio.run(main())
