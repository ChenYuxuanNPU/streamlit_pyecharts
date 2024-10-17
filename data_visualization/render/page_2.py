import pandas as pd
import streamlit as st

from data_visualization.tool import func as visual_func


def get_area_list() -> list:
    return ["永平", "石井", "新市", "江高", "人和", "太和", "钟落潭"]


def get_area_dataframe_columns_list() -> list:
    return ["年份", "片镇", "人数"]


def get_period_list() -> list:
    return ["高中", "初中", "小学", "幼儿园"]


def get_period_dataframe_columns_list() -> list:
    return ["年份", "学段", "人数"]


def get_vocational_level_list() -> list:
    return ["专业技术十三级", "专业技术十二级", "专业技术十一级", "专业技术十级",
            "专业技术九级", "专业技术八级", "专业技术七级", "专业技术六级", "专业技术五级", "专业技术四级", ]


def show_multi_years_teacher_0_vocational_level(year_list: list) -> None:
    data = visual_func.load_json_data(folder="result", file_name="teacher_info")


def show_multi_years_teacher_0_area(year_list: list) -> None:
    data = visual_func.load_json_data(folder="result", file_name="teacher_info")

    output = {}

    df = pd.DataFrame(columns=get_area_dataframe_columns_list())

    temp = []
    for year in year_list:
        for area in get_area_list():
            temp.append(
                pd.DataFrame(
                    [[year, area, data[year]["在编"]["全区"]["所有学段"]["片区统计"].get(area, None)]],
                    columns=get_area_dataframe_columns_list()
                )
            )

    df = pd.concat(temp, ignore_index=True)

    for area in get_area_list():
        output[f"{area}"] = [[year, data[year]["在编"]["全区"]["所有学段"]["片区统计"].get(area, None)] for year in
                             year_list]

    with st.container(border=True):
        visual_func.draw_line_chart(data=output, title="", x_axis=year_list, label_list=get_area_list(), is_symbol_show=False)

        visual_func.draw_unstack_bar_chart(data=df, x_axis=get_area_dataframe_columns_list()[0],
                                           y_axis=get_area_dataframe_columns_list()[2],
                                           label=get_area_dataframe_columns_list()[1])

        visual_func.draw_horizontal_bar_chart(data=df, x_axis=get_area_dataframe_columns_list()[0],
                                              y_axis=get_area_dataframe_columns_list()[2],
                                              label=get_area_dataframe_columns_list()[1])

    return None


def show_multi_years_teacher_0_period(year_list: list) -> None:
    data = visual_func.load_json_data(folder="result", file_name="teacher_info")

    output = {}

    df = pd.DataFrame(columns=get_period_dataframe_columns_list())

    temp = []
    for year in year_list:
        for period in get_period_list():
            temp.append(
                pd.DataFrame(
                    [[year, period, data[year]["在编"]["全区"]["所有学段"]["学段统计"].get(period, None)]],
                    columns=get_period_dataframe_columns_list()
                )
            )

    df = pd.concat(temp, ignore_index=True)
    print(df)

    for period in get_period_list():
        output[f"{period}"] = [[year, data[year]["在编"]["全区"]["所有学段"]["学段统计"].get(period, None)] for year in
                               year_list]

    with st.container(border=True):
        visual_func.draw_line_chart(data=output, title="", x_axis=year_list, label_list=get_period_list())

        visual_func.draw_unstack_bar_chart(data=df, x_axis=get_period_dataframe_columns_list()[0],
                                           y_axis=get_period_dataframe_columns_list()[2],
                                           label=get_period_dataframe_columns_list()[1])

        visual_func.draw_horizontal_bar_chart(data=df, x_axis=get_period_dataframe_columns_list()[0],
                                              y_axis=get_period_dataframe_columns_list()[2],
                                              label=get_period_dataframe_columns_list()[1])

    return None


if __name__ == '__main__':
    show_multi_years_teacher_0_period(year_list=["2023", "2024"])
