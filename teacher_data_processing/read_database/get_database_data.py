import json
from pathlib import Path


def get_teacher_table_list() -> dict:
    """
    获取在编与否、年份与教师信息表名的逻辑关系，供其他模块查询json文件时获取
    :return: get_teacher_table_list()["在编"]["2024"]='teacher_data_0_2024'
    """

    with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\database\database_basic_info.json",
              "r", encoding='UTF-8') as file:  # ISO-8859-1
        loaded_data = json.load(file)

    teacher_table_list = loaded_data['teacher_table_list']

    return teacher_table_list


class MyError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def string_link(str1: str, str2: str, start_sign: int):
    """
    生成sql语句时连接查询条件
    :param str1: 查询语句或条件
    :param str2: 条件
    :param start_sign: str1是sql语句还是条件。0代表是语句，因此用where开头；1代表是条件，因此用and连接
    :return: 连接后的sql语句
    """

    if start_sign == 0:
        return f'{str1} where {str2} '

    elif start_sign == 1:
        return f'{str1} and {str2} '

    else:
        raise MyError("字符串结合不符合预期")


def generate_sql_sentence_check(scope: str, area_name: str, school_name: str, info: list, kind: str, period: str = None) -> list[bool | str]:
    """
    检查生成sql语句所用的参数是否有不合理的地方
    :param scope: 查询范围，可以填全区、片区、学校
    :param area_name: 片区名
    :param school_name: 校名
    :param info: 字段列表
    :param kind: 教师类型，在编或编外
    :param period: 学段，可以不填或填高中、初中、小学、幼儿园
    :return: 返回一个结果列表，首项为布尔值，真代表通过检验；第二项是文本型错误信息
    """

    # 判断是否有选择限定类型但未填信息的情况
    if scope == "片区" and area_name == "":
        return [False, "未填写片区"]

    if scope == "学校" and school_name == "":
        return [False, "未填写学校"]

    # 检查插入的info项是否与info_num对应
    if not isinstance(info, list):
        return [False, "传入info不是列表"]

    if kind not in ["在编", '编外']:
        return [False, f"kind参数错误:{kind}"]

    if period not in [None, "高中", "初中", "小学", "幼儿园", ""]:
        return [False, f"period参数错误:{period}"]

    return [True, "正常"]


