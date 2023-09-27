from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db' # DBの格納先

engine = create_engine(
  SQL_ALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False}
) # crud操作を行うための基盤を作成

SessionLocal = sessionmaker(autoflush=False,bind=engine) # DBへのセッションを定義する
Base = declarative_base() # DB作成時に必要となるクラスを定義
