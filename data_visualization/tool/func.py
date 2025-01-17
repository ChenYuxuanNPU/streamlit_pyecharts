import json
import re
import sqlite3
import time
from collections import Counter
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


class DataFrameContainer:
    """
    用于动态返回多个dataframe
    """

    def __init__(self):
        # 初始化一个空字典来存储 DataFrame
        self.dataframes = {}

    def add_dataframe(self, name, df):
        # 添加一个 DataFrame 到字典中，使用 name 作为键
        self.dataframes[name] = df

    def get_dataframe(self, name):
        # 根据名称获取 DataFrame
        return self.dataframes.get(name, None)

    def remove_dataframe(self, name):
        # 根据名称移除 DataFrame
        if name in self.dataframes:
            del self.dataframes[name]

    def list_dataframes(self):
        # 列出所有存储的 DataFrame 的名称
        return list(self.dataframes.keys())

    def all_dataframes(self):
        # 返回一个包含所有 DataFrame 的字典
        return self.dataframes.copy()


def get_year_list(kind: Literal["school_info", "teacher_info"]) -> list:
    """
    获取教师信息年份列表并按照年份逆序排序（由后到前）
    :return:
    """
    match kind:

        case "school_info":
            return sorted(
                load_json_data(
                    folder="database", file_name="database_basic_info"
                )["list_for_update_school_info"],
                reverse=True
            )

        case "teacher_info":

            return sorted(
                list(
                    set(
                        [data[0] for data in load_json_data(folder="database", file_name="database_basic_info")[
                            "list_for_update_teacher_info"]]
                    )
                ),
                reverse=True
            )

        case _:
            return [None]


def get_area_list() -> list[str]:
    """
    片镇列表：["永平", "石井", "新市", "江高", "人和", "太和", "钟落潭"]
    :return:
    """

    return ["直管", "永平", "石井", "新市", "江高", "人和", "太和", "钟落潭"]


def get_period_list() -> list[str]:
    """
    学段列表：["高中", "初中", "小学", "幼儿园"]
    :return:
    """
    return ["高中", "初中", "小学", "幼儿园"]


def get_edu_bg_list() -> list[str]:
    """
    学历列表：["专科", "本科", "硕士研究生", "博士研究生"]
    :return:
    """
    return ["专科", "本科", "硕士研究生", "博士研究生"]


def get_vocational_level_list() -> list[str]:
    """
    职称列表：["三级教师", "二级教师", "一级教师", "高级教师", "正高级教师"]
    :return:
    """
    return ["三级教师", "二级教师", "一级教师", "高级教师", "正高级教师"]


def get_vocational_level_detail_list() -> list[str]:
    """
    专业技术等级列表：["专业技术十三级", "试用期（未定级）", "专业技术十二级", "专业技术十一级", "专业技术十级", "专业技术九级", "专业技术八级", "专业技术七级", "专业技术六级", "专业技术五级", "专业技术四级", ]
    :return:
    """
    return ["专业技术十三级", "试用期（未定级）", "专业技术十二级", "专业技术十一级", "专业技术十级",
            "专业技术九级", "专业技术八级", "专业技术七级", "专业技术六级", "专业技术五级", "专业技术四级", ]


def shorten_vocational_level_detail_dict() -> dict:
    """
    用于缩短专业技术等级名称
    :return:
    """
    return {
        "专业技术十三级": "十三级",
        "试用期（未定级）": "试用期",
        "专业技术十二级": "十二级",
        "专业技术十一级": "十一级",
        "专业技术十级": "十级",
        "专业技术九级": "九级",
        "专业技术八级": "八级",
        "专业技术七级": "七级",
        "专业技术六级": "六级",
        "专业技术五级": "五级",
        "专业技术四级": "四级",
    }


def get_discipline_list() -> list[str]:
    """
    学科列表：["语文", "数学", "英语", "物理", "化学", "生物", "思想政治", "历史", "地理", "体育", "音乐", "美术", "科学", "信息技术", "劳动", "心理健康", "幼儿教育"]
    :return:
    """
    return [
        "语文", "数学", "英语", "物理", "化学", "生物", "思想政治", "历史", "地理", "体育", "音乐", "美术",
        "科学", "信息技术", "劳动", "心理健康", "幼儿教育"
    ]


