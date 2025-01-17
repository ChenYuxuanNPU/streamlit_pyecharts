# 生成创建数据库时需要构建字段的mysql语句
# 不需要单独跑，被其他文件调用
import json

from update_database.func import *


def get_words_dict() -> dict:
    """
    获取存储数据表字段名的字典
    :return: 字段名字典
    """

    with open(fr"{Path(__file__).resolve().parent.parent.parent}\json_file\database\database_basic_info.json", "r",
              encoding="UTF-8") as file:
        json_data = json.load(file)

        words_dict = json_data["words_dict"]

        return words_dict


def make_sql_sentence(kind) -> str:
    """
    生成形如("校名" text,"学校类型" text,"统一社会信用代码" text)的sql语句片段
    :param 查询内容中文解释
    :return: sql语句片段
    """

    lang = "eng"  # 默认字段名为英文

    # 分为在编教师（2023年在编教师信息）、编外教师（2023年编外教师信息）、学校数据（2023年学校情况一览表）几类
    # 根据查询信息的类型取出年份，找到对应的words

    words = get_words_dict()[kind]

    for item in "".join(words):
        if is_chinese_char(char=item):
            lang = "chn"

    sql_sentence = ' text,'.join([f'"{item}"' for item in words]) + ' text' if lang == "chn" else ' text,'.join(
        [f'{item}' for item in words]) + ' text'

    print(f"{kind}的sql_sentence:{sql_sentence} (make_sql_sentence.py)")

    return sql_sentence


if __name__ == '__main__':
    make_sql_sentence("2023年编外教师信息")
    # print(json_file_path)
