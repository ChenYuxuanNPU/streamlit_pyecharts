from data_processing.read_database import get_database_data as gd
from data_processing.tool import module as m_proc

kind_list = m_proc.kind_list
period_list = m_proc.period_list


def update():
    result = []

    c, conn = m_proc.connect_database()

    json_data = m_proc.load_json_data(file_name="output")

    # 下面更新在编非编都有的字段

    # 首先更新全区的在编非编信息
    for kind in kind_list:  # ["在编", "非编"]:

        # 下面在字典中更新数据库查询结果

        # 先统计下总人数
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=[""], scope="全区")

        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/所有学段/总人数", value=result, json_data=json_data)
        # json_data[kind]['全区']['所有学段']['总人数'] = copy.deepcopy(result)

        result = []

        # 总人数统计结束

        ###
        # 全区最高学历统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高学历"], scope="全区")

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                sorted(
                    c.fetchall(), key=lambda x: m_proc.educational_background_order[x[0]]
                )
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/所有学段/最高学历", value=result, json_data=json_data)
        # json_data[kind]['全区']['所有学段']['最高学历'] = copy.deepcopy(result)

        result = []

        # 全区学历统计结束

        ###
        # 全区性别统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["性别"], scope="全区", order="asc")

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                c.fetchall()
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/所有学段/性别", value=result, json_data=json_data)

        result = []

        # 全区性别统计结束

        ###
        # 全区片区统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["片区"],
                                                scope="全区", order="asc")

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                c.fetchall()
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/所有学段/片区统计", value=result, json_data=json_data)
        # json_data[kind]['全区']['所有学段']['片区统计'] = copy.deepcopy(result)

        result = []

        ###
        # 全区学段分布统计
        ###

        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["学段"],
                                                scope="全区", additional_requirement=["period != '其他'"])

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                sorted(
                    c.fetchall(), key=lambda x: m_proc.period_order[x[0]]
                )
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/所有学段/学段统计", value=result, json_data=json_data)
        # json_data[kind]['全区']['所有学段']['学段统计'] = copy.deepcopy(result)

        result = []

        # 全区学段分布统计结束

        ###
        # 全区骨干教师统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["骨干教师"], scope="全区")

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = m_proc.combine_none_and_others(
                dict(
                    sorted(
                        c.fetchall(), key=lambda x: m_proc.cadre_teacher_order[x[0]]
                    )
                )
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/所有学段/骨干教师", value=result, json_data=json_data)
        # json_data[kind]['全区']['所有学段']['骨干教师'] = copy.deepcopy(result)

        result = []

        # 全区骨干教师统计结束

        ###
        # 全区教师资格统计
        ###

        # 先统计全区没有教资的
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], scope="全区",
                                                additional_requirement=["level_of_teacher_certification == '无'"])

        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/所有学段/教师资格/未持教师资格", value=result,
                                      json_data=json_data)
        # json_data[kind]['全区']['所有学段']['教师资格']['未持教师资格'] = copy.deepcopy(result)

        result = []

        # 再统计有教资的
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], scope="全区",
                                                additional_requirement=["level_of_teacher_certification != '无'"])

        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/所有学段/教师资格/持有教师资格", value=result,
                                      json_data=json_data)
        # json_data[kind]['全区']['所有学段']['教师资格']['持有教师资格'] = copy.deepcopy(result)

        result = []

        ###
        # 全区教师资格统计 - 幼儿园
        ###

        # 先统计没有教资的
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], scope="全区",
                                                period="幼儿园",
                                                additional_requirement=["level_of_teacher_certification == '无'"])

        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/幼儿园/教师资格/未持教师资格", value=result,
                                      json_data=json_data)
        # json_data[kind]['全区']['幼儿园']['教师资格']['未持教师资格'] = copy.deepcopy(result)

        result = []

        # 再统计有教资的
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], scope="全区",
                                                period="幼儿园",
                                                additional_requirement=["level_of_teacher_certification != '无'"])

        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/幼儿园/教师资格/持有教师资格", value=result,
                                      json_data=json_data)
        # json_data[kind]['全区']['幼儿园']['教师资格']['持有教师资格'] = copy.deepcopy(result)

        result = []

        ###
        # 全区教师资格统计 - 中小学
        ###

        # 先统计没有教资的
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], scope="全区",
                                                additional_requirement=["level_of_teacher_certification == '无'",
                                                                        "period != '幼儿园'"])

        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/中小学/教师资格/未持教师资格", value=result,
                                      json_data=json_data)
        # json_data[kind]['全区']['中小学']['教师资格']['未持教师资格'] = copy.deepcopy(result)

        result = []

        # 再统计有教资的
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], scope="全区",
                                                additional_requirement=["level_of_teacher_certification != '无'",
                                                                        "period != '幼儿园'"])

        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/中小学/教师资格/持有教师资格", value=result,
                                      json_data=json_data)
        # json_data[kind]['全区']['中小学']['教师资格']['持有教师资格'] = copy.deepcopy(result)

        result = []

        # 全区教师资格统计结束

        ###
        # 全区最高职称统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高职称"], scope="全区")

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = m_proc.combine_highest_title(
                sorted(
                    c.fetchall(), key=lambda x: m_proc.highest_title_order[x[0]]
                )
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/所有学段/最高职称", value=result, json_data=json_data)
        # json_data[kind]['全区']['所有学段']['最高职称'] = copy.deepcopy(result)

        result = []

        # 全区最高职称统计结束

        ###
        # 全区三名工作室主持人统计
        ###

        # 这里统计有多少是主持人
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["三名工作室"],
                                                scope="全区", additional_requirement=["title_01 != '无'"])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/所有学段/三名工作室/三名工作室主持人", value=result,
                                      json_data=json_data)
        # json_data[kind]['全区']['所有学段']['三名工作室']['三名工作室主持人'] = copy.deepcopy(result)

        result = []

        # 这里统计有多少不是主持人
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["三名工作室"],
                                                scope="全区", additional_requirement=["title_01 == '无'"])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/所有学段/三名工作室/无", value=result, json_data=json_data)
        # json_data[kind]['全区']['所有学段']['三名工作室']['无'] = copy.deepcopy(result)

        result = []

        # 全区三名工作室主持人统计结束

        ###
        # 全区人数分布top10数量统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["学校"],
                                                scope="全区", limit=10, order="desc", )

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = m_proc.simplify_school_name(
                dict1=dict(
                    c.fetchall()
                )
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"{kind}/全区/所有学段/教师分布", value=result, json_data=json_data)

        result = []

        # 全区人数分布top10统计结束

    # 这里更新一下在编和非编的独特的字段
    json_data = data_00_unique(json_data=json_data, c=c, conn=conn)

    json_data = data_01_unique(json_data=json_data, c=c, conn=conn)

    # 这里更新全区在编不同学段的统计信息
    json_data = period_update(json_data=json_data, c=c, conn=conn)

    m_proc.save_json_data(json_data=json_data, file_name="output")

    m_proc.disconnect_database(conn=conn)


