import json
import time

import pyecharts.options as opts
import streamlit as st
from pyecharts.charts import Bar
from pyecharts.charts import Pie
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
    "小学": "小学"
}


# 用来检查module模块是否被正确import
def hello():
    return "hello world"


# 设置页面全局属性
def set_page_configuration(title: str, icon: str):
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout='wide'
    )


def draw_pie(data: dict, title: str, height=0, formatter="{b}:{d}%", pos_left='20%'):

    if height == 0:
        height = int(get_monitors()[0].height / 1080) * 350

    with st.container(border=True):
        st_pyecharts(
            chart=(
                Pie()
                .add("", [(k, v) for k, v in data.items()],
                     center=["50%", "60%"], radius="65%", percent_precision=1)
                .set_global_opts(title_opts=opts.TitleOpts(title=title),
                                 legend_opts=opts.LegendOpts(pos_left=pos_left))
                .set_series_opts(label_opts=opts.LabelOpts(formatter=formatter))
                # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}, {d}%"))
            ),
            height=f"{height}px"
        )


# 画之前先测试下有没有问题
def draw_multi_pie(inner_data: dict, outer_data: dict, title: str, height=0, formatter="{b}:{d}%"):

    if height == 0:
        height = int(get_monitors()[0].height / 1080) * 350

    with st.container(border=True):
        st_pyecharts(
            chart=(
                Pie()
                .add(
                    series_name="1",
                    data_pair=inner_data,
                    radius=["15%", "30%"],
                    label_opts=opts.LabelOpts(position="outside"),
                )
                .add(
                    series_name="2",
                    radius=["50%", "65%"],
                    data_pair=outer_data,
                    label_opts=opts.LabelOpts(
                        position="outside",
                    ),
                )
                .set_global_opts(tooltip_opts=opts.TooltipOpts(is_show=False))
                .set_series_opts(
                    tooltip_opts=opts.TooltipOpts(
                        trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
                    )
                )
            ),
            height=f"{height}px"
        )


def draw_1col_bar(data: dict, title: str, height=0):

    if height == 0:
        height = int(get_monitors()[0].height / 1080) * 350

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
        height = int(get_monitors()[0].height / 1080) * 350

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


def draw_dataframe(data, hide_index=True, width=1920, height=-1):

    if height == -1:
        height = int(get_monitors()[0].height / 1080) * 388  # 可以取350、380

    st.dataframe(
        data=data,
        height=height,
        width=width,
        hide_index=hide_index
    )


def load_json_data(file_name: str):

    # 读取现有json文件
    with open(fr"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\result\{file_name}.json",
              "r", encoding="UTF-8") as file:
        json_data = json.load(file)

    return json_data


def save_json_data(json_data: dict, file_name: str):

    with open(fr"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\result\{file_name}.json",
              "w", encoding="UTF-8") as file:
        # 将生成的数据保存至json文件中
        json.dump(json_data, file, indent=4, ensure_ascii=False)

    return 0


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
def stream_data(sentence: str, delay=0.015):
    for word in sentence:
        yield word
        time.sleep(delay)


# 用来简化校名
def simplify_school_name(dict1: dict):
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


def session_state_initial():

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


def reset_others(page: int):

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


def reset_self(page: int):

    match page:

        case 4:
            st.session_state.page4_search_flag = False
            st.session_state.page4_kind_0_flag = False
            st.session_state.page4_kind_1_flag = False

        case _:
            pass


def session_state_reset(page: int):

    # 刷新其他页面
    reset_others(page=page)

    # 重置本页面信息
    reset_self(page=page)


def page1_show_detail_info():
    st.session_state.page1_show_detail = True


def page1_hide_detail_info():
    st.session_state.page1_show_detail = False

