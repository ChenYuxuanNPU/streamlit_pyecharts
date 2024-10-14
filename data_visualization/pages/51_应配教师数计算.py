import sys
from pathlib import Path

import streamlit as st

# 加入项目路径
sys.path.append(
    str(
        Path(__file__).resolve().parent.parent.parent
    )
)

from data_visualization.tool import func as visual_func
from data_visualization.render import page_51 as r

# 初始化全局变量
# visual_func.session_state_initial()

# 清空其他页暂用变量
visual_func.session_state_reset(page=51)

# 设置全局属性
visual_func.set_page_configuration(title="学校教师数据", icon=":house_with_garden:")

# 标题
st.markdown(
    "<h1 style='text-align: center;'>应配教师数</h1>",
    unsafe_allow_html=True
)

st.divider()

col0, col1, col2 = st.columns(spec=3)

with col0:
    grade_1 = st.number_input("一年级班数", value=0, min_value=0, max_value=30)
    grade_4 = st.number_input("四年级班数", value=0, min_value=0, max_value=30)
    grade_7 = st.number_input("七年级班数", value=0, min_value=0, max_value=30)

with col1:
    grade_2 = st.number_input("二年级班数", value=0, min_value=0, max_value=30)
    grade_5 = st.number_input("五年级班数", value=0, min_value=0, max_value=30)
    grade_8 = st.number_input("八年级班数", value=0, min_value=0, max_value=30)

with col2:
    grade_3 = st.number_input("三年级班数", value=0, min_value=0, max_value=30)
    grade_6 = st.number_input("六年级班数", value=0, min_value=0, max_value=30)
    grade_9 = st.number_input("九年级班数", value=0, min_value=0, max_value=30)

_, col_mid, _ = st.columns([1, 2, 1])
with col_mid:
    lessons = st.number_input(
        "输入课时量",
        value=10,
        min_value=0,
        max_value=35
    )

st.divider()

r.show_result(
    lessons=lessons,
    grade_1=grade_1,
    grade_2=grade_2,
    grade_3=grade_3,
    grade_4=grade_4,
    grade_5=grade_5,
    grade_6=grade_6,
    grade_7=grade_7,
    grade_8=grade_8,
    grade_9=grade_9
)
