from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time
from sqlalchemy import select

from tests_sync.db import SessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def get_new_amount(i: int) -> Decimal:
    return Decimal(i + 100) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


def main() -> None:
    start = time.time()

    try:
        for i in range(COUNT):
            with SessionLocal() as session:
                booking = session.scalars(
                    select(Booking).where(Booking.book_ref == generate_book_ref(i))
                ).first()

                if booking:
                    booking.total_amount = get_new_amount(i)
                    booking.book_date = get_curr_date()

                session.commit()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy. Test 12. Single update. {COUNT} entries\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    main()
