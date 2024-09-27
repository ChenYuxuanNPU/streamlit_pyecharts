from teacher_data_processing.read_database import get_database_data as gd
from teacher_data_processing.tool import func as tch_proc_func

kind_list = tch_proc_func.kind_list
area_list = tch_proc_func.area_list
period_list = tch_proc_func.period_list


def update(kind: str, year: str, ) -> dict:
    result = []

    c, conn = tch_proc_func.connect_database()

    json_data = tch_proc_func.load_json_data(folder="result", file_name="teacher_info")

    # 在字典中更新数据库查询结果
    for area in area_list:

        # 先统计下总人数
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=[""], scope="片区", area_name=area,
                                                year=year)

        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错:{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/总人数", value=result,
                                                  json_data=json_data)
        # json_data[kind]['片区'][area]['所有学段']['总人数'] = copy.deepcopy(result)

        result = []

        # 总人数统计结束

        ###
        # 在编人员最高学历统计 - 分片区
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高学历"], scope="片区",
                                                area_name=area, year=year)

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                sorted(
                    c.fetchall(), key=lambda x: tch_proc_func.educational_background_order[x[0]]
                )
            )

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/最高学历", value=result,
                                                  json_data=json_data)
        # json_data[kind]['片区'][area]['所有学段']['最高学历'] = copy.deepcopy(result)
        result = []

        # 片区最高学历统计结束

        ###
        # 在编人员性别统计 - 分片区
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["性别"], scope="片区", year=year,
                                                area_name=area, order="asc")

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

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/性别", value=result,
                                                  json_data=json_data)
        # json_data[kind]['片区'][area]['所有学段']['性别'] = copy.deepcopy(result)
        result = []

        # 片区性别统计结束

        ###
        # 片区学段分布统计
        ###

        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["任教学段"], scope="片区", area_name=area, year=year,
                                                additional_requirement=['"任教学段" != "其他"'])

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                sorted(
                    c.fetchall(), key=lambda x: tch_proc_func.period_order[x[0]]
                )
            )

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/学段统计", value=result,
                                                  json_data=json_data)
        # json_data[kind]['片区'][area]['所有学段']['学段统计'] = copy.deepcopy(result)

        result = []

        # 片区学段分布统计结束

        ###
        # 片区最高职称统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["最高职称"], scope="片区",
                                                area_name=area, year=year)

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = tch_proc_func.combine_highest_title(
                sorted(
                    c.fetchall(), key=lambda x: tch_proc_func.highest_title_order[x[0]]
                )
            )

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/最高职称", value=result,
                                                  json_data=json_data)
        # json_data[kind]['片区'][area]['所有学段']['最高职称'] = copy.deepcopy(result)

        result = []

        # 片区最高职称统计结束

        ###
        # 片区骨干教师统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=1, info=["骨干教师"], scope="片区",
                                                area_name=area, year=year)

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = tch_proc_func.combine_none_and_others(
                dict(
                    sorted(
                        c.fetchall(), key=lambda x: tch_proc_func.cadre_teacher_order[x[0]]
                    )
                )
            )

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/骨干教师", value=result,
                                                  json_data=json_data)
        # json_data[kind]['片区'][area]['所有学段']['骨干教师'] = copy.deepcopy(result)
        result = []

        # 片区骨干教师统计结束

        ###
        # 片区教师资格统计
        ###
        # 先统计没有教资的
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], scope="片区",
                                                area_name=area, year=year,
                                                additional_requirement=['"教师资格学段" = "无"'])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/教师资格/未持教师资格",
                                                  value=result,
                                                  json_data=json_data)
        # json_data[kind]['片区'][area]['所有学段']['教师资格']['未持教师资格'] = copy.deepcopy(result)
        result = []

        # 再统计有教资的
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], scope="片区",
                                                area_name=area, year=year,
                                                additional_requirement=['"教师资格学段" != "无"'])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/教师资格/持有教师资格",
                                                  value=result,
                                                  json_data=json_data)
        # json_data[kind]['片区'][area]['所有学段']['教师资格']['持有教师资格'] = copy.deepcopy(result)
        result = []

        ###
        # 片区教师资格统计 - 幼儿园
        ###
        # 先统计没有教资的
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"],
                                                period="幼儿园", area_name=area, scope="片区", year=year,
                                                additional_requirement=['"教师资格学段" = "无"'])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/幼儿园/教师资格/未持教师资格",
                                                  value=result,
                                                  json_data=json_data)
        # json_data[kind]['片区'][area]['幼儿园']['教师资格']['未持教师资格'] = copy.deepcopy(result)
        result = []

        # 再统计有教资的
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], year=year,
                                                period="幼儿园", scope="片区", area_name=area,
                                                additional_requirement=['"教师资格学段" != "无"'])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/幼儿园/教师资格/持有教师资格",
                                                  value=result,
                                                  json_data=json_data)
        # json_data[kind]['片区'][area]['幼儿园']['教师资格']['持有教师资格'] = copy.deepcopy(result)
        result = []

        ###
        # 片区教师资格统计 - 中小学
        ###
        # 先统计没有教资的
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], scope="片区",
                                                area_name=area, year=year,
                                                additional_requirement=['"教师资格学段" = "无"', '"任教学段" != "幼儿园"'])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/中小学/教师资格/未持教师资格",
                                                  value=result,
                                                  json_data=json_data)
        # json_data[kind]['片区'][area]['中小学']['教师资格']['未持教师资格'] = copy.deepcopy(result)
        result = []

        # 再统计有教资的
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["教师资格"], scope="片区",
                                                area_name=area, year=year,
                                                additional_requirement=['"教师资格学段" != "无"', '"任教学段" != "幼儿园"'])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/中小学/教师资格/持有教师资格",
                                                  value=result,
                                                  json_data=json_data)
        # json_data[kind]['片区'][area]['中小学']['教师资格']['持有教师资格'] = copy.deepcopy(result)
        result = []

        # 片区教师资格统计结束

        ###
        # 片区三名工作室主持人统计
        ###

        # 这里统计有多少是主持人
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["四名工作室主持人"], scope="片区",
                                                area_name=area, year=year,
                                                additional_requirement=['"四名工作室主持人" != "无"'])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(
            route=f"{year}/{kind}/片区/{area}/所有学段/四名工作室/四名工作室主持人",
            value=result,
            json_data=json_data)

        result = []

        # 这里统计有多少不是主持人
        sql_sentence = gd.generate_sql_sentence(kind=kind, info_num=-1, info=["四名工作室主持人"], scope="片区",
                                                area_name=area, year=year,
                                                additional_requirement=['四名工作室主持人 = "无"'])
        try:
            c.execute(sql_sentence)
            result = c.fetchall()[0][0]

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/四名工作室/无",
                                                  value=result,
                                                  json_data=json_data)
        # json_data[kind]['片区'][area]['所有学段']['三名工作室']['无'] = copy.deepcopy(result)

        result = []

        # 片区三名工作室主持人统计结束

    # 更新一下在编和编外的特殊信息
    json_data = data_00_unique(json_data=json_data, year=year, kind=kind, c=c, conn=conn)

    json_data = data_01_unique(json_data=json_data, year=year, kind=kind, c=c, conn=conn)

    tch_proc_func.save_json_data(json_data=json_data, folder="result", file_name="teacher_info")

    tch_proc_func.disconnect_database(conn=conn)

    return json_data


