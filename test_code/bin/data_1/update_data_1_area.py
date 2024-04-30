import json
import copy

from data_processing.read_database import get_database_data as gd
from data_processing.tool import module as m


def update():
    result = []

    c, conn = m.connect_database()

    with open(r"/json/result/output.json",
              "r", encoding="UTF-8") as file:
        json_data = json.load(file)

    # 在字典中更新数据库信息
    for area in m.area_list:

        # 先统计下总人数
        sql_sentence = gd.generate_sql_sentence(kind="非编", info_num=-1, info=[""], scope="片区",
                                                area_name=area)

        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data['非编']['片区'][area]['所有学段']['总人数'] = copy.deepcopy(result)
        result = []

        ###
        # 非编人员最高学历统计 - 分片区
        ###
        sql_sentence = gd.generate_sql_sentence(kind="非编", info_num=1, info=["最高学历"], scope="片区",
                                                area_name=area)

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

        json_data['非编']['片区'][area]['所有学段']['最高学历'] = copy.deepcopy(result)
        result = []

        ###
        # 非编人员骨干教师统计 - 分片区
        ###
        sql_sentence = gd.generate_sql_sentence(kind="非编", info_num=1, info=["骨干教师"], scope="片区",
                                                area_name=area)

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

        json_data['非编']['片区'][area]['所有学段']['骨干教师'] = copy.deepcopy(result)
        result = []

        ###
        # 非编人员教师资格统计 - 分片区
        ###
        # 先统计没有教资的
        sql_sentence = gd.generate_sql_sentence(kind="非编", info_num=-1, info=["教师资格"], scope="片区",
                                                area_name=area,
                                                additional_requirement=["level_of_teacher_certification == '无'"])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data['非编']['片区'][area]['所有学段']['教师资格']['未持教师资格'] = copy.deepcopy(result)
        result = []

        # 再统计有教资的
        sql_sentence = gd.generate_sql_sentence(kind="非编", info_num=-1, info=["教师资格"], scope="片区",
                                                area_name=area,
                                                additional_requirement=["level_of_teacher_certification != '无'"])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data['非编']['片区'][area]['所有学段']['教师资格']['持有教师资格'] = copy.deepcopy(result)
        result = []

        ###
        # 非编人员教师资格统计 - 幼儿园
        ###
        # 先统计没有教资的
        sql_sentence = gd.generate_sql_sentence(kind="非编", info_num=-1, info=["教师资格"],
                                                period="幼儿园", area_name=area, scope="片区",
                                                additional_requirement=["level_of_teacher_certification == '无'"])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data['非编']['片区'][area]['所有学段']['幼儿园教师资格']['未持教师资格'] = copy.deepcopy(result)
        result = []

        # 再统计有教资的
        sql_sentence = gd.generate_sql_sentence(kind="非编", info_num=-1, info=["教师资格"],
                                                period="幼儿园", scope="片区", area_name=area,
                                                additional_requirement=["level_of_teacher_certification != '无'"])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data['非编']['片区'][area]['所有学段']['幼儿园教师资格']['持有教师资格'] = copy.deepcopy(result)
        result = []

        ###
        # 非编人员教师资格统计 - 中小学
        ###
        # 先统计没有教资的
        sql_sentence = gd.generate_sql_sentence(kind="非编", info_num=-1, info=["教师资格"], scope="片区",
                                                area_name=area,
                                                additional_requirement=["level_of_teacher_certification == '无'",
                                                                        "period != '幼儿园'"])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data['非编']['片区'][area]['所有学段']['中小学教师资格']['未持教师资格'] = copy.deepcopy(result)
        result = []

        # 再统计有教资的
        sql_sentence = gd.generate_sql_sentence(kind="非编", info_num=-1, info=["教师资格"], scope="片区",
                                                area_name=area,
                                                additional_requirement=["level_of_teacher_certification != '无'",
                                                                        "period != '幼儿园'"])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data['非编']['片区'][area]['所有学段']['中小学教师资格']['持有教师资格'] = copy.deepcopy(result)
        result = []

    with open(r"/json/result/output.json",
              "w", encoding="UTF-8") as file:

        # 将生成的数据保存至output.json中
        json.dump(json_data, file, indent=4, ensure_ascii=False)

    m.disconnect_database(conn=conn)
