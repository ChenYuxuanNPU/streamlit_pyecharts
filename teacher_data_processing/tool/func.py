import copy
import sqlite3
import json

from teacher_data_processing.read_database import get_database_data as gd

with open(r"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\database\database_basic_info.json",
          "r", encoding='UTF-8') as file:  # ISO-8859-1
    loaded_data = json.load(file)

database_name = loaded_data["database_name"]

# 用来设置排序
educational_background_order = {'博士研究生': 1, '硕士研究生': 2, '大学本科': 3, "大学专科": 4, "中专": 5, "高中": 6,
                                "高中及以下": 7, None: 7}

highest_title_order = {'三级教师': 1, '二级教师': 2, '一级教师': 3, '高级教师': 4, '正高级教师': 5,
                       '初级职称（非中小学系列）': 6,
                       '中级职称（非中小学系列）': 7, '高级职称（非中小学系列）': 8, '未取得职称': 9, None: 10}

current_administrative_position_order = {'无': 1, '中层副职': 2, '中层正职': 3, '副校级': 4, '正校级': 5,
                                         '党组织书记兼校长': 6, '党组织书记': 7, None: 8}

cadre_teacher_order = {'无': 1, '白云区骨干教师': 2, '广州市骨干教师': 3, '广东省骨干教师': 4, '外省市骨干教师': 5,
                       '其他': 6,
                       None: 7}

area_of_supporting_education_order = {'片内': 1, '区内': 2, '外市': 3, '外省': 4, '无': 5, None: 6}

period_order = {'幼儿园': 1, '小学': 2, '初中': 3, '高中': 4, '中职': 5, "无": 6, None: 7}

level_of_teacher_certification_order = {'幼儿园': 1, '小学': 2, '初级中学': 3, '高级中学': 4, '中职专业课': 5,
                                        '高等学校': 6, '无': 7, None: 8}

area_list = ["永平", "江高", "石井", "新市", "人和", "太和", "钟落潭"]

kind_list = ["在编", "编外"]

period_list = ["高中", "初中", "小学", "幼儿园"]

# 985、211、部属师范院校统计
code_of_985 = ("10003 10001 10614 10335 10384 10533 10558 10486 10246 10487 10284 10286 10610 10247 10055 10422 10002 "
               "10248 10561 10183 10269 10532 10611 10698 10213 18213 10358 10423 10141 10056 10027 10145 10007 10006 "
               "10730 10699 10712 10019 10052 1045 19248 91002 19246 7321").split()
code_of_211 = ("10003 10001 10614 10335 10384 10533 10558 10486 10246 10487 10284 10286 10610 10247 10055 10422 10002 "
               "10248 10561 10183 10269 10532 10611 10698 10213 18213 10358 10423 10141 10056 10027 10145 10007 10006 "
               "10730 10699 10712 10019 10052 1045 19248 91002 19246 7321 10635 10559 10033 10280 10285 10613 10497 "
               "10459 10295 10520 10697 10255 10403 10651 10294 10290 10030 10511 10589 10251 10359 19359 10710 10701 "
               "10288 10272 10054 10079 10008 10287 10004 10386 10053 10574 10036 10034 10319 10357 10080 10718 10217 "
               "10013 10673 10005 10542 10200 10593 10140 10112 10151 10504 10657 10271 10626 10022 10759 10184 10010 "
               "10045 10307 10316 10225 10043 10126 10026 10755 10224 10749 10425 10062 10694 10743 11414 10491 11413 "
               "11415 19635 19414").split()
code_of_affiliate = "10027 10269 10200 10511 10718 10635".split()


class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# kind:"在编","编外"
def connect_database():
    conn = sqlite3.connect(
        f"C:\\Users\\1012986131\\Desktop\\python\\streamlit_pyecharts\\database\\{database_name}"
    )
    c = conn.cursor()

    return c, conn


def disconnect_database(conn):
    conn.close()


def load_json_data(file_name: str):

    # 读取现有json文件
    with open(fr"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\result\{file_name}.json",
              "r", encoding="UTF-8") as file:
        json_data = json.load(file)

    return json_data


def save_json_data(json_data: dict, file_name: str):

    with open(fr"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\result\{file_name}.json",
              "w", encoding="UTF-8") as f:
        # 将生成的数据保存至json文件中
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    return 0


def reverse_label_and_value(old_list: list):
    new_list = []
    for sub_list in old_list:
        new_list.append(sub_list[::-1])

    return new_list


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


# 将无和其他合并到无中
def combine_none_and_others(input_dict: dict):
    output = copy.deepcopy(input_dict)

    if "无" in list(input_dict.keys()) and "其他" in list(input_dict.keys()):
        del output["其他"]
        output["无"] += input_dict["其他"]
    return output


