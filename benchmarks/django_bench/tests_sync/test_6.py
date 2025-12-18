import time

import django
django.setup()

from core.models import Booking

def main() -> None:
  start = time.time()

  try:
    _ = Booking.objects.first()
  except Exception:
    pass

  end = time.time()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 6. Find first\n'
    f'elapsed_sec={elapsed:.4f};'
  )


if __name__ == '__main__':
  main()
