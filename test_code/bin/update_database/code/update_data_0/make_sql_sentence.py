#生成创建数据库时需要构建字段的mysql语句
#不需要单独跑，被其他文件调用

def make_sql_sentence():
    words = ("school_name	school_classification	school_id	name	id	gender	date_of_birth	ethnic	"
             "place_of_birth	marriage	political_status	date_of_joining_CPC	educational_background	degree	"
             "graduate_school	graduate_school_id	graduate_time	major	educational_background_highest	"
             "degree_highest	graduate_school_highest	graduate_time_highest	major_highest	date_of_work	"
             "date_of_joining_byedu	date_of_becoming_a_staff	date_of_joining_current_school	"
             "current_administrative_position	administrative_level	grade_to_teach	major_discipline	"
             "subsidiary_discipline	note_for_vocation	highest_title	major_of_title	date_of_getting_title	"
             "current_educational_level	current_level	date_of_reaching_level	level_of_mandarin	"
             "level_of_teacher_certification	discipline_of_certification	cadre_teacher	title_01	"
             "date_of_title_01	title_02	title_03	school_name_of_supporting_education	"
             "area_of_supporting_education	start_date_of_supporting_education	end_date_of_supporting_education	"
             "school_name_of_communication	start_date_of_communication	end_date_of_communication	current_address	"
             "phone_number	id_from_edu_net	emergency_contact	relationship_of_emergency_contact	"
             "phone_number_of_emergency_contact	note_for_communication	note_for_all	current_age area	period	"
             "is_certain_teacher")

    sentence_title = words.split()
    # print(len(sentence_title))

    for i in range(0, len(sentence_title)):
        if (i == len(sentence_title) - 1):
            sentence_title[i] = sentence_title[i] + " TEXT"
        else:
            sentence_title[i] = sentence_title[i] + " TEXT,"

    # print(sentence_title)

    sql_sentence = ""

    for word in sentence_title:
        sql_sentence = sql_sentence + word

    print(f"sql_sentence:{sql_sentence}（update_data_0.make_sql_sentence.py）")

    return sql_sentence

