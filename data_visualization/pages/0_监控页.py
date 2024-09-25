import sys
from pathlib import Path

import streamlit as st

from data_visualization.tool import func as visual_func

# 加入项目路径
sys.path.append(
    str(
        Path(__file__).resolve().parent.parent.parent
    )
)

# 清空其他页暂用变量
visual_func.session_state_reset(page=2)

st.write("全局变量状态:")
st.write(st.session_state)
