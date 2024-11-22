import json
from pathlib import Path

from update_database.module import update_data as ud


# 下面整块都是更新数据库要用的信息


def get_database_name() -> str:
    return "educational_data.db"


# todo:插入新表时在这里要加新的数据表名
def get_table_name_dict() -> dict:
    """
    获取数据表中文解释和数据源excel文件名对应的字典
    :return: {数据表中文解释：data_source表格名}
    """

    return {
        "2023年在编教师信息": "teacher_data_0_2023",
        "2023年编外教师信息": "teacher_data_1_2023",
        "2023年学校情况一览表": "school_info_sum_2023",
        "2024年在编教师信息": "teacher_data_0_2024",
        "2024年编外教师信息": "teacher_data_1_2024",
    }


def get_kind_list() -> list:
    """
    table_name_dict.keys()
    :return: 数据表中文解释
    """
    return list(get_table_name_dict().keys())


# todo:插入新表时在这里要加表格名
def get_xlsx_file_and_sheet_name() -> dict:
    """
    获取数据表中文解释和数据源文件名、表格表名
    :return: {中文解释:[表格名, 表格表名]}
    """

    return {
        "2023年在编教师信息": ["teacher_data_0_2023.xlsx", "Sheet1"],
        "2023年编外教师信息": ["teacher_data_1_2023.xlsx", "Sheet1"],
        "2023年学校情况一览表": ["2023年教育事业统计报表对账表.xlsx", "一览表"],
        "2024年在编教师信息": ["teacher_data_0_2024.xlsx", "Sheet1"],
        "2024年编外教师信息": ["teacher_data_1_2024.xlsx", "Sheet1"],
    }


