import sys
from data_processing.read_database import get_database_data as gd
from data_processing.tool import module as m_proc


def update():
    result = []

    c, conn = m_proc.connect_database()

    json_data = m_proc.load_json_data(file_name="teacher_info")

    # 这里统计所有学校教师总数的列表
    sql_sentence = ('select * from ('
                    'select school_name, school_id, school_classification, area, count(school_name) count, "0" as kind '
                    'from data_0 group by school_name '
                    'union all '
                    'select school_name, school_id, school_classification, area, count(school_name) count, "1" as kind '
                    'from data_1 where is_teacher == "是" group by school_name) '
                    'order by count desc')

    try:
        c.execute(sql_sentence)
        result = c.fetchall()

    except Exception as e:
        print(f"执行mysql语句时报错：{e}")

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
                        break

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
                        break

                    school_dict[item[0]][4] = int(item[4])

                    school_dict[item[0]][5] = school_dict[item[0]][3] + school_dict[item[0]][4]

                case _:
                    break

    json_data = m_proc.dict_assignment(route=f"学校教师总数", value=school_dict, json_data=json_data)

    result = []

    # 所有学校教师总数统计结束

    m_proc.save_json_data(json_data=json_data, file_name="teacher_info")

    m_proc.disconnect_database(conn=conn)


if __name__ == '__main__':

    update()
