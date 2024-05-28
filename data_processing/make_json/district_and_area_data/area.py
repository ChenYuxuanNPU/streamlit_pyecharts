import json

from data_processing.read_database import get_database_data as gd
from data_processing.tool import module as m

kind_list = m.kind_list
area_list = m.area_list
period_list = m.period_list


def update():
    result = []

    c, conn = m.connect_database()

    with open(r"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\result\output.json",
              "r", encoding="UTF-8") as file:
        json_data = json.load(file)

    # 在字典中更新数据库查询结果
    for area in area_list:

        for kind in kind_list:

            # 先统计下总人数
            sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=[""], scope="片区", area_name=area)

            try:
                c.execute(sql_sentence)
                result = c.fetchall()[0][0]

            except Exception as e:
                print(f"执行mysql语句时报错：{e}")

            finally:
                conn.commit()

            json_data = m.dict_assignment(route=f"{kind}/片区/{area}/所有学段/总人数", value=result,
                                          json_data=json_data)
            # json_data[kind]['片区'][area]['所有学段']['总人数'] = copy.deepcopy(result)

            result = []

            # 总人数统计结束

            ###
            # 在编人员最高学历统计 - 分片区
            ###
            sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高学历"], scope="片区",
                                                    area_name=area)

            # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
            try:
                c.execute(sql_sentence)
                result = dict(
                    sorted(
                        c.fetchall(), key=lambda x: m.educational_background_order[x[0]]
                    )
                )

            except Exception as e:
                print(f"执行mysql语句时报错：{e}")

            finally:
                conn.commit()

            json_data = m.dict_assignment(route=f"{kind}/片区/{area}/所有学段/最高学历", value=result,
                                          json_data=json_data)
            # json_data[kind]['片区'][area]['所有学段']['最高学历'] = copy.deepcopy(result)
            result = []

            # 片区最高学历统计结束

            ###
            # 片区学段分布统计
            ###

            sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["学段"], scope="片区", area_name=area,
                                                    additional_requirement=["period != '其他'"])

            # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
            try:
                c.execute(sql_sentence)
                result = dict(
                    sorted(
                        c.fetchall(), key=lambda x: m.period_order[x[0]]
                    )
                )

            except Exception as e:
                print(f"执行mysql语句时报错：{e}")

            finally:
                conn.commit()

            json_data = m.dict_assignment(route=f"{kind}/片区/{area}/所有学段/学段统计", value=result,
                                          json_data=json_data)
            # json_data[kind]['片区'][area]['所有学段']['学段统计'] = copy.deepcopy(result)

            result = []

            # 片区学段分布统计结束

            ###
            # 片区最高职称统计
            ###
            sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高职称"], scope="片区",
                                                    area_name=area)

            # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
            try:
                c.execute(sql_sentence)
                result = m.combine_highest_title(
                    sorted(
                        c.fetchall(), key=lambda x: m.highest_title_order[x[0]]
                    )
                )

            except Exception as e:
                print(f"执行mysql语句时报错：{e}")

            finally:
                conn.commit()

            json_data = m.dict_assignment(route=f"{kind}/片区/{area}/所有学段/最高职称", value=result,
                                          json_data=json_data)
            # json_data[kind]['片区'][area]['所有学段']['最高职称'] = copy.deepcopy(result)

            result = []

            # 片区最高职称统计结束

            ###
            # 片区骨干教师统计
            ###
            sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["骨干教师"], scope="片区",
                                                    area_name=area)

            # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
            try:
                c.execute(sql_sentence)
                result = m.combine_none_and_others(
                    dict(
                        sorted(
                            c.fetchall(), key=lambda x: m.cadre_teacher_order[x[0]]
                        )
                    )
                )

            except Exception as e:
                print(f"执行mysql语句时报错：{e}")

            finally:
                conn.commit()

            json_data = m.dict_assignment(route=f"{kind}/片区/{area}/所有学段/骨干教师", value=result,
                                          json_data=json_data)
            # json_data[kind]['片区'][area]['所有学段']['骨干教师'] = copy.deepcopy(result)
            result = []

            # 片区骨干教师统计结束

            ###
            # 片区教师资格统计
            ###
            # 先统计没有教资的
            sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], scope="片区",
                                                    area_name=area,
                                                    additional_requirement=["level_of_teacher_certification == '无'"])
            try:
                c.execute(sql_sentence)
                result = c.fetchall()[0][0]

            except Exception as e:
                print(f"执行mysql语句时报错：{e}")

            finally:
                conn.commit()

            json_data = m.dict_assignment(route=f"{kind}/片区/{area}/所有学段/教师资格/未持教师资格", value=result,
                                          json_data=json_data)
            # json_data[kind]['片区'][area]['所有学段']['教师资格']['未持教师资格'] = copy.deepcopy(result)
            result = []

            # 再统计有教资的
            sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], scope="片区",
                                                    area_name=area,
                                                    additional_requirement=["level_of_teacher_certification != '无'"])
            try:
                c.execute(sql_sentence)
                result = c.fetchall()[0][0]

            except Exception as e:
                print(f"执行mysql语句时报错：{e}")

            finally:
                conn.commit()

            json_data = m.dict_assignment(route=f"{kind}/片区/{area}/所有学段/教师资格/持有教师资格", value=result,
                                          json_data=json_data)
            # json_data[kind]['片区'][area]['所有学段']['教师资格']['持有教师资格'] = copy.deepcopy(result)
            result = []

            ###
            # 片区教师资格统计 - 幼儿园
            ###
            # 先统计没有教资的
            sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"],
                                                    period="幼儿园", area_name=area, scope="片区",
                                                    additional_requirement=["level_of_teacher_certification == '无'"])
            try:
                c.execute(sql_sentence)
                result = c.fetchall()[0][0]

            except Exception as e:
                print(f"执行mysql语句时报错：{e}")

            finally:
                conn.commit()

            json_data = m.dict_assignment(route=f"{kind}/片区/{area}/幼儿园/教师资格/未持教师资格", value=result,
                                          json_data=json_data)
            # json_data[kind]['片区'][area]['幼儿园']['教师资格']['未持教师资格'] = copy.deepcopy(result)
            result = []

            # 再统计有教资的
            sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"],
                                                    period="幼儿园", scope="片区", area_name=area,
                                                    additional_requirement=["level_of_teacher_certification != '无'"])
            try:
                c.execute(sql_sentence)
                result = c.fetchall()[0][0]

            except Exception as e:
                print(f"执行mysql语句时报错：{e}")

            finally:
                conn.commit()

            json_data = m.dict_assignment(route=f"{kind}/片区/{area}/幼儿园/教师资格/持有教师资格", value=result,
                                          json_data=json_data)
            # json_data[kind]['片区'][area]['幼儿园']['教师资格']['持有教师资格'] = copy.deepcopy(result)
            result = []

            ###
            # 片区教师资格统计 - 中小学
            ###
            # 先统计没有教资的
            sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], scope="片区",
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

            json_data = m.dict_assignment(route=f"{kind}/片区/{area}/中小学/教师资格/未持教师资格", value=result,
                                          json_data=json_data)
            # json_data[kind]['片区'][area]['中小学']['教师资格']['未持教师资格'] = copy.deepcopy(result)
            result = []

            # 再统计有教资的
            sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], scope="片区",
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

            json_data = m.dict_assignment(route=f"{kind}/片区/{area}/中小学/教师资格/持有教师资格", value=result,
                                          json_data=json_data)
            # json_data[kind]['片区'][area]['中小学']['教师资格']['持有教师资格'] = copy.deepcopy(result)
            result = []

            # 片区教师资格统计结束

            ###
            # 片区三名工作室主持人统计
            ###

            # 这里统计有多少是主持人
            sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["三名工作室"], scope="片区",
                                                    area_name=area,
                                                    additional_requirement=["title_01 != '无'"])
            try:
                c.execute(sql_sentence)
                result = c.fetchall()[0][0]

            except Exception as e:
                print(f"执行mysql语句时报错：{e}")

            finally:
                conn.commit()

            json_data = m.dict_assignment(route=f"{kind}/片区/{area}/所有学段/三名工作室/三名工作室主持人",
                                          value=result,
                                          json_data=json_data)
            # json_data[kind]['片区'][area]['所有学段']['三名工作室']['三名工作室主持人'] = copy.deepcopy(result)

            result = []

            # 这里统计有多少不是主持人
            sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["三名工作室"], scope="片区",
                                                    area_name=area,
                                                    additional_requirement=["title_01 == '无'"])
            try:
                c.execute(sql_sentence)
                result = c.fetchall()[0][0]

            except Exception as e:
                print(f"执行mysql语句时报错：{e}")

            finally:
                conn.commit()

            json_data = m.dict_assignment(route=f"{kind}/片区/{area}/所有学段/三名工作室/无", value=result,
                                          json_data=json_data)
            # json_data[kind]['片区'][area]['所有学段']['三名工作室']['无'] = copy.deepcopy(result)

            result = []

            # 片区三名工作室主持人统计结束

    # 更新一下在编和非编的特殊信息
    json_data = data_00_unique(json_data=json_data, c=c, conn=conn)

    json_data = data_01_unique(json_data=json_data, c=c, conn=conn)

    with open(r"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\result\output.json",
              "w", encoding="UTF-8") as file:

        # 将生成的数据保存至output.json中
        json.dump(json_data, file, indent=4, ensure_ascii=False)

    m.disconnect_database(conn=conn)


