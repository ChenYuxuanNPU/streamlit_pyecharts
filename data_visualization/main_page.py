import sys

import streamlit as st

# --server.port 8503

sys.path.append(
    r'C:\Users\1012986131\Desktop\python\streamlit_pyecharts'
)
from data_visualization.tool import func as visual_func

st.set_page_config(
    page_title="首页",
    page_icon=":sunrise:",
    layout="wide",
)

# 初始化全局变量
visual_func.session_state_initial()

# 清空其他页暂用变量
visual_func.session_state_reset(page=-1)

st.title("欢迎使用白云区教师数据可视化系统")

st.balloons()

