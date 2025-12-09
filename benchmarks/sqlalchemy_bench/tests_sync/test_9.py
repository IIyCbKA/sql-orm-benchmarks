import time
from sqlalchemy import select

from tests_sync.db import SessionLocal
from core.models import Booking


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def main() -> None:
    start = time.time()

    try:
        with SessionLocal() as session:
            stmt = select(Booking).where(Booking.book_ref == generate_book_ref(1))
            book = session.scalars(stmt).one_or_none()

            if book:
                _ = len(book.tickets)
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy. Test 9. Nested find unique\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    main()
