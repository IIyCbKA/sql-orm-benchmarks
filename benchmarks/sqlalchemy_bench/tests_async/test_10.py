import asyncio
import time
from datetime import datetime, timedelta, UTC
from decimal import Decimal
from sqlalchemy import select, asc
from tests_async.db import AsyncSessionLocal
from core.models import Booking
import os

LIMIT = int(os.environ.get('LIMIT', '250'))
OFFSET = int(os.environ.get('OFFSET', '500'))


async def main() -> None:
    now = datetime.now(UTC)
    date_from = now - timedelta(days=30)
    amount_low = Decimal('50.00')
    amount_high = Decimal('500.00')
    start = time.time()

    try:
        async with AsyncSessionLocal() as session:
            stmt = (
                select(Booking)
                .where(
                    Booking.total_amount.between(amount_low, amount_high),
                    Booking.book_date >= date_from
                )
                .order_by(asc(Booking.total_amount))
                .limit(LIMIT)
                .offset(OFFSET)
            )

            result = await session.scalars(stmt)
            results = result.all()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy Async. Test 10. Filter, paginate & sort\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == "__main__":
    asyncio.run(main())
