import asyncio
from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time

from tests_async.db import AsyncSessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


async def main() -> None:
    start = time.time()

    for i in range(COUNT):
        try:
            async with AsyncSessionLocal() as session:
                item = Booking(
                    book_ref=generate_book_ref(i),
                    book_date=get_curr_date(),
                    total_amount=generate_amount(i),
                )
                session.add(item)
                await session.commit()
        except Exception:
            pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy Async. Test 1. Single create. {COUNT} entities\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == "__main__":
    asyncio.run(main())