def get_grad_school_list() -> list[str]:
    """
    毕业院校类型列表：["985院校", "部属师范院校", "211院校"]
    :return:
    """
    return ["985院校", "部属师范院校", "211院校"]


def get_kind_list() -> list[str]:
    """

    :return: ["在编", "编外"]
    """
    return ["在编", "编外"]


def get_end_dict() -> dict:
    """
    用于设置柱状图不同学段展示的数量（因为不同学段简略校名后长度差别较大）
    :return: {"高中": 70,"初中": 70,"小学": 70,"幼儿园": 95}
    """
    return {
        "高中": 70,
        "初中": 70,
        "小学": 70,
        "幼儿园": 95
    }


def get_trans_period(kind: Literal["option_to_string", "string_to_option"]) -> dict:
    """
    转换学段与对应选项\n
    option_to_string: 选项内容转换为字段\n
    string_to_option: 字段转换为选项内容
    :param kind: 转换方式
    :return: {"所有学段": None,"高中": "高中","初中": "初中","小学": "小学",None: None}
    """
    match kind:
        case "option_to_string":
            return {
                "所有学段": None,
                "高中": "高中",
                "初中": "初中",
                "小学": "小学",
                "幼儿园": "幼儿园",
                None: None
            }
        case "string_to_option":
            return {
                "高中": "高中",
                "初中": "初中",
                "小学": "小学",
                "幼儿园": "幼儿园",
                None: "所有学段"
            }
        case _:
            return {}


def get_school_codes() -> dict:
    """
    用于获取不同类型院校的院校代码\n
    keys:"985","国优计划","部属师范","211"
    :return:
    """

    return load_json_data(folder="source", file_name="院校级别")


# def get_code_of_985() -> list[str]:
#     """
#     985院校代码列表
#     :return:
#     """
#     return ['10003', '10001', '10614', '10335', '10384', '10533', '10558', '10486', '10246', '10487', '10284', '10286',
#             '10610', '10247', '10055', '10422', '10002', '10248', '10561', '10183', '10269', '10532', '10611', '10698',
#             '10213', '18213', '10358', '10423', '10141', '10056', '10027', '10145', '10007', '10006', '10730', '10699',
#             '10712', '10019', '10052', '19248', '91002', '19246', '7321']
#
#
# def get_code_of_nettp() -> list[str]:
#     """
#     国优计划（国家优秀中小学教师培养计划）院校代码列表
#     :return:
#     """
#     return ["10001", "10003", "10027", "19027", "10056", "10141", "10183", "10200", "10246", "10248", "10247", "10269",
#             "10284", "10286", "10335", "10384", "10486", "10487", "10511", "10533", "10558", "10611", "10635", "10698",
#             "10718", "10730", "10006", "10007", "14430", "10285", "10300", "10532", "10542", "10610", "10213", "10699",
#             "10422", "14325", "10295", "10028", "10319", "10574", ]
#
#
# def get_code_of_affiliate() -> list[str]:
#     """
#     部属师范院校代码列表
#     :return:
#     """
#     return ['10027', '10269', '10200', '10511', '10718', '10635']
#
#
# def get_code_of_211() -> list[str]:
#     """
#     211院校代码列表
#     :return:
#     """
#     return ['10003', '10001', '10614', '10335', '10384', '10533', '10558', '10486', '10246', '10487', '10284', '10286',
#             '10610', '10247', '10055', '10422', '10002', '10248', '10561', '10183', '10269', '10532', '10611', '10698',
#             '10213', '18213', '10358', '10423', '10141', '10056', '10027', '10145', '10007', '10006', '10730', '10699',
#             '10712', '10019', '10052', '19248', '91002', '19246', '7321', '10635', '10559', '10033', '10280',
#             '10285', '10613', '10497', '10459', '10295', '10520', '10697', '10255', '10403', '10651', '10294', '10290',
#             '10030', '10511', '10589', '10251', '10359', '19359', '10710', '10701', '10288', '10272', '10054', '10079',
#             '10008', '10287', '10004', '10386', '10053', '10574', '10036', '10034', '10319', '10357', '10080', '10718',
#             '10217', '10013', '10673', '10005', '10542', '10200', '10593', '10140', '10112', '10151', '10504', '10657',
#             '10271', '10626', '10022', '10759', '10184', '10010', '10045', '10307', '10316', '10225', '10043', '10126',
#             '10026', '10755', '10224', '10749', '10425', '10062', '10694', '10743', '11414', '10491', '11413', '11415',
#             '19635', '19414', '91030', '90026']


