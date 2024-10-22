import sqlite3

from teacher_data_processing.read_database import get_database_data as gd
from teacher_data_processing.tool import func as tch_proc_func

kind_list = tch_proc_func.get_kind_list()
period_list = tch_proc_func.get_period_list()


def update(kind: str, school_name: str, year: str, period: str = None) -> None:
    """
    根据校名、学段、是否在编进行某所学校内教师信息统计
    :param kind: 是否在编
    :param school_name: 校名
    :param year: 年份
    :param period: 学段
    :return: 无
    """

    if kind not in ["在编", '编外']:
        raise tch_proc_func.MyError("kind参数错误")

    if period not in [None, "所有学段", "高中", "初中", "小学", "幼儿园", ""]:
        raise tch_proc_func.MyError("period参数错误")

    else:
        period = period if period not in ["所有学段", ""] else None

    result = []

    c, conn = tch_proc_func.connect_database()

    json_data = tch_proc_func.load_json_data(folder="result", file_name="teacher_info")

    # 检查一下有没有这个学校和学段，没有的话就报错
    check_result = tch_proc_func.school_name_and_period_check(kind=kind, school_name=school_name, period=period,
                                                              year=year)
    if not check_result[0]:
        print(check_result[1])
        return None

    ###
    # 统计总人数 - 分学校
    ###

    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=[""], scope="学校", year=year,
                                            school_name=school_name, period=period)

    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/总人数",
        value=result, json_data=json_data)

    result = []

    # 学校总人数统计结束

    ###
    # 最高学历统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高学历"], scope="学校", year=year,
                                            school_name=school_name, period=period)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = dict(
            sorted(
                c.fetchall(), key=lambda x: tch_proc_func.get_educational_background_order()[x[0]]
            )
        )

    except Exception as e:
        print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/最高学历",
        value=result, json_data=json_data)

    result = []

    # 学校最高学历统计结束

    ###
    # 性别统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["性别"], scope="学校", year=year,
                                            school_name=school_name, period=period, order="asc")

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = dict(
            c.fetchall()
        )

    except Exception as e:
        print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/性别",
        value=result, json_data=json_data)

    result = []

    # 学校性别统计结束

    ###
    # 最高职称统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高职称"], scope="学校", year=year,
                                            school_name=school_name, period=period)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = tch_proc_func.combine_highest_title(
            sorted(
                c.fetchall(), key=lambda x: tch_proc_func.get_highest_title_order()[x[0]]
            )
        )

    except Exception as e:
        print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/最高职称",
        value=result, json_data=json_data)

    result = []

    # 学校最高职称统计结束

    ###
    # 在编人员骨干教师统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["骨干教师"], scope="学校", year=year,
                                            school_name=school_name, period=period)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = tch_proc_func.combine_none_and_others(
            dict(
                sorted(
                    c.fetchall(), key=lambda x: tch_proc_func.get_cadre_teacher_order()[x[0]]
                )
            )
        )

    except Exception as e:
        print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/骨干教师",
        value=result, json_data=json_data)

    result = []

    ###
    # 学校教师资格统计
    ###
    # 先统计没有教资的
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格学段"], period=period,
                                            scope="学校", school_name=school_name, year=year,
                                            additional_requirement=['"教师资格学段" = "无"'])
    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/教师资格/未持教师资格",
        value=result, json_data=json_data)

    result = []

    # 再统计有教资的
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格学段"], period=period,
                                            scope="学校", school_name=school_name, year=year,
                                            additional_requirement=['"教师资格学段" != "无"'])
    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/教师资格/持有教师资格",
        value=result, json_data=json_data)

    result = []

    # 学校教师资格统计结束

    # 统计一下在编编外的特殊信息
    if kind == "在编":
        json_data = data_00_unique(json_data=json_data, school_name=school_name, period=period, c=c, conn=conn,
                                   year=year, kind=kind)

    elif kind == "编外":
        json_data = data_01_unique(json_data=json_data, school_name=school_name, period=period, c=c, conn=conn,
                                   year=year, kind=kind)

    tch_proc_func.save_json_data(json_data=json_data, folder="result", file_name="teacher_info")

    tch_proc_func.disconnect_database(conn=conn)

    return None


