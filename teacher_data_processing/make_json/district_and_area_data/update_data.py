from teacher_data_processing.make_json.district_and_area_data import district, area, custom_data
from teacher_data_processing.tool import func as tch_proc_func


def update() -> None:
    """
    根据database_basic_info的信息更新所有区级、片区级教师数据
    :return:
    """

    for (year, kind) in tch_proc_func.load_json_data(folder="database", file_name="database_basic_info")["list_for_update_teacher_info"]:

        district.update(kind=kind, year=year)

        area.update(kind=kind, year=year)

    # 更新学校教师总数
    # 只要年份有数据就更新，不考虑是否收集完了在编、编外数据
    custom_data_list = set(item[0] for item in tch_proc_func.load_json_data(folder="database", file_name="database_basic_info")["list_for_update_teacher_info"])

    for year in custom_data_list:

        custom_data.update(year=year)


if __name__ == '__main__':
    update()
    pass
