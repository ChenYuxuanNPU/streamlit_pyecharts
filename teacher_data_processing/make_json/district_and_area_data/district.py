from teacher_data_processing.tool.func import *


def update(year: str, kind: str) -> dict:
    """
    更新某一年某一类型区级教师数据
    :param year: 年份
    :param kind: 在编或编外
    :return: 更新结果字典
    """

    json_data = load_json_data(folder="result", file_name="teacher_info")

    #  下面更新在编和编外都有的字段

    #  先统计下总人数
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/总人数",
                                value=execute_sql_sentence(
                                    sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year}')[
                                    0][0],
                                json_data=json_data)

    #  统计全区最高学历
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/最高学历",
                                value=dict(
                                    sorted(
                                        execute_sql_sentence(
                                            sentence=f'select "最高学历", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} group by "最高学历"'),
                                        key=lambda x: get_educational_background_order()[x[0]]
                                    )
                                ),
                                json_data=json_data)

    #  统计全区性别
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/性别",
                                value=dict(
                                    execute_sql_sentence(
                                        sentence=f'select "性别", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} group by "性别" order by count(*) asc')
                                ),
                                json_data=json_data)

    #  统计全区片镇
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/片区统计",
                                value=dict(
                                    sorted(
                                        execute_sql_sentence(
                                            sentence=f'select "区域", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} group by "区域" order by count(*) asc'),
                                        key=lambda x: get_area_order()[x[0]]
                                    )
                                ),
                                json_data=json_data)

    #  统计全区学段分布
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/学段统计",
                                value=dict(
                                    sorted(
                                        execute_sql_sentence(
                                            sentence=f'select "任教学段",count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "任教学段" != "其他" group by "任教学段"'),
                                        key=lambda x: get_period_order()[x[0]]
                                    )
                                ),
                                json_data=json_data)

    #  统计全区骨干教师
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/骨干教师",
                                value=combine_none_and_others(
                                    dict(
                                        sorted(
                                            execute_sql_sentence(
                                                sentence=f'select "骨干教师",count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} group by "骨干教师"'),
                                            key=lambda x: get_cadre_teacher_order()[x[0]]
                                        )
                                    )
                                ),
                                json_data=json_data)

    #  统计全区教师资格

    #  先统计全区没有教资的
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/教师资格/未持有教师资格",
                                value=execute_sql_sentence(
                                    sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "教师资格学段" = "无"')[
                                    0][0],
                                json_data=json_data)

    #  再统计有教资的
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/教师资格/持有教师资格",
                                value=execute_sql_sentence(
                                    sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "教师资格学段" != "无"')[
                                    0][0],
                                json_data=json_data)

    #  统计全区教师资格 - 幼儿园

    #  先统计没有教资的
    json_data = dict_assignment(route=f"{year}/{kind}/全区/幼儿园/教师资格/未持有教师资格",
                                value=execute_sql_sentence(
                                    sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "任教学段" = "幼儿园" and "教师资格学段" = "无"')[
                                    0][0],
                                json_data=json_data)

    #  再统计有教资的
    json_data = dict_assignment(route=f"{year}/{kind}/全区/幼儿园/教师资格/持有教师资格",
                                value=execute_sql_sentence(
                                    sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "任教学段" = "幼儿园" and "教师资格学段" != "无"')[
                                    0][0],
                                json_data=json_data)

    #  统计全区教师资格 - 中小学

    #  先统计没有教资的
    json_data = dict_assignment(route=f"{year}/{kind}/全区/中小学/教师资格/未持有教师资格",
                                value=execute_sql_sentence(
                                    sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "教师资格学段" = "无" and "任教学段" != "幼儿园"')[
                                    0][0],
                                json_data=json_data)

    #  再统计有教资的
    json_data = dict_assignment(route=f"{year}/{kind}/全区/中小学/教师资格/持有教师资格",
                                value=execute_sql_sentence(
                                    sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "教师资格学段" != "无" and "任教学段" != "幼儿园"')[
                                    0][0],
                                json_data=json_data)

    #  统计全区最高职称
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/最高职称",
                                value=combine_highest_title(
                                    sorted(
                                        execute_sql_sentence(
                                            sentence=f'select "最高职称", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} group by "最高职称"'),
                                        key=lambda x: get_highest_title_order()[x[0]]
                                    )
                                ),
                                json_data=json_data)

    #  统计全区三名工作室主持人

    #  这里统计有多少是主持人
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/四名工作室/四名工作室主持人",
                                value=execute_sql_sentence(
                                    sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "四名工作室主持人" != "无"')[
                                    0][0],
                                json_data=json_data)

    #  这里统计有多少不是主持人
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/四名工作室/无",
                                value=execute_sql_sentence(
                                    sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "四名工作室主持人" = "无"')[
                                    0][0],
                                json_data=json_data)

    #  统计全区人数分布前三十数量
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/教师分布前三十",
                                value=simplify_school_name(
                                    d=dict(
                                        execute_sql_sentence(
                                            sentence=f'select "校名", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "学校类型" != "幼儿园" and "学校类型" != "教学支撑单位" group by "校名" order by count(*) desc limit 30')
                                    )
                                ),
                                json_data=json_data)

    #  统计全区人数分布倒数前三十数量
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/教师分布后三十",
                                value=simplify_school_name(
                                    d=dict(
                                        execute_sql_sentence(
                                            sentence=f'select "校名", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "学校类型" != "幼儿园" and "学校类型" != "教学支撑单位" group by "校名" order by count(*) asc limit 30')
                                    )
                                ),
                                json_data=json_data)

    match kind:

        case "在编":

            #  这里更新一下在编的独特的字段
            json_data = data_00_unique(json_data=json_data, year=year, kind=kind)

            #  这里更新全区在编不同学段的统计信息
            # json_data = period_update(json_data=json_data, year=year, kind=kind)

        case "编外":
            pass
            #  这里更新一下编外的独特的字段
            json_data = data_01_unique(json_data=json_data, year=year, kind=kind)

        case _:
            print("报错 district.py")

    save_json_data(json_data=json_data, folder="result", file_name="teacher_info")

    return json_data


