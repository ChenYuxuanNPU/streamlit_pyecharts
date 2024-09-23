#
# 这个文件用来生成c.executemany中的sql语句，并将generation_of_input_data中的数据与语句一起插入数据库中
# 不需要单独跑，被update_database调用
#

import os
import sqlite3

from update_database.module import make_input_data


# 返回给定的第n层的父目录路径
def get_nth_parent_dir(n) -> str:
    path = os.path.abspath(__file__)

    for _ in range(n):
        path = os.path.dirname(path)

    return path


def insert_data(database_name, table_name, kind):

    # 用来连接数据库插入数据
    conn = sqlite3.connect(fr"{get_nth_parent_dir(n=3)}\database\{database_name}")
    c = conn.cursor()

    result = make_input_data.read_input_data(kind=kind)

    # 用来生成批量插入的语句
    sentence_for_executemany = ""  # 用来放很多问号
    print(fr"import来的{kind}数据长度为：{str(len(result[0]))} (data_insert.py)")

    for _ in range(0, len(result[0]) - 1):
        sentence_for_executemany = sentence_for_executemany + "? , "
    sentence_for_executemany = sentence_for_executemany + "?"

    sql_sentence = "insert into " + table_name + " values ( " + sentence_for_executemany + " )"

    # 插入数据
    try:
        # 插入数据
        c.executemany(sql_sentence, result)

    except Exception as e:
        print('\033[1;91m' + r"执行mysql语句时报错:%s (data_insert.py)" % e + '\033[0m')

    finally:
        conn.commit()
        conn.close()
        print(fr"{kind}数据插入成功 (data_insert.py)")


if __name__ == '__main__':
    pass
