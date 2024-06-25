import sys

import streamlit as st

sys.path.append(
    r'C:\Users\1012986131\Desktop\python\streamlit_pyecharts'
)

from data_visualization.tool import func as visual_func
from screeninfo import get_monitors

height = int(get_monitors()[0].height / 1080) * 350

visual_func.session_state_reset(page=5)

# 读取现有json文件
json_data = visual_func.load_json_data(file_name="teacher_info")

# 设置全局属性
visual_func.set_page_configuration(title="义务教育优质均衡", icon=":star:")

st.divider()
st.write(st.session_state)

st.info("测试组件")
# with st.container(border=True):
#
#     st.selectbox(
#         "选择需要查询的学段",
#         ["1", "2"],
#         index=None,
#         placeholder="单击选择学段",
#     )
#
#     st.write('Count = ', st.session_state.page100_count)
#
#     increment = st.button('Increment')
#     if increment:
#         st.session_state.page100_count += 1
#         st.rerun()
#
#     st.write('Count = ', st.session_state.page100_count)


import streamlit as st

if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True


def reset():
    st.session_state.clicked = False


st.button('Click me', on_click=click_button, disabled=st.session_state.clicked)

if st.session_state.clicked:
    st.write('Button clicked!')

    if st.button("点击查看111"):
        st.write(111)

    st.button("reset", on_click=reset)
