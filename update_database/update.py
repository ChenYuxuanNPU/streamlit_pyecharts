from update_database.func import *
from update_database.module.update_data import *

if __name__ == '__main__':
    with open(fr"{Path(__file__).resolve().parent.parent}\json_file\database\database_basic_info.json",
              "w+", encoding="UTF-8") as file:
        json.dump(get_database_basic_info(), file, indent=4, ensure_ascii=False)

    update_data(database_name=get_database_name(),
                kind_list=get_kind_list(),
                table_name_dict=get_table_name_dict())

    print("所有数据更新成功 (update.py)")