def distinguish_school_id(school_id: str | int, label_length: str = Literal["long", "short"]) -> list:
    """
    根据院校代码生成学校所属类型的列表（由于985要统计到211里）\n
    label_length = long: ["985院校", "国优计划院校", "211院校", "部属师范院校", "其他院校"]的某个子串\n
    label_length = short: ["985", "国优计划", "211", "部属师范", "其他院校"]的某个子串
    :param school_id: 给定的院校代码
    :param label_length: 返回字串长度类型，短会省略院校二字
    :return: 院校所属类型列表
    """

    output = []
    flag = 0

    for key, value in get_school_codes().items():
        if str(school_id) in value:
            flag = 1
            output.append(f"{key}院校" if label_length == "long" else f"{key}")

    if flag == 0:
        output.append("其他院校")

    return output


def print_color_text(text: str | int | float, color_code='\033[1;91m', reset_code='\033[0m') -> None:
    """
    输出带颜色的字符串，可以用于控制台警告
    :param text: 输出的文本
    :param color_code: 颜色起始代码
    :param reset_code: 颜色结束代码
    :return: 无
    """

    print(f"{color_code}{str(text)}{reset_code}")

    return None


def top_n_second_items_with_transformation(two_d_list: list[list[str]], first_item_value: str, n: int,
                                           transformation_dict: dict) -> list[list[str]]:
    """
    统计二维列表中子列表首项为first_item_value的次项出现频率前n的数据
    :param two_d_list: 二维列表，子列表首项为first_item_value对应项，子列表第二项为需要统计数量的数据
    :param first_item_value: 规定要查询二位列表中首项为x的值
    :param n: 输出的是频率最高的前n项
    :param transformation_dict: 待转换的字典，key对应的是二维列表的第二项数据（即统计结果的首项数据项），value是对应key需要转换的目标值
    :return: 二维列表，子列表中首项为数据（two_d_list中第二项，第一项省略），次项为频数，且按照次项大小排序
    """
    # 统计满足条件的第二项的出现次数
    counter = Counter()
    for sublist in two_d_list:
        if sublist[0] == first_item_value:
            counter[sublist[1]] += 1

    # 获取出现次数最多的前n项及其数量
    most_common_items = counter.most_common(n)

    # 根据转换字典对结果进行转换
    transformed_list = []
    for item, count in most_common_items:
        transformed_item = transformation_dict.get(item, item)  # 如果item在字典中，则获取对应的value，否则不变
        transformed_list.append([transformed_item, count])

    return transformed_list


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

    try:
        print_color_text(text=f'正在执行：{sentence}', color_code='\033[1;94m')
        c.execute(sentence)

        conn.commit()

    except Exception as e:
        conn.rollback()

        print_color_text(text=str(e))
        print_color_text(text=sentence)

    finally:
        result = c.fetchall()

        disconnect_database(conn=conn)

    return result


def del_tuple_in_list(data: list) -> list:
    """
    将形如[('1',), ('2',), ('3',),]的数据转化为[1, 2, 3,]
    :param data:带有元组的列表
    :return: 清洗后的列表
    """

    if not data or not data[0]:
        return []

    if not isinstance(data[0], tuple):
        return data

    output = []

    output.extend(single_data[0] for single_data in data)

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
    year3   data7   data8   data9\n
    结果如下：\n
    index   label1   label2 label3\n
    year2   rate1   rate2    rate3\n
    year3   rate4   rate5    rate6\n
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


