import json
from update_database.module import update_data as ud

if __name__ == '__main__':

    database_name = ["data_0.db", "data_1.db"]

    kind_list = ["在编", "非编"]

    table_name = "teacher_info"

    database_basic_info = {
        "database_name": database_name,
        "kind_list": kind_list,
        "table_name": table_name
    }

    # print(database_basic_info)

    with open(r"/json/database/database_basic_info.json", "w") as file:
        json.dump(database_basic_info, file)

    for i in range(0, 2):
        ud.update_data(kind=kind_list[i], database_name=database_name[i], table_name=table_name)
