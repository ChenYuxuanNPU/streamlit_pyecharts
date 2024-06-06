import json

from data_processing.read_database import get_database_data as gd
from data_processing.tool import module as m_proc

kind_list = m_proc.kind_list
period_list = m_proc.period_list


# 这里根据校名、学段、是否在编进行学校信息统计
def update(kind: str, school_name: str, period=None):
    if kind not in ["在编", '非编']:
        raise m_proc.MyError("kind参数错误")

    if period not in [None, "高中", "初中", "小学", "幼儿园", ""]:
        raise m_proc.MyError("period参数错误")

    result = []

    c, conn = m_proc.connect_database()

    json_data = m_proc.load_json_data(file_name="output")

    # 检查一下有没有这个学校和学段，没有的话就报错
    check_result = m_proc.school_name_and_period_check(kind=kind, school_name=school_name, period=period)
    if not check_result[0]:

        print(check_result[1])
        return -1

    ###
    # 统计总人数 - 分学校
    ###

    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=[""], scope="学校",
                                            school_name=school_name, period=period)

    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    json_data = m_proc.dict_assignment(
        route=f"{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/总人数",
        value=result, json_data=json_data)

    # print(f"{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/总人数")

    # if period is None:
    #     json_data['在编']['学校'][school_name]['所有学段']['总人数'] = copy.deepcopy(result)
    #
    # if period is not None:
    #     json_data['在编']['学校'][school_name][period]['总人数'] = copy.deepcopy(result)

    result = []

    # 学校总人数统计结束

    ###
    # 最高学历统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高学历"], scope="学校",
                                            school_name=school_name, period=period)

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

    json_data = m_proc.dict_assignment(
        route=f"{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/最高学历",
        value=result, json_data=json_data)

    result = []

    # 学校最高学历统计结束

    ###
    # 性别统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["性别"], scope="学校",
                                            school_name=school_name, period=period, order="asc")

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

    json_data = m_proc.dict_assignment(
        route=f"{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/性别",
        value=result, json_data=json_data)

    result = []

    # 学校性别统计结束

    ###
    # 最高职称统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高职称"], scope="学校",
                                            school_name=school_name, period=period)

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

    json_data = m_proc.dict_assignment(
        route=f"{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/最高职称",
        value=result, json_data=json_data)

    result = []

    # 学校最高职称统计结束

    ###
    # 在编人员骨干教师统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["骨干教师"], scope="学校",
                                            school_name=school_name, period=period)

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

    json_data = m_proc.dict_assignment(
        route=f"{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/骨干教师",
        value=result, json_data=json_data)

    result = []

    ###
    # 学校教师资格统计
    ###
    # 先统计没有教资的
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], period=period,
                                            scope="学校", school_name=school_name,
                                            additional_requirement=["level_of_teacher_certification == '无'"])
    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    json_data = m_proc.dict_assignment(
        route=f"{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/教师资格/未持教师资格",
        value=result, json_data=json_data)

    result = []

    # 再统计有教资的
    sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], period=period,
                                            scope="学校", school_name=school_name,
                                            additional_requirement=["level_of_teacher_certification != '无'"])
    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    json_data = m_proc.dict_assignment(
        route=f"{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/教师资格/持有教师资格",
        value=result, json_data=json_data)

    result = []

    # 学校教师资格统计结束

    # 统计一下在编非编的特殊信息
    json_data = data_00_unique(json_data=json_data, school_name=school_name, period=period, c=c, conn=conn) \
        if kind == "在编" else data_01_unique(json_data=json_data, school_name=school_name, period=period, c=c, conn=conn)

    m_proc.save_json_data(json_data=json_data, file_name="output")

    m_proc.disconnect_database(conn=conn)


# 更新一些在编特有的信息
def data_00_unique(json_data: dict, school_name: str, c, conn, period=None):
    result = []

    ###
    # 在编人员年龄统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["年龄"], scope="学校",
                                            school_name=school_name, period=period)

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

    json_data = m_proc.dict_assignment(
        route=f"在编/学校/{school_name}/{period if period is not None else "所有学段"}/年龄",
        value=result, json_data=json_data)

    # if period is None:
    #     json_data['在编']['学校'][school_name]['所有学段']['年龄'] = copy.deepcopy(dict(result))
    #
    # if period is not None:
    #     json_data['在编']['学校'][school_name][period]['年龄'] = copy.deepcopy(dict(result))

    result = []

    # 在编人员年龄统计（分学校）结束

    ###
    # 在编人员主教学科统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["主教学科"], scope="学校", school_name=school_name,
                                            period=period, limit=20, order="desc",
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

    json_data = m_proc.dict_assignment(
        route=f"在编/学校/{school_name}/{period if period is not None else "所有学段"}/主教学科",
        value=result, json_data=json_data)

    result = []

    # 在编人员学科统计（分学校）结束

    ###
    # 在编人员院校级别统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=0, info=["院校代码"], scope="学校",
                                            school_name=school_name, period=period,
                                            additional_requirement=["(educational_background = '大学本科' "
                                                                    "or educational_background = '硕士研究生' "
                                                                    "or educational_background = '博士研究生')"])

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

    json_data = m_proc.dict_assignment(
        route=f"在编/学校/{school_name}/{period if period is not None else "所有学段"}/院校级别",
        value=result, json_data=json_data)

    result = []

    # 在编人员毕业院校统计（分学校）结束

    ###
    # 在编人员三名工作室主持人统计 - 分学校
    ###
    # 这里统计有多少是主持人
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=-1, info=["三名工作室"], school_name=school_name,
                                            period=period, scope="学校", additional_requirement=["title_01 != '无'"])
    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    json_data = m_proc.dict_assignment(
        route=f"在编/学校/{school_name}/{period if period is not None else "所有学段"}/三名工作室/三名工作室主持人",
        value=result, json_data=json_data)

    result = []

    # 这里统计有多少不是主持人
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=-1, info=["三名工作室"],school_name=school_name,
                                            period=period, scope="学校", additional_requirement=["title_01 == '无'"])
    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    json_data = m_proc.dict_assignment(
        route=f"在编/学校/{school_name}/{period if period is not None else "所有学段"}/三名工作室/无",
        value=result, json_data=json_data)

    result = []

    # 在编人员三名工作室主持人统计（分学校）结束

    ###
    # 在编人员支教地域统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["支教地域"], scope="学校",
                                            school_name=school_name, period=period)

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

    json_data = m_proc.dict_assignment(
        route=f"在编/学校/{school_name}/{period if period is not None else "所有学段"}/支教地域",
        value=result, json_data=json_data)

    result = []

    # 在编人员支教地域统计（分学校）结束

    return json_data


# 更新一些非在编特有的信息
def data_01_unique(json_data: dict, school_name: str, c, conn, period=None):
    return json_data


if __name__ == '__main__':
    pass
    # update(kind="在编", school_name="广州市白云中学", period="高中")
    # update(kind="在编", school_name="广州市白云区广州空港实验中学")
    # update(kind="非编", school_name="广州市实验外语学校", period="高中")
    # update(kind="非编", school_name="广州市实验外语学校")
