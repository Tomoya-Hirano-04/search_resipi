import streamlit as st
import pandas as pd
import random
from google.oauth2.service_account import ServiceAccountCredentials
import gspread

# Google APIの認証情報を設定
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

# スプレッドシートにアクセス
gClient = gspread.authorize(credentials)
SPREADSHEET_KEY = '1SCDRGmNwEfiNvNYE4aGBM6tlkCEeNsIh-tsB1NgixgY'
worksheet = gClient.open_by_key(SPREADSHEET_KEY).worksheet('編集中')

# 月ごとの情報を格納する辞書
months_dict = {
    '9～11カ月頃（後期）': ['鶏肉とトマトのスープ煮', 'ほうれん草とササミのおひたし', '小松菜のごまあえ'],
    # 他の月の情報を追加する
}

# Streamlitアプリケーション
st.title('ベビーフードのレシピ')
month = st.selectbox('月齢を選択してください', options=list(months_dict.keys()))

# 該当する月のレシピを抽出
month_data = worksheet.get_all_values()[1:]  # 1行目はヘッダーのため除外
month_data = [row for row in month_data if row[0] == month]

# ランダムにレシピを選択
recipe = None
while not recipe:
    candidate = random.choice(months_dict[month])
    for row in month_data:
        if all(ing in row[2] for ing in candidate.split(' ')):
            recipe = row
            break

# レシピの表示
st.subheader(recipe[1])
st.write('材料1：', recipe[2])
st.write('材料2：', recipe[3])
st.write('作り方：', recipe[4])