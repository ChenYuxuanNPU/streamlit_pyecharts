import json
import time
from inspect import stack
from pathlib import Path

import pandas as pd
import pyecharts.options as opts
import streamlit as st
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Pie
from pyecharts.charts import WordCloud
from screeninfo import get_monitors
from streamlit_echarts import st_pyecharts

kind_list = ["在编", "编外"]

end_dict = {
    "高中": 70,
    "初中": 70,
    "小学": 70,
    "幼儿园": 95
}

trans_period = {
    "所有学段": None,
    "高中": "高中",
    "初中": "初中",
    "小学": "小学",
    None: None
}


# 用来检查module模块是否被正确import
def hello() -> str:
    return "hello world"


# 设置页面全局属性
def set_page_configuration(title: str, icon: str) -> None:
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout='wide'
    )

    return None


# 记得画图的代码顺序是先插入数据再set样式！
def draw_pie_chart(data: pd.DataFrame | dict, title: str, height=0, formatter="{b}:{d}%", pos_left='20%',
                   center_to_bottom='60%') -> None:
    if height == 0:
        height = int(get_monitors()[0].height / 1080) * 350

    if isinstance(data, dict):
        chart_data = [(k, v) for k, v in data.items()]
    elif isinstance(data, pd.DataFrame):
        return None
    else:
        return None

    chart = Pie()

    chart.add("", chart_data, center=["50%", center_to_bottom], radius="65%",
              percent_precision=1)

    chart.set_global_opts(title_opts=opts.TitleOpts(title=title),
                          legend_opts=opts.LegendOpts(pos_left=pos_left))
    chart.set_series_opts(label_opts=opts.LabelOpts(formatter=formatter))

    with st.container(border=True):
        st_pyecharts(
            chart=chart,
            height=f"{height}px"
        )

    return None


# 画之前先测试下有没有问题
def draw_multi_pie_chart(inner_data: dict, outer_data: dict, title: str, height=0, formatter="{b}:{d}%") -> None:
    if height == 0:
        height = int(get_monitors()[0].height / 1080) * 350

    chart = Pie()

    chart.add(
        series_name="1",
        data_pair=inner_data,
        radius=["15%", "30%"],
        label_opts=opts.LabelOpts(position="outside"),
    )

    chart.add(
        series_name="2",
        radius=["50%", "65%"],
        data_pair=outer_data,
        label_opts=opts.LabelOpts(
            position="outside",
        )
    )

    chart.set_global_opts(tooltip_opts=opts.TooltipOpts(is_show=False)).set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        )
    )

    with st.container(border=True):
        st_pyecharts(
            chart=chart,
            height=f"{height}px"
        )

    return None


def draw_bar_chart(data: pd.DataFrame | dict, title: str, height=0, end=100, is_show_visual_map=True) -> None:
    if height == 0:
        height = int(get_monitors()[0].height / 1080) * 350

    if isinstance(data, dict):
        chart_data = [values for values in data.values()]
    elif isinstance(data, pd.DataFrame):
        return None
    else:
        return None

    chart = Bar()
    chart.add_xaxis([keys for keys in data.keys()])
    chart.add_yaxis("总人数", chart_data)

    chart.set_global_opts(title_opts=opts.TitleOpts(title=title),
                          legend_opts=opts.LegendOpts(is_show=False),
                          datazoom_opts=opts.DataZoomOpts(is_show=True, range_start=0, range_end=end),
                          visualmap_opts=opts.VisualMapOpts(is_show=is_show_visual_map, pos_right="1%",
                                                            pos_top="30%",
                                                            max_=max([values for values in data.values()])))
    chart.set_series_opts(label_opts=opts.LabelOpts(position="top"))

    with (st.container(border=True)):
        st_pyecharts(
            chart=chart,
            height=f"{height}px"
        )

    return None


def draw_line_chart(data: pd.DataFrame | dict, title: str, x_axis: list, label_list: list, height=0, is_symbol_show=True) -> None:
    if height == 0:
        height = int(get_monitors()[0].height / 1080) * 350

    if isinstance(data, dict):
        chart_data = data
    elif isinstance(data, pd.DataFrame):
        return None
    else:
        return None

    chart = Line()

    chart.add_xaxis(x_axis)

    for label in label_list:
        chart.add_yaxis(label, [item[1] for item in data[label]], is_connect_nones=True, is_symbol_show=is_symbol_show)

    chart.set_global_opts(title_opts=opts.TitleOpts(title=title))

    st_pyecharts(
        chart=chart,
        height=f"{height}px"
    )

    return None


def draw_horizontal_bar_chart(data: pd.DataFrame | dict, x_axis: str, y_axis: str, label: str) -> None:

    st.bar_chart(data=data, x=x_axis, y=y_axis, color=label, horizontal=True, height=100*data['年份'].nunique())


def draw_unstack_bar_chart(data: pd.DataFrame | dict, x_axis: str, y_axis: str, label: str) -> None:
    st.bar_chart(data=data, x=x_axis, y=y_axis, color=label, stack=False)


# def draw_1col_bar(data: dict, title: str, height=0):
#
#     if height == 0:
#         height = int(get_monitors()[0].height / 1080) * 350
#
#     with st.container(border=True):
#         st_pyecharts(
#             chart=(
#                 Bar()
#                 .add_xaxis([keys for keys in data.keys()])
#                 .add_yaxis("总人数", [values for values in data.values()])
#                 .set_series_opts(label_opts=opts.LabelOpts(position="top"))
#                 .set_global_opts(title_opts=opts.TitleOpts(title=title),
#                                  legend_opts=opts.LegendOpts(is_show=False),
#                                  datazoom_opts=opts.DataZoomOpts(is_show=True, range_start=0, range_end=100),
#                                  visualmap_opts=opts.VisualMapOpts(is_show=False,
#                                                                    max_=max([values for values in data.values()])))
#             ),
#             height=f"{height}px"
#         )


