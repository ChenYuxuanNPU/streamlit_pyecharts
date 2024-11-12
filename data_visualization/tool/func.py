import json
import re
import sqlite3
import time
from pathlib import Path
from typing import Literal, Iterable

import pandas as pd
import pyecharts.options as opts
import streamlit as st
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Pie
from pyecharts.charts import WordCloud
from screeninfo import get_monitors
from streamlit_echarts import st_pyecharts


def get_kind_list() -> list[str]:
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


def connect_database() -> tuple[sqlite3.Cursor, sqlite3.Connection]:
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


def execute_sql_sentence(sentence: str, ) -> list:
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


def array_to_dataframe(array: list, index_label: str | int = 0) -> pd.DataFrame:
    """
    将二维列表转换为dataframe，其中子列表首项为列名，次项为数据
    :param array: 待转换的二维列表，要求子列表长度为2
    :param index_label: 希望的dataframe行名
    :return:
    """

    columns = [row[0] for row in array]
    values = [row[1] for row in array]

    data_dict = {columns[i]: [values[i]] for i in range(len(columns))}

    return pd.DataFrame(data_dict, index=[index_label])


def sort_dataframe_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    将给定的dataframe按照列名重新排序，汉字在前，数字在后且从小到大（即使数字在列名中为文本格式）
    :param df: 需要重新排序的数据
    :return:
    """
    return df[[col for col in df.columns if re.match(r'[\u4e00-\u9fff]+', col)] + sorted(
        [col for col in df.columns if col.isdigit()], key=int)]


def get_growth_rate_from_one_row_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    用于计算年间增长率，示例如下：\n
    原dataframe：\n
    index   year1   year2   year3\n
    index   data1   data2   data3\n
    结果如下：\n
    index   year2   year3\n
    0       rate2   rate3\n
    :param df: 用于计算增长率的数据，列名为年份，只有一行且不考虑index取值
    :return: 返回增长率dataframe（不包含首年）
    """
    """
    df_dict:{
    "2024": 200,
    "2023": 100
    }
    """
    df = sort_dataframe_columns(df=df)
    df.reset_index(drop=True, inplace=True)
    df_dict = df.to_dict()

    output = {}
    for i in range(1, len(df_dict.keys())):
        this_year = list(df_dict.keys())[i]
        last_year = list(df_dict.keys())[i - 1]

        output[this_year] = {0: round(100 * (df_dict[this_year][0] / df_dict[last_year][0] - 1), 2)}

    return pd.DataFrame(output)


