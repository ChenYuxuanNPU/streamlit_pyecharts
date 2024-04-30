# 用来获取文档中的内容并更新数据库
# 不需要单独跑，在生成图片的figure_output_district中被调用

import os
import sqlite3

from update_database.module import make_database, data_insert


def update_data(database_name, kind_list, table_name_list):

    # 删除旧数据库
    # 路径：C:\Users\1012986131\Desktop\python\streamlit_pyecharts\update_database\data_source\database\data.db
    if os.path.exists("C:\\Users\\1012986131\\Desktop\\python\\streamlit_pyecharts\\database\\" + database_name):
        os.remove("C:\\Users\\1012986131\\Desktop\\python\\streamlit_pyecharts\\database\\" + database_name)

    # 在新数据库中插入两张表所需的数据
    for i in range(0, 2):

        table_name = table_name_list[i]
        kind = kind_list[i]

        # 创建新的数据表并规定字段
        make_database.create_table(database_name=database_name, table_name=table_name, kind=kind)
        print(f"{kind}数据表创建成功！（update_data.py）")

        # 将表格中数据插入数据库中
        data_insert.insert_data(database_name=database_name, table_name=table_name, kind=kind)
        print(f"{kind}数据插入成功！（update_data.py）")

        print("")
