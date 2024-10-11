import sqlite3
import sys

from teacher_data_processing.tool import func as tch_proc_func


# 当缺少编外数据表时收集在编数据
def update_teacher_0_only(year: str, c: sqlite3.Cursor) -> list:

    c.execute(
        f'select "校名", "统一社会信用代码", "学校类型", "区域", count("校名") count, "0" as "编制类型" from teacher_data_0_{year} group by "校名" order by count desc')

    return c.fetchall()


# 当缺少编内数据表时收集编外数据
def update_teacher_1_only(year: str, c: sqlite3.Cursor) -> list:

    c.execute(
        f'select "校名", "统一社会信用代码", "学校类型", "区域", count("校名") count, "1" as "编制类型" from teacher_data_1_{year} group by "校名" order by count desc')

    return c.fetchall()


def update(year: str) -> dict:
    result = []

    c, conn = tch_proc_func.connect_database()

    json_data = tch_proc_func.load_json_data(folder="result", file_name="teacher_info")

    # 这里统计所有学校教师总数的列表
    sql_sentence = ('select * from ('
                    'select "校名", "统一社会信用代码", "学校类型", "区域", count("校名") count, "0" as "编制类型" '
                    f'from teacher_data_0_{year} group by "校名" '
                    'union all '
                    'select "校名", "统一社会信用代码", "学校类型", "区域", count("校名") count, "1" as "编制类型" '
                    f'from teacher_data_1_{year} group by "校名") '
                    'order by count desc')

    try:
        c.execute(sql_sentence)
        result = c.fetchall()

    except Exception as e:
        print(str(e))

        if str(e) == f"no such table: teacher_data_0_{year}":

            print(f"custom_data.py:缺少{year}年的在编教师数据,将只更新编外教师数据")
            result = update_teacher_1_only(year=year, c=c)

        elif str(e) == f"no such table: teacher_data_1_{year}":

            print(f"custom_data.py:缺少{year}年的编外教师数据,将只更新在编教师数据")
            result = update_teacher_0_only(year=year, c=c)

        else:
            return {}

    finally:
        conn.commit()

    school_dict = {}

    for item in result:

        # 列表里没有对应的学校
        if item[0] not in school_dict.keys():

            match item[5]:
                case "0":
                    school_dict[item[0]] = [item[1], item[2], item[3], int(item[4]), 0, int(item[4])]

                case "1":
                    school_dict[item[0]] = [item[1], item[2], item[3], 0, int(item[4]), int(item[4])]

                case _:
                    break

        # 已经有这所学校的另一个类别了
        else:

            match item[5]:
                case "0":
                    # 如果前面已经有在编的
                    if school_dict[item[0]][3] != 0:
                        print("")
                        print(f"error data_processing/make_json/district_and_area_data/"
                              f"custom_data.py update() line {sys._getframe().f_lineno}:")
                        print(f"{item[0]}有多条在编信息")
                        print("")
                        return {}

                    school_dict[item[0]][3] = int(item[4])

                    school_dict[item[0]][5] = school_dict[item[0]][3] + school_dict[item[0]][4]

                case "1":
                    # 如果前面已经有编外的
                    if school_dict[item[0]][4] != 0:
                        print("")
                        print(f"error data_processing/make_json/district_and_area_data/"
                              f"custom_data.py update() line {sys._getframe().f_lineno}:")
                        print(f"{item[0]}有多条编外信息")
                        print("")
                        return {}

                    school_dict[item[0]][4] = int(item[4])

                    school_dict[item[0]][5] = school_dict[item[0]][3] + school_dict[item[0]][4]

                case _:
                    break

    json_data = tch_proc_func.dict_assignment(route=f"{year}/学校教师总数", value=school_dict, json_data=json_data)

    result = []

    # 所有学校教师总数统计结束

    tch_proc_func.save_json_data(json_data=json_data, folder="result", file_name="teacher_info")

    tch_proc_func.disconnect_database(conn=conn)

    return json_data


if __name__ == '__main__':

    update(year="2024")
