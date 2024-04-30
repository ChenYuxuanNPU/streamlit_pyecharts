import json
from update_database.module import update_data as ud


if __name__ == '__main__':

    database_name = "teacher_info.db"

    kind_list = ["在编", "非编"]

    table_name = {
        "在编": "data_0",
        "非编": "data_1"
    }

    table_name_list = list(table_name.values())

    database_basic_info = {
        "database_name": database_name,
        "kind_list": kind_list,
        "table_name": table_name
    }

    # print(database_basic_info)

    with open(r"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\database\database_basic_info.json",
              "w", encoding="UTF-8")as file:
        json.dump(database_basic_info, file, indent=4, ensure_ascii=False)

    # 在其他文件里循环，避免分段更新的问题
    ud.update_data(kind_list=kind_list, database_name=database_name, table_name_list=table_name_list)

    # 这里做合并数据库
