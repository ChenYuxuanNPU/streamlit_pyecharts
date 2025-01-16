# 用来获取文档中的内容并更新数据库
# 不需要单独跑

from update_database.module.data_insert import *
from update_database.module.make_database import *


def update_data(kind_list: list, ) -> None:
    """
    用于更新数据库，包含数据表生成，字段规定，数据插入
    :param kind_list: 在编/编外
    :return: 无
    """

    # 在新数据库中插入两张教师数据表所需的数据
    for kind in kind_list:
        print(f"正在更新：{kind} (update_data.py)")

        table_name = get_table_name_dict()[kind]

        # 创建新的数据表并规定字段
        clear_table(table_name=table_name, kind=kind)

        # 将表格中数据插入数据库中
        insert_data(table_name=table_name, kind=kind)
        print(f"{kind}数据更新成功 (update_data.py)")

        print("")


