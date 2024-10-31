import json
import time
import sqlite3
import pandas as pd
import pyecharts.options as opts
import streamlit as st
import re

from pathlib import Path
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Pie
from pyecharts.charts import WordCloud
from screeninfo import get_monitors
from streamlit_echarts import st_pyecharts
from typing import Tuple


def get_kind_list() -> list:
    """

    :return: ["在编", "编外"]
    """
    return ["在编", "编外"]


def get_end_dict() -> dict:
    """

    :return: {"高中": 70,"初中": 70,"小学": 70,"幼儿园": 95}
    """
    return {
        "高中": 70,
        "初中": 70,
        "小学": 70,
        "幼儿园": 95
    }


def get_trans_period() -> dict:
    """

    :return: {"所有学段": None,"高中": "高中","初中": "初中","小学": "小学",None: None}
    """
    return {
        "所有学段": None,
        "高中": "高中",
        "初中": "初中",
        "小学": "小学",
        None: None
    }


def print_color_text(text: str | int | float, color_code='\033[1;91m', reset_code='\033[0m') -> None:
    """
    输出带颜色的字符串，可以用于控制台警告
    :param text: 输出的文本
    :param color_code: 颜色起始代码
    :param reset_code: 颜色结束代码
    :return: 无
    """

    print(f"{color_code} {str(text)} {reset_code}")

    return None


def get_database_name() -> str:
    """
    根据database_basic_info.json获取数据库名
    :return: 数据库名
    """

    with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\database\database_basic_info.json",
              "r", encoding='UTF-8') as file:  # ISO-8859-1
        loaded_data = json.load(file)

    database_name = loaded_data["database_name"]

    return database_name


def connect_database() -> Tuple[sqlite3.Cursor, sqlite3.Connection]:
    """
    用于连接数据库
    :return:
    """

    conn = sqlite3.connect(
        fr"{Path(__file__).resolve().parent.parent.parent}\database\{get_database_name()}"
    )
    c = conn.cursor()

    return c, conn


def disconnect_database(conn) -> None:
    """
    用于断开数据库
    :param conn:
    :return:
    """

    conn.close()

    return None


def execute_sql_sentence(sentence: str,) -> list:
    """
    执行数据库语句并返回列表
    :param sentence: 需要执行的语句
    :return:
    """

    c, conn = connect_database()

    result = []
    try:
        c.execute(sentence)
        result = c.fetchall()

    except Exception as e:
        print_color_text(text=str(e))

    disconnect_database(conn=conn)

    return result


def del_tuple_in_list(data: list) -> list:
    """
    将形如[('1',), ('2',), ('3',),]的数据转化为[1, 2, 3,]
    :param data:带有元组的列表
    :return: 清洗后的列表
    """

    if not isinstance(data[0], tuple):
        return data

    output = []

    for single_data in data:
        output.append(single_data[0])

    return output


