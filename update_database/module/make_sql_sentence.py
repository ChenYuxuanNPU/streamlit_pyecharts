# 生成创建数据库时需要构建字段的mysql语句
# 不需要单独跑，被其他文件调用

import json

from pathlib import Path

with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\database\database_basic_info.json", "r",
          encoding="UTF-8") as file:
    json_data = json.load(file)

    words_dict = json_data["words_dict"]


def make_sql_sentence(kind):
    lang = "chn"  # 默认字段名为中文

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
    # print(json_file_path)
