import os
import sys

import streamlit as st


# --server.port 8503
def get_nth_parent_dir(n):
    path = os.path.abspath(__file__)

    for _ in range(n):
        path = os.path.dirname(path)

    return path


sys.path.append(
    get_nth_parent_dir(n=2)
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

st.markdown(
    "<h1 style='text-align: center;'>欢迎使用白云区教师数据可视化系统</h1>",
    unsafe_allow_html=True
)

st.balloons()
