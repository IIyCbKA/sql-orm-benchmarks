from core.models import Booking
from core.database import db
import os
import statistics
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def main() -> None:
  with db.connection_context():
    try:
      refs = [generate_book_ref(i) for i in range(COUNT)]
      bookings = list(Booking.select().where(Booking.book_ref.in_(refs)))
    except Exception as e:
      print(f'[ERROR] Test 12 failed (data preparation): {e}')
      sys.exit(1)

    results: list[int] = []

    try:
      for booking in bookings:
        start = time.perf_counter_ns()

        booking.delete_instance()

        end = time.perf_counter_ns()
        results.append(end - start)
    except Exception as e:
      print(f'[ERROR] Test 12 failed (delete phase): {e}')
      sys.exit(1)

    elapsed = statistics.median(results)

    print(
      f'Peewee ORM (sync). Test 12. Single delete. {COUNT} entities\n'
      f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
  main()
