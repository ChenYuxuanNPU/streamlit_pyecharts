# 生成创建数据库时需要构建字段的mysql语句
# 不需要单独跑，被其他文件调用

def make_sql_sentence(kind):
    lang = "eng"

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

    # 分为在编教师（2023年在编教师信息）、编外教师（2023年编外教师信息）、学校数据（2023年学校情况一览表）几类
    # 根据查询信息的类型取出年份，找到对应的word

    if "在编教师信息" in kind:
        words = words_dict[f"teacher_info_0_{kind[0:4]}_word"]

    # if kind == "2023年在编教师信息":
    #     words = teacher_info_0_2023_word

    elif "编外教师信息" in kind:
        words = words_dict[f"teacher_info_1_{kind[0:4]}_word"]

    # elif kind == "2023年编外教师信息":
    #     words = teacher_info_1_2023_word

    elif "学校情况一览表" in kind:
        words = words_dict[f"school_info_sum_{kind[0:4]}_word"]
        lang = "chn"

    # elif kind == "2023年学校情况一览表":
    #     words = school_info_sum_2023_word
    #     lang = "chn"

    else:
        print(r"参数错误 (make_sql_sentence.py)")
        return -1

    sentence_title = words.split()

    # 中文字段要加双引号
    if lang == "chn":
        for i in range(len(sentence_title)):
            # sentence_title[i] = '"' + sentence_title[i] + '"'
            sentence_title[i] = f'"{sentence_title[i]}"'

    for i in range(0, len(sentence_title)):
        if i == len(sentence_title) - 1:
            sentence_title[i] += " TEXT"
        else:
            sentence_title[i] += " TEXT,"

    sql_sentence = ""

    for word in sentence_title:
        sql_sentence = sql_sentence + word

    print(f"{kind}的sql_sentence:{sql_sentence} (make_sql_sentence.py)")

    return sql_sentence


if __name__ == '__main__':
    make_sql_sentence("2023年编外教师信息")
