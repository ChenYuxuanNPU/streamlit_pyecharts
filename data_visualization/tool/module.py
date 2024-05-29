import time
import json
import streamlit as st
import pyecharts.options as opts

from screeninfo import get_monitors
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Pie
from pyecharts.charts import Bar


end_dict = {
    "高中": 70,
    "初中": 70,
    "小学": 70,
    "幼儿园": 95
}


# 用来检查module模块是否被正确import
def hello():
    return "hello world"


# 设置页面全局属性
def set_page_configuration():
    st.set_page_config(
        page_title='区级数据',
        page_icon=':light_rail:',
        layout='wide'
    )


def draw_pie(data: dict, title: str, height=0):

    if height == 0:

        for monitor in get_monitors():
            height = int(monitor.height / 1080) * 350

    with st.container(border=True):
        st_pyecharts(
            chart=(
                Pie()
                .add("", [(k, v) for k, v in data.items()],
                     center=["50%", "60%"], radius="65%", percent_precision=1)
                .set_global_opts(title_opts=opts.TitleOpts(title=title),
                                 legend_opts=opts.LegendOpts(pos_left='20%' if len(title) > 2 else "15%"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
                # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}, {d}%"))
            ),
            height=f"{height}px"
        )


def draw_1col_bar(data: dict, title: str, height=0):

    if height == 0:

        for monitor in get_monitors():
            height = int(monitor.height / 1080) * 350

    with st.container(border=True):
        st_pyecharts(
            chart=(
                Bar()
                .add_xaxis([keys for keys in data.keys()])
                .add_yaxis("总人数", [values for values in data.values()])
                .set_series_opts(label_opts=opts.LabelOpts(position="top"))
                .set_global_opts(title_opts=opts.TitleOpts(title=title),
                                 legend_opts=opts.LegendOpts(is_show=False),
                                 visualmap_opts=opts.VisualMapOpts(is_show=False,
                                                                   max_=max([values for values in data.values()])))
            ),
            height=f"{height}px"
        )


def draw_2col_bar(data: dict, title: str, height=0, end=70):

    if height == 0:

        for monitor in get_monitors():
            height = int(monitor.height / 1080) * 350

    with st.container(border=True):
        st_pyecharts(
            chart=(
                Bar()
                .add_xaxis([keys for keys in data.keys()])
                .add_yaxis("总人数", [values for values in data.values()])
                .set_series_opts(label_opts=opts.LabelOpts(position="top"))
                .set_global_opts(title_opts=opts.TitleOpts(title=title),
                                 legend_opts=opts.LegendOpts(is_show=False),
                                 datazoom_opts=opts.DataZoomOpts(is_show=True, range_start=0, range_end=end),
                                 visualmap_opts=opts.VisualMapOpts(is_show=True, pos_right="1%", pos_top="30%",
                                                                   max_=max([values for values in data.values()])))
            ),
            height=f"{height}px"
        )


def load_json_data():
    # 读取现有json文件
    with open(r"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\result\output.json",
              "r", encoding="UTF-8") as file:
        json_data = json.load(file)

    return json_data


# 这里是给片区不同学段的可视化做的
def show_period(period: str, data: dict):
    st.info(f"在编{period}信息")

    with st.container(border=False):
        c0, c1 = st.columns([2, 1])

        with c0:
            draw_2col_bar(data=data["在编"]["全区"][period]["主教学科"], title="主教学科", end=end_dict[period])

        with c1:
            draw_pie(data=data["在编"]["全区"][period]["年龄"], title="年龄")

        c0, c1, c2 = st.columns(spec=3)

        with c0:
            draw_pie(data=data["在编"]["全区"][period]["最高学历"], title="最高学历")

        with c1:
            draw_1col_bar(data=data["在编"]["全区"][period]["院校级别"], title="毕业院校")

        with c2:
            draw_pie(data=data["在编"]["全区"][period]["最高职称"], title="职称")


# 用来插入st.write_stream的数据
def stream_data(sentence: str, delay=0.03):
    for word in sentence:
        yield word
        time.sleep(delay)
