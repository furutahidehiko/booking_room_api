import datetime
from pydantic import BaseModel, Field

"""
Fast APIのデータ構造
"""

class CreateBooking(BaseModel):
  user_id: int
  room_id: int
  booked_num: int
  start_datetime:datetime.datetime
  end_datetime:datetime.datetime

class Booking(CreateBooking):
  booking_id: int

  # sql_alchemyのデータに対応するため
  class Config:
    orm_mode = True

class CreateUser(BaseModel):
  username: str = Field(max_length=12)


class User(CreateUser):
  user_id: int

  class Config:
    orm_mode = True

class CreateRoom(BaseModel):
  room_name: str = Field(max_length=12)
  capacity: int
class Room(CreateRoom):
  room_id: int

  class Config:
    orm_mode = True
