import asyncio
import time
from sqlalchemy import select
from tests_async.db import AsyncSessionLocal
from core.models import Booking

async def main() -> None:
    start = time.time()

    try:
        async with AsyncSessionLocal() as session:
            result = await session.scalars(select(Booking))
            bookings = result.all()

            for b in bookings:
                _ = b.book_ref
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy Async. Test 5. Find all (materialized)\n'
        f'elapsed_sec={elapsed:.4f};'
    )

if __name__ == "__main__":
    asyncio.run(main())
