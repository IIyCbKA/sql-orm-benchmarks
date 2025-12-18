import asyncio
import time

import django
django.setup()

from core.models import Booking

async def main() -> None:
  start = time.time()

  try:
    book = await Booking.objects.afirst()
    if book:
      _ = [t async for t in book.tickets.all()]
  except Exception:
    pass

  end = time.time()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 7. Nested find first\n'
    f'elapsed_sec={elapsed:.4f};'
  )


if __name__ == '__main__':
  asyncio.run(main())
