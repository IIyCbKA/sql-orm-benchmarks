from decimal import Decimal
import asyncio
import os
import time

import django
django.setup()

from asgiref.sync import sync_to_async
from core.models import Booking
from django.db import transaction

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


@sync_to_async
def update_nested_sync():
  try:
    with transaction.atomic():
      for i in range(COUNT):
        booking = Booking.objects.filter(book_ref=generate_book_ref(i)).first()
        if booking:
          booking.total_amount += Decimal('10.00')
          booking.save(update_fields=['total_amount'])
          for ticket in booking.tickets.all():
            ticket.passenger_name = 'Nested update'
            ticket.save(update_fields=['passenger_name'])
  except Exception:
    pass


async def main() -> None:
  start = time.perf_counter_ns()

  try:
    await update_nested_sync()
  except Exception:
    pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 13. Nested batch update. {COUNT} entries\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  asyncio.run(main())