# age_list参数代表年龄列表，如[22,23,25]
# age_count_list参数代表求和后的年龄列表，如[(年龄,个数),(年龄,个数)]
def age_statistics(age_list=None, age_count_list=None):
    data = [0, 0, 0, 0, 0, 0, 0, 0]
    label = ["25岁以下", "25-29岁", "30-34岁", "35-39岁", "40-44岁", "45-49岁", "50-54岁", "55岁及以上"]

    if age_list is not None:
        for age in age_list:
            if int(age) < 25:
                data[0] = data[0] + 1

            elif 25 <= int(age) < 30:
                data[1] = data[1] + 1

            elif 30 <= int(age) < 35:
                data[2] = data[2] + 1

            elif 35 <= int(age) < 40:
                data[3] = data[3] + 1

            elif 40 <= int(age) < 45:
                data[4] = data[4] + 1

            elif 45 <= int(age) < 50:
                data[5] = data[5] + 1

            elif 50 <= int(age) < 55:
                data[6] = data[6] + 1

            elif int(age) >= 55:
                data[7] = data[7] + 1

            else:
                print("有一个奇怪的年龄：")
                print(age)

        return combine_label_and_data(label=label, data=data)

    if age_count_list is not None:

        for single_data in age_count_list:
            if int(single_data[0]) < 25:
                data[0] = data[0] + int(single_data[1])

            elif 25 <= int(single_data[0]) < 30:
                data[1] = data[1] + int(single_data[1])

            elif 30 <= int(single_data[0]) < 35:
                data[2] = data[2] + int(single_data[1])

            elif 35 <= int(single_data[0]) < 40:
                data[3] = data[3] + int(single_data[1])

            elif 40 <= int(single_data[0]) < 45:
                data[4] = data[4] + int(single_data[1])

            elif 45 <= int(single_data[0]) < 50:
                data[5] = data[5] + int(single_data[1])

            elif 50 <= int(single_data[0]) < 55:
                data[6] = data[6] + int(single_data[1])

            elif int(single_data[0]) >= 55:
                data[7] = data[7] + int(single_data[1])

            else:
                print("有一个奇怪的年龄：")
                print(single_data)

        return combine_label_and_data(label=label, data=data)

    else:
        print("传入的内容不合要求")


def combine_label_and_data(label: list, data: list):
    if not len(label) == len(data):
        raise MyError("label和data长度不对")

    return {a: b for a, b in zip(label, data)}


def del_tuple_in_list(data: list):
    output = []

    for single_data in data:
        output.append(single_data[0])

    return output


def distinguish_school_id(school_id: str):
    output = []

    if school_id in code_of_985:
        output.append("985院校")

    if school_id in code_of_211:
        output.append("211院校")

    if school_id in code_of_affiliate:
        output.append("部属师范院校")

    if school_id not in code_of_985 + code_of_211 + code_of_affiliate:
        output.append("其他院校")

    return output


def count_school_id(data: list):
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


def combine_highest_title(title_list: list):
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
def combine_administrative_position(ap_list: list):
    output = {
        "无": 0,
        "中层副职": 0,
        "中层正职": 0,
        "副校级": 0,
        "正校级": 0,
    }

    for a_p in ap_list:
        if a_p[0] in list(output.keys()):
            output[a_p[0]] += a_p[1]
        elif a_p[0] in ["党组织书记兼校长", "党组织书记"]:
            output["正校级"] += a_p[1]
        else:
            print(f"{a_p[0]}未插入")

    return output


# 用来检查是否有这个学校/这个学校有没有这个学段
def school_name_and_period_check(kind: str, school_name: str, period=None):
    if kind not in ["在编", '编外']:
        return [False, "kind参数错误"]

    if period not in [None, "高中", "初中", "小学", "幼儿园", ""]:
        return [False, "period参数错误"]

    result = []

    c, conn = connect_database()

    # 不考虑学段，只看有没有这个学校
    if period is None:

        # 只统计个数时info项无效
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=[""], scope="学校",
                                                school_name=school_name)

        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

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
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=[""], scope="学校",
                                                school_name=school_name, period=period)

        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

        finally:
            conn.commit()

        disconnect_database(conn=conn)

        if result != 0:
            return [True]

        if result == 0:
            return [False, f"未找到{school_name}的{period}{kind}教师"]

    return [False, "school_name_or_period_check函数异常"]


# 这个函数用来解决字典赋值但找不到位置的问题
# route的格式：字段1/字段2/字段3

def dict_assignment(route: str, value, json_data: dict):
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
