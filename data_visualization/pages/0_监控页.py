import sys

import streamlit as st

from data_visualization.tool import func as visual_func

sys.path.append(
    r'C:\Users\1012986131\Desktop\python\streamlit_pyecharts'
)

# 清空其他页暂用变量
visual_func.session_state_reset(page=2)

st.write("全局变量状态:")
st.write(st.session_state)
