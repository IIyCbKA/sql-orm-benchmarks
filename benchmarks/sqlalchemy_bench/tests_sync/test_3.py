from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time

from sqlalchemy import insert
from tests_sync.db import SessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'c{i:05d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


def main() -> None:
    start = time.time()

    rows = []
    curr_date = get_curr_date()

    for i in range(COUNT):
        rows.append({
            "book_ref": generate_book_ref(i),
            "book_date": curr_date,
            "total_amount": generate_amount(i),
        })

    try:
        with SessionLocal() as session:
            session.execute(
                insert(Booking),
                rows,
            )
            session.commit()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy. Test 3. Bulk create. {COUNT} entities\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    main()
