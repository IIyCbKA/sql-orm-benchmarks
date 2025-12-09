import time

from tests_sync.db import SessionLocal
from core.models import Booking


def main() -> None:
    start = time.time()

    try:
        with SessionLocal() as session:
            book = session.query(Booking).first()
            _ = len(book.tickets)
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy. Test 7. Nested find first\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    main()
