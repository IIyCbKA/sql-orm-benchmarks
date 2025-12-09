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
                    session.delete(booking)

            session.commit()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy. Test 14. Batch delete. {COUNT} entries\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    main()
