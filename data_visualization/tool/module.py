import copy
import sqlite3
import json
import time

from data_processing.read_database import get_database_data as gd


def load_json_data():
    # 读取现有json文件
    with open(r"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\result\output.json",
              "r", encoding="UTF-8") as file:
        json_data = json.load(file)

    return json_data


# 用来检查module模块是否被正确import
def hello():
    return "hello world"


# 用来插入st.write_stream的数据
def stream_data(sentence: str, delay=0.03):
    for word in sentence:
        yield word
        time.sleep(delay)
