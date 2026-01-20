from database import db
from peewee import (
  Model, CharField, DateTimeField, DecimalField,
  TextField, BooleanField, ForeignKeyField
)

class BaseModel(Model):
  class Meta:
    database = db
    schema = 'bookings'


class Booking(BaseModel):
  book_ref = CharField(primary_key=True, max_length=6)
  book_date = DateTimeField()
  total_amount = DecimalField(max_digits=10, decimal_places=2)

  class Meta:
    table_name = 'bookings'


class Ticket(BaseModel):
  ticket_no = CharField(primary_key=True, max_length=13)
  book_ref = ForeignKeyField(
    Booking,
    field=Booking.book_ref,
    column_name='book_ref',
    backref='tickets',
    on_delete=None,
  )
  passenger_id = TextField()
  passenger_name = TextField()
  outbound = BooleanField()

  class Meta:
    table_name = 'tickets'
    indexes = (
      (('book_ref', 'passenger_id', 'outbound'), True),
    )
