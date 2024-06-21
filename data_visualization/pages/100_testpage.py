import sys

import streamlit as st

sys.path.append(
    r'C:\Users\1012986131\Desktop\python\streamlit_pyecharts'
)

from data_visualization.tool import func as visual_func
from screeninfo import get_monitors

for monitor in get_monitors():
    height = int(monitor.height / 1080) * 350

# 读取现有json文件
json_data = visual_func.load_json_data(file_name="teacher_info")

# 设置全局属性
visual_func.set_page_configuration(title="义务教育优质均衡", icon=":star:")

if 'fc' not in st.session_state:
    st.session_state.fc = 0

print(st.session_state.fc)


def fuck():
    st.session_state.fc += 1


st.selectbox(
        "选择需要查询的学段",
        ["1", "2"],
        index=None,
        placeholder="单击选择学段",
    )

if st.button("111"):
    fuck()

st.write(st.session_state.fc)