# def draw_2col_bar(data: dict, title: str, height=0, end=70):
#
#     if height == 0:
#         height = int(get_monitors()[0].height / 1080) * 350
#
#     with st.container(border=True):
#         st_pyecharts(
#             chart=(
#                 Bar()
#                 .add_xaxis([keys for keys in data.keys()])
#                 .add_yaxis("总人数", [values for values in data.values()])
#                 .set_series_opts(label_opts=opts.LabelOpts(position="top"))
#                 .set_global_opts(title_opts=opts.TitleOpts(title=title),
#                                  legend_opts=opts.LegendOpts(is_show=False),
#                                  datazoom_opts=opts.DataZoomOpts(is_show=True, range_start=0, range_end=end),
#                                  visualmap_opts=opts.VisualMapOpts(is_show=True, pos_right="1%", pos_top="30%",
#                                                                    max_=max([values for values in data.values()])))
#             ),
#             height=f"{height}px"
#         )


def draw_dataframe(data, hide_index=True, width=1920, height=-1) -> None:
    if height == -1:
        height = int(get_monitors()[0].height / 1080) * 388  # 可以取350、388

    st.dataframe(
        data=data,
        height=height,
        width=width,
        hide_index=hide_index
    )


def draw_word_cloud_chart(words: list, title: str, height=-1, height_factor=1300, shape="circle") -> None:
    if height == -1:
        height = int(get_monitors()[0].height / 1080) * height_factor  # 可以取350、388

    st_pyecharts(
        chart=(
            WordCloud()
            .add(series_name=title, data_pair=words, word_size_range=[25, 40], shape=shape, width="1400px",
                 height=f"{height_factor + 50}px", pos_top="2%")
            # .set_global_opts(title_opts=opts.TitleOpts(title=title))
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=title, title_textstyle_opts=opts.TextStyleOpts(font_size=40), pos_left="center", pos_top="2%"
                ),
            )
            # .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
        ),
        height=f"{height}px"
    )


def load_json_data(folder: str, file_name: str) -> dict:
    # 读取现有json文件
    with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\{folder}\{file_name}.json",
              "r", encoding="UTF-8") as f:
        json_data = json.load(f)

    return json_data


def save_json_data(json_data: dict, folder: str, file_name: str) -> None:
    with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\{folder}\{file_name}.json",
              "w", encoding="UTF-8") as f:
        # 将生成的数据保存至json文件中
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    return None


# 用来插入st.write_stream的数据
def stream_data(sentence: str, delay=0.015) -> str:
    for word in sentence:
        yield word
        time.sleep(delay)


# 用来简化校名
def simplify_school_name(dict1: dict) -> dict:
    temp = [item for item in dict1.items()]
    temp_item = ""
    output = []

    for item in temp:
        temp_item = item[0]

        if len(temp_item) > 6 and temp_item[0:6] == "广州市白云区":
            temp_item = temp_item[6:]

        if len(temp_item) > 3 and temp_item[0:3] == "广州市":
            temp_item = temp_item[3:]

        if len(temp_item) > 3 and temp_item[0:3] == "广州市":
            temp_item = temp_item[3:]

        if len(temp_item) > 2 and temp_item[0:2] == "广州":
            temp_item = temp_item[2:]

        if len(temp_item) > 2 and temp_item[0:2] == "学校":
            temp_item = temp_item[2:]

        if len(temp_item) > 2 and temp_item[-2:] == "学校":
            temp_item = temp_item[:-2]

        output.append([temp_item, item[1]])

    output_dict = {}

    for item in output:
        output_dict[item[0]] = item[1]

    return output_dict


def count_empty_values(lst: list) -> int:
    count = 0

    for item in lst:
        if item is None or item == '' or item == [] or item == {} or item == ():
            count += 1
            # 如果需要处理其他类型的空值，可以在这里添加条件
            # 例如：elif isinstance(item, list) and not item:
            #          count += 1

    return count


# 初始化软件所有session_state变量，仅在主页使用
def session_state_initial() -> None:
    # page1数据大屏的按钮和具体信息展示
    if 'page1_show_detail' not in st.session_state:
        st.session_state.page1_show_detail = False

    # page4中的展示判断符
    if 'page4_search_flag' not in st.session_state:
        st.session_state.page4_search_flag = False

    # page4中的在编展示判断符
    if 'page4_kind_0_flag' not in st.session_state:
        st.session_state.page4_kind_0_flag = False

    # page4中的编外展示判断符
    if 'page4_kind_1_flag' not in st.session_state:
        st.session_state.page4_kind_1_flag = False


def reset_others(page: int) -> None:
    if page != 1:
        st.session_state.page1_show_detail = False

    if page != 2:
        pass

    if page != 3:
        pass

    if page != 4:
        st.session_state.page4_search_flag = False
        st.session_state.page4_kind_0_flag = False
        st.session_state.page4_kind_1_flag = False


def reset_self(page: int) -> None:
    # 重置所有页面变量
    match page:

        case 4:
            st.session_state.page4_search_flag = False
            st.session_state.page4_kind_0_flag = False
            st.session_state.page4_kind_1_flag = False

        case _:
            pass


def session_state_reset(page: int) -> None:
    # 刷新其他页面
    reset_others(page=page)

    # 重置本页面信息
    # reset_self(page=page)


def page1_show_detail_info() -> None:
    st.session_state.page1_show_detail = True


def page1_hide_detail_info() -> None:
    st.session_state.page1_show_detail = False
