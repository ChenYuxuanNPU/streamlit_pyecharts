#
# 这个文件用来生成c.executemany中的sql语句，并将generation_of_input_data中的数据与语句一起插入数据库中
# 不需要单独跑，被update_database调用
#

import sqlite3

from update_database.code.module import make_input_data


def insert_data(database_name, table_name, kind):
    # 用来连接数据库插入数据
    conn = sqlite3.connect("C:\\Users\\1012986131\\Desktop\\python\\streamlit_pyecharts\\database\\" + database_name)
    c = conn.cursor()

    result = make_input_data.read_input_data(kind=kind)

    # 用来生成批量插入的语句
    sentence_for_executemany = ""  # 用来放很多问号
    print(fr"import来的数据长度为：{str(len(result[0]))}（data_insert.py）")

    for _ in range(0, len(result[0]) - 1):
        sentence_for_executemany = sentence_for_executemany + "? , "
    sentence_for_executemany = sentence_for_executemany + "?"

    sql_sentence = "insert into " + table_name + " values ( " + sentence_for_executemany + " )"

    # 插入数据
    try:
        # 插入数据
        c.executemany(sql_sentence, result)

    except Exception as e:
        print(r"执行mysql语句时报错：%s （data_insert.py）" % e)

    finally:
        conn.commit()
        conn.close()
        print(r"数据插入成功（data_insert.py）")
