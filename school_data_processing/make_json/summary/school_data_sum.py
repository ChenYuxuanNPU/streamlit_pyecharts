from school_data_processing.read_database.update_database_data import *
from school_data_processing.tool.func import *


def update() -> None:
    """
    从源json文件中取出dict，更新需要的年份，再保存至json文件
    :return: 无
    """

    save_json_data(json_data=get_school_data_sum(), folder="result", file_name="school_info")


if __name__ == '__main__':
    update()