###
# 这里更新在编独特的字段
###

def data_00_unique(json_data: dict, c, conn):
    result = []

    ###
    # 全区在编人员年龄统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["年龄"], scope="全区")

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = m_proc.age_statistics(
            age_count_list=c.fetchall()
        )

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    json_data = m_proc.dict_assignment(route="在编/全区/所有学段/年龄", value=result, json_data=json_data)
    # json_data['在编']['全区']['所有学段']['年龄'] = copy.deepcopy(dict(result))
    result = []

    # 全区在编年龄统计结束

    ###
    # 全区在编人员主教学科统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["主教学科"],
                                            scope="全区", limit=20, order="desc",
                                            additional_requirement=["major_discipline != '无'"])

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = dict(
            c.fetchall()
        )

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    json_data = m_proc.dict_assignment(route="在编/全区/所有学段/主教学科", value=result, json_data=json_data)
    # json_data['在编']['全区']['所有学段']['主教学科'] = copy.deepcopy(result)
    result = []

    # 全区在编人员主教学科统计结束

    ###
    # 全区在编人员院校级别统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=0, info=["院校代码"], scope="全区",
                                            additional_requirement=["(educational_background == '大学本科' "
                                                                    "or educational_background == '硕士研究生' "
                                                                    "or educational_background == '博士研究生')"])

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = m_proc.count_school_id(
            c.fetchall()
        )

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    json_data = m_proc.dict_assignment(route="在编/全区/所有学段/院校级别", value=result, json_data=json_data)
    # json_data['在编']['全区']['所有学段']['院校级别'] = copy.deepcopy(result)
    result = []

    # 全区在编人员院校级别统计结束

    ###
    # 全区在编人员行政职务统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["行政职务"], scope="全区")

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = m_proc.combine_administrative_position(
            sorted(
                c.fetchall(), key=lambda x: m_proc.current_administrative_position_order[x[0]]
            )
        )

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    json_data = m_proc.dict_assignment(route="在编/全区/所有学段/行政职务", value=result, json_data=json_data)
    # json_data['在编']['全区']['所有学段']['行政职务'] = copy.deepcopy(result)
    result = []

    # 全区在编人员行政职务统计结束

    ###
    # 全区在编人员支教地域统计
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["支教地域"], scope="全区", )

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = dict(
            sorted(
                c.fetchall(), key=lambda x: m_proc.area_of_supporting_education_order[x[0]]
            )
        )

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    json_data = m_proc.dict_assignment(route="在编/全区/所有学段/支教地域", value=result, json_data=json_data)
    # json_data['在编']['全区']['所有学段']['支教地域'] = copy.deepcopy(result)
    result = []

    # 全区在编人员支教地域统计结束

    return json_data