# 更新一些在编特有的信息
def data_00_unique(json_data: dict, c, conn):
    result = []

    for area in area_list:

        ###
        # 片区在编人员年龄统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["年龄"], scope="片区", area_name=area)

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = m.age_statistics(
                age_count_list=c.fetchall()
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m.dict_assignment(route=f"在编/片区/{area}/所有学段/年龄", value=result, json_data=json_data)
        # json_data['在编']['片区'][area]['所有学段']['年龄'] = copy.deepcopy(dict(result))
        result = []

        # 片区在编年龄统计结束

        ###
        # 片区在编人员主教学科统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["主教学科"], scope="片区",
                                                area_name=area,
                                                limit=20, order="desc",
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

        json_data = m.dict_assignment(route=f"在编/片区/{area}/所有学段/主教学科", value=result, json_data=json_data)
        # json_data['在编']['片区'][area]['所有学段']['主教学科'] = copy.deepcopy(result)
        result = []

        # 片区在编人员主教学科统计结束

        ###
        # 片区在编人员行政职务统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["行政职务"], scope="片区",
                                                area_name=area)

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = m.combine_administrative_position(
                sorted(
                    c.fetchall(), key=lambda x: m.current_administrative_position_order[x[0]]
                )
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m.dict_assignment(route=f"在编/片区/{area}/所有学段/行政职务", value=result, json_data=json_data)
        # json_data['在编']['片区'][area]['所有学段']['行政职务'] = copy.deepcopy(result)
        result = []

        # 片区在编人员行政职务统计结束

        ###
        # 片区在编人员院校级别统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=0, info=["院校代码"], scope="片区",
                                                area_name=area,
                                                additional_requirement=["(educational_background == '大学本科' "
                                                                        "or educational_background == '硕士研究生' "
                                                                        "or educational_background == '博士研究生')"])

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

        json_data = m.dict_assignment(route=f"在编/片区/{area}/所有学段/院校级别", value=result, json_data=json_data)
        # json_data['在编']['片区'][area]['所有学段']['院校级别'] = copy.deepcopy(result)
        result = []

        # 片区在编人员院校级别统计结束

        ###
        # 片区在编人员支教地域统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["支教地域"], scope="片区",
                                                area_name=area)

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                sorted(
                    c.fetchall(), key=lambda x: m.area_of_supporting_education_order[x[0]]
                )
            )

        except Exception as e:
            print(f"执行mysql语句时报错：{e}")

        finally:
            conn.commit()

        json_data = m.dict_assignment(route=f"在编/片区/{area}/所有学段/支教地域", value=result, json_data=json_data)
        # json_data['在编']['片区'][area]['所有学段']['支教地域'] = copy.deepcopy(result)
        result = []

        # 片区在编人员支教地域统计结束

    return json_data


# 更新一些非在编特有的信息
def data_01_unique(json_data: dict, c, conn):
    return json_data


if __name__ == '__main__':
    update()
