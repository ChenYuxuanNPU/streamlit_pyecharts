from teacher_data_processing.make_json.district_and_area_data import district, area, custom_data
from teacher_data_processing.tool import func as tch_proc_func


# 数一下教师数据中有多少个年份是在编和编外都有的
# def cal_custom_data_list() -> list:
#
#     custom_dict = {}
#
#     for (year, kind) in tch_proc_func.load_json_data(folder="database", file_name="database_basic_info")["list_for_update_teacher_info"]:
#
#         if year not in custom_dict.keys():
#             custom_dict[year] = 1
#
#         else:
#             custom_dict[year] += 1
#
#     custom_list = [years for years in custom_dict.keys() if custom_dict[years] > 1]
#
#     return custom_list


def update():

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
