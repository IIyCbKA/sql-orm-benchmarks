from decimal import Decimal
import os

import django
django.setup()

from core.models import Booking, Ticket
from django.utils import timezone

COUNT = int(os.environ.get('WARMUP_ITERATIONS', '20'))


def warm_up() -> None:
  for i in range(COUNT):
    b = Booking(
      book_ref=f'warm{i:02d}',
      book_date=timezone.now(),
      total_amount=Decimal('5.00')
    )

    t = Ticket(
      ticket_no=f'warm{i:09d}',
      book_ref=b,
      passenger_id=f'warm{i:05d}',
      passenger_name='Warm',
      outbound=True
    )

    _ = Booking.objects.get(book_ref=f'warm{i:02d}')
    __ = Ticket.objects.get(ticket_no=f'warm{i:09d}')

    b.total_amount = Decimal('2.00')
    b.save(update_fields=['total_amount'])

    t.passenger_name = 'WarmUpdate'
    t.save(update_fields=['passenger_name'])

    b.delete()
    t.delete()

  print('Warm-uo done')


if __name__ == '__main__':
  warm_up()
