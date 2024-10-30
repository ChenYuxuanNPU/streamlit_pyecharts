import sys
from pathlib import Path

import pandas as pd
import pyecharts.options as opts
import streamlit as st
from pyecharts.charts import Bar, Line

# 加入项目路径
sys.path.append(
    str(
        Path(__file__).resolve().parent.parent.parent
    )
)

from data_visualization.tool import func as visual_func
from screeninfo import get_monitors
from streamlit_echarts import st_pyecharts

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
    "<h1 style='text-align: center;'>超大杯</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h2 style='text-align: center;'>大杯</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align: center;'>中杯</h3>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align: center;'>小杯</h4>",
    unsafe_allow_html=True
)

# st.title("Cats!")
#
# row1 = st.columns(3)
# row2 = st.columns(3)
#
# grid = [col.container(height=200) for col in row1 + row2]
# safe_grid = [card.empty() for card in grid]
#
#
# def black_cats():
#     st.title("🐈‍⬛ 🐈‍⬛")
#     st.markdown("🐾 🐾 🐾 🐾")
#
#
# def orange_cats():
#     st.title("🐈 🐈")
#     st.markdown("🐾 🐾 🐾 🐾")
#
#
# @st.fragment
# def herd_black_cats(card_a, card_b, card_c):
#     st.button("Herd the black cats")
#     container_a = card_a.container()
#     container_b = card_b.container()
#     container_c = card_c.container()
#     with container_a:
#         black_cats()
#     with container_b:
#         black_cats()
#     with container_c:
#         black_cats()
#
#
# @st.fragment
# def herd_orange_cats(card_a, card_b, card_c):
#     st.button("Herd the orange cats")
#     container_a = card_a.container()
#     container_b = card_b.container()
#     container_c = card_c.container()
#     with container_a:
#         orange_cats()
#     with container_b:
#         orange_cats()
#     with container_c:
#         orange_cats()


# with st.sidebar:
#     herd_black_cats(grid[0].empty(), grid[2].empty(), grid[4].empty())
#     herd_orange_cats(grid[1].empty(), grid[3].empty(), grid[5].empty())
#     st.button("Herd all the cats")

# c, conn = tch_proc_func.connect_database()
#
# c.execute("select political_status,count(*) from teacher_data_0 where current_administrative_position != '无' and "
#           "current_administrative_position != '中层正职' and current_administrative_position != '中层副职' group by "
#           "political_status order by count(*) desc")
#
# party_1 = c.fetchall()
#
# with st.container(border=True):
#     st.markdown(
#         "<h4 style='text-align: center;'>这是一个居中的标题</h4>",
#         unsafe_allow_html=True
#     )
#
#     st_pyecharts(
#         chart=(
#             Pie()
#             .add("", [(k, v) for k, v in dict(party_1).items()],
#                  center=["50%", "60%"], radius="65%", percent_precision=1)
#             # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
#             .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}人,占比{d}%"))
#         ),
#         height=f"{height}px"
#     )
#
# st.date_input("When's your birthday", datetime.date(2019, 7, 6))
#
# tch_proc_func.disconnect_database(conn=conn)

age_list = [str(x) for x in range(17, 66)]
df = pd.DataFrame(
    data={
        "性别": ["男", "女"],
    },
    columns=["性别"] + age_list
)
df.fillna(value=20, inplace=True)


#
# print(df)
#
# x_data = age_list
# chart_1 = Bar()
# chart_1.add_xaxis(xaxis_data=x_data)
# chart_1.add_yaxis(
#     series_name="男",
#     y_axis=df[df['性别'] == "男"].drop('性别', axis=1).iloc[0].tolist(),
#     label_opts=opts.LabelOpts(is_show=False),
# )
# chart_1.add_yaxis(
#     series_name="女",
#     y_axis=df[df['性别'] == "女"].drop('性别', axis=1).iloc[0].tolist(),
#     label_opts=opts.LabelOpts(is_show=False),
# )
# chart_1.extend_axis(
#     yaxis=opts.AxisOpts(
#         name="人数",
#         type_="value",
#         min_=0,
#         max_=100,
#         interval=20,
#         axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
#     )
# )
#
# chart_1.set_global_opts(
#     tooltip_opts=opts.TooltipOpts(
#         is_show=True, trigger="axis", axis_pointer_type="cross"
#     ),
#     xaxis_opts=opts.AxisOpts(
#         type_="category",
#         axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
#     ),
#     yaxis_opts=opts.AxisOpts(
#         name="人数",
#         type_="value",
#         min_=0,
#         max_=100,
#         interval=20,
#         axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
#         axistick_opts=opts.AxisTickOpts(is_show=True),
#         splitline_opts=opts.SplitLineOpts(is_show=True),
#     ),
# )
#
# chart_2 = Line()
# chart_2.add_xaxis(xaxis_data=x_data)
# chart_2.add_yaxis(
#     series_name="合计",
#     yaxis_index=1,
#     y_axis=df[df['性别'] == "合计"].drop(columns=['性别']).iloc[0].tolist(),
#     label_opts=opts.LabelOpts(is_show=False),
# )
#
# chart_1.overlap(chart_2)
# with st.container(border=True):
#     st_pyecharts(chart_1, height="700px")

# print(df.drop(columns="性别", axis=1).values.max()
visual_func.draw_mixed_bar_and_line(df=df,x_list=[str(x) for x in range(17, 66)],label_column="性别",xaxis_label="柱状图轴",yaxis_label="折线图轴")


df.loc[len(df)] = ["合计1"] + df[df.columns.difference(['性别'])].sum().tolist()
visual_func.draw_mixed_bar_and_line(df=df,x_list=[str(x) for x in range(17, 66)],label_column="性别",xaxis_label="柱状图轴",yaxis_label="折线图轴",line_label="合计1")

