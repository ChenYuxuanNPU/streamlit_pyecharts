import sqlite3

from teacher_data_processing.read_database import get_database_data as gd
from teacher_data_processing.tool import func as tch_proc_func


def update(year: str, kind: str) -> dict:
    """
    更新某一年某一类型区级教师数据
    :param year: 年份
    :param kind: 在编或编外
    :return: 更新结果字典
    """
    result = []

    c, conn = tch_proc_func.connect_database()

    json_data = tch_proc_func.load_json_data(folder="result", file_name="teacher_info")

    # 下面更新在编和编外都有的字段

    # 先统计下总人数
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=[""], scope="全区", year=year)

    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/总人数", value=result,
                                              json_data=json_data)

    result = []

    # 总人数统计结束

    ###
    # 全区最高学历统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高学历"], scope="全区", year=year)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)

        result = dict(
            sorted(
                c.fetchall(), key=lambda x: tch_proc_func.get_educational_background_order()[x[0]]
            )
        )

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/最高学历", value=result,
                                              json_data=json_data)

    result = []

    # 全区学历统计结束

    ###
    # 全区性别统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["性别"], scope="全区", order="asc", year=year)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = dict(
            c.fetchall()
        )

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/性别", value=result,
                                              json_data=json_data)

    result = []

    # 全区性别统计结束

    ###
    # 全区片区统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["区域"],
                                            scope="全区", order="asc", year=year)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = dict(
            sorted(
                c.fetchall(), key=lambda x: tch_proc_func.get_area_order()[x[0]]
            )
        )

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')
        print("111")

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/片区统计", value=result,
                                              json_data=json_data)

    result = []

    ###
    # 全区学段分布统计
    ###

    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["任教学段"], year=year,
                                            scope="全区", additional_requirement=['"任教学段" != "其他"'])

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = dict(
            sorted(
                c.fetchall(), key=lambda x: tch_proc_func.get_period_order()[x[0]]
            )
        )

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/学段统计", value=result,
                                              json_data=json_data)

    result = []

    # 全区学段分布统计结束

    ###
    # 全区骨干教师统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["骨干教师"], scope="全区", year=year)

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
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/骨干教师", value=result,
                                              json_data=json_data)

    result = []

    # 全区骨干教师统计结束

    ###
    # 全区教师资格统计
    ###

    # 先统计全区没有教资的
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格学段"], scope="全区", year=year,
                                            additional_requirement=['"教师资格学段" = "无"'])

    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/教师资格/未持有教师资格",
                                              value=result,
                                              json_data=json_data)

    result = []

    # 再统计有教资的
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格学段"], scope="全区", year=year,
                                            additional_requirement=['"教师资格学段" != "无"'])

    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/教师资格/持有教师资格", value=result,
                                              json_data=json_data)

    result = []

    ###
    # 全区教师资格统计 - 幼儿园
    ###

    # 先统计没有教资的
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格学段"], scope="全区",
                                            period="幼儿园", year=year,
                                            additional_requirement=['"教师资格学段" = "无"'])

    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/幼儿园/教师资格/未持有教师资格", value=result,
                                              json_data=json_data)

    result = []

    # 再统计有教资的
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格学段"], scope="全区",
                                            period="幼儿园", year=year,
                                            additional_requirement=['"教师资格学段" != "无"'])

    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/幼儿园/教师资格/持有教师资格", value=result,
                                              json_data=json_data)

    result = []

    ###
    # 全区教师资格统计 - 中小学
    ###

    # 先统计没有教资的
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格学段"], scope="全区", year=year,
                                            additional_requirement=['"教师资格学段" = "无"', '"任教学段" != "幼儿园"'])

    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/中小学/教师资格/未持有教师资格", value=result,
                                              json_data=json_data)

    result = []

    # 再统计有教资的
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格学段"], scope="全区", year=year,
                                            additional_requirement=['"教师资格学段" != "无"', '"任教学段" != "幼儿园"'])

    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/中小学/教师资格/持有教师资格", value=result,
                                              json_data=json_data)

    result = []

    # 全区教师资格统计结束

    ###
    # 全区最高职称统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高职称"], scope="全区", year=year)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = tch_proc_func.combine_highest_title(
            sorted(
                c.fetchall(), key=lambda x: tch_proc_func.get_highest_title_order()[x[0]]
            )
        )

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/最高职称", value=result,
                                              json_data=json_data)

    result = []

    # 全区最高职称统计结束

    ###
    # 全区三名工作室主持人统计
    ###

    # 这里统计有多少是主持人
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["四名工作室主持人"], year=year,
                                            scope="全区", additional_requirement=['"四名工作室主持人" != "无"'])
    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/四名工作室/四名工作室主持人",
                                              value=result,
                                              json_data=json_data)

    result = []

    # 这里统计有多少不是主持人
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["四名工作室主持人"], year=year,
                                            scope="全区", additional_requirement=['"四名工作室主持人" = "无"'])
    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/四名工作室/无", value=result,
                                              json_data=json_data)

    result = []

    # 全区三名工作室主持人统计结束

    ###
    # 全区人数分布前三十数量统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["校名"], year=year,
                                            scope="全区", limit=30, order="desc",
                                            additional_requirement=['"学校类型" != "幼儿园" and "学校类型" != "教学支撑单位"'])

    try:
        c.execute(sql_sentence)
        result = dict(
            c.fetchall()
        )

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/教师分布前三十", value=result,
                                              json_data=json_data)

    result = []

    # 全区人数分布前三十统计结束

    ###
    # 全区人数分布倒三十数量统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["校名"], year=year,
                                            scope="全区", limit=30, order="asc", additional_requirement=[
            '"学校类型" != "幼儿园" and "学校类型" != "教学支撑单位"'])

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = dict(
            c.fetchall()
        )

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/教师分布后三十", value=result,
                                              json_data=json_data)

    result = []

    # 全区人数分布倒三十统计结束

    match kind:

        case "在编":

            # 这里更新一下在编的独特的字段
            json_data = data_00_unique(json_data=json_data, c=c, conn=conn, year=year, kind=kind)

            # 这里更新全区在编不同学段的统计信息
            json_data = period_update(json_data=json_data, c=c, conn=conn, year=year, kind=kind)

        case "编外":

            # 这里更新一下编外的独特的字段
            json_data = data_01_unique(json_data=json_data, c=c, conn=conn, year=year, kind=kind)

        case _:
            print("报错 district.py")

    tch_proc_func.save_json_data(json_data=json_data, folder="result", file_name="teacher_info")

    tch_proc_func.disconnect_database(conn=conn)

    return json_data