def fillnan_and_del_0_lines_in_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    补全dataframe中所有空单元格并删除空行或空列
    :param df: 待处理的dataframe
    :return:
    """
    df.fillna(value=0, inplace=True)

    df = df.loc[:, ~(df == 0).all()]  # 删除全为0的列
    df = df[(df != 0).any(axis=1)]

    return df


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
        return float(n * (number // n + 1))


def biggest_multiple_of_n_geq(number: int | float, n: int | float) -> float:
    """
    返回小于等于等于输入值的最大的n的倍数,返回值被强制类型转换为float以应对n为小数的情况
    :param number: 输入值
    :param n: 倍数因子
    :return:
    """
    if number % n == 0:
        return float(number)
    else:
        return float(n * (number // n))


def calculate_figure_border(number: int | float, direction: Literal["up", "down"],
                            multiple_for_border: int | float = 50, ) -> float:
    """
    根据输入的图表极值设定大于等于该正值或小于等于该负值的最小/大的图表边界\n
    示例（n=10）：\n
    25(up) -> 30, 30(up/down) -> 30, -5(down) -> -10, -10(up/down) -> -10
    :param number: 输入值
    :param direction: 取值方向，up代表在number远离0侧，down代表在number接近0侧
    :param multiple_for_border: 倍数因子
    :return:
    """
    if number == 0:
        return 0

    if number > 0 and direction == "down":
        return biggest_multiple_of_n_geq(number=number, n=multiple_for_border)

    if number > 0 and direction == "up":
        return smallest_multiple_of_n_geq(number=number, n=multiple_for_border)

    if number < 0 and direction == "down":
        return -1 * smallest_multiple_of_n_geq(number=abs(number), n=multiple_for_border)

    if number < 0 and direction == "up":
        return -1 * biggest_multiple_of_n_geq(number=abs(number), n=multiple_for_border)


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


def draw_bar_chart(data: pd.DataFrame | dict, title: str, height: int = 0, axis_font_size: int = 12,
                   is_visual_map_show: bool = True,
                   is_datazoom_show: bool = False, datazoom_start: int = 0, datazoom_end: int = 100, ) -> None:
    """
    绘制柱状图
    :param data: 绘图所用数据
    :param title: 图表标题
    :param height: 图表高度，默认根据分辨率自适应
    :param axis_font_size: 坐标轴标签字体大小
    :param is_visual_map_show: 是否显示动态进度条
    :param is_datazoom_show: 是否展示下方的缩放选择栏
    :param datazoom_start: 缩放选择栏起始值
    :param datazoom_end: 缩放选择栏结束值
    :return:
    """

    if height == 0:
        height = int(get_monitors()[0].height / 1080) * 350

    if isinstance(data, dict):
        chart = Bar()
        chart.add_xaxis([keys for keys in data.keys()])
        chart.add_yaxis("总人数", [values for values in data.values()])

    elif isinstance(data, pd.DataFrame):
        return None

    else:
        return None

    chart.set_global_opts(title_opts=opts.TitleOpts(title=title),
                          legend_opts=opts.LegendOpts(is_show=False),
                          xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=axis_font_size)),
                          datazoom_opts=opts.DataZoomOpts(is_show=is_datazoom_show, range_start=datazoom_start,
                                                          range_end=datazoom_end),
                          visualmap_opts=opts.VisualMapOpts(is_show=is_visual_map_show, pos_right="1%",
                                                            pos_top="30%",
                                                            max_=max([values for values in data.values()])))

    chart.set_series_opts(label_opts=opts.LabelOpts(position="top"))

    with (st.container(border=True)):
        st_pyecharts(
            chart=chart,
            height=f"{height}px"
        )

    return None


def draw_line_chart(data: pd.DataFrame, title: str,
                    mark_line_y: int = None,
                    formatter: str = "{value}",
                    height: int = 350, axis_font_size: int = 12,
                    is_symbol_show: bool = True, symbol_size: int = 2, is_label_show: bool = False,
                    is_smooth: bool = False, is_datazoom_show: bool = False,
                    datazoom_start: int = 0, datazoom_end: int = 100, ) -> None:
    """
    绘制折线图
    :param data: 绘图所用数据
    :param title: 图表标题
    :param mark_line_y: 标记线绝对高度
    :param formatter: 坐标轴单位
    :param height: 图表高度，默认根据分辨率自适应
    :param axis_font_size: 坐标轴标签字体大小
    :param is_symbol_show: 是否在鼠标悬停数据点时显示信息，数据点是否扩大为圈圈
    :param symbol_size: 数据点圆圈大小
    :param is_label_show: 是否在数据点上显示数值
    :param is_smooth: 是否平滑展示曲线
    :param is_datazoom_show: 是否展示下方的缩放选择栏
    :param datazoom_start: 缩放选择栏起始值
    :param datazoom_end: 缩放选择栏结束值
    :return:
    """

    height = int(get_monitors()[0].height / 1080) * height

    chart = Line()

    chart.add_xaxis(data.columns.tolist())

    for label in data.index:
        chart.add_yaxis(series_name=label,
                        y_axis=data.loc[label].tolist(),
                        is_connect_nones=True,
                        is_symbol_show=is_symbol_show,
                        symbol_size=symbol_size,
                        is_smooth=is_smooth,
                        label_opts=opts.LabelOpts(is_show=False),
                        markline_opts=opts.MarkLineOpts(
                            data=[opts.MarkLineItem(y=mark_line_y, symbol="none")], symbol="none",
                            label_opts=opts.LabelOpts(is_show=is_label_show, distance=5),
                            linestyle_opts=opts.LineStyleOpts(color="grey", type_="dashed")
                        ) if mark_line_y is not None else None,
                        )

    chart.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter=formatter)),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=axis_font_size)),
        datazoom_opts=opts.DataZoomOpts(is_show=is_datazoom_show, range_start=datazoom_start, range_end=datazoom_end),
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

    return None


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

    return None


def get_mixed_bar_and_yaxis_opts(max_: int | float | None, data_max: int | float | None, min_: int | float | None,
                                 data_min: int | float | None, kind: Literal["bar", "line"], num_divisions: int,
                                 multiple_for_border: int = 50) \
        -> tuple[int | float, int | float, int | float,]:
    """
    返回柱状-折线图坐标轴所需数据
    :param multiple_for_border: 将数据极值往上或往下取multiple_for_border的最接近的倍数作为坐标轴高的参数之一
    :param max_: 强制坐标轴最大值
    :param data_max: 坐标轴对应数据最大值
    :param min_: 强制坐标轴最小值
    :param data_min: 坐标轴对应数据最小值
    :param kind: 图表类型（柱状或折线）
    :param num_divisions: 坐标轴分段数
    :return: [坐标轴最大值， 坐标轴最小值， 坐标轴间隔]
    """
    match kind:
        case "line":
            axis_max = max_ if max_ is not None else calculate_figure_border(number=data_max,
                                                                             multiple_for_border=multiple_for_border,
                                                                             direction="up")
            axis_min = min_ if min_ is not None else 2 * calculate_figure_border(number=data_min,
                                                                                 multiple_for_border=multiple_for_border,
                                                                                 direction="down") - axis_max
        case "bar":
            axis_max = max_ if max_ is not None else 2 * calculate_figure_border(number=data_max,
                                                                                 multiple_for_border=multiple_for_border,
                                                                                 direction="up")
            axis_min = min_ if min_ is not None else 0

        case _:
            raise ValueError('kind not in ["bar", "line"]')

    return axis_max, axis_min, (axis_max - axis_min) / num_divisions


def draw_mixed_bar_and_line(df_bar: pd.DataFrame, df_line: pd.DataFrame,
                            bar_axis_label: str, line_axis_label: str,
                            bar_max_: int | float = None, bar_min_: int | float = None,
                            line_max_: int | float = None, line_min_: int | float = None,
                            multiple_for_border: int = 50,
                            mark_line_y: int = None, mark_line_type: Literal["min", "max", "average"] = None,
                            is_mark_line_label_show: bool = False,
                            is_symbol_show: bool = True, symbol_size: int = 2, is_smooth: bool = False,
                            is_datazoom_show: bool = True, datazoom_start: int = 0, datazoom_end: int = 100,
                            height: int | float = 0,
                            bar_formatter: str = "{value}", line_formatter: str = "{value}",
                            x_axis_font_size: int = 12) -> None:
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
    :param multiple_for_border: 将数据极值往上或往下取multiple_for_border的最接近的倍数作为坐标轴高的参数之一
    :param mark_line_y: 折线图标记线高度（高优先级）
    :param mark_line_type: 折线图标记线类型（str，可填"min"/"max"/"average"，低优先级）
    :param is_mark_line_label_show: 是否展示markline的label
    :param is_symbol_show: 是否在鼠标悬停数据点时显示信息，数据点是否扩大为圈圈
    :param symbol_size: 数据点圆圈大小
    :param is_smooth: 是否平滑展示曲线
    :param is_datazoom_show: 是否展示下方的缩放选择栏
    :param datazoom_start: 缩放选择栏起始值
    :param datazoom_end: 缩放选择栏结束值
    :param height: 图表高度
    :param bar_formatter: 柱状图坐标轴单位
    :param line_formatter: 折线图坐标轴单位
    :param x_axis_font_size: x轴字体大小
    :return:
    """

    if df_bar.empty or df_line.empty:
        return None

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

    elif 0 < height <= 5:
        height *= int(get_monitors()[0].height / 1080) * 720

    bar_chart = Bar()
    bar_chart.add_xaxis(xaxis_data=df_bar.columns)
    bar_max, bar_min, bar_interval = get_mixed_bar_and_yaxis_opts(max_=bar_max_, data_max=df_bar.values.max(),
                                                                  min_=bar_min_, data_min=df_bar.values.min(),
                                                                  kind="bar", num_divisions=10,
                                                                  multiple_for_border=multiple_for_border)

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
                                                                     kind="line", num_divisions=10,
                                                                     multiple_for_border=multiple_for_border)

    if mark_line_y is not None:

        for line in df_line.index:
            line_chart.add_yaxis(
                series_name=line,
                yaxis_index=1,
                y_axis=df_line.loc[line].tolist(),
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True,
                is_symbol_show=is_symbol_show,
                symbol_size=symbol_size,
                is_smooth=is_smooth,
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(y=mark_line_y, symbol="none")], symbol="none",
                    label_opts=opts.LabelOpts(is_show=is_mark_line_label_show, distance=5),
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
                is_connect_nones=True,
                is_symbol_show=is_symbol_show,
                symbol_size=symbol_size,
                is_smooth=is_smooth,
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(type_=mark_line_type, symbol="none")],
                    symbol="none", label_opts=opts.LabelOpts(is_show=is_mark_line_label_show),
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
                is_connect_nones=True,
                is_symbol_show=is_symbol_show,
                symbol_size=symbol_size,
                is_smooth=is_smooth,
            )

    bar_chart.set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            is_show=True, trigger="axis", axis_pointer_type="cross"
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
            axislabel_opts=opts.LabelOpts(font_size=x_axis_font_size)
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
        datazoom_opts=opts.DataZoomOpts(is_show=is_datazoom_show, range_start=datazoom_start, range_end=datazoom_end),
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

    return None


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

    return None


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

    return None


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
def stream_data(sentence: str, delay=0.01) -> str:
    """
    用于分批输出数据，配合st.write_stream()实现逐条一个个字生成的效果
    :param sentence: 需要输出的语句
    :param delay: 字间时间延迟
    :return:
    """
    for word in sentence:
        yield word
        time.sleep(delay)