# todo:插入新表时在这里要加数据库字段名
def get_words_dict() -> dict:
    """
    获取不同数据表的字段
    :return: {数据表名: (字段)}
    """

    return {
        "teacher_info_0_2023_word": ("校名 学校类型 统一社会信用代码 姓名 身份证号 性别 民族 "
                                     "籍贯 婚姻状况 政治面貌 入党（团）时间 参加工作前学历 参加工作前学位 "
                                     "参加工作前毕业院校 参加工作前毕业院校代码 参加工作前毕业时间 参加工作前所学专业 最高学历 "
                                     "最高学位 最高学历毕业院校 最高学历毕业时间 最高学历所学专业 参加工作时间 "
                                     "进入白云教育系统时间 入编时间 入现单位时间 "
                                     "行政职务 行政职务任职时间 任教年级 主教学科 "
                                     "兼教学科 最高职称 职称证专业 职称认定时间 "
                                     "现聘职称 专业技术岗位 专业技术岗位聘用时间 普通话水平 "
                                     "教师资格学段 教师资格学科 骨干教师 四名工作室主持人 "
                                     "四名工作室主持人确定时间 市级以上荣誉 市级以上人才项目 支教单位名称 "
                                     "支教地域 支教开始时间 支教结束时间 交流单位名称 交流开始时间 交流结束时间 "
                                     "常住地址 手机号 教育网短号 紧急联系人 与紧急联系人的关系 "
                                     "紧急联系方式 备注 年龄 "
                                     "区域 任教学段 是否音体美专任教师"),

        "teacher_info_1_2023_word": ("校名 学校类型 统一社会信用代码 姓名 身份证号 性别 民族 "
                                     "籍贯 婚姻状况 政治面貌 入党（团）时间 参加工作前学历 参加工作前学位 "
                                     "参加工作前毕业院校 参加工作前毕业时间 参加工作前所学专业 最高学历 最高学位 "
                                     "最高学历毕业院校 最高学历毕业时间 最高学历所学专业 参加工作时间 "
                                     "进入白云教育系统时间 入现单位时间 行政职务 行政职务任职时间 任教年级 "
                                     "主教学科 最高职称 职称证专业 职称认定时间 "
                                     "普通话水平 教师资格学段 教师资格学科 骨干教师 四名工作室主持人 "
                                     "四名工作室主持人确定时间 市级以上荣誉 市级以上人才项目 常住地址 手机号 紧急联系人 "
                                     "与紧急联系人的关系 紧急联系方式 "
                                     "备注 区域 任教学段 是否音体美专任教师 年龄"),

        "school_info_sum_2023_word": ("学段 合计学校数 公办学校数 民办学校数 合计学生数 公办学校学生数 公办学校非白云区户籍学生数 公办学校白云区户籍学生数 公办学校非广州市户籍学生数 "
                                      "公办学校广州市户籍学生数 民办学校学生数 民办学校非白云区户籍学生数 民办学校白云区户籍学生数 民办学校非广州市户籍学生数 民办学校广州市户籍学生数 合计教职工数 "
                                      "公办学校教职工数 民办学校教职工数 合计专任教师数 公办学校专任教师数 民办学校专任教师数 合计班额数"),
        "teacher_info_0_2024_word": ("校名 学校类型 统一社会信用代码 姓名 身份证号 性别 民族 "
                                     "籍贯 婚姻状况 政治面貌 入党（团）时间 参加工作前学历 参加工作前学位 "
                                     "参加工作前毕业院校 参加工作前毕业院校代码 参加工作前毕业时间 参加工作前所学专业 最高学历 "
                                     "最高学位 最高学历毕业院校 最高学历毕业时间 最高学历所学专业 参加工作时间 "
                                     "进入白云教育系统时间 入编时间 入现单位时间 "
                                     "行政职务 行政职务任职时间 任教年级 主教学科 "
                                     "兼教学科 最高职称 职称证专业 职称证发证时间 职称认定时间 "
                                     "现聘职称 现聘职称聘用时间 专业技术岗位 专业技术岗位聘用时间 普通话水平 "
                                     "教师资格学段 教师资格学科 骨干教师 四名工作室主持人 "
                                     "四名工作室主持人确定时间 市级以上荣誉 市级以上人才项目 支教单位名称 "
                                     "支教地域 支教开始时间 支教结束时间 "
                                     "交流单位名称 交流开始时间 交流结束时间 常住地址 "
                                     "手机号 教育网短号 紧急联系人 与紧急联系人的关系 "
                                     "紧急联系方式 备注 年龄 区域 任教学段 2024年9月编制所在学段 2024年9月在岗状态 "
                                     "是否音体美专任教师 党内职务级别 校内其他职务"),
        "teacher_info_1_2024_word": ("校名 学校类型 统一社会信用代码 姓名 身份证号 性别 民族 "
                                     "籍贯 婚姻状况 政治面貌 入党（团）时间 参加工作前学历 参加工作前学位 "
                                     "参加工作前毕业院校 参加工作前毕业时间 参加工作前所学专业 最高学历 最高学位 "
                                     "最高学历毕业院校 最高学历毕业时间 最高学历所学专业 参加工作时间 "
                                     "进入白云教育系统时间 入现单位时间 行政职务 行政职务任职时间 任教年级 "
                                     "主教学科 最高职称 职称证专业 职称认定时间 "
                                     "普通话水平 教师资格学段 教师资格学科 骨干教师 四名工作室主持人 "
                                     "四名工作室主持人确定时间 市级以上荣誉 市级以上人才项目 常住地址 手机号 紧急联系人 "
                                     "与紧急联系人的关系 紧急联系方式 "
                                     "备注 区域 任教学段 是否音体美专任教师 年龄 教师身份"),
    }


# todo:插入新表时在这里要加新的表格名
def get_teacher_table_list() -> dict:
    """
    建立在编与否、年份与教师信息表名的逻辑关系，供其他模块查询json文件时获取
    :return: {在编/编外: 年份: 数据表名}
    """

    return {
        '在编': {
            '2023': 'teacher_data_0_2023',
            '2024': 'teacher_data_0_2024',
        },
        '编外': {
            '2023': 'teacher_data_1_2023',
            '2024': 'teacher_data_1_2024',
        },
    }


def get_school_table_list() -> dict:
    """
    用于获取某一年份学校报表数据的数据表名
    :return: {年份: 数据表名}
    """

    return {
        '2023': 'school_info_sum_2023',
    }


# todo:插入新教师数据表时在这里要加新的年份和类型组合
def get_list_for_update_teacher_info() -> list:
    """
    获取现在数据库有的年份及是否在编的组合构成的列表
    :return: [(年份, 在编/编外)]
    """

    return [('2023', "在编"), ('2023', "编外"), ('2024', "在编"), ('2024', "编外")]