def sort_dataframe_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    将给定的dataframe按照列名重新排序，汉字在前，数字在后且从小到大（即使数字在列名中为文本格式）
    :param df: 需要重新排序的数据
    :return:
    """
    return df[[col for col in df.columns if re.match(r'[\u4e00-\u9fff]+', col)] + sorted([col for col in df.columns if col.isdigit()], key=int)]


def smallest_multiple_of_n_geq(number: int, n: int) -> int:
    """
    返回比输入值大的最小的n的倍数
    :param number:
    :param n:
    :return:
    """
    if number % n == 0:
        return number
    else:
        return (number // n + 1) * n


def set_page_configuration(title: str, icon: str) -> None:
    """
    设置页面全局属性
    :param title: 标签页标题
    :param icon: 标签页图表
    :return:
    """
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout='wide'
    )

    return None


# 切记画图的代码顺序是先插入数据再set样式！
def draw_pie_chart(data: pd.DataFrame | dict, title: str, height=0, formatter="{b}:{d}%", pos_left='20%',
                   center_to_bottom='60%') -> None:
    """
    绘制饼图
    :param data: 绘图所用数据
    :param title: 图表标题
    :param height: 图标高度
    :param formatter: 图表标签形式
    :param pos_left: 图表离左侧间距，百分比，如"20%"
    :param center_to_bottom: 图标中心离底部间距，百分比，如"60%"
    :return:
    """

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
    """
    绘制两层饼图
    :param inner_data: 内圈数据
    :param outer_data: 外圈数据
    :param title: 图表标题
    :param height: 图表高度
    :param formatter: 图表标签形式
    :return:
    """

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
    """
    绘制柱状图
    :param data: 绘图所用数据
    :param title: 图表标题
    :param height: 图表高度，默认根据分辨率自适应
    :param end: 图标下方动态进度条最大值
    :param is_show_visual_map: 是否显示动态进度条
    :return:
    """

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


def draw_line_chart(data: pd.DataFrame | dict, title: str, x_axis: list, label_list: list, height=0,
                    is_symbol_show=True) -> None:
    """
    绘制折线图
    :param data: 绘图所用数据
    :param title: 图表标题
    :param x_axis: x轴字段
    :param label_list: 不同折线对应的label
    :param height: 图表高度，默认根据分辨率自适应
    :param is_symbol_show: 是否在数据点上显示数值
    :return:
    """

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
    """
    绘制streamlit原生水平柱状图
    :param data: 绘图所用数据
    :param x_axis: x轴名称
    :param y_axis: y轴名称
    :param label: 柱状数据对应标签
    :return:
    """

    st.bar_chart(data=data, x=x_axis, y=y_axis, color=label, horizontal=True, height=100 * data['年份'].nunique())


def draw_unstack_bar_chart(data: pd.DataFrame | dict, x_axis: str, y_axis: str, label: str) -> None:
    """
    绘制streamlit原生不堆叠的柱状图
    :param data: 绘图所用数据
    :param x_axis: x轴名称
    :param y_axis: y轴名称
    :param label: 柱状数据对应标签
    :return:
    """
    st.bar_chart(data=data, x=x_axis, y=y_axis, color=label, stack=False)


def draw_mixed_bar_and_line(df: pd.DataFrame, x_list: list[str | int],
                            label_column: str,
                            bar_axis_label: str, line_axis_label: str,
                            bar_axis_max_factor: int = 2, line_axis_max_factor: int = 1.25,
                            height: int = 0, line_label: str | None = None, formatter: str = "{value}") -> None:
    """
    根据dataframe的数据生成一个柱状图和折线图并存的图表\n
    df格式：\n
    label列名  x1 x2 x3\n
    label1    y1 y2 y3\n
    label2    y4 y5 y6\n
    如果要对label3做折线图，line_label=label3\n
    label3    y7 y8 y9\n
    line_label不填则自动加一条求和汇总行作为折线图
    :param df: 数据表
    :param x_list: x轴坐标列表list[int]
    :param label_column: 标签列的列名，这一列用于告诉图表柱状图每一条柱是谁的数据
    :param bar_axis_label: 左侧柱状图坐标轴名
    :param line_axis_label: 右侧柱状图坐标轴名
    :param bar_axis_max_factor: 柱状图坐标轴最高值系数
    :param line_axis_max_factor: 折线图坐标轴最高值系数
    :param height: 图表高度
    :param line_label: 折线图对应标签，若为空则自动统计对于x的求和
    :param formatter: 坐标轴单位
    :return:
    """

    # 处理一下可能存在的空值
    df.fillna(value=0, inplace=True)

    if label_column not in df.columns.to_list():
        print_color_text(text="未在df数据中找到标签列 （draw_mixed_bar_and_line()）")
        return None

    if None in df[label_column].to_list():
        print_color_text(text="df数据标签列中包含空值 （draw_mixed_bar_and_line()）")
        return None

    if line_label is not None and line_label not in df[label_column].drop_duplicates().to_list():
        print_color_text(text="未在df数据标签列中找到折线图对应行标签 （draw_mixed_bar_and_line()）")
        return None

    if height == 0:
        height = int(get_monitors()[0].height / 1080) * 720

    bar_chart = Bar()
    bar_chart.add_xaxis(xaxis_data=x_list)

    for label in df[label_column].drop_duplicates().to_list():
        if label != line_label:
            bar_chart.add_yaxis(
                series_name=label,
                y_axis=df[df[df.columns[0]] == label].drop(columns=label_column, axis=1).iloc[0].tolist(),
                label_opts=opts.LabelOpts(is_show=False),
            )

    line_chart = Line()
    line_chart.add_xaxis(xaxis_data=x_list)
    line_chart.add_yaxis(
        series_name="合计" if line_label is None else line_label,
        yaxis_index=1,
        y_axis=df[df.columns.difference([label_column])].sum().tolist() if line_label is None else
        df[df[label_column] == line_label].drop(columns=[label_column]).iloc[0].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
    )

    bar_chart.set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            is_show=True, trigger="axis", axis_pointer_type="cross"
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
        ),
        yaxis_opts=opts.AxisOpts(
            name=bar_axis_label,
            type_="value",
            min_=0,
            max_=smallest_multiple_of_n_geq(
                number=int(
                    bar_axis_max_factor * int(
                        df.drop(columns=label_column, axis=1).values.max() if line_label is None else
                        df[df[label_column] != line_label].drop(columns=label_column, axis=1).values.max()
                    )
                ),
                n=100
            ),
            interval=smallest_multiple_of_n_geq(
                number=int(
                    bar_axis_max_factor * int(
                        df.drop(columns=label_column, axis=1).values.max() if line_label is None else
                        df[df[label_column] != line_label].drop(columns=label_column, axis=1).values.max()
                    )
                ),
                n=100
            ) / 10,
            axislabel_opts=opts.LabelOpts(formatter=formatter),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )

    bar_chart.extend_axis(
        yaxis=opts.AxisOpts(
            name=line_axis_label,
            type_="value",
            min_=0,
            max_=smallest_multiple_of_n_geq(
                number=int(
                    line_axis_max_factor * int(
                        df.drop(columns=label_column, axis=1).sum().max() if line_label is None else
                        df[df[label_column] != line_label].drop(columns=label_column, axis=1).sum().max()
                    )
                ),
                n=100
            ),
            interval=smallest_multiple_of_n_geq(
                number=int(
                    line_axis_max_factor * int(
                        df.drop(columns=label_column, axis=1).sum().max() if line_label is None else
                        df[df[label_column] != line_label].drop(columns=label_column, axis=1).sum().max()
                    )
                ),
                n=100
            ) / 10,
            axislabel_opts=opts.LabelOpts(formatter=formatter),
        )
    )

    bar_chart.overlap(line_chart)

    with st.container(border=True):
        st_pyecharts(bar_chart, height=f"{height}px")


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


def draw_dataframe(data: pd.DataFrame = None, hide_index=True, width=1920, height=-1) -> None:
    """
    绘制streamlit原生dataframe表格
    :param data: 绘制的内容
    :param hide_index: 是否隐藏最左侧序号列
    :param width: 宽度，默认1920
    :param height: 高度，默认388（标题行+12行数据）
    :return:
    """

    if height == -1:
        height = int(get_monitors()[0].height / 1080) * 388  # 可以取350、388

    st.dataframe(
        data=data,
        height=height,
        width=width,
        hide_index=hide_index
    )


def draw_word_cloud_chart(words: list, title: str, height=-1, height_factor=1300, shape="circle") -> None:
    """
    绘制词云图
    :param words: 词列表，以出现频率作为数值
    :param title: 图表标题
    :param height: 图表高度，默认按照相对高度设置
    :param height_factor: 图表相对高度，默认1300
    :param shape: 词云图形状，默认圆形
    :return:
    """

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
    """
    根据文件夹名和json文件名读取json文件中的数据
    :param folder: json_file下的文件夹名
    :param file_name: 文件夹内的json文件名（不带json后缀）
    :return: dict型数据
    """

    json_data = {}

    try:
        with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\{folder}\{file_name}.json",
                  "r", encoding="UTF-8") as f:
            json_data = json.load(f)

    except Exception as e:
        print_color_text(text=f"{e}")

    finally:
        return json_data


def save_json_data(json_data: dict, folder: str, file_name: str) -> None:
    """
    将dict数据保存至json_file下某个文件夹下的json文件中
    :param json_data: 需要保存的dict数据
    :param folder: json_file下的文件夹名
    :param file_name: json文件名，不需要带.json后缀
    :return:
    """

    with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\{folder}\{file_name}.json",
              "w", encoding="UTF-8") as f:
        # 将生成的数据保存至json文件中
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    return None


# 用来插入st.write_stream的数据
def stream_data(sentence: str, delay=0.015) -> str:
    """
    用于分批输出数据，配合st.write_stream()实现逐条一个个字生成的效果
    :param sentence: 需要输出的语句
    :param delay: 字间时间延迟
    :return:
    """
    for word in sentence:
        yield word
        time.sleep(delay)


def simplify_school_name(dict1: dict) -> dict:
    """
    简化校名（对于输入的字典只化简key的校名）
    :param dict1: 校名数据，形如：{'广州市培英中学': ['124401114553841006', '完全中学', '直管', 412, 0, 412], '广州市第六十五中学': ['12440111455384127X', '完全中学', '直管', 349, 0, 349],}
    :return: 返回化简后的字典，只有每一个校名key被修改了，value不变
    """
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
    """
    判断列表中空值的数量，空值包括None，""，空列表，空字典，空元组等
    :param lst: 需要查空的列表
    :return:
    """
    count = 0

    for item in lst:
        if item is None or item == '' or item == [] or item == {} or item == ():
            count += 1
            # 如果需要处理其他类型的空值，可以在这里添加条件
            # 例如：elif isinstance(item, list) and not item:
            #          count += 1

    return count


def session_state_initial() -> None:
    """
    初始化软件所有session_state变量，仅在主页使用
    :return:
    """
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
    """
    重置其他页的session_state变量
    :param page: 当前页标签
    :return:
    """
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
    """
    重置本页面session_state变量
    :param page: 当前页标签
    :return:
    """

    match page:

        case 4:
            st.session_state.page4_search_flag = False
            st.session_state.page4_kind_0_flag = False
            st.session_state.page4_kind_1_flag = False

        case _:
            pass


def session_state_reset(page: int) -> None:
    """
    重置所有页面的session_state变量
    :param page: 当前页标签
    :return:
    """

    # 刷新其他页面
    reset_others(page=page)

    # 重置本页面信息
    # reset_self(page=page)


def page1_show_detail_info() -> None:
    """
    page1中展开信息按钮绑定的函数
    :return:
    """
    st.session_state.page1_show_detail = True


def page1_hide_detail_info() -> None:
    """
    page1中收起信息按钮绑定的函数
    :return:
    """
    st.session_state.page1_show_detail = False
