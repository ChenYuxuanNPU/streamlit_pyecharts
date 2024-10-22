import copy
import json
import sqlite3
from pathlib import Path
from typing import Tuple

from teacher_data_processing.read_database import get_database_data as gd


# 用来设置排序
# todo:插入新表时要在这里添加新的下拉选项
def get_educational_background_order() -> dict:
    """
    学历排序
    :return:
    """

    return {
        '博士研究生': 1, '硕士研究生': 2, '本科': 3, "专科": 4, "高中": 5, "高中及以下": 6,
        "中师": 7, "中专（非师范）": 8, "中专": 9, None: 10
    }


def get_highest_title_order() -> dict:
    """
    职称排序
    :return:
    """

    return {
        '三级教师': 1, '二级教师': 2, '一级教师': 3, '高级教师': 4, '正高级教师': 5,
        '初级职称（非中小学系列）': 6,
        '中级职称（非中小学系列）': 7, '高级职称（非中小学系列）': 8, '未取得职称': 9, None: 10
    }


def get_current_administrative_position_order() -> dict:
    """
    行政职务排序
    :return:
    """

    return {
        '党组织书记兼校长': 1, '党组织书记': 2, '正校级': 3, '副校级': 4, '中层正职': 5,
        '中层副职': 6, '团委书记': 7, '团委副书记': 8, '少先队大队辅导员': 9,
        '少先队副大队辅导员': 10, '工会主席': 11, '工会副主席': 12, '无': 13, None: 14
    }


def get_cadre_teacher_order() -> dict:
    """
    骨干教师排序
    :return:
    """

    return {
        '无': 1, '白云区骨干教师': 2, '广州市骨干教师': 3, '广东省骨干教师': 4, '外省市骨干教师': 5,
        '其他': 6,
        None: 7
    }


def get_area_of_supporting_education_order() -> dict:
    """
    支教地域排序
    :return:
    """

    return {'片内': 1, '区内': 2, '外市': 3, '外省': 4, '无': 5, None: 6}


def get_period_order() -> dict:
    """
    学段排序
    :return:
    """

    return {'幼儿园': 1, '小学': 2, '初中': 3, '高中': 4, '中职': 5, "无": 6, None: 7}


def get_level_of_teacher_certification_order() -> dict:
    """
    教师资格排序
    :return:
    """

    return {
        '幼儿园': 1, '小学': 2, '初级中学': 3, '高级中学': 4, '中职专业课': 5, '中职实习指导教师': 6,
        '高等学校': 7, '无': 8, None: 9
    }


def get_area_order() -> dict:
    """
    片镇排序（直管为首位）
    :return:
    """

    return {"直管": 1, "永平": 2, "石井": 3, "新市": 4, "江高": 5, "人和": 6, "太和": 7, "钟落潭": 8, None: 9}


def get_area_list() -> list:
    """
    片镇列表：["永平", "石井", "新市", "江高", "人和", "太和", "钟落潭"]
    :return:
    """

    return ["永平", "石井", "新市", "江高", "人和", "太和", "钟落潭"]


def get_kind_list() -> list:
    """
    教师类型：["在编", "编外"]
    :return:
    """

    return ["在编", "编外"]


def get_period_list() -> list:
    """
    常用学段列表：["高中", "初中", "小学", "幼儿园"]
    :return:
    """

    return ["高中", "初中", "小学", "幼儿园"]


def get_code_of_985() -> list:
    """
    985院校代码列表
    :return:
    """

    return ("10003 10001 10614 10335 10384 10533 10558 10486 10246 10487 10284 10286 10610 10247 10055 10422 10002 "
            "10248 10561 10183 10269 10532 10611 10698 10213 18213 10358 10423 10141 10056 10027 10145 10007 10006 "
            "10730 10699 10712 10019 10052 1045 19248 91002 19246 7321").split()


def get_code_of_211() -> list:
    """
    211院校代码列表
    :return:
    """

    return ("10003 10001 10614 10335 10384 10533 10558 10486 10246 10487 10284 10286 10610 10247 10055 10422 10002 "
            "10248 10561 10183 10269 10532 10611 10698 10213 18213 10358 10423 10141 10056 10027 10145 10007 10006 "
            "10730 10699 10712 10019 10052 1045 19248 91002 19246 7321 10635 10559 10033 10280 10285 10613 10497 "
            "10459 10295 10520 10697 10255 10403 10651 10294 10290 10030 10511 10589 10251 10359 19359 10710 10701 "
            "10288 10272 10054 10079 10008 10287 10004 10386 10053 10574 10036 10034 10319 10357 10080 10718 10217 "
            "10013 10673 10005 10542 10200 10593 10140 10112 10151 10504 10657 10271 10626 10022 10759 10184 10010 "
            "10045 10307 10316 10225 10043 10126 10026 10755 10224 10749 10425 10062 10694 10743 11414 10491 11413 "
            "11415 19635 19414").split()


def get_code_of_affiliate() -> list:
    """
    部属师范院校代码列表
    :return:
    """

    return "10027 10269 10200 10511 10718 10635".split()


