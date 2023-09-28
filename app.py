import streamlit as st
import random
import requests
import json
import datetime

from json_serial import json_serial

page = st.sidebar.selectbox('Choose your page',['users','rooms','bookings'])

if page == 'users':
  st.title('ユーザー登録画面')

  with st.form(key='user'):
    username: str = st.text_input('ユーザー名',max_chars=12) # 12字文字以内
    data = {'username':username}
    submit_button = st.form_submit_button(label='送信') # form専用ボタン

  if submit_button: # ボタンが押されたかどうか
    # st.write('## 送信データ') # デバック用
    # st.json(data) # どんなデータが入っているか確認するため
    st.write('## レスポンス結果')
    url = 'http://127.0.0.1:8000/users'
    res = requests.post(url,data=json.dumps(data))
    if res.status_code == 200:
      st.success('ユーザー登録完了')
    else:
      st.error('ユーザー登録失敗')
    st.json(res.json())

elif page == 'rooms':
  st.title('会議室登録画面')

  with st.form(key='room'):
    room_id: int = random.randint(0,10) # 0~10のランダムな整数を生成
    room_name: str = st.text_input('会議室名',max_chars=12) # 12字文字以内
    capacity: int = st.number_input('定員',step=1)
    data = {
      'room_name':room_name,
      'capacity':capacity
    }
    submit_button = st.form_submit_button(label='送信') # form専用ボタン

  if submit_button: # ボタンが押されたかどうか
    # st.write('## 送信データ') # デバック用
    # st.json(data) # どんなデータが入っているか確認するため
    st.write('## レスポンス結果')
    url = 'http://127.0.0.1:8000/rooms'
    res = requests.post(url,data=json.dumps(data))
    if res.status_code == 200:
      st.success('会議室登録完了')
    else:
      st.error('会議室登録失敗')
    # st.write(res.status_code)
    st.json(res.json())

elif page == 'bookings':
  st.title('APIテスト画面(予約)')

  with st.form(key='bookings'):
    booking_id: int = random.randint(0,10) # 0~10のランダムな整数を生成
    user_id: int = random.randint(0,10) # 0~10のランダムな整数を生成
    room_id: int = random.randint(0,10) # 0~10のランダムな整数を生成
    book_num: int = st.number_input('予約人数',step=1)
    date = st.date_input('日付を入力',min_value=datetime.date.today())
    start_time = st.time_input('開始時刻',value=datetime.time(hour=9,minute=0))
    end_time = st.time_input('終了時刻', value=datetime.time(hour=20,minute=0))
    data = {
      'booking_id':booking_id,
      'user_id':user_id,
      'room_id':room_id,
      'booked_num':book_num,
      'start_datetime':datetime.datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=start_time.hour,
        minute=start_time.minute
      ),
      'end_datetime':datetime.datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=end_time.hour,
        minute=end_time.minute
      )
    }
    submit_button = st.form_submit_button(label='送信') # form専用ボタン


  if submit_button: # ボタンが押されたかどうか
    st.write('## 送信データ') # デバック用
    st.json(data) # どんなデータが入っているか確認するため
    st.write('## レスポンス結果')
    url = 'http://127.0.0.1:8000/bookings'
    res = requests.post(url,data=json.dumps(data,default=json_serial))
    st.write(res.status_code)
    st.json(res.json())

else:
  st.write('404 Not found')
