import asyncio
import time
from sqlalchemy import select
from tests_async.db import AsyncSessionLocal
from core.models import Booking


async def main() -> None:
    start = time.time()

    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Booking).limit(1))
            _ = result.scalars().first()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy Async. Test 6. Find first\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == "__main__":
    asyncio.run(main())
