# 用来获取文档中的内容并更新数据库
# 不需要单独跑，在生成图片的figure_output_district中被调用

import os
import sqlite3

from update_database.code.module import make_database, data_insert


def update_data(database_name,kind,table_name):
    # main函数里的内容不会被调用就直接运行
    print("正在更新数据库（update_data.py）")

    # 删除旧数据库
    # 路径：C:\Users\1012986131\Desktop\python\streamlit_pyecharts\update_database\data_source\database\data_0.db
    if os.path.exists("C:\\Users\\1012986131\\Desktop\\python\\streamlit_pyecharts\\database\\" + database_name):
        os.remove("C:\\Users\\1012986131\\Desktop\\python\\streamlit_pyecharts\\database\\" + database_name)

    # 用来连接数据库
    conn = sqlite3.connect("C:\\Users\\1012986131\\Desktop\\python\\streamlit_pyecharts\\database\\" + database_name)
    c = conn.cursor()

    # 创建新的数据表并规定字段
    make_database.create_table(database_name=database_name, table_name=table_name, kind=kind)
    print("数据表创建成功！（update_data.py）")

    # 将表格中数据插入数据库中
    data_insert.insert_data(database_name=database_name, table_name=table_name, kind=kind)

    print("")
