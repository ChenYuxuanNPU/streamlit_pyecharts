#
# 这个文件主要用来生成新数据表或删除原数据表，建表的时候要设定表字段数据类型，因此调用generation_of_sql_sentence
# 不需要单独跑，被update_database调用
#

import sqlite3

from update_database.code.module import make_sql_sentence


def create_table(database_name, table_name,kind):
    # 用来连接数据库插入数据
    conn = sqlite3.connect("C:\\Users\\1012986131\\Desktop\\python\\streamlit_pyecharts\\database\\" + database_name)
    c = conn.cursor()

    sql_sentence = make_sql_sentence.make_sql_sentence(kind=kind)

    try:
        # 创建数据表
        c.execute("""create table """ + table_name + """( """ + sql_sentence + """)""")

        # 删除数据表
        # c.execute("""drop table """ + table_name)

    except Exception as e:
        print(r"执行mysql语句时报错：%s(make_input_data.py）" % e)

    finally:
        conn.commit()
        conn.close()
