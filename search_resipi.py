import streamlit as st
import pandas as pd
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google APIの認証情報を設定
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)

# スプレッドシートにアクセス
gClient = gspread.authorize(credentials)
SPREADSHEET_KEY = '1SCDRGmNwEfiNvNYE4aGBM6tlkCEeNsIh-tsB1NgixgY'
worksheet = gClient.open_by_key(SPREADSHEET_KEY).worksheet('編集中')

# worksheetの値をDataFrameに変換
data = worksheet.get_all_values()
headers = data.pop(0)
df = pd.DataFrame(data, columns=headers)

# Streamlitのサイドバーに月齢を選択するセレクトボックスを表示
selected_month = st.sidebar.selectbox("月齢を選択してください", ["9～11カ月頃（後期）"])

# 選択された月齢に一致する行をフィルタリング
filtered_df = df[df["months"] == selected_month]

# Streamlitのテキストボックスに食材名を入力させる
search_term = st.text_input("食材名を入力してください")

# 食材名を含む行をフィルタリング
filtered_df = filtered_df[filtered_df["ingredients&quantity_１"].str.contains(search_term)]

# フィルタリングされた行がある場合、ランダムに一つを選択して結果を表示
if len(filtered_df) > 0:
    selected_row = filtered_df.sample(1)
    name = selected_row["name"].values[0]
    ingredients1 = selected_row["ingredients&quantity_１"].values[0]
    ingredients2 = selected_row["ingredients&quantity_2"].values[0]
    how_to_make = selected_row["how to make"].values[0]
    st.write("料理名:", name)
    st.write("材料1:", ingredients1)
    st.write("材料2:", ingredients2)
    st.write("作り方:", how_to_make)
else:
    st.write("該当するレシピがありません。")