# 更新一些在编特有的信息
def data_00_unique(json_data: dict, school_name: str, year: str, kind: str, c: sqlite3.Cursor, conn: sqlite3.Connection, period: str = None) -> dict:
    """
    根据校名、学段、是否在编进行某所学校内在编教师信息统计
    :param json_data: 经过更新在编编外都有的信息后的json文件
    :param school_name: 校名
    :param year: 年份
    :param kind: 是否在编
    :param c: 数据库连接
    :param conn: 数据库连接
    :param period: 学段
    :return: 更新后生成的字典
    """

    result = []

    ###
    # 在编人员年龄统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["年龄"], scope="学校", year=year,
                                            school_name=school_name, period=period)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = tch_proc_func.age_statistics(
            age_count_list=c.fetchall()
        )

    except Exception as e:
        print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/年龄",
        value=result, json_data=json_data)

    result = []

    # 在编人员年龄统计（分学校）结束

    ###
    # 在编人员主教学科统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["主教学科"], scope="学校",
                                            school_name=school_name,
                                            period=period, limit=20, order="desc", year=year,
                                            additional_requirement=['"主教学科" != "无"'])

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = dict(
            c.fetchall()
        )

    except Exception as e:
        print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/主教学科",
        value=result, json_data=json_data)

    result = []

    # 在编人员学科统计（分学校）结束

    ###
    # 在编人员院校级别统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=0, info=["参加工作前毕业院校代码"], scope="学校",
                                            year=year,
                                            school_name=school_name, period=period,
                                            additional_requirement=['("参加工作前学历" = "本科" '
                                                                    'or "参加工作前学历" = "硕士研究生" '
                                                                    'or "参加工作前学历" = "博士研究生")'])

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = tch_proc_func.count_school_id(
            c.fetchall()
        )

    except Exception as e:
        print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/院校级别",
        value=result, json_data=json_data)

    result = []

    # 在编人员毕业院校统计（分学校）结束

    ###
    # 在编人员三名工作室主持人统计 - 分学校
    ###
    # 这里统计有多少是主持人
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=-1, info=["四名工作室主持人"], school_name=school_name,
                                            year=year,
                                            period=period, scope="学校", additional_requirement=['"四名工作室主持人" != "无"'])
    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/四名工作室/四名工作室主持人",
        value=result, json_data=json_data)

    result = []

    # 这里统计有多少不是主持人
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=-1, info=["四名工作室主持人"], school_name=school_name,
                                            year=year,
                                            period=period, scope="学校", additional_requirement=['"四名工作室主持人" = "无"'])
    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/四名工作室/无",
        value=result, json_data=json_data)

    result = []

    # 在编人员三名工作室主持人统计（分学校）结束

    ###
    # 在编人员支教地域统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["支教地域"], scope="学校", year=year,
                                            school_name=school_name, period=period)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = dict(
            sorted(
                c.fetchall(), key=lambda x: tch_proc_func.get_area_of_supporting_education_order()[x[0]]
            )
        )

    except Exception as e:
        print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/支教地域",
        value=result, json_data=json_data)

    result = []

    # 在编人员支教地域统计（分学校）结束

    return json_data


# 更新一些非在编特有的信息
def data_01_unique(json_data: dict, school_name: str, year: str, kind: str, c: sqlite3.Cursor, conn: sqlite3.Connection, period: str = None) -> dict:
    """
    根据校名、学段、是否在编进行某所学校内在编教师信息统计
    :param json_data: 经过更新在编编外都有的信息后的json文件
    :param school_name: 校名
    :param year: 年份
    :param kind: 是否在编
    :param c: 数据库连接
    :param conn: 数据库连接
    :param period: 学段
    :return: 更新后生成的字典
    """
    return json_data


if __name__ == '__main__':
    pass
    # update(kind="在编", school_name="广州市白云中学", period="高中", year="2023")
    # update(kind="在编", school_name="广州市白云区广州空港实验中学", year="2023")
    # update(kind="编外", school_name="广州市实验外语学校", period="高中", year="2023")
    # update(kind="在编", school_name="广州市培英中学", year="2023")
