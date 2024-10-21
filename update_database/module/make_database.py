#
# 这个文件主要用来生成新数据表或删除原数据表，建表的时候要设定表字段数据类型，因此调用generation_of_sql_sentence
# 不需要单独跑，被update_database调用
#

import sqlite3
from pathlib import Path

from openpyxl.pivot.fields import Boolean

from update_database.module import make_sql_sentence
from update_database.tool import func as makedb_func


def clear_table(database_name: str, table_name: str, kind: str) -> None:
    """
    创建新的数据表或清空已有数据表
    :param database_name: 数据库名
    :param table_name: 数据表名
    :param kind: 在编/编外
    :return: 无
    """
    # 用来连接数据库插入数据
    result = [0]
    conn = sqlite3.connect(fr"{Path(__file__).resolve().parent.parent.parent}\database\{database_name}")
    c = conn.cursor()

    try:
        c.execute(f"select name from sqlite_master")
        result = makedb_func.del_tuple_in_list(c.fetchall())

    except Exception as e:
        print('\033[1;91m' + r"执行mysql语句时报错:%s(make_database.py)" % e + '\033[0m')

    finally:
        conn.commit()

    if table_name in result:

        # 删除原有的数据表
        try:
            # 删除数据表
            c.execute(f"drop table {table_name}")

        except Exception as e:
            print('\033[1;91m' + r"执行mysql语句时报错:%s(make_database.py)" % e + '\033[0m')

        finally:
            conn.commit()

    sql_sentence = make_sql_sentence.make_sql_sentence(kind=kind)

    try:
        # 创建数据表
        c.execute(f"create table {table_name} ({sql_sentence})")

    except Exception as e:
        print('\033[1;91m' + r"执行mysql语句时报错:%s(make_database.py)" % e + '\033[0m')

    finally:
        conn.commit()
        conn.close()

    print(f"{kind}数据表创建成功 (make_database.py)")