def data_00_unique(json_data: dict, year: str, c: sqlite3.Cursor, conn: sqlite3.Connection, kind: str = "在编") -> dict:
    """
    更新在编独特的信息
    :param json_data: 基础数据更新后的字典
    :param year: 年份
    :param c: 数据库连接
    :param conn: 数据库连接
    :param kind: 在编或编外，默认在编
    :return:
    """

    result = []

    ###
    # 全区在编人员年龄统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["年龄"], scope="全区", year=year)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = tch_proc_func.age_statistics(
            age_count_list=c.fetchall()
        )

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/年龄", value=result,
                                              json_data=json_data)

    result = []

    # 全区在编年龄统计结束

    ###
    # 全区在编人员主教学科统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["主教学科"], year=year,
                                            scope="全区", limit=20, order="desc",
                                            additional_requirement=['"主教学科" != "无"'])

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = dict(
            c.fetchall()
        )

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/主教学科", value=result,
                                              json_data=json_data)

    result = []

    # 全区在编人员主教学科统计结束

    ###
    # 全区在编人员专业技术岗位统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["专业技术岗位"], scope="全区",
                                            year=year,)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = dict(
            c.fetchall()
        )

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/专业技术岗位", value=result,
                                              json_data=json_data)
    result = []

    # 全区在编人员专业技术岗位统计结束

    ###
    # 全区在编人员院校级别统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=0, info=["参加工作前毕业院校代码"], scope="全区",
                                            year=year,
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
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/院校级别", value=result,
                                              json_data=json_data)

    result = []

    # 全区在编人员院校级别统计结束

    ###
    # 全区在编人员行政职务统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["行政职务"], scope="全区", year=year)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        # result = tch_proc_func.combine_administrative_position(
        #     sorted(
        #         c.fetchall(), key=lambda x: tch_proc_func.get_current_administrative_position_order()[x[0]]
        #     )
        # )

        result = dict(
            sorted(
                c.fetchall(), key=lambda x: tch_proc_func.get_current_administrative_position_order()[x[0]]
            )
        )

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/行政职务", value=result,
                                              json_data=json_data)

    result = []

    # 全区在编人员行政职务统计结束

    ###
    # 全区在编人员支教地域统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["支教地域"], scope="全区", year=year)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = dict(
            sorted(
                c.fetchall(), key=lambda x: tch_proc_func.get_area_of_supporting_education_order()[x[0]]
            )
        )

    except Exception as e:
        print('\033[1;91m' + f"{e}" + '\033[0m')

    finally:
        conn.commit()

    json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/所有学段/支教地域", value=result,
                                              json_data=json_data)

    result = []

    # 全区在编人员支教地域统计结束

    return json_data


