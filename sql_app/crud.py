from sqlalchemy.orm import Session
from sql_app import schemas, models

""" ユーザー 一覧取得
db:ユーザ一覧の取得先データベース情報
skip:何個目までのデータを取得対象から外すかの指定
limit:取得制限(何個目までのデータを取るかどうか)
"""
def get_users(db: Session, skip: int = 0, limit: int = 100):
  """
  db.query(models.User):DBからmodelsのUserテーブルのデータを検索する
  """
  return db.query(models.User).offset(skip).limit(limit).all

""" 会議室一覧取得 """
def get_rooms(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Room).offset(skip).limit(limit).all

""" 予約一覧取得 """
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Booking).offset(skip).limit(limit).all

""" ユーザー登録 """
def create_user(db: Session, user: schemas.User):
  db_user = models.User(username=user.username)
  db.add(db_user) # dbへ登録
  db.commit() # 登録をcommit
  db.refresh(db_user)
  return db_user

""" 会議室登録 """
def create_room(db: Session, room: schemas.Room):
  db_room = models.Room(room_name=room.room_name, capacity=room.capacity)
  db.add(db_room) # dbへ登録
  db.commit() # 登録をcommit
  db.refresh(db_room)
  return db_room

""" 会議室予約 """
def create_booking(db: Session, booking: schemas.Booking):
  db_booking = models.Booking(
      user_id = booking.user_id,
      room_id = booking.room_id,
      booked_num = booking.booked_num,
      start_datetime = booking.start_datetime,
      end_datetime = booking.end_datetime
    )
  db.add(db_booking) # dbへ登録
  db.commit() # 登録をcommit
  db.refresh(db_booking)
  return db_booking
