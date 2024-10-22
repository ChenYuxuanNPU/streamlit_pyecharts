from school_data_processing.read_database import update_database_data as sch_ud
from school_data_processing.tool import func as sch_proc_func


def update(year: str) -> None:
    """
    从源json文件中取出dict，更新需要的年份，再保存至json文件
    :param year: 需要更新的年份
    :return: 无
    """

    json_data = sch_proc_func.load_json_data(folder="result", file_name="school_info")

    json_data = sch_ud.get_school_data_sum(json_data=json_data, year=year)

    sch_proc_func.save_json_data(json_data=json_data, folder="result", file_name="school_info")


if __name__ == '__main__':
    update(year="2023")
