import asyncio
import os
import time
from datetime import datetime, UTC
from decimal import Decimal

import asyncpg
from tests_async.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'b{i:05d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal("10.00")


async def main() -> None:
    start = time.time()

    try:
        conn = await get_connection()

        async with conn.transaction():
            for i in range(COUNT):
                await conn.execute(
                    """
                    INSERT INTO bookings.bookings (book_ref, book_date, total_amount)
                    VALUES ($1, $2, $3)
                    """,
                    generate_book_ref(i),
                    datetime.now(UTC),
                    generate_amount(i),
                )

        await conn.close()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'Pure async SQL (asyncpg). Test 2. Transaction insert\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == "__main__":
    asyncio.run(main())
