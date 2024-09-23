import json

from update_database.module import update_data as ud

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

words_dict = {
    "teacher_info_0_2023_word": ("school_name school_classification school_id name id gender date_of_birth ethnic "
                                 "place_of_birth marriage political_status date_of_joining_CPC educational_background degree "
                                 "graduate_school graduate_school_id graduate_time major educational_background_highest "
                                 "degree_highest graduate_school_highest graduate_time_highest major_highest date_of_work "
                                 "date_of_joining_byedu date_of_becoming_a_staff date_of_joining_current_school "
                                 "current_administrative_position administrative_level grade_to_teach major_discipline "
                                 "subsidiary_discipline note_for_vocation highest_title major_of_title date_of_getting_title "
                                 "current_educational_level current_level date_of_reaching_level level_of_mandarin "
                                 "level_of_teacher_certification discipline_of_certification cadre_teacher title_01 "
                                 "date_of_title_01 title_02 title_03 school_name_of_supporting_education "
                                 "area_of_supporting_education start_date_of_supporting_education "
                                 "end_date_of_supporting_education "
                                 "school_name_of_communication start_date_of_communication end_date_of_communication "
                                 "current_address "
                                 "phone_number id_from_edu_net emergency_contact relationship_of_emergency_contact "
                                 "phone_number_of_emergency_contact note_for_communication note_for_all current_age "
                                 "area period "
                                 "is_certain_teacher"),
    "teacher_info_1_2023_word": ("school_name school_classification school_id name id gender date_of_birth ethnic "
                                 "place_of_birth marriage political_status date_of_joining_CPC educational_background degree "
                                 "graduate_school graduate_time major educational_background_highest degree_highest "
                                 "graduate_school_highest graduate_time_highest major_highest date_of_work "
                                 "date_of_joining_byedu "
                                 "date_of_joining_current_school current_administrative_position administrative_level "
                                 "grade_to_teach "
                                 "major_discipline note_for_vocation highest_title major_of_title date_of_getting_title "
                                 "level_of_mandarin level_of_teacher_certification discipline_of_certification "
                                 "cadre_teacher title_01 "
                                 "date_of_title_01 title_02 title_03 current_address phone_number emergency_contact "
                                 "relationship_of_emergency_contact phone_number_of_emergency_contact note_for_communication "
                                 "note_for_all area is_teacher period is_certain_teacher"),
    "school_info_sum_2023_word": ("学段 合计学校数 公办学校数 民办学校数 合计学生数 公办学校学生数 公办学校非白云区户籍学生数 公办学校白云区户籍学生数 公办学校非广州市户籍学生数 "
                                  "公办学校广州市户籍学生数 民办学校学生数 民办学校非白云区户籍学生数 民办学校白云区户籍学生数 民办学校非广州市户籍学生数 民办学校广州市户籍学生数 合计教职工数 "
                                  "公办学校教职工数 民办学校教职工数 合计专任教师数 公办学校专任教师数 民办学校专任教师数 合计班额数")
}

if __name__ == '__main__':

    # print(database_basic_info)

    with open(r"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json_file\database\database_basic_info.json",
              "w", encoding="UTF-8") as file:
        json.dump(database_basic_info, file, indent=4, ensure_ascii=False)

    if ud.update_data(database_name=database_name,
                      kind_list=kind_list,
                      table_name_list=table_name_list):
        print("所有数据更新成功 (update.py)")
