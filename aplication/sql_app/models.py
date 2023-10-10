from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from .database import Base

"""
SQL Alchemyのデータ構造
"""

class User(Base):
    """usersテーブルのモデル"""
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

class Room(Base):
    """roomsテーブルのモデル"""
    __tablename__ = 'rooms'

    room_id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String, unique=True, index=True)
    capacity = Column(Integer)

# ondelete = 'CASCADE' 親表の対象行が削除されたときに対応する子表の行も削除する
# ondelete = 'SET NULL' 親表の対象行が削除されたときに対応する子表の行をnullにする
class Booking(Base):
    """bookingsテーブルのモデル"""
    __tablename__ = 'bookings'

    booking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.user_id, ondelete="CASCADE",), nullable=False)
    room_id = Column(Integer,  ForeignKey(User.user_id, ondelete="CASCADE"),  nullable=False)
    booked_num = Column(Integer)
    start_datetime = Column(DateTime,  nullable=False)
    end_datetime = Column(DateTime,  nullable=False)
