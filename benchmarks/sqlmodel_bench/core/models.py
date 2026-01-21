from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, CHAR, Text, Boolean, Numeric, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import SQLModel, Field, Relationship


class Booking(SQLModel, table=True):
  __tablename__ = 'bookings'

  book_ref: str = Field(sa_column=Column(CHAR(6), primary_key=True))
  book_date: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False))
  total_amount: Decimal = Field(sa_column=Column(Numeric, nullable=False))

  tickets: list["Ticket"] = Relationship(
    back_populates='booking',
    sa_relationship_kwargs={
      'cascade': 'save-update, merge',
      'passive_deletes': True,
    },
  )

  __table_args__ = (
    Index('idx_book_ref', 'book_ref'),
  )


class Ticket(SQLModel, table=True):
  __tablename__ = 'tickets'

  ticket_no: str = Field(sa_column=Column(Text, primary_key=True))

  book_ref: str = Field(sa_column=Column(
    CHAR(6), ForeignKey('bookings.book_ref'), nullable=False
  ))

  passenger_id: str = Field(sa_column=Column(Text, nullable=False))
  passenger_name: str = Field(sa_column=Column(Text, nullable=False))
  outbound: bool = Field(sa_column=Column(Boolean, nullable=False))

  booking: Booking = Relationship(back_populates='tickets')

  __table_args__ = (
    Index('idx_ticket_no', 'ticket_no'),
    UniqueConstraint('book_ref', 'passenger_id', 'outbound',
      name='unique_constraint_book_ref_passenger_id_outbound'),
  )