from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from sql_app import models,crud,schemas
from sql_app.database import SessionLocal, engine
from typing import List
import logging

""" DBの作成を行う
bind = engine でどのデータベース基盤を使うかを指定する
"""
models.Base.metadata.create_all(bind=engine) # DBの作成を行う

""" DBとのSessionを確立するための処理 """
def get_db():
  """依存関係を作成する
    一回のリクエストで使用されるセッションインスタンスを作成し、
    リクエストが終了したらclose()する

    Yields:
        db: SQLAlchemyで生成したセッションインスタンス
    """
  db = SessionLocal()
  try:
    # responseを返した後に、その他処理を行い時に、yieldを使う
    yield db
  except:
    logging.warning('db connect fail!')
  finally:
    db.close()



app = FastAPI()

# @app.get("/")
# async def index():
#   return{"message":"Success"}

# Read Api
""" ユーザー一覧を取得するAPI
response_model=List[schemas.User]:レスポンスにschemas.Userのデータ構造を複数(ユーザー数)形に指定している

"""
@app.get("/users", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  """  Depends(get_db)でdbに代入するget_dbを強制指定する """
  users = crud.get_users(db=db, skip=skip, limit=limit)
  return users

@app.get("/rooms",response_model=List[schemas.Room])
async def read_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  """  Depends(get_db)でdbに代入するget_dbを強制指定する """
  rooms = crud.get_rooms(db=db, skip=skip, limit=limit)
  return rooms

@app.get("/bookings",response_model=List[schemas.Booking])
async def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  """  Depends(get_db)でdbに代入するget_dbを強制指定する """
  bookings = crud.get_bookings(db=db, skip=skip, limit=limit)
  return bookings

# Post Api
@app.post("/users",response_model=schemas.User)
async def create_user(user:schemas.CreateUser,db: Session = Depends(get_db)):
  result_user = crud.create_user(db=db, user=user)
  return result_user

@app.post("/rooms",response_model=schemas.Room)
async def create_room(room:schemas.CreateRoom,db: Session = Depends(get_db)):
  result_room = crud.create_room(db=db, room=room)
  return result_room

@app.post("/bookings",response_model=schemas.Booking)
async def create_booking(booking:schemas.CreateBooking,db: Session = Depends(get_db)):
  result_booking = crud.create_booking(db=db, booking=booking)
  return result_booking
