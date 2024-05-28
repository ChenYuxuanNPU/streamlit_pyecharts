import json
import streamlit as st
import pandas as pd
import numpy as np
import pyecharts.options as opts
from screeninfo import get_monitors
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Pie
from pyecharts.charts import Bar


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
    page_title='区级数据',
    page_icon=':light_rail:',
    layout='wide'
)

# 获取屏幕纵向像素值
for monitor in get_monitors():
    img_height = int(monitor.height / 1080) * 350

# 读取现有json文件

with open(r"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\result\output.json",
          "r", encoding="UTF-8") as file:
    json_data = json.load(file)

# 标题
st.title("各片镇教师数据")

with st.container(border=True):
    area = st.selectbox(
        "想查询哪一个片镇的信息？",
        ("永平", "石井", "新市", "人和", "江高", "太和", "钟落潭"),
        index=None,
        placeholder="单击选择区域",
    )

    if area is not None:
        st.success(f"{area}在编所有学段信息")

        with st.container(border=False):
            col0, col1, col2 = st.columns(spec=3)

            with col0:
                # 在编年龄统计
                draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["年龄"], height=img_height, title="年龄")

                # 在编学段统计
                draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["学段统计"], height=img_height,
                         title="学段统计")

            with col1:
                # 在编学历统计
                draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["最高学历"], height=img_height,
                         title="最高学历")

                with col1:
                    # 在编毕业院校统计
                    draw_1col_bar(data=json_data["在编"]["片区"][area]["所有学段"]["院校级别"], height=img_height,
                                  title="毕业院校")

            with col2:
                # 在编职称统计
                draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["最高职称"], height=img_height, title="职称")

                # 在编行政职务统计
                draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["行政职务"], height=img_height,
                         title="行政职务")

            # 在编学科统计
            draw_1col_bar(data=json_data["在编"]["片区"][area]["所有学段"]["主教学科"], height=img_height,
                          title="主教学科")

            col0, col1, col2 = st.columns(spec=3)

            with col0:
                # 在编骨干教师统计
                draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["骨干教师"], height=img_height,
                         title="骨干教师")

            with col1:
                # 在编教师支教统计
                draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["支教地域"], height=img_height,
                         title="支教地域")

            with col2:
                # 在编三名教师统计
                draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["三名工作室"], height=img_height,
                         title="三名统计")

        st.success("编外所有学段教师信息")

        with st.container(border=False):
            col0, col1, col2 = st.columns(spec=3)

            with col0:
                # 非编学段统计
                draw_pie(data=json_data["非编"]["片区"][area]["所有学段"]["学段统计"], height=img_height,
                         title="学段统计")

                # 非编教师资格统计
                draw_pie(data=json_data["非编"]["片区"][area]["所有学段"]["教师资格"], height=img_height,
                         title="教师资格")

            with col1:
                # 非编学历统计
                draw_pie(data=json_data["非编"]["片区"][area]["所有学段"]["最高学历"], height=img_height,
                         title="最高学历")

                # 非编中小学教师资格统计
                draw_pie(data=json_data["非编"]["片区"][area]["中小学"]["教师资格"], height=img_height, title="中小学")

            with col2:
                # 非编职称统计
                draw_pie(data=json_data["非编"]["片区"][area]["所有学段"]["最高职称"], height=img_height, title="职称")

                # 非编幼儿园教师资格统计
                draw_pie(data=json_data["非编"]["片区"][area]["幼儿园"]["教师资格"], height=img_height, title="幼儿园")