###
# 这里更新非编独特的字段
###

def data_01_unique(json_data: dict, c, conn):
    return json_data


###
# 这里更新在编不同学段的统计信息
###

def period_update(json_data: dict, c, conn):
    result = []

    # 遍历四个学段
    for period in period_list:

        ###
        # 全区分学段人员年龄统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["年龄"], scope="全区", period=period)

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = m_proc.age_statistics(
                age_count_list=c.fetchall()
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"在编/全区/{period}/年龄", value=result, json_data=json_data)
        # json_data['在编']['全区'][period]['年龄'] = copy.deepcopy(dict(result))
        result = []

        # 全区分学段人员年龄统计结束

        ###
        # 全区分学段人员性别统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["性别"],
                                                scope="全区", period=period, order="asc")

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                c.fetchall()
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"在编/全区/{period}/性别", value=result, json_data=json_data)
        # json_data['在编']['全区'][period]['性别'] = copy.deepcopy(dict(result))
        result = []

        # 全区分学段人员性别统计结束

        ###
        # 全区分学段主教学科统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["主教学科"],
                                                scope="全区", limit=20, order="desc", period=period,
                                                additional_requirement=["major_discipline != '无'"])

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                c.fetchall()
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"在编/全区/{period}/主教学科", value=result, json_data=json_data)
        # json_data['在编']['全区'][period]['主教学科'] = copy.deepcopy(result)
        result = []

        # 全区分学段主教学科统计结束

        ###
        # 全区分学段最高学历统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["最高学历"], scope="全区", period=period)

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                sorted(
                    c.fetchall(), key=lambda x: m_proc.educational_background_order[x[0]]
                )
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"在编/全区/{period}/最高学历", value=result, json_data=json_data)
        # json_data['在编']['全区'][period]['最高学历'] = copy.deepcopy(result)

        result = []

        # 全区分学段学历统计结束

        ###
        # 全区分学段最高职称统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["最高职称"], scope="全区", period=period)

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = m_proc.combine_highest_title(
                sorted(
                    c.fetchall(), key=lambda x: m_proc.highest_title_order[x[0]]
                )
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"在编/全区/{period}/最高职称", value=result, json_data=json_data)

        result = []

        # 全区分学段最高职称统计结束

        ###
        # 全区分学段在编人员院校级别统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=0, info=["院校代码"], scope="全区", period=period,
                                                additional_requirement=["(educational_background == '大学本科' "
                                                                        "or educational_background == '硕士研究生' "
                                                                        "or educational_background == '博士研究生')"])

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = m_proc.count_school_id(
                c.fetchall()
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m_proc.dict_assignment(route=f"在编/全区/{period}/院校级别", value=result, json_data=json_data)

        result = []

        # 全区分学段在编人员院校级别统计结束

    return json_data


if __name__ == '__main__':
    update()
