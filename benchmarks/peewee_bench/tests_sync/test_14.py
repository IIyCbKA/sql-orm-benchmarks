from core.models import Booking
from core.database import db
import os
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'c{i:05d}'


def main() -> None:
  with db.connection_context():
    try:
      refs = [generate_book_ref(i) for i in range(COUNT)]
    except Exception as e:
      print(f'[ERROR] Test 14 failed (data preparation): {e}')
      sys.exit(1)

    start = time.perf_counter_ns()

    try:
      Booking.delete().where(Booking.book_ref.in_(refs)).execute()
    except Exception as e:
      print(f'[ERROR] Test 14 failed (delete phase): {e}')
      sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
      f'Peewee ORM (sync). Test 14. Bulk delete. {COUNT} entities\n'
      f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
  main()
