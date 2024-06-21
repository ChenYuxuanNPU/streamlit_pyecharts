# 用来获取文档中的内容并更新数据库
# 不需要单独跑

from update_database.module import make_database, data_insert


def update_data(database_name, kind_list, table_name_list):
    if len(kind_list) != len(table_name_list):
        print("插入数据长度不同")
        return False

    # 在新数据库中插入两张教师数据表所需的数据
    for i in range(len(kind_list)):

        table_name = table_name_list[i]
        kind = kind_list[i]

        # 创建新的数据表并规定字段
        if make_database.clear_table(database_name=database_name, table_name=table_name, kind=kind):
            print(f"{kind}数据表创建成功 (update_data.py)")

        # 将表格中数据插入数据库中
        data_insert.insert_data(database_name=database_name, table_name=table_name, kind=kind)
        print(f"{kind}数据更新成功 (update_data.py)")

        print("")

    return True

