import time

import django
django.setup()

from core.models import Booking

def main() -> None:
  start = time.time()

  try:
    _ = list(Booking.objects.all())
  except Exception:
    pass

  end = time.time()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 5. Find all\n'
    f'elapsed_sec={elapsed:.4f};'
  )


if __name__ == '__main__':
  main()