def simplify_school_name(d: dict) -> dict:
    """
    简化校名（对于输入的字典只化简key的校名）
    :param d: 校名数据，形如：{'广州市培英中学': ['124401114553841006', '完全中学', '直管', 412, 0, 412], '广州市第六十五中学': ['12440111455384127X', '完全中学', '直管', 349, 0, 349],}
    :return: 返回化简后的字典，只有每一个校名key被修改了，value不变
    """
    temp = [item for item in d.items()]
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

        if len(temp_item) > 2 and temp_item[-2:] == "学校":
            temp_item = temp_item[:-2]

        if len(temp_item) > 4 and temp_item[0:4] == "广大附中":
            temp_item = f"广附{temp_item[4:]}"

        if len(temp_item) > 4 and temp_item[0:4] == "华师附中":
            temp_item = f"华附{temp_item[4:]}"

        if len(temp_item) > 4 and temp_item[-4:] == "职业技术":
            temp_item = temp_item[:-4]

        # 针对广二师实验优化 广东第二师范学院实验中学
        temp_item = simplify_string(s=temp_item, pattern=r'^(.*?)东第(.*?)范学院(.*?)$')

        # 针对广外实验优化 广东外语外贸大学实验中学
        temp_item = simplify_string(s=temp_item, pattern=r'^(.*?)东(.*?)语外贸大学(.*?)$')

        temp_item = simplify_string(s=temp_item, pattern=r'^(.*?)附属第(.*?)学$')
        temp_item = simplify_string(s=temp_item, pattern=r'^(.*?)第(.*?)初级(.*?)学$')
        temp_item = simplify_string(s=temp_item, pattern=r'^(.*?)属(.*?)学(.*?)$')
        temp_item = simplify_string(s=temp_item, pattern=r'^(.*?)第(.*?)学(.*?)$')

        output.append([temp_item, item[1]])

    output_dict = {}

    for item in output:
        output_dict[item[0]] = item[1]

    return output_dict