# todo:插入新学校数据表时在这里要加新的年份和类型组合
def get_list_for_update_school_info() -> list:
    """
    获取现在数据库有的年份及是否在编的组合构成的列表
    :return: [(年份, 在编/编外)]
    """

    return ['2023']


def get_database_basic_info() -> dict:
    """
    返回database_basic_info.json中的信息
    :return:
    """
    return {
        "database_name": get_database_name(),
        "kind_list": get_kind_list(),
        "table_name_dict": get_table_name_dict(),
        "xlsx_file_and_sheet_name": get_xlsx_file_and_sheet_name(),
        "words_dict": get_words_dict(),
        "teacher_table_list": get_teacher_table_list(),
        "school_table_list": get_school_table_list(),
        "list_for_update_teacher_info": get_list_for_update_teacher_info(),
        "list_for_update_school_info": get_list_for_update_school_info()
    }


# teacher_info_0_2023_word = ("school_name school_classification school_id name id gender date_of_birth ethnic "
#                             "place_of_birth marriage political_status date_of_joining_CPC educational_background degree "
#                             "graduate_school graduate_school_id graduate_time major educational_background_highest "
#                             "degree_highest graduate_school_highest graduate_time_highest major_highest date_of_work "
#                             "date_of_joining_byedu date_of_becoming_a_staff date_of_joining_current_school "
#                             "current_administrative_position administrative_level grade_to_teach major_discipline "
#                             "subsidiary_discipline note_for_vocation highest_title major_of_title date_of_getting_title "
#                             "current_educational_level current_level date_of_reaching_level level_of_mandarin "
#                             "level_of_teacher_certification discipline_of_certification cadre_teacher title_01 "
#                             "date_of_title_01 title_02 title_03 school_name_of_supporting_education "
#                             "area_of_supporting_education start_date_of_supporting_education "
#                             "end_date_of_supporting_education "
#                             "school_name_of_communication start_date_of_communication end_date_of_communication "
#                             "current_address "
#                             "phone_number id_from_edu_net emergency_contact relationship_of_emergency_contact "
#                             "phone_number_of_emergency_contact note_for_communication note_for_all current_age "
#                             "area period "
#                             "is_certain_teacher")
#
# teacher_info_1_2023_word = ("school_name school_classification school_id name id gender date_of_birth ethnic "
#                             "place_of_birth marriage political_status date_of_joining_CPC educational_background degree "
#                             "graduate_school graduate_time major educational_background_highest degree_highest "
#                             "graduate_school_highest graduate_time_highest major_highest date_of_work "
#                             "date_of_joining_byedu "
#                             "date_of_joining_current_school current_administrative_position administrative_level "
#                             "grade_to_teach "
#                             "major_discipline note_for_vocation highest_title major_of_title date_of_getting_title "
#                             "level_of_mandarin level_of_teacher_certification discipline_of_certification "
#                             "cadre_teacher title_01 "
#                             "date_of_title_01 title_02 title_03 current_address phone_number emergency_contact "
#                             "relationship_of_emergency_contact phone_number_of_emergency_contact note_for_communication "
#                             "note_for_all area is_teacher period is_certain_teacher")
#
# school_info_sum_2023_word = ("学段 合计学校数 公办学校数 民办学校数 合计学生数 公办学校学生数 公办学校非白云区户籍学生数 公办学校白云区户籍学生数 公办学校非广州市户籍学生数 "
#                              "公办学校广州市户籍学生数 民办学校学生数 民办学校非白云区户籍学生数 民办学校白云区户籍学生数 民办学校非广州市户籍学生数 民办学校广州市户籍学生数 合计教职工数 "
#                              "公办学校教职工数 民办学校教职工数 合计专任教师数 公办学校专任教师数 民办学校专任教师数 合计班额数")

if __name__ == '__main__':
    # print(database_basic_info)

    with open(fr"{Path(__file__).resolve().parent.parent}\json_file\database\database_basic_info.json",
              "w+", encoding="UTF-8") as file:
        json.dump(get_database_basic_info(), file, indent=4, ensure_ascii=False)

    ud.update_data(database_name=get_database_name(),
                   kind_list=get_kind_list(),
                   table_name_dict=get_table_name_dict())

    print("所有数据更新成功 (update.py)")
