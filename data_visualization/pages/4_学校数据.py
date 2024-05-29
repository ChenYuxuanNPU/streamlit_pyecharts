import json
import sys
import time
import pyecharts.options as opts
import streamlit as st

sys.path.append(
    r'C:\Users\1012986131\Desktop\python\streamlit_pyecharts'
)

from pyecharts.charts import Bar
from pyecharts.charts import Pie
from screeninfo import get_monitors
from streamlit_echarts import st_pyecharts
from data_processing.tool import module as m_proc
from data_visualization.tool import module as m_visu
from data_processing.make_json.school_data import school as s


def draw_pie(data: dict, height: int, title: str):
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


def draw_1col_bar(data: dict, height: int, title: str):
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


def draw_2col_bar(data: dict, height: int, title: str, end=70):
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


# 设置全局属性
st.set_page_config(
    page_title='学校数据',
    page_icon=':bus:',
    layout='wide'
)

# 获取屏幕纵向像素值
for monitor in get_monitors():
    img_height = int(monitor.height / 1080) * 350

# 读取现有json文件
json_data = m_visu.load_json_data()

# 标题
st.title("学校教师数据")

with st.container(border=True):
    col0, col1 = st.columns([1, 1.5])

    with col0:
        school_name = st.text_input("请输入校名")
        period = st.selectbox(
            "选择学段（默认所有学段）",
            ("", "高中", "初中", "小学"),
        )
        kind = st.selectbox(
            "选择类型",
            ("在编", "非编"),
        )

        if st.button("查询"):

            if school_name is None or school_name == "":
                st.warning("校名为空", icon="⚠️")

            else:

                check_result = m_proc.school_name_and_period_check(kind=kind, school_name=school_name, period=period)
                if not check_result[0]:
                    st.warning(check_result[1], icon="⚠️")

                else:
                    st.success("查询成功", icon="✅")

                    intro = [
                        "11111111111111",
                        "22222222222",
                        "2333333333333"
                    ]

                    with col1:
                        st.subheader(f"{school_name} - 学校概况")

                        # 流式插入学校基础介绍
                        for i in range(len(intro)):
                            st.write_stream(m_visu.stream_data(sentence=intro[i]))
