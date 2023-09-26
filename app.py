import streamlit as st
import random
import requests
import json

st.title('APIテスト画面(ユーザー)')

with st.form(key='user'):
  user_id: int = random.randint(0,10) # 0~10のランダムな整数を生成
  username: str = st.text_input('ユーザー名',max_chars=12) # 12字文字以内
  data = {
    'user_id':user_id,
    'username':username
  }
  submit_button = st.form_submit_button(label='送信') # form専用ボタン

if submit_button: # ボタンが押されたかどうか
  st.write('## 送信データ') # デバック用
  st.json(data) # どんなデータが入っているか確認するため
  st.write('## レスポンス結果')
  url = 'http://127.0.0.1:8000/users'
  res = requests.post(url,data=json.dumps(data))
  st.write(res.status_code)
  st.json(res.json())