def simplify_string(s: str, pattern: str) -> str:
    """
    用于匹配字符串并且删除其中特定的某些字\n
    如：需要将X第Y学更新为XY，可以设置pattern为r'^(.*?)第(.*?)学$'
    :param s: 需要缩短的字符串
    :param pattern: 匹配用的正则表达式
    :return:
    """
    if re.match(pattern=pattern, string=s):
        return "".join(re.match(pattern, s).groups())
    else:
        return s


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

    #  page3用于获取年份列表长度进行判断
    if 'page3_year_length' not in st.session_state:
        st.session_state.page3_year_length = 0

    #  page3用于获取片镇列表长度进行判断
    if 'page3_area_length' not in st.session_state:
        st.session_state.page3_area_length = 0

    #  page3用于获取年份实际查询列表，避免更改列表后马上修改图表
    if 'page3_year_list' not in st.session_state:
        st.session_state.page3_year_list = []

    #  page3用于获取片镇实际查询列表，避免更改列表后马上修改图表
    if 'page3_area_list' not in st.session_state:
        st.session_state.page3_area_list = []

    #  page3用于获取实际查询学段，避免更改后马上修改图表
    if 'page3_period' not in st.session_state:
        st.session_state.page3_period = None

    #  page3用于更换查询状态
    if 'page3_search_flag' not in st.session_state:
        st.session_state.page3_search_flag = False

    #  page4用于获取参数
    if 'page4_year_list' not in st.session_state:
        st.session_state.page4_year_list = []

    if 'page4_school_list' not in st.session_state:
        st.session_state.page4_school_list = []

    if 'page4_period' not in st.session_state:
        st.session_state.page4_period = None

    #  page4用于决定查询类型
    if 'page4_info_kind' not in st.session_state:
        st.session_state.page4_info_kind = None

    # page4中的在编展示判断符
    if 'page4_1_year_and_1_school_kind_0_flag' not in st.session_state:
        st.session_state.page4_1_year_and_1_school_kind_0_flag = False

    # page4中的编外展示判断符
    if 'page4_1_year_and_1_school_kind_1_flag' not in st.session_state:
        st.session_state.page4_1_year_and_1_school_kind_1_flag = False

    return None


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
        st.session_state.page3_search_flag = False

        st.session_state.page3_year_length = 0
        st.session_state.page3_area_length = 0

        st.session_state.page3_year_list = []
        st.session_state.page3_area_list = []
        st.session_state.page3_period = None

    if page != 4:
        st.session_state.page4_1_year_and_1_school_kind_0_flag = False
        st.session_state.page4_1_year_and_1_school_kind_1_flag = False

        st.session_state.page4_year_list = []

        st.session_state.page4_school_list = []

        st.session_state.page4_period = None

        st.session_state.page4_info_kind = None

    return None