###
# 这里更新编外独特的字段
###

def data_01_unique(json_data: dict, year: str, c: sqlite3.Cursor, conn: sqlite3.Connection, kind: str = "编外") -> dict:
    """
    更新编外独特的信息
    :param json_data: 基础数据更新后的字典
    :param year: 年份
    :param c: 数据库连接
    :param conn: 数据库连接
    :param kind: 在编或编外，默认编外
    :return:
    """

    return json_data


def period_update(json_data: dict, year: str, c: sqlite3.Cursor, conn: sqlite3.Connection, kind: str = "在编") -> dict:
    """
    更新在编不同学段的统计信息
    :param json_data: 基础数据更新后的字典
    :param year: 年份
    :param c: 数据库连接
    :param conn: 数据库连接
    :param kind: 在编或编外，默认在编
    :return:
    """

    result = []

    # 遍历四个学段
    for period in tch_proc_func.get_period_list():

        ###
        # 全区分学段人员年龄统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["年龄"], scope="全区", period=period,
                                                year=year)

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = tch_proc_func.age_statistics(
                age_count_list=c.fetchall()
            )

        except Exception as e:
            print('\033[1;91m' + f"{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/{period}/年龄", value=result,
                                                  json_data=json_data)
        # json_data['在编']['全区'][period]['年龄'] = copy.deepcopy(dict(result))
        result = []

        # 全区分学段人员年龄统计结束

        ###
        # 全区分学段人员性别统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["性别"], year=year,
                                                scope="全区", period=period, order="asc")

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                c.fetchall()
            )

        except Exception as e:
            print('\033[1;91m' + f"{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/{period}/性别", value=result,
                                                  json_data=json_data)
        # json_data['在编']['全区'][period]['性别'] = copy.deepcopy(dict(result))
        result = []

        # 全区分学段人员性别统计结束

        ###
        # 全区分学段主教学科统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["主教学科"], year=year,
                                                scope="全区", limit=20, order="desc", period=period,
                                                additional_requirement=['"主教学科" != "无"'])

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                c.fetchall()
            )

        except Exception as e:
            print('\033[1;91m' + f"{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/{period}/主教学科", value=result,
                                                  json_data=json_data)
        # json_data['在编']['全区'][period]['主教学科'] = copy.deepcopy(result)
        result = []

        # 全区分学段主教学科统计结束

        ###
        # 全区分学段最高学历统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高学历"], scope="全区", period=period,
                                                year=year)

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                sorted(
                    c.fetchall(), key=lambda x: tch_proc_func.get_educational_background_order()[x[0]]
                )
            )

        except Exception as e:
            print('\033[1;91m' + f"{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/{period}/最高学历", value=result,
                                                  json_data=json_data)
        # json_data['在编']['全区'][period]['最高学历'] = copy.deepcopy(result)

        result = []

        # 全区分学段学历统计结束

        ###
        # 全区分学段最高职称统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高职称"], scope="全区", period=period,
                                                year=year)

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = tch_proc_func.combine_highest_title(
                sorted(
                    c.fetchall(), key=lambda x: tch_proc_func.get_highest_title_order()[x[0]]
                )
            )

        except Exception as e:
            print('\033[1;91m' + f"{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/{period}/最高职称", value=result,
                                                  json_data=json_data)

        result = []

        # 全区分学段最高职称统计结束

        ###
        # 全区分学段在编人员院校级别统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=0, info=["参加工作前毕业院校代码"], scope="全区",
                                                period=period,
                                                year=year,
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
            print('\033[1;91m' + f"{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/全区/{period}/院校级别", value=result,
                                                  json_data=json_data)

        result = []

        # 全区分学段在编人员院校级别统计结束

    return json_data


if __name__ == '__main__':
    update(year="2023", kind="在编")
    update(year="2023", kind="编外")
