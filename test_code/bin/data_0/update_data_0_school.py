import json
import copy

from data_processing.read_database import get_database_data as gd
from data_processing.tool import module as m


def update(kind: str, school_name: str, period=None):

    if kind not in ["在编", '非编']:
        raise m.MyError("kind参数错误")

    if period not in [None, "高中", "初中", "小学", "幼儿园", ""]:
        raise m.MyError("period参数错误")

    result = []

    c, conn = m.connect_database()

    # 为学校和学段初始化字典，避免多层字典的插入引起KeyError
    with open(r"/json/result/output.json",
              "r", encoding="UTF-8") as file:
        json_data = json.load(file)

    # if m.school_name_or_period_check(kind=kind, school_name=school_name, period=period):
    #
    #     json_data = m.json_school_and_period_initialization(kind=kind, school_name=school_name, period=period)
    #
    # else:
    #     raise m.MyError("校名或学段有误")


    ###
    # 统计在编人员总人数 - 分学校
    ###

    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=-1, info=[""], scope="学校",
                                            school_name=school_name, period=period)

    try:
        c.execute(sql_sentence)
        result = c.fetchall()[0][0]

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    if period is None:
        json_data['在编']['学校'][school_name]['所有学段']['总人数'] = copy.deepcopy(result)

    if period is not None:
        json_data['在编']['学校'][school_name][period]['总人数'] = copy.deepcopy(result)

    result = []


    ###
    # 在编人员最高学历统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["最高学历"], scope="学校",
                                            school_name=school_name, period=period)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = dict(
            m.reverse_count_and_info(
                sorted(
                    c.fetchall(), key=lambda x: m.educational_background_order[x[1]]
                )
            )
        )

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    if period is None:
        json_data['在编']['学校'][school_name]['所有学段']['最高学历'] = copy.deepcopy(result)

    if period is not None:
        json_data['在编']['学校'][school_name][period]['最高学历'] = copy.deepcopy(result)

    result = []


    ###
    # 在编人员年龄统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["年龄"], scope="学校",
                                            school_name=school_name, period=period)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = m.age_statistics(
            age_count_list=m.reverse_count_and_info(
                c.fetchall()
            )
        )

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    if period is None:
        json_data['在编']['学校'][school_name]['所有学段']['年龄'] = copy.deepcopy(dict(result))

    if period is not None:
        json_data['在编']['学校'][school_name][period]['年龄'] = copy.deepcopy(dict(result))

    result = []


    ###
    # 在编人员最高职称统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["最高职称"], scope="学校",
                                            school_name=school_name, period=period)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = m.combine_highest_title(
            m.reverse_count_and_info(
                sorted(
                    c.fetchall(), key=lambda x: m.highest_title_order[x[1]]
                )
            )
        )

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    if period is None:
        json_data['在编']['学校'][school_name]['所有学段']['最高职称'] = copy.deepcopy(result)

    if period is not None:
        json_data['在编']['学校'][school_name][period]['最高职称'] = copy.deepcopy(result)

    result = []


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
            m.reverse_count_and_info(
                c.fetchall()
            )
        )

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    if period is None:
        json_data['在编']['学校'][school_name]['所有学段']['主教学科'] = copy.deepcopy(result)

    if period is not None:
        json_data['在编']['学校'][school_name][period]['主教学科'] = copy.deepcopy(result)

    result = []


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
        result = m.count_school_id(
            c.fetchall()
        )

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    if period is None:
        json_data['在编']['学校'][school_name]['所有学段']['院校级别'] = copy.deepcopy(result)

    if period is not None:
        json_data['在编']['学校'][school_name][period]['院校级别'] = copy.deepcopy(result)

    result = []


    ###
    # 在编人员行政职务统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["行政职务"], scope="学校",
                                            school_name=school_name, period=period)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = m.combine_administrative_position(
            m.reverse_count_and_info(
                sorted(
                    c.fetchall(), key=lambda x: m.current_administrative_position_order[x[1]]
                )
            )
        )

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    if period is None:
        json_data['在编']['学校'][school_name]['所有学段']['行政职务'] = copy.deepcopy(result)

    if period is not None:
        json_data['在编']['学校'][school_name][period]['行政职务'] = copy.deepcopy(result)

    result = []


    ###
    # 在编人员骨干教师统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["骨干教师"], scope="学校",
                                            school_name=school_name, period=period)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = m.combine_none_and_others(
            dict(
                m.reverse_count_and_info(
                    sorted(
                        c.fetchall(), key=lambda x: m.cadre_teacher_order[x[1]]
                    )
                )
            )
        )

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    if period is None:
        json_data['在编']['学校'][school_name]['所有学段']['骨干教师'] = copy.deepcopy(result)

    if period is not None:
        json_data['在编']['学校'][school_name][period if period is not None else '所有学段']['骨干教师'] = copy.deepcopy(result)

    result = []


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

    if period is None:
        json_data['在编']['学校'][school_name]['所有学段']['三名工作室'] = {}
        json_data['在编']['学校'][school_name]['所有学段']['三名工作室']['三名工作室主持人'] = copy.deepcopy(result)

    if period is not None:
        json_data['在编']['学校'][school_name][period]['三名工作室'] = {}
        json_data['在编']['学校'][school_name][period]['三名工作室']['三名工作室主持人'] = copy.deepcopy(result)

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

    if period is None:
        json_data['在编']['学校'][school_name]['所有学段']['三名工作室'] = {}
        json_data['在编']['学校'][school_name]['所有学段']['三名工作室']['无'] = copy.deepcopy(result)

    if period is not None:
        json_data['在编']['学校'][school_name][period]['三名工作室'] = {}
        json_data['在编']['学校'][school_name][period]['三名工作室']['无'] = copy.deepcopy(result)

    result = []

    ###
    # 在编人员支教地域统计 - 分学校
    ###
    sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["支教地域"], scope="学校",
                                            school_name=school_name, period=period)

    # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
    try:
        c.execute(sql_sentence)
        result = dict(
            m.reverse_count_and_info(
                sorted(
                    c.fetchall(), key=lambda x: m.area_of_supporting_education_order[x[1]]
                )
            )
        )

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

    finally:
        conn.commit()

    if period is None:
        json_data['在编']['学校'][school_name]['所有学段']['支教地域'] = copy.deepcopy(copy.deepcopy(result))

    if period is not None:
        json_data['在编']['学校'][school_name][period]['支教地域'] = copy.deepcopy(copy.deepcopy(result))

    result = []

    # 更新数据
    with open(r"/json/result/output.json",
              "w", encoding="UTF-8") as file:
        # 将生成的数据保存至output.json中
        json.dump(json_data, file, indent=4, ensure_ascii=False)

    m.disconnect_database(conn=conn)


if __name__ == '__main__':
    update(kind="在编", school_name="广州市白云中学", )
    update(kind="在编", school_name="广州市白云中学", period="高中")