def session_state_reset(page: int) -> None:
    """
    重置所有页面的session_state变量
    :param page: 当前页标签
    :return:
    """

    # 刷新其他页面
    reset_others(page=page)

    return None


def page1_show_detail_info() -> None:
    """
    page1中展开信息按钮绑定的函数
    :return:
    """
    st.session_state.page1_show_detail = True

    return None


def page1_hide_detail_info() -> None:
    """
    page1中收起信息按钮绑定的函数
    :return:
    """
    st.session_state.page1_show_detail = False

    return None


def page3_show_info(year_list: list, area_list: list, period: str or None) -> None:
    """
    判断片镇页参数是否合理并返回结果
    :param year_list: 当前查询年份列表
    :param area_list: 当前查询片镇列表
    :param period: 学段列表
    :return:
    """

    if min(len(year_list), len(area_list)) > 1:

        # st.session_state.page3_search_flag = False
        st.toast("年份与片镇不能同时多选！", icon="🥺")

    elif min(len(year_list), len(area_list)) == 0:

        if len(year_list) == 0:
            st.toast("需要选择查询的年份", icon="🥱")

        if len(area_list) == 0:
            st.toast("需要选择查询的片镇", icon="🥱")

    else:

        st.session_state.page3_year_list = year_list
        st.session_state.page3_area_list = area_list
        st.session_state.page3_period = period

        st.session_state.page3_year_length = len(year_list)
        st.session_state.page3_area_length = len(area_list)

        st.session_state.page3_search_flag = True

    return None


if __name__ == '__main__':
    pass