def fill_scope_kind_period_others(info_num: int, info: list, scope: str, year: str,
                                  kind: str, school_name: str = "", area_name: str = "", period: str = None,
                                  limit: int = 0, order: str = "", additional_requirement: list = None, ) -> str:
    """
    根据参数填充sql语句
    :param info_num: 字段数量，-1代表统计count(*)，0代表统计某一个字段，1代表统计某一个字段及其count(*)，info_num>1代表查询多个字段
    :param info: 字段列表
    :param scope: 查询范围（全区，片区，学校）
    :param year: 年份
    :param kind: 教师类别（在编、编外）
    :param school_name: 校名
    :param area_name: 片区名
    :param period: 学段
    :param limit: 限制查询结果的数量
    :param order: 正序（asc）或逆序（desc）
    :param additional_requirement:
    :return: 返回sql语句
    """

    start_sign = 0  # 0代表初始第一个条件，1代表后续条件

    # 采集某一字段的统计数据
    if info_num == 1:

        sql_sentence = fr'select "{info[0]}",count(*) from {get_teacher_table_list()[kind][year]} '

        if scope == "全区":
            pass

        elif scope == "学校":
            sql_sentence = string_link(str1=sql_sentence, str2=fr' "校名" = "{school_name}" ',
                                       start_sign=start_sign)
            start_sign = 1

        elif scope == "片区":
            sql_sentence = string_link(str1=sql_sentence, str2=fr' "区域" = "{area_name}" ', start_sign=start_sign)
            start_sign = 1

        if period is not None and period != "":
            sql_sentence = string_link(str1=sql_sentence, str2=fr' "任教学段" = "{period}" ', start_sign=start_sign)
            start_sign = 1

        if additional_requirement is not None:
            for requirement in additional_requirement:
                sql_sentence = string_link(str1=sql_sentence, str2=f' {requirement} ', start_sign=start_sign)
                start_sign = 1

        # 加入count语句的分类 group by
        sql_sentence += fr' group by "{info[0]}" '

        # 根据情况加入order by
        if order == 'asc':
            sql_sentence += " order by count(*) asc "

        if order == 'desc':
            sql_sentence += ' order by count(*) desc '

        # 加入限制条数（主要针对主教学科）
        if limit > 0:
            sql_sentence += fr' limit {limit} '

    elif info_num > 1 or info_num == 0:

        sql_sentence = fr'select '

        # 0的时候不需要叠
        if info_num == 0:
            sql_sentence += f' "{info[0]}" '

        else:
            for i in range(0, len(info)):

                if i == 0:
                    sql_sentence += f' "{info[i]}" '

                else:
                    sql_sentence += f', "{info[i]}" '

        sql_sentence += f' from {get_teacher_table_list()[kind][year]} '

        if scope == "全区":
            pass

        elif scope == "学校":
            sql_sentence = string_link(str1=sql_sentence, str2=fr' "校名" = "{school_name}" ',
                                       start_sign=start_sign)
            start_sign = 1

        elif scope == "片区":
            sql_sentence = string_link(str1=sql_sentence, str2=fr' "区域" = "{area_name}" ', start_sign=start_sign)
            start_sign = 1

        if period is not None and period != "":
            sql_sentence = string_link(str1=sql_sentence, str2=fr' "任教学段" = "{period}" ', start_sign=start_sign)
            start_sign = 1

        if additional_requirement is not None:
            for requirement in additional_requirement:
                sql_sentence = string_link(str1=sql_sentence, str2=requirement, start_sign=start_sign)
                start_sign = 1

        # 加入限制条数（主要针对主教学科）
        if limit > 0:
            sql_sentence += fr' limit {limit} '

    elif info_num == -1:

        sql_sentence = fr'select count(*) from {get_teacher_table_list()[kind][year]} '

        if scope == "全区":
            pass

        elif scope == "学校":
            sql_sentence = string_link(str1=sql_sentence, str2=fr' "校名" = "{school_name}" ',
                                       start_sign=start_sign)
            start_sign = 1

        elif scope == "片区":
            sql_sentence = string_link(str1=sql_sentence, str2=fr' "区域" = "{area_name}" ', start_sign=start_sign)
            start_sign = 1

        if period is not None and period != "":
            sql_sentence = string_link(str1=sql_sentence, str2=fr' "任教学段" = "{period}" ', start_sign=start_sign)
            start_sign = 1

        if additional_requirement is not None:
            for requirement in additional_requirement:
                sql_sentence = string_link(str1=sql_sentence, str2=requirement, start_sign=start_sign)
                start_sign = 1

    else:
        raise MyError("info_num不对劲")

    return sql_sentence


def generate_sql_sentence(kind: str, info_num: int, info: list, scope: str, year: str,
                          school_name: str = "", area_name: str = "", period: str = None,
                          limit: int = 0, order: str = "", additional_requirement: list = None, ) -> str:
    """
    用于根据参数检查并生成sql语句
    :param kind: 教师类型（在编，编外）
    :param info_num: ，-1代表统计count(*)，0代表统计某一个字段，1代表统计某一个字段及其count(*)，info_num>1代表查询多个字段
    :param info: 字段列表
    :param scope: 查询范围（全区，片区，学校）
    :param year: 年份
    :param school_name: 校名
    :param area_name: 片区名
    :param period: 学段
    :param limit: 结果条数限制
    :param order: 正序（asc）或逆序（desc）
    :param additional_requirement: 额外查询条件列表
    :return: sql语句
    """
    check_result = generate_sql_sentence_check(scope=scope, area_name=area_name, school_name=school_name, info=info,
                                               kind=kind, period=period)
    if not check_result[0]:
        print(check_result[1])
        raise MyError("插入内容验证不通过")

    sql_sentence = fill_scope_kind_period_others(info_num=info_num, info=info, scope=scope, school_name=school_name,
                                                 area_name=area_name, kind=kind, limit=limit, order=order, year=year,
                                                 period=period, additional_requirement=additional_requirement)

    return sql_sentence
