import os
import sys

import streamlit as st

from data_visualization.tool import func as visual_func


# 返回给定的第n层的父目录路径
def get_nth_parent_dir(n):
    path = os.path.abspath(__file__)

    for _ in range(n):
        path = os.path.dirname(path)

    return path


sys.path.append(
    get_nth_parent_dir(n=3)
)


# sys.path.append(
#     r'C:\Users\1012986131\Desktop\python\streamlit_pyecharts'
# )

# 清空其他页暂用变量
visual_func.session_state_reset(page=2)

st.write("全局变量状态:")
st.write(st.session_state)
