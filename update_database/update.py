from update_database.module.update_data import *

if __name__ == '__main__':
    with open(fr"{Path(__file__).resolve().parent.parent}\json_file\database\database_basic_info.json",
              "w+", encoding="UTF-8") as file:
        json.dump(get_database_basic_info(), file, indent=4, ensure_ascii=False)

    update_data(kind_list=get_kind_list(), )

    print("所有数据更新成功 (update.py)")
