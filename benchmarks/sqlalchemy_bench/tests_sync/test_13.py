from decimal import Decimal
import os
import time
from sqlalchemy import select

from tests_sync.db import SessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def main() -> None:
    start = time.time()

    try:
        with SessionLocal() as session:
            for i in range(COUNT):
                booking = session.scalars(
                    select(Booking).where(Booking.book_ref == generate_book_ref(i))
                ).first()

                if booking:
                    booking.total_amount += Decimal('10.00')

                    for ticket in booking.tickets:
                        ticket.passenger_name = 'Nested update'

            session.commit()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy. Test 13. Nested batch update. {COUNT} entries\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    main()