def data_00_unique(json_data: dict, year: str, kind: str = "在编") -> dict:
    """
    更新在编独特的信息
    :param json_data: 基础数据更新后的字典
    :param year: 年份
    :param kind: 在编或编外，默认在编
    :return:
    """

    #  统计全区在编人员年龄
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/年龄",
                                value=age_statistics(
                                    age_count_list=execute_sql_sentence(
                                        sentence=f'select "年龄", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} group by "年龄"')
                                ),
                                json_data=json_data)

    #  统计全区在编人员主教学科
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/主教学科",
                                value=dict(
                                    execute_sql_sentence(
                                        sentence=f'select "主教学科", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "主教学科" != "无" group by "主教学科" order by count(*) desc limit 20')
                                ),
                                json_data=json_data)

    #  统计全区在编人员专业技术岗位
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/专业技术岗位",
                                value=dict(
                                    execute_sql_sentence(
                                        sentence=f'select "专业技术岗位", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} group by "专业技术岗位"')
                                ),
                                json_data=json_data)

    #  统计全区在编人员院校级别
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/院校级别",
                                value=count_school_id(
                                    execute_sql_sentence(
                                        sentence=f'select "参加工作前毕业院校代码" from teacher_data_{0 if kind == "在编" else 1}_{year} where ("参加工作前学历" in ("本科", "硕士研究生", "博士研究生"))')
                                ),
                                json_data=json_data)

    #  统计全区在编人员行政职务
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/行政职务",
                                value=dict(
                                    sorted(
                                        execute_sql_sentence(
                                            sentence=f'select "行政职务", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} group by "行政职务"'),
                                        key=lambda x: get_current_administrative_position_order()[x[0]]
                                    )
                                ),
                                json_data=json_data)

    #  统计全区在编人员支教地域
    json_data = dict_assignment(route=f"{year}/{kind}/全区/所有学段/支教地域",
                                value=dict(
                                    sorted(
                                        execute_sql_sentence(
                                            sentence=f'select "支教地域", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} group by "支教地域"'),
                                        key=lambda x: get_area_of_supporting_education_order()[x[0]]
                                    )
                                ),
                                json_data=json_data)

    return json_data