# 更新一些在编特有的信息
def data_00_unique(json_data: dict, kind: str, year: str, c, conn):
    result = []

    for area in area_list:

        ###
        # 片区在编人员年龄统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["年龄"], scope="片区", area_name=area, year=year)

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

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/年龄", value=result,
                                                  json_data=json_data)
        # json_data['在编']['片区'][area]['所有学段']['年龄'] = copy.deepcopy(dict(result))
        result = []

        # 片区在编年龄统计结束

        ###
        # 片区在编人员主教学科统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["主教学科"], scope="片区",
                                                area_name=area, year=year,
                                                limit=20, order="desc",
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

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/主教学科", value=result,
                                                  json_data=json_data)
        # json_data['在编']['片区'][area]['所有学段']['主教学科'] = copy.deepcopy(result)
        result = []

        # 片区在编人员主教学科统计结束

        ###
        # 片区在编人员行政职务统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["行政职务"], scope="片区", year=year,
                                                area_name=area)

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = tch_proc_func.combine_administrative_position(
                sorted(
                    c.fetchall(), key=lambda x: tch_proc_func.current_administrative_position_order[x[0]]
                )
            )

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/行政职务", value=result,
                                                  json_data=json_data)
        # json_data['在编']['片区'][area]['所有学段']['行政职务'] = copy.deepcopy(result)
        result = []

        # 片区在编人员行政职务统计结束

        ###
        # 片区在编人员院校级别统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=0, info=["参加工作前毕业院校代码"], scope="片区",
                                                area_name=area, year=year,
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

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/院校级别", value=result,
                                                  json_data=json_data)
        # json_data['在编']['片区'][area]['所有学段']['院校级别'] = copy.deepcopy(result)
        result = []

        # 片区在编人员院校级别统计结束

        ###
        # 片区在编人员支教地域统计
        ###
        sql_sentence = gd.generate_sql_sentence(kind="在编", info_num=1, info=["支教地域"], scope="片区",
                                                area_name=area, year=year)

        # 取出结果后，先进行排序，然后将count(*)与字段反转，强制转换为字典
        try:
            c.execute(sql_sentence)
            result = dict(
                sorted(
                    c.fetchall(), key=lambda x: tch_proc_func.area_of_supporting_education_order[x[0]]
                )
            )

        except Exception as e:
            print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

        finally:
            conn.commit()

        json_data = tch_proc_func.dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/支教地域", value=result,
                                                  json_data=json_data)
        # json_data['在编']['片区'][area]['所有学段']['支教地域'] = copy.deepcopy(result)
        result = []

        # 片区在编人员支教地域统计结束

    return json_data


# 更新一些非在编特有的信息
def data_01_unique(json_data: dict, kind: str, year: str, c, conn):
    return json_data


if __name__ == '__main__':
    update(kind="在编", year="2023")
