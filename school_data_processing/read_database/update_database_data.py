from school_data_processing.tool.func import *


def get_school_data_sum(json_data: dict, year: str, ) -> dict:
    """
    从数据库中读取某一年学校信息的表，获取字段名及数据，并将数据保存至json文件中
    :param json_data: json文件原数据
    :param year: 需要更新的年份
    :return: 更新后的json文件数据
    """

    table_name = load_json_data(folder="database", file_name="database_basic_info")["table_name_dict"][
        f"{year}年学校信息总览"]

    temp = []
    result = []
    period_list = []

    c, conn = connect_database()

    # 首先将字段名取出
    try:
        c.execute(f"pragma table_info({table_name})")
        result = c.fetchall()

    except Exception as e:
        print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

    finally:
        conn.commit()

    for item in result:
        temp.append(item[1])  # temp存放的是数据库中表的字段列表

    # 然后提取数据
    try:
        c.execute(f"select * from {table_name}")
        result = c.fetchall()

    except Exception as e:
        print('\033[1;91m' + f"执行mysql语句时报错：{e}" + '\033[0m')

    finally:
        conn.commit()

    for item in result:

        for i in range(2, len(temp)):
            json_data = dict_assignment(route=f"{item[0]}/{item[1]}/{temp[i]}", value=int(item[i]), json_data=json_data)

        if item[1] != "合计":
            period_list.append(item[1])

    # 生成学段列表
    json_data = dict_assignment(route=f"学段列表", value=period_list, json_data=json_data)

    disconnect_database(conn=conn)

    return json_data


if __name__ == '__main__':
    pass