class MyError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def print_color_text(text: str, color_code='\033[1;91m', reset_code='\033[0m') -> None:
    """
    输出带颜色的字符串，可以用于控制台警告
    :param text: 输出的文本
    :param color_code: 颜色起始代码
    :param reset_code: 颜色结束代码
    :return: 无
    """

    print(color_code + text + reset_code)

    return None


# kind:"在编","编外"
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


def load_json_data(folder: str, file_name: str) -> dict:
    """
    从文件夹中加载json文件
    :param folder: json_file下的文件夹名
    :param file_name: json文件名，不需要带.json后缀
    :return: json文件形成的字典
    """

    with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\{folder}\{file_name}.json",
              "r", encoding="UTF-8") as f:
        json_data = json.load(f)

    return json_data


def save_json_data(json_data: dict, folder: str, file_name: str) -> None:
    """
    将dict保存到json_file下folder/file_name.json下
    :param json_data: 要保存的dict
    :param folder: json_file下的文件夹名
    :param file_name: json文件名，不需要带.json后缀
    :return:
    """

    with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\{folder}\{file_name}.json",
              "w", encoding="UTF-8") as f:
        # 将生成的数据保存至json文件中
        json.dump(json_data, f, indent=4, ensure_ascii=False)

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


def reverse_label_and_value(old_list: list) -> list:
    """
    用于反转子列表的顺序
    :param old_list: 原二维列表
    :return: 子列表反转后的列表
    """

    new_list = []
    for sub_list in old_list:
        new_list.append(sub_list[::-1])

    return new_list