def data_01_unique(json_data: dict, year: str, kind: str = "编外") -> dict:
    """
    更新编外独特的信息
    :param json_data: 基础数据更新后的字典
    :param year: 年份
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

    #  遍历四个学段
    for period in get_period_list():

        ###
        #  全区分学段人员年龄统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["年龄"], scope="全区", period=period,
                                                year=year)

        #  取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = age_statistics(
                age_count_list=c.fetchall()
            )

        except Exception as e:
            print('\033[1;91m' + f"{e}" + '\033[0m')
            print(sql_sentence)

        finally:
            conn.commit()

        json_data = dict_assignment(route=f"{year}/{kind}/全区/{period}/年龄", value=result,
                                    json_data=json_data)
        #  json_data['在编']['全区'][period]['年龄'] = copy.deepcopy(dict(result))
        result = []

        #  全区分学段人员年龄统计结束

        ###
        #  全区分学段人员性别统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["性别"], year=year,
                                                scope="全区", period=period, order="asc")

        #  取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                c.fetchall()
            )

        except Exception as e:
            print('\033[1;91m' + f"{e}" + '\033[0m')
            print(sql_sentence)

        finally:
            conn.commit()

        json_data = dict_assignment(route=f"{year}/{kind}/全区/{period}/性别", value=result,
                                    json_data=json_data)
        #  json_data['在编']['全区'][period]['性别'] = copy.deepcopy(dict(result))
        result = []

        #  全区分学段人员性别统计结束

        ###
        #  全区分学段主教学科统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["主教学科"], year=year,
                                                scope="全区", limit=20, order="desc", period=period,
                                                additional_requirement=['"主教学科" != "无"'])

        #  取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                c.fetchall()
            )

        except Exception as e:
            print('\033[1;91m' + f"{e}" + '\033[0m')
            print(sql_sentence)

        finally:
            conn.commit()

        json_data = dict_assignment(route=f"{year}/{kind}/全区/{period}/主教学科", value=result,
                                    json_data=json_data)
        #  json_data['在编']['全区'][period]['主教学科'] = copy.deepcopy(result)
        result = []

        #  全区分学段主教学科统计结束

        ###
        #  全区分学段最高学历统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高学历"], scope="全区", period=period,
                                                year=year)

        #  取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                sorted(
                    c.fetchall(), key=lambda x: get_educational_background_order()[x[0]]
                )
            )

        except Exception as e:
            print('\033[1;91m' + f"{e}" + '\033[0m')
            print(sql_sentence)

        finally:
            conn.commit()

        json_data = dict_assignment(route=f"{year}/{kind}/全区/{period}/最高学历", value=result,
                                    json_data=json_data)
        #  json_data['在编']['全区'][period]['最高学历'] = copy.deepcopy(result)

        result = []

        #  全区分学段学历统计结束

        ###
        #  全区分学段最高职称统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高职称"], scope="全区", period=period,
                                                year=year)

        #  取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = combine_highest_title(
                sorted(
                    c.fetchall(), key=lambda x: get_highest_title_order()[x[0]]
                )
            )

        except Exception as e:
            print('\033[1;91m' + f"{e}" + '\033[0m')
            print(sql_sentence)

        finally:
            conn.commit()

        json_data = dict_assignment(route=f"{year}/{kind}/全区/{period}/最高职称", value=result,
                                    json_data=json_data)

        result = []

        #  全区分学段最高职称统计结束

        ###
        #  全区分学段在编人员院校级别统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=0, info=["参加工作前毕业院校代码"], scope="全区",
                                                period=period,
                                                year=year,
                                                additional_requirement=[
                                                    '("参加工作前学历" in ("本科", "硕士研究生", "博士研究生"))'])

        #  取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = count_school_id(
                c.fetchall()
            )

        except Exception as e:
            print('\033[1;91m' + f"{e}" + '\033[0m')
            print(sql_sentence)

        finally:
            conn.commit()

        json_data = dict_assignment(route=f"{year}/{kind}/全区/{period}/院校级别", value=result,
                                    json_data=json_data)

        result = []

        #  全区分学段在编人员院校级别统计结束

    return json_data


if __name__ == '__main__':
    update(year="2023", kind="在编")
    update(year="2023", kind="编外")
    update(year="2024", kind="在编")
    update(year="2024", kind="编外")
