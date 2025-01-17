#
# 这个文件主要用来生成新数据表或删除原数据表，建表的时候要设定表字段数据类型，因此调用generation_of_sql_sentence
# 不需要单独跑，被update_database调用
#


from update_database.module.make_sql_sentence import *


def clean_table(table_name: str, kind: str) -> None:
    """
    创建新的数据表或清空已有数据表
    :param table_name: 数据表名
    :param kind: 查询内容中文解释
    :return: 无
    """

    is_table_exists = True if table_name in del_tuple_in_list(
        data=execute_sql_sentence(
            sentence=f"select name from sqlite_master"
        )
    ) else False

    if not is_table_exists:
        execute_sql_sentence(
            sentence=f"create table {table_name} ({make_sql_sentence(kind=kind)})"
        )

        print(f"{kind}数据表创建成功 (refresh_table.py)")

    else:

        if "教师信息" in kind:

            delete_old_data(table_name=f'teacher_data_{"0" if kind[5:7] == "在编" else "1"}', year=f'{kind[0:4]}')

            add_new_columns(table_name=f'teacher_data_{"0" if kind[5:7] == "在编" else "1"}', kind=kind)

        elif "学校信息总览" in kind:

            delete_old_data(table_name=f'school_data_sum', year=f'{kind[0:4]}')

            """
            暂时不需要，因为这部分的字段名大概率不会变，会的话再改
            """


def delete_old_data(table_name: str, year: str) -> None:
    """
    删除数据表中对应年份的数据
    :param table_name: 希望更新的数据表
    :param year: 当前更新年份
    :return:
    """

    is_rows_exist = True if \
        execute_sql_sentence(
            sentence=f'select count(*) from {table_name} where "采集年份" = "{year}"'
        )[0][0] > 0 else False

    if is_rows_exist:
        execute_sql_sentence(
            sentence=f'delete from {table_name} where "采集年份" = "{year}"'
        )


def add_new_columns(table_name: str, kind: str) -> None:
    """
    为数据表增加缺失的列
    :param table_name: 需要新增列的数据表
    :param kind: 查询内容中文解释
    :return:
    """

    exist_columns_list = [item[1] for item in execute_sql_sentence(
        sentence=f'pragma table_info({table_name})'
    )]

    expect_columns_list = get_words_dict()[kind]

    for item in expect_columns_list:
        if item not in exist_columns_list:
            execute_sql_sentence(
                sentence=f'alter table {table_name} add column "{item}" text'
            )


if __name__ == '__main__':
    pass