def get_growth_rate_from_multi_rows_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    用于计算年间增长率，示例如下：\n
    原dataframe：\n
    index   label1   label2   label3\n
    year1   data1   data2   data3\n
    year2   data4   data5   data6\n
    结果如下：\n
    index   label1   label2 label3\n
    year1   rate1   rate2    rate3\n
    year2   rate4   rate5    rate6\n
    :param df: 用于计算增长率的数据，列名为年份，只有一行且不考虑index取值
    :return: 返回增长率dataframe（不包含首年）
    """
    """
    df_dict:{
    "2024":{
        25:100,
        26:200
        },
    "2023"：{
        25：50，
        24：100
        }
    }
    """

    df_dict = df.to_dict()
    # print(df_dict)
    # print(df.index.tolist())
    output = {}

    for i in range(1, len(df.index.tolist())):
        this_year = df.index.tolist()[i]
        last_year = df.index.tolist()[i - 1]

        # print(f"this_year:{this_year}")

        output[f"{last_year[-2:]}-{this_year[-2:]}年增长率"] = {}
        # print(output)

        for column in df.columns:
            if df_dict[column][this_year] != 0 and df_dict[column][last_year] != 0:
                output[f"{last_year[-2:]}-{this_year[-2:]}年增长率"][column] = round(
                    100 * (df_dict[column][this_year] / df_dict[column][last_year] - 1), 2)
            else:
                output[f"{last_year[-2:]}-{this_year[-2:]}年增长率"][column] = 0.00

    return pd.DataFrame(output).T


def is_sublist(subset: Iterable, superset: Iterable) -> bool:
    """
    判断subset是否为superset的子集
    :param subset: 判断的子集
    :param superset: 判断的全集
    :return:
    """
    return set(subset).issubset(set(superset))


def max_dict_depth(d: dict, depth=1):
    """
    统计字典最大深度
    :param d: 待求字典
    :param depth: 用于递归的参数，别填
    :return:
    """
    # 使用列表推导式找到所有嵌套字典的最大深度
    child_depths = [max_dict_depth(value, depth + 1) for value in d.values() if isinstance(value, dict)]

    # 如果child_depths为空，说明没有嵌套字典，直接返回当前深度
    if not child_depths:
        return depth

    # 否则，返回嵌套字典中的最大深度
    return max(child_depths)


def convert_dict_to_dataframe(d: dict) -> pd.DataFrame:
    """
    将两层的嵌套字典转换为pd.Dataframe
    :param d: 输入的字典\n
    两层字典：第一层为行名，第二层为列名\n
    :return:
    """
    """
    df_dict:{
    "2024":{
        25:100,
        26:200
        },
    "2023"：{
        25：50，
        24：100
        }
    }
    """
    if max_dict_depth(d=d) == 2:
        return pd.DataFrame.from_dict(d, orient='index')

    else:
        return pd.DataFrame()


def smallest_multiple_of_n_geq(number: int | float, n: int | float) -> float:
    """
    返回大于等于输入值的最小的n的倍数,返回值被强制类型转换为float以应对n为小数的情况
    :param number: 输入值
    :param n: 倍数因子
    :return:
    """
    if number % n == 0:
        return float(number)
    else:
        return float((number // n + 1) * n)


def calculate_figure_border(number: int | float, n: int | float) -> float:
    """
    根据输入的图表极值设定大于等于该正值或小于等于该负值的最小/大的图表边界\n
    示例（n=10）：\n
    25 -> 30, 30 -> 30, -5 -> -10, -10 -> -10
    :param number: 输入值
    :param n: 倍数因子
    :return:
    """

    if number == 0:
        return 0

    if number > 0:
        return smallest_multiple_of_n_geq(number=number, n=n)

    if number < 0:
        return -1 * smallest_multiple_of_n_geq(number=abs(number), n=n)


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


def draw_line_chart(data: pd.DataFrame | dict, title: str,
                    x_axis: list = None, label_list: list = None,
                    mark_line_y: int = None,
                    formatter: str = "{value}",
                    height=350, is_symbol_show=True, ) -> None:
    """
    绘制折线图
    :param data: 绘图所用数据
    :param title: 图表标题
    :param x_axis: x轴字段
    :param label_list: 不同折线对应的label
    :param mark_line_y: 标记线绝对高度
    :param formatter: 坐标轴单位
    :param height: 图表高度，默认根据分辨率自适应
    :param is_symbol_show: 是否在数据点上显示数值
    :return:
    """

    height = int(get_monitors()[0].height / 1080) * height

    chart = Line()

    if isinstance(data, dict) and x_axis is not None and label_list is not None:

        chart.add_xaxis(x_axis)

        for label in label_list:
            chart.add_yaxis(series_name=label,
                            y_axis=[item[1] for item in data[label]],
                            is_connect_nones=True, is_symbol_show=is_symbol_show,
                            markline_opts=opts.MarkLineOpts(
                                data=[opts.MarkLineItem(y=mark_line_y, symbol="none")], symbol="none",
                                label_opts=opts.LabelOpts(is_show=True if mark_line_y == 0 else False,
                                                          distance=5),
                                linestyle_opts=opts.LineStyleOpts(color="grey", type_="dashed")
                            ) if mark_line_y is not None else None
                            )

    elif isinstance(data, pd.DataFrame):

        chart.add_xaxis(data.columns.tolist())

        for label in data.index:
            chart.add_yaxis(series_name=label,
                            y_axis=data.loc[label].tolist(),
                            is_connect_nones=True, is_symbol_show=is_symbol_show,
                            markline_opts=opts.MarkLineOpts(
                                data=[opts.MarkLineItem(y=mark_line_y, symbol="none")], symbol="none",
                                label_opts=opts.LabelOpts(is_show=True if mark_line_y == 0 else False,
                                                          distance=5),
                                linestyle_opts=opts.LineStyleOpts(color="grey", type_="dashed")
                            ) if mark_line_y is not None else None
                            )

    else:
        return None

    chart.set_global_opts(title_opts=opts.TitleOpts(title=title),
                          yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter=formatter))
                          )

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


def get_mixed_bar_and_yaxis_opts(max_: int | float | None, data_max: int | float | None, min_: int | float | None,
                                 data_min: int | float | None, kind: Literal["bar", "line"], n: int)\
                                 -> tuple[int | float, int | float, int | float,]:
    """
    返回柱状-折线图坐标轴所需数据
    :param max_: 强制坐标轴最大值
    :param data_max: 坐标轴对应数据最大值
    :param min_: 强制坐标轴最小值
    :param data_min: 坐标轴对应数据最小值
    :param kind: 图表类型（柱状或折线）
    :param n: 坐标轴分段数
    :return: [坐标轴最大值， 坐标轴最小值， 坐标轴间隔（）]
    """
    match kind:
        case "line":
            axis_max = max_ if max_ is not None else calculate_figure_border(number=data_max, n=50)
            axis_min = min_ if min_ is not None else 2 * calculate_figure_border(number=data_min, n=50) - axis_max
        case "bar":
            axis_max = max_ if max_ is not None else 2 * calculate_figure_border(number=data_max, n=50)
            axis_min = min_ if min_ is not None else 0

        case _:
            raise ValueError('kind not in ["bar", "line"]')

    return axis_max, axis_min, (axis_max - axis_min) / n


def draw_mixed_bar_and_line(df_bar: pd.DataFrame, df_line: pd.DataFrame,
                            bar_axis_label: str, line_axis_label: str,
                            bar_max_: int | float = None, bar_min_: int | float = None,
                            line_max_: int | float = None, line_min_: int | float = None,
                            mark_line_y: int = None, mark_line_type: Literal["min", "max", "average"] = None,
                            mark_line_label_is_show: bool = False,
                            height: int | float = 0,
                            bar_formatter: str = "{value}", line_formatter: str = "{value}") -> None:
    """
    根据dataframe的数据生成一个柱状图和折线图并存的图表\n
    df_bar格式：\n
    index     x1 x2 x3\n
    label1    y1 y2 y3\n
    label2    y4 y5 y6\n
    df_line格式(index应该与df_bar的index相同)：\n
    index     x1 x2 x3\n
    label3    y7 y8 y9\n
    label4    y10 y11 y12\n
    图表最大值默认设置：分别以大于等于图表最大值的最小50的公倍数（普通数据）或0.5的公倍数（小数或比率）作为图表最大值，其中factor项用于调整bar和line的相对位置
    :param df_bar: 柱状图数据表
    :param df_line: 折线图数据表
    :param bar_axis_label: 左侧柱状图坐标轴名
    :param line_axis_label: 右侧柱状图坐标轴名
    :param bar_max_: 柱状图强制最大值
    :param bar_min_: 柱状图强制最小值
    :param line_max_: 折线图强制最大值
    :param line_min_: 折线图强制最小值
    :param mark_line_y: 折线图标记线高度（高优先级）
    :param mark_line_type: 折线图标记线类型（str，可填"min"/"max"/"average"，低优先级）
    :param mark_line_label_is_show: 是否展示markline的label
    :param height: 图表高度
    :param bar_formatter: 柱状图坐标轴单位
    :param line_formatter: 折线图坐标轴单位
    :return:
    """

    # 处理一下可能存在的空值
    df_bar.fillna(value=0, inplace=True)
    df_line.fillna(value=0, inplace=True)

    if df_bar.columns.tolist() != df_line.columns.tolist():
        print_color_text(df_bar.columns.tolist())
        print_color_text(df_line.columns.tolist())
        print_color_text(text="两个dataframe数据列不相同")
        return None

    if height == 0:
        height = int(get_monitors()[0].height / 1080) * 720

    bar_chart = Bar()
    bar_chart.add_xaxis(xaxis_data=df_bar.columns)
    bar_max, bar_min, bar_interval = get_mixed_bar_and_yaxis_opts(max_=bar_max_, data_max=df_bar.values.max(),
                                                                  min_=bar_min_, data_min=df_bar.values.min(),
                                                                  kind="bar", n=10)

    for label in df_bar.index:
        bar_chart.add_yaxis(
            series_name=label,
            y_axis=df_bar.loc[label].tolist(),
            label_opts=opts.LabelOpts(is_show=False),
        )

    line_chart = Line()
    line_chart.add_xaxis(xaxis_data=df_line.columns)
    line_max, line_min, line_interval = get_mixed_bar_and_yaxis_opts(max_=line_max_, data_max=df_line.values.max(),
                                                                     min_=line_min_, data_min=df_line.values.min(),
                                                                     kind="line", n=10)

    if mark_line_y is not None:

        for line in df_line.index:
            line_chart.add_yaxis(
                series_name=line,
                yaxis_index=1,
                y_axis=df_line.loc[line].tolist(),
                label_opts=opts.LabelOpts(is_show=False),
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(y=mark_line_y, symbol="none")], symbol="none",
                    label_opts=opts.LabelOpts(is_show=mark_line_label_is_show, distance=5),
                    linestyle_opts=opts.LineStyleOpts(color="grey", type_="dashed"))
                # MarkLineItem中的symbol代表标记线开始侧标记，MarkLineOpts中的symbol代表标记线结束侧标记
            )

    elif mark_line_type in ["min", "max", "average"]:

        for line in df_line.index:
            line_chart.add_yaxis(
                series_name=line,
                yaxis_index=1,
                y_axis=df_line.loc[line].tolist(),
                label_opts=opts.LabelOpts(is_show=False),
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(type_=mark_line_type, symbol="none")],
                    symbol="none", label_opts=opts.LabelOpts(is_show=mark_line_label_is_show),
                    linestyle_opts=opts.LineStyleOpts(color="grey", type_="dashed"))
                # MarkLineItem中的symbol代表标记线开始侧标记，MarkLineOpts中的symbol代表标记线结束侧标记
            )
    else:

        for line in df_line.index:
            line_chart.add_yaxis(
                series_name=line,
                yaxis_index=1,
                y_axis=df_line.loc[line].tolist(),
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
            max_=bar_max,
            min_=bar_min,
            interval=bar_interval,
            axislabel_opts=opts.LabelOpts(formatter=bar_formatter),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )

    bar_chart.extend_axis(
        yaxis=opts.AxisOpts(
            name=line_axis_label,
            type_="value",
            max_=line_max,
            min_=line_min,
            interval=line_interval,
            axislabel_opts=opts.LabelOpts(formatter=line_formatter),
        )
    )

    bar_chart.overlap(line_chart)

    with st.container(border=True):
        st_pyecharts(bar_chart, height=f"{height}px")


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


if __name__ == '__main__':
    print(is_sublist(subset=['增长率'], superset=['2023', '2024', '增长率']))
