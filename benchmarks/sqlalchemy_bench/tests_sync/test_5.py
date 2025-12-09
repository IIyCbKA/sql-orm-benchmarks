import time

from sqlalchemy import select
from tests_sync.db import SessionLocal
from core.models import Booking


def main() -> None:
    start = time.time()

    try:
        with SessionLocal() as session:
            _ = session.execute(select(Booking)).scalars().all()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy. Test 5. Find all\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    main()
