# 用来获取文档中的内容并更新数据库
# 不需要单独跑

from update_database.module.data_insert import *
from update_database.module.make_database import *


def update_data(database_name: str, kind_list: list, table_name_dict: dict) -> None:
    """
    用于更新数据库，包含数据表生成，字段规定，数据插入
    :param database_name: 数据库名
    :param kind_list: 在编/编外
    :param table_name_dict: 数据表名的对照字典
    :return: 无
    """

    # 在新数据库中插入两张教师数据表所需的数据
    for kind in kind_list:
        print(f"正在更新：{kind} (update_data.py)")

        table_name = table_name_dict[kind]

        # 创建新的数据表并规定字段
        clear_table(database_name=database_name, table_name=table_name, kind=kind)

        # 将表格中数据插入数据库中
        insert_data(database_name=database_name, table_name=table_name, kind=kind)
        print(f"{kind}数据更新成功 (update_data.py)")

        print("")


