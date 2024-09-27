import sys
from pathlib import Path

import streamlit as st

# --server.port 8503

# 加入项目路径
# 切记主页在上层，不要套三个.parent
sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

from data_visualization.tool import func as visual_func

# 初始化全局变量
visual_func.session_state_initial()

# 清空其他页暂用变量
visual_func.session_state_reset(page=-1)

st.set_page_config(
    page_title="首页",
    page_icon=":sunrise:",
    layout="wide",
)

st.markdown(
    "<h1 style='text-align: center;'>欢迎使用白云区教师数据可视化系统</h1>",
    unsafe_allow_html=True
)

st.balloons()
