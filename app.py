import streamlit as st
import requests
import json
import datetime
import pandas as pd

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
  st.title('会議室予約画面')
  # ユーザー 一覧取得
  users_url = 'http://127.0.0.1:8000/users'
  res = requests.get(users_url)
  users = res.json()
  # ユーザー名をkey、ユーザーIDをvalue
  users_dict = {}
  for user in users:
    users_dict[user['username']] = user['user_id']

  # 会議室一覧取得
  rooms_url = 'http://127.0.0.1:8000/rooms'
  res = requests.get(rooms_url)
  rooms = res.json()
  rooms_dict = {}
  for room in rooms:
    rooms_dict[room['room_name']] = {
      'room_id': room['room_id'],
      'capacity':room['capacity']
    }

  st.write('### 会議室一覧')
  df_rooms = pd.DataFrame(rooms)
  df_rooms.columns = ['会議室名','定員','会議室ID']
  st.table(df_rooms)


  with st.form(key='bookings'):
    username: str = st.selectbox('予約者名', users_dict.keys())
    room_name: str = st.selectbox('会議室名', rooms_dict.keys())
    booked_num: int = st.number_input('予約人数',step=1,min_value=1)
    date = st.date_input('日付を入力',min_value=datetime.date.today())
    start_time = st.time_input('開始時刻',value=datetime.time(hour=9,minute=0))
    end_time = st.time_input('終了時刻', value=datetime.time(hour=20,minute=0))
    submit_button = st.form_submit_button(label='予約登録') # form専用ボタン


  if submit_button: # ボタンが押されたかどうか
    user_id: int = users_dict[username] # usernameに紐づくuser_idを取得する
    room_id: int = rooms_dict[room_name]['room_id'] #room_nameに紐づくroom_idを取得する(capacityではなくidのためroom_dict[room_name]['room_id']の形式)
    capacity: int = rooms_dict[room_name]['capacity'] #room_nameに紐づくcapacityを取得する(capacityではなくidのためroom_dict[room_name]['capacity']の形式)

    data = {
      'user_id':user_id,
      'room_id':room_id,
      'booked_num':booked_num,
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

    # 定員以下の予約人数の場合
    if booked_num <= capacity:
      # st.write('## 送信データ') # デバック用
      # st.json(data) # どんなデータが入っているか確認するため
      # st.write('## レスポンス結果')
      url = 'http://127.0.0.1:8000/bookings'
      res = requests.post(url,data=json.dumps(data,default=json_serial))
      if res.status_code == 200:
        st.success('予約完了いたしました')
      else:
        st.error('予約に失敗しました')
      # st.write(res.status_code)
      st.json(res.json())
    else:
      st.error(f'{room_name}の定員は{capacity}名です。\n{capacity}名以下で予約を行なってください')

else:
  st.write('404 Not found')
