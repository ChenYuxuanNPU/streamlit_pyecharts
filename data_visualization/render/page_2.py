import pandas as pd
import numpy as np

from data_visualization.tool import func as visual_func


def get_area_list() -> list:
    return ["永平", "石井", "新市", "江高", "人和", "太和", "钟落潭"]


def get_vocational_level_list() -> list:
    return ["专业技术十三级", "专业技术十二级", "专业技术十一级", "专业技术十级",
            "专业技术九级", "专业技术八级", "专业技术七级", "专业技术六级", "专业技术五级", "专业技术四级",]


def show_multi_years_teacher_0_vocational_level(year_list: list) -> None:

    data = visual_func.load_json_data(folder="result", file_name="teacher_info")


def show_multi_years_teacher_0_area(year_list: list) -> None:

    data = visual_func.load_json_data(folder="result", file_name="teacher_info")

    output = {}

    for area in get_area_list():

        output[f"{area}"] = [[year, data[year]["在编"]["全区"]["所有学段"]["片区统计"].get(area, None)] for year in year_list]

    visual_func.draw_line_chart(data=output, title="", x_axis=year_list, label_list=get_area_list())

    return None


if __name__ == '__main__':
    print(show_multi_years_teacher_0_area(year_list=["2023", "2024"]))

