from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time

from tests_sync.db import SessionLocal
from core.models import Booking, Ticket

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'd{i:05d}'


def generate_ticket_no(i: int) -> str:
    return f'98{i:11d}'


def generate_passenger_id(i: int) -> str:
    return f'p{i:08d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


def main() -> None:
    start = time.time()

    try:
        with SessionLocal() as session:
            for i in range(COUNT):
                booking = Booking(
                    book_ref=generate_book_ref(i),
                    book_date=get_curr_date(),
                    total_amount=generate_amount(i),
                )

                ticket = Ticket(
                    ticket_no=generate_ticket_no(i),
                    passenger_id=generate_passenger_id(i),
                    passenger_name="Test",
                    outbound=True,
                )

                # связь как у PonyORM
                ticket.book_ref = booking

                session.add(booking)
                session.add(ticket)

            session.commit()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy. Test 4. Nested create. {COUNT} entities\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    main()