def simplify_school_name(dict1: dict) -> dict:
    """
    简化校名，删除前缀“广州市白云区”、“广州市”、“白云区”、“广州”，删除后缀“学校”
    :param dict1:
    :return:
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


def combine_none_and_others(input_dict: dict) -> dict:
    """
    将字典中键为无和其他的值合并到无中
    :param input_dict: 需要合并的字典
    :return: 合并后的字典
    """

    output = copy.deepcopy(input_dict)

    if "无" in list(input_dict.keys()) and "其他" in list(input_dict.keys()):
        del output["其他"]
        output["无"] += input_dict["其他"]
    return output


def age_statistics(age_list=None, age_count_list=None) -> dict:
    """
    用于将零散的年龄列表合并为统计求和后的年龄列表
    :param age_list: 年龄列表，如[22,23,25]
    :param age_count_list: 求和后的年龄列表，如[(年龄,个数),(年龄,个数)]
    :return: 年龄及个数的二维列表
    """

    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    label = ["20岁及以下", "21-25岁", "25-29岁", "30-34岁", "35-39岁", "40-44岁", "45-49岁", "50-54岁", "55-60岁",
             "60岁及以上"]

    if age_list is not None:
        for age in age_list:
            if int(age) <= 20:
                data[0] += 1

            elif 20 < int(age) < 25:
                data[1] += 1

            elif 25 <= int(age) < 30:
                data[2] += 1

            elif 30 <= int(age) < 35:
                data[3] += 1

            elif 35 <= int(age) < 40:
                data[4] += 1

            elif 40 <= int(age) < 45:
                data[5] += 1

            elif 45 <= int(age) < 50:
                data[6] += 1

            elif 50 <= int(age) < 55:
                data[7] += 1

            elif 55 <= int(age) < 60:
                data[8] += 1

            elif int(age) >= 60:
                data[9] += 1

            else:
                print("有一个奇怪的年龄：")
                print(age)

        return combine_label_and_data(label=label, data=data)

    if age_count_list is not None:

        for single_data in age_count_list:
            if int(single_data[0]) <= 20:
                data[0] += int(single_data[1])

            elif 20 < int(single_data[0]) < 25:
                data[1] += int(single_data[1])

            elif 25 <= int(single_data[0]) < 30:
                data[2] += int(single_data[1])

            elif 30 <= int(single_data[0]) < 35:
                data[3] += int(single_data[1])

            elif 35 <= int(single_data[0]) < 40:
                data[4] += int(single_data[1])

            elif 40 <= int(single_data[0]) < 45:
                data[5] += int(single_data[1])

            elif 45 <= int(single_data[0]) < 50:
                data[6] += int(single_data[1])

            elif 50 <= int(single_data[0]) < 55:
                data[7] += int(single_data[1])

            elif 55 <= int(single_data[0]) < 60:
                data[8] += int(single_data[1])

            elif int(single_data[0]) >= 60:
                data[9] += int(single_data[1])

            else:
                print("有一个奇怪的年龄：")
                print(single_data)

        return combine_label_and_data(label=label, data=data)

    else:
        print("传入的内容不合要求")
        return {}


def combine_label_and_data(label: list, data: list) -> dict:
    """
    将画图用的label与data列表合并为字典
    :param label:label列表
    :param data:data列表
    :return: 合并后的字典
    """

    if not len(label) == len(data):
        raise MyError("label和data长度不对")

    return {a: b for a, b in zip(label, data)}


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


def distinguish_school_id(school_id: str) -> list:
    """
    根据院校代码生成学校所属类型的列表（由于985要统计到211里）
    :param school_id: 给定的院校代码
    :return: ["985院校", "211院校", "部属师范院校", "其他院校"]的某个子串
    """

    output = []

    if school_id in get_code_of_985():
        output.append("985院校")

    if school_id in get_code_of_211():
        output.append("211院校")

    if school_id in get_code_of_affiliate():
        output.append("部属师范院校")

    if school_id not in get_code_of_985() + get_code_of_211() + get_code_of_affiliate():
        output.append("其他院校")

    return output


def count_school_id(data: list) -> dict:
    """
    统计985211人数
    :param data: 院校代码列表，形如[('10699',), ('10558',), ('10561',),]
    :return: 985、211、部署示范及其他的人数列表
    """

    output = {
        '985院校': 0,
        '部属师范院校': 0,
        '211院校': 0,
        '其他院校': 0
    }

    id_list = del_tuple_in_list(data=data)

    for school_id in id_list:
        flag = distinguish_school_id(school_id=school_id)

        for kind in flag:
            output[kind] += 1

    return output


def combine_highest_title(title_list: list) -> dict:
    """
    将非中小学系列职称合并
    :param title_list:职称列表
    :return: 合并后的职称字典
    """

    output = {
        "未取得职称": 0,
        "三级教师": 0,
        "二级教师": 0,
        "一级教师": 0,
        "高级教师": 0,
        "正高级教师": 0,
        "其他职称（非教师）": 0
    }

    for titles in title_list:
        if titles[0] in list(output.keys()):
            output[titles[0]] += titles[1]
        elif titles[0] in ['初级职称（非中小学系列）', '中级职称（非中小学系列）', '高级职称（非中小学系列）']:
            output["其他职称（非教师）"] += titles[1]
        else:
            print(f"{titles[0]}未插入")

    return output


# 这里要把党组织书记和党组织书记兼校长合并到正校级里
# def combine_administrative_position(ap_list: list) -> dict:
#     output = {
#         "无": 0,
#         "中层副职": 0,
#         "中层正职": 0,
#         "副校级": 0,
#         "正校级": 0,
#     }
#
#     for a_p in ap_list:
#         if a_p[0] in list(output.keys()):
#             output[a_p[0]] += a_p[1]
#         elif a_p[0] in ["党组织书记兼校长", "党组织书记"]:
#             output["正校级"] += a_p[1]
#         else:
#             print(f"{a_p[0]}未插入")
#
#     return output


# 用来检查是否有这个学校/这个学校有没有这个学段
def school_name_and_period_check(kind: str, school_name: str, year: str, period=None) -> list:
    """
    用于检查给定的校名或校名和学段的组合在某一年的数据中是否存在
    :param kind: 在编或编外
    :param school_name: 校名
    :param year: 年份
    :param period: 学段，不填默认所有学段
    :return: [True/False, 错误信息]
    """

    if kind not in ["在编", '编外']:
        return [False, "kind参数错误"]

    if period not in [None, "所有学段", "高中", "初中", "小学", "幼儿园", ""]:
        return [False, "period参数错误"]

    else:
        period = period if period not in ["所有学段", ""] else None

    result = []

    c, conn = connect_database()

    # 不考虑学段，只看有没有这个学校
    if period is None:

        # 只统计个数时info项无效
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=[""], scope="学校", year=year,
                                                school_name=school_name)

        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

            if "no such table" in str(e):
                return [False, f"未找到{school_name}的{period}{kind}教师"]

        finally:
            conn.commit()

        disconnect_database(conn=conn)

        if result != 0:
            return [True]

        if result == 0:
            return [False, f"未找到{school_name}的{kind}教师信息"]

    # 考虑学段，有学校且有对应学段才返回True
    if period is not None:

        # 只统计个数时info项无效
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=[""], scope="学校", year=year,
                                                school_name=school_name, period=period)

        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

            if "no such table" in str(e):
                return [False, f"未找到{school_name}的{period}{kind}教师"]

        finally:
            conn.commit()

        disconnect_database(conn=conn)

        if result != 0:
            return [True]

        if result == 0:
            return [False, f"未找到{school_name}的{period}{kind}教师"]

    return [False, "school_name_or_period_check函数异常"]


def dict_assignment(route: str, value, json_data: dict) -> dict:
    """
    在不知道字典是否有对应路径的情况下插入数据，避免了无中间路径报key error
    :param route: 数据在字典中的位置，每一层的key使用斜杠"/"分开，如f"{year}/{kind}/片区/{area}/所有学段/"
    :param value: 需要插入的数据
    :param json_data: 原字典
    :return: 插入后字典
    """

    route_list = route.split("/")
    temp = json_data

    for item in route_list:
        if item is not route_list[-1]:
            if item in temp:
                temp = temp[item]

            else:
                temp[item] = {}
                temp = temp[item]

    try:
        temp[route_list[-1]] = copy.deepcopy(value)
    except Exception as e:
        print('\033[1;91m' + f"module.dict_assignment:{e}" + '\033[0m')
        print('\033[1;91m' + f"{route}路径上有奇怪的原始值" + '\033[0m')

    return json_data


if __name__ == '__main__':
    pass
