import json
from pathlib import Path

with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\database\database_basic_info.json",
          "r", encoding='UTF-8') as file:  # ISO-8859-1
    loaded_data = json.load(file)

table_name_dict = loaded_data['table_name_dict']

# 为了简化前面所有kind参数，直接用在编编外，在查数据库的时候因为json文件用的是跟其他信息区分的名字，所以要在这里加一步区分
trans_kind = {
    "在编": "在编教师信息",
    "编外": "编外教师信息"
}


class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# 切记空格后置
# kind:在编，编外(str)
# info_num:提取的参数个数，多个参数则一起取.1代表统计个数，大于1代表提取所有参数，0代表提取某一参数但不count,-1代表只统计count值(int)
# info:字段名(最高学历、最高职称等),放文本列表(list)
# scope:全区，片区，学校(str)
# school_name:校名(str)
# area_name:片区(str)
# period:高中、初中、小学、幼儿园（str）
# limit:限制搜索条数(int)
# order:限制特定搜索顺序，asc/desc(str)
# additional_requirement:额外的查询条件(list)

def info_trans(info: str):
    info_dict = {
        "最高学历": "educational_background_highest",
        "最高职称": "highest_title",
        "年龄": "current_age",
        "主教学科": "major_discipline",
        "院校代码": "graduate_school_id",  # 切记这里搜完数据库以后要数据统计，生成统计结果以后插院校级别的json文件里
        "行政职务": "current_administrative_position",
        "骨干教师": "cadre_teacher",
        "三名工作室": "title_01",
        "支教地域": "area_of_supporting_education",
        "教师资格": "level_of_teacher_certification",
        "片区": "area",
        "任教年级": "grade_to_teach",
        "学段": "period",
        "学校": "school_name",
        "性别": "gender"
    }

    return info_dict.get(info, "*")


def string_link(str1: str, str2: str, start_sign: int):
    if start_sign == 0:
        return f"{str1} where {str2} "

    elif start_sign == 1:
        return f"{str1} and {str2} "

    else:
        raise MyError("字符串结合不符合预期")


def generate_sql_sentence_check(scope: str, area_name: str, school_name: str, info: list, kind: str, period=None):
    # 判断是否有选择限定类型但未填信息的情况
    if scope == "片区" and area_name == "":
        return [False, "未填写片区"]

    if scope == "学校" and school_name == "":
        return [False, "未填写学校"]

    # 检查插入的info项是否与info_num对应
    if not isinstance(info, list):
        return [False, "传入info不是列表"]

    if kind not in ["在编", '编外']:
        return [False, "kind参数错误"]

    if period not in [None, "高中", "初中", "小学", "幼儿园", ""]:
        return [False, "period参数错误"]

    return [True]


