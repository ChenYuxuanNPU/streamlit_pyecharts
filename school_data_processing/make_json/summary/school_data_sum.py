from school_data_processing.read_database.update_database_data import *
from school_data_processing.tool.func import *


def update(year: str) -> None:
    """
    从源json文件中取出dict，更新需要的年份，再保存至json文件
    :param year: 需要更新的年份
    :return: 无
    """

    json_data = load_json_data(folder="result", file_name="school_info")

    json_data = get_school_data_sum(json_data=json_data, year=year)

    save_json_data(json_data=json_data, folder="result", file_name="school_info")


if __name__ == '__main__':
    update(year="2023")
