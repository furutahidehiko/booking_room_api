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
  user_list = {}
  for user in users:
    # usernameをkeyに辞書型のデータに整形
    user_list[user['username']] = user['user_id']

  # 会議室一覧取得
  rooms_url = 'http://127.0.0.1:8000/rooms'
  res = requests.get(rooms_url)
  rooms = res.json()
  room_list = {}
  for room in rooms:
    # room_nameをkeyに辞書型のデータに整形
    room_list[room['room_name']] = {
      'room_id': room['room_id'],
      'capacity':room['capacity']
    }
  st.write('### 会議室一覧')
  df_rooms = pd.DataFrame(rooms)
  df_rooms.columns = ['会議室名','定員','会議室ID']
  st.table(df_rooms)

  # 予約一覧取得
  bookings_url = 'http://127.0.0.1:8000/bookings'
  res = requests.get(bookings_url)
  bookings = res.json()
  df_bookings = pd.DataFrame(bookings)
  users_id = {}
  for user in users:
    # user_idをkeyに辞書型のデータに整形
    users_id[user['user_id']] = user['username']
  rooms_id = {}
  for room in rooms:
    # room_idをkeyに辞書型のデータに整形
    rooms_id[room['room_id']] = {
      'room_name': room['room_name'],
      'capacity':room['capacity']
    }

  # idを各値に変換（予約が増えるたびにxにユーザidが代入されユーザ名に変換される）
  conversion_user_name = lambda x: users_id[x]
  conversion_room_name = lambda x: rooms_id[x]['room_name']
  conversion_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime('%Y/%m/%d %H:%M')

  # 特定の列に適用
  df_bookings['user_id'] = df_bookings['user_id'].map(conversion_user_name)
  df_bookings['room_id'] = df_bookings['room_id'].map(conversion_room_name)
  df_bookings['start_datetime'] = df_bookings['start_datetime'].map(conversion_datetime)
  df_bookings['end_datetime'] = df_bookings['end_datetime'].map(conversion_datetime)

  df_bookings = df_bookings.rename(columns={
    'user_id':'予約者名',
    'room_id':'会議室名',
    'booked_num':'予約人数',
    'start_datetime':'開始時刻',
    'end_datetime':'終了時刻',
    'booking_id':'予約番号',
  })

  st.write('### 予約一覧')
  st.table(df_bookings)


  with st.form(key='bookings'):
    username: str = st.selectbox('予約者名', user_list.keys())
    room_name: str = st.selectbox('会議室名', room_list.keys())
    booked_num: int = st.number_input('予約人数',step=1,min_value=1)
    date = st.date_input('日付を入力',min_value=datetime.date.today())
    start_time = st.time_input('開始時刻',value=datetime.time(hour=9,minute=0))
    end_time = st.time_input('終了時刻', value=datetime.time(hour=20,minute=0))
    submit_button = st.form_submit_button(label='予約登録') # form専用ボタン


  if submit_button: # ボタンが押されたかどうか
    user_id: int = user_list[username] # usernameに紐づくuser_idを取得する
    room_id: int = room_list[room_name]['room_id'] #room_nameに紐づくroom_idを取得する(capacityではなくidのためroom_dict[room_name]['room_id']の形式)
    capacity: int = room_list[room_name]['capacity'] #room_nameに紐づくcapacityを取得する(capacityではなくidのためroom_dict[room_name]['capacity']の形式)

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
    if booked_num > capacity:
      st.error(f'{room_name}の定員は{capacity}名です。\n{capacity}名以下で予約を行なってください')
    # 開始時刻 >= 終了時刻
    elif start_time >= end_time:
      st.error('開始時刻が終了時刻を超えています')
    # 開始時刻が9:00より早い場合 or 終了時刻が20:00より遅い場合
    elif start_time < datetime.time(hour=9, minute=0, second=0) or end_time > datetime.time(hour=20, minute=0, second=0):
      st.error('利用時間は9:00~20:00の間になります')
    else:
      # 会議室予約
      # st.write('## 送信データ') # デバック用
      # st.json(data) # どんなデータが入っているか確認するため
      # st.write('## レスポンス結果')
      detail_text = 'Cannot register due to duplicate appointment time'
      url = 'http://127.0.0.1:8000/bookings'
      res = requests.post(url,data=json.dumps(data,default=json_serial))
      if res.status_code == 200:
        st.success('予約完了いたしました')
      elif res.status_code == 404 and res.json()['detail'] == detail_text:
        st.error('指定の開始時間もしくは終了時間はすでに予約済みとなります')
      else:
        st.error('予約に失敗しました')
      # st.write(res.status_code)
      st.json(res.json())

else:
  st.write('404 Not found')
