import datetime
import os
import sys

import pyecharts.options as opts
import streamlit as st


# 返回给定的第n层的父目录路径
def get_nth_parent_dir(n):
    path = os.path.abspath(__file__)

    for _ in range(n):
        path = os.path.dirname(path)

    return path


sys.path.append(
    get_nth_parent_dir(n=3)
)

from data_visualization.tool import func as visual_func
from teacher_data_processing.tool import func as tch_proc_func
from screeninfo import get_monitors
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Pie

height = int(get_monitors()[0].height / 1080) * 350

visual_func.session_state_reset(page=5)

# 读取现有json文件
json_data = visual_func.load_json_data(folder="result", file_name="teacher_info")

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
    st.divider()

# school_cloud(json_data)

st.button("刷新！")

st.markdown(
    "<h1 style='text-align: center;'>这是一个居中的标题</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h2 style='text-align: center;'>这是一个居中的标题</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align: center;'>这是一个居中的标题</h3>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align: center;'>这是一个居中的标题</h4>",
    unsafe_allow_html=True
)

st.title("Cats!")

row1 = st.columns(3)
row2 = st.columns(3)

grid = [col.container(height=200) for col in row1 + row2]
safe_grid = [card.empty() for card in grid]


def black_cats():
    st.title("🐈‍⬛ 🐈‍⬛")
    st.markdown("🐾 🐾 🐾 🐾")


def orange_cats():
    st.title("🐈 🐈")
    st.markdown("🐾 🐾 🐾 🐾")


@st.experimental_fragment
def herd_black_cats(card_a, card_b, card_c):
    st.button("Herd the black cats")
    container_a = card_a.container()
    container_b = card_b.container()
    container_c = card_c.container()
    with container_a:
        black_cats()
    with container_b:
        black_cats()
    with container_c:
        black_cats()


@st.experimental_fragment
def herd_orange_cats(card_a, card_b, card_c):
    st.button("Herd the orange cats")
    container_a = card_a.container()
    container_b = card_b.container()
    container_c = card_c.container()
    with container_a:
        orange_cats()
    with container_b:
        orange_cats()
    with container_c:
        orange_cats()


with st.sidebar:
    herd_black_cats(grid[0].empty(), grid[2].empty(), grid[4].empty())
    herd_orange_cats(grid[1].empty(), grid[3].empty(), grid[5].empty())
    st.button("Herd all the cats")

c, conn = tch_proc_func.connect_database()

c.execute("select political_status,count(*) from teacher_data_0 where current_administrative_position != '无' and "
          "current_administrative_position != '中层正职' and current_administrative_position != '中层副职' group by "
          "political_status order by count(*) desc")

party_1 = c.fetchall()

with st.container(border=True):
    st.markdown(
        "<h4 style='text-align: center;'>这是一个居中的标题</h4>",
        unsafe_allow_html=True
    )

    st_pyecharts(
        chart=(
            Pie()
            .add("", [(k, v) for k, v in dict(party_1).items()],
                 center=["50%", "60%"], radius="65%", percent_precision=1)
            # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}人,占比{d}%"))
        ),
        height=f"{height}px"
    )

st.date_input("When's your birthday", datetime.date(2019, 7, 6))

tch_proc_func.disconnect_database(conn=conn)