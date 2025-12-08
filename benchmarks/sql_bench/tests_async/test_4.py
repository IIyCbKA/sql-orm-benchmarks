import asyncio
import time
from datetime import datetime, timedelta, UTC
from decimal import Decimal

from tests_async.db import get_connection

async def main() -> None:
    now = datetime.now(UTC)
    date_from = now - timedelta(days=30)
    amount_low = Decimal("50.00")
    amount_high = Decimal("500.00")

    start = time.time()

    try:
        conn = await get_connection()

        result = await conn.fetchval(
            """
            SELECT COUNT(*)
            FROM bookings.bookings
            WHERE total_amount BETWEEN $1 AND $2
              AND book_date >= $3
            """,
            amount_low,
            amount_high,
            date_from,
        )

        await conn.close()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'Pure async SQL (asyncpg). Test 4. Filter large\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    asyncio.run(main())