def fill_scope_kind_period_others(info_num: int, info: list, scope: str,
                                  kind: str, school_name="", area_name="", period=None,
                                  limit=0, order="", additional_requirement=None, ):
    start_sign = 0  # 0代表初始第一个条件，1代表后续条件

    # 采集某一字段的统计数据
    if info_num == 1:

        sql_sentence = fr"select {info_trans(info[0])},count(*) from {table_name_dict[trans_kind[kind]]} "

        if kind == "在编":
            pass

        elif kind == "编外":
            sql_sentence = string_link(str1=sql_sentence, str2=fr"is_teacher == '是'", start_sign=start_sign)
            start_sign = 1

        if scope == "全区":
            pass

        elif scope == "学校":
            sql_sentence = string_link(str1=sql_sentence, str2=fr"school_name == '{school_name}'",
                                       start_sign=start_sign)
            start_sign = 1

        elif scope == "片区":
            sql_sentence = string_link(str1=sql_sentence, str2=fr"area == '{area_name}'", start_sign=start_sign)
            start_sign = 1

        if period is not None and period != "":
            sql_sentence = string_link(str1=sql_sentence, str2=fr"period == '{period}'", start_sign=start_sign)
            start_sign = 1

        if additional_requirement is not None:
            for requirement in additional_requirement:
                sql_sentence = string_link(str1=sql_sentence, str2=requirement, start_sign=start_sign)
                start_sign = 1

        # 加入count语句的分类 group by
        sql_sentence = sql_sentence + fr" group by {info_trans(info[0])} "

        # 根据情况加入order by
        if order == "asc":
            sql_sentence = sql_sentence + " order by count(*) asc "

        if order == "desc":
            sql_sentence = sql_sentence + " order by count(*) desc "

        # 加入限制条数（主要针对主教学科）
        if limit > 0:
            sql_sentence = sql_sentence + fr" limit {limit} "

    elif info_num > 1 or info_num == 0:

        sql_sentence = fr"select "

        # 0的时候不需要叠
        if info_num == 0:
            sql_sentence = sql_sentence + info_trans(info[0])

        else:
            for i in range(0, len(info)):

                if i == 0:
                    sql_sentence = sql_sentence + info_trans(info[i])

                else:
                    sql_sentence = sql_sentence + "," + info_trans(info[i]) + " "

        sql_sentence = sql_sentence + f" from {table_name_dict[trans_kind[kind]]} "

        if kind == "在编":
            pass

        elif kind == "编外":
            sql_sentence = string_link(str1=sql_sentence, str2=fr"is_teacher == '是'", start_sign=start_sign)
            start_sign = 1

        if scope == "全区":
            pass

        elif scope == "学校":
            sql_sentence = string_link(str1=sql_sentence, str2=fr"school_name == '{school_name}'",
                                       start_sign=start_sign)
            start_sign = 1

        elif scope == "片区":
            sql_sentence = string_link(str1=sql_sentence, str2=fr"area == '{area_name}'", start_sign=start_sign)
            start_sign = 1

        if period is not None and period != "":
            sql_sentence = string_link(str1=sql_sentence, str2=fr"period == '{period}'", start_sign=start_sign)
            start_sign = 1

        if additional_requirement is not None:
            for requirement in additional_requirement:
                sql_sentence = string_link(str1=sql_sentence, str2=requirement, start_sign=start_sign)
                start_sign = 1

        # 加入限制条数（主要针对主教学科）
        if limit > 0:
            sql_sentence = sql_sentence + fr" limit {limit} "

    elif info_num == -1:

        sql_sentence = fr"select count(*) from {table_name_dict[trans_kind[kind]]} "

        if kind == "在编":
            pass

        elif kind == "编外":
            sql_sentence = string_link(str1=sql_sentence, str2=fr"is_teacher == '是'", start_sign=start_sign)
            start_sign = 1

        if scope == "全区":
            pass

        elif scope == "学校":
            sql_sentence = string_link(str1=sql_sentence, str2=fr"school_name == '{school_name}'",
                                       start_sign=start_sign)
            start_sign = 1

        elif scope == "片区":
            sql_sentence = string_link(str1=sql_sentence, str2=fr"area == '{area_name}'", start_sign=start_sign)
            start_sign = 1

        if period is not None and period != "":
            sql_sentence = string_link(str1=sql_sentence, str2=fr"period == '{period}'", start_sign=start_sign)
            start_sign = 1

        if additional_requirement is not None:
            for requirement in additional_requirement:
                sql_sentence = string_link(str1=sql_sentence, str2=requirement, start_sign=start_sign)
                start_sign = 1

    else:
        raise MyError("info_num不对劲")

    return sql_sentence


# 切记空格后置
# kind:在编，编外(str)
# info_num:提取的参数个数，多个参数则一起取.1代表统计个数，大于1代表提取所有参数，0代表提取某一参数但不count,-1代表只统计count值(int)
# info:字段名(最高学历、最高职称等),放文本列表(list)
# scope:全区，片区，学校(str)
# school_name:校名(str)
# area_name:片区(str)
# period:高中、初中、小学、幼儿园(str)
# limit:限制搜索条数(int)
# order:限制特定搜索顺序，asc/desc(str)
# additional_requirement:额外的查询条件(list)

def generate_sql_sentence(kind: str, info_num: int, info: list, scope: str,
                          school_name="", area_name="", period=None,
                          limit=0, order="", additional_requirement=None, ):
    check_result = generate_sql_sentence_check(scope=scope, area_name=area_name, school_name=school_name, info=info,
                                               kind=kind, period=period)
    if not check_result[0]:
        print(check_result[1])
        raise MyError("插入内容验证不通过")

    sql_sentence = fill_scope_kind_period_others(info_num=info_num, info=info, scope=scope, school_name=school_name,
                                                 area_name=area_name, kind=kind, limit=limit, order=order,
                                                 period=period, additional_requirement=additional_requirement)

    return sql_sentence
