import json

from update_database.module import update_data as ud

if __name__ == '__main__':

    database_name = "educational_data.db"

    # 0,1代表教师信息
    kind_list = ["2023年在编教师信息", "2023年编外教师信息", "2023年学校情况一览表"]

    # kind_list里的内容与下面字典的键要一一对应
    table_name = {
        "2023年在编教师信息": "teacher_data_0_2023",
        "2023年编外教师信息": "teacher_data_1_2023",
        "2023年学校情况一览表": "school_info_sum_2023"
    }

    xlsx_file_and_sheet_name = {
        "2023年在编教师信息": ["teacher_data_0.xlsx", "Sheet1"],
        "2023年编外教师信息": ["teacher_data_1.xlsx", "Sheet1"],
        "2023年学校情况一览表": ["2023年教育事业统计报表对账表.xlsx", "一览表"],
    }

    table_name_list = list(table_name.values())

    database_basic_info = {
        "database_name": database_name,
        "kind_list": kind_list,
        "table_name": table_name,
        "xlsx_file_and_sheet_name": xlsx_file_and_sheet_name
    }

    # print(database_basic_info)

    with open(r"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json_file\database\database_basic_info.json",
              "w", encoding="UTF-8") as file:
        json.dump(database_basic_info, file, indent=4, ensure_ascii=False)

    if ud.update_data(database_name=database_name,
                      kind_list=kind_list,
                      table_name_list=table_name_list):
        print("所有数据更新成功 (update.py)")
