import asyncio
import time

import django
django.setup()

from core.models import Booking

async def main() -> None:
  start = time.time()

  try:
    _ = [b async for b in Booking.objects.all()]
  except Exception:
    pass

  end = time.time()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 5. Find all\n'
    f'elapsed_sec={elapsed:.4f};'
  )


if __name__ == '__main__':
  asyncio.run(main())
