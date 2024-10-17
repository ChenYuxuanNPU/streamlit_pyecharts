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


def get_edu_bg_list() -> list:
    return ["博士研究生", "硕士研究生", "本科", "专科"]


def get_edu_bg_dataframe_columns_list() -> list:
    return ["年份", "最高学历", "人数"]


def get_vocational_level_list() -> list:
    return ["正高级教师", "高级教师", "一级教师", "二级教师", "三级教师"]


def get_vocational_level_dataframe_columns_list() -> list:
    return ["年份", "聘用职称", "人数"]


def get_vocational_level_detail_list() -> list:
    return ["试用期（未定级）", "专业技术十三级", "专业技术十二级", "专业技术十一级", "专业技术十级",
            "专业技术九级", "专业技术八级", "专业技术七级", "专业技术六级", "专业技术五级", "专业技术四级", ]


def get_vocational_level_detail_dataframe_columns_list() -> list:
    return ["年份", "专业技术等级", "人数"]


def get_discipline_list() -> list:
    return [
        "语文", "数学", "英语", "思想政治", "历史", "地理", "物理", "化学", "生物", "体育", "音乐", "美术",
        "科学", "信息技术", "通用技术", "劳动", "心理健康"
    ]


def get_discipline_dataframe_columns_list() -> list:
    return ["年份", "学科", "人数"]


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

        left, right = st.columns(spec=2)

        with left:
            visual_func.draw_line_chart(data=output, title="", x_axis=year_list, label_list=get_area_list(),
                                        is_symbol_show=False)
        with right:
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

    for period in get_period_list():
        output[f"{period}"] = [[year, data[year]["在编"]["全区"]["所有学段"]["学段统计"].get(period, None)] for year in
                               year_list]

    with st.container(border=True):
        left, right = st.columns(spec=2)

        with left:
            visual_func.draw_line_chart(data=output, title="", x_axis=year_list, label_list=get_period_list())

        with right:
            visual_func.draw_unstack_bar_chart(data=df, x_axis=get_period_dataframe_columns_list()[0],
                                               y_axis=get_period_dataframe_columns_list()[2],
                                               label=get_period_dataframe_columns_list()[1])

        visual_func.draw_horizontal_bar_chart(data=df, x_axis=get_period_dataframe_columns_list()[0],
                                              y_axis=get_period_dataframe_columns_list()[2],
                                              label=get_period_dataframe_columns_list()[1])

    return None


def show_multi_years_teacher_0_edu_bg(year_list: list) -> None:
    data = visual_func.load_json_data(folder="result", file_name="teacher_info")

    output = {}

    df = pd.DataFrame(columns=get_edu_bg_dataframe_columns_list())

    temp = []
    for year in year_list:
        for edu_bg in get_edu_bg_list():
            temp.append(
                pd.DataFrame(
                    [[year, edu_bg, data[year]["在编"]["全区"]["所有学段"]["最高学历"].get(edu_bg, None)]],
                    columns=get_edu_bg_dataframe_columns_list()
                )
            )

    df = pd.concat(temp, ignore_index=True)

    for edu_bg in get_edu_bg_list():
        output[f"{edu_bg}"] = [[year, data[year]["在编"]["全区"]["所有学段"]["最高学历"].get(edu_bg, None)] for year in
                               year_list]

    with st.container(border=True):
        left, right = st.columns(spec=2)

        with left:
            visual_func.draw_line_chart(data=output, title="", x_axis=year_list, label_list=get_edu_bg_list(),
                                        is_symbol_show=False)

        with right:
            visual_func.draw_unstack_bar_chart(data=df, x_axis=get_edu_bg_dataframe_columns_list()[0],
                                               y_axis=get_edu_bg_dataframe_columns_list()[2],
                                               label=get_edu_bg_dataframe_columns_list()[1])

        visual_func.draw_horizontal_bar_chart(data=df, x_axis=get_edu_bg_dataframe_columns_list()[0],
                                              y_axis=get_edu_bg_dataframe_columns_list()[2],
                                              label=get_edu_bg_dataframe_columns_list()[1])

    return None


def show_multi_years_teacher_0_vocational_level(year_list: list) -> None:
    data = visual_func.load_json_data(folder="result", file_name="teacher_info")

    output = {}

    df = pd.DataFrame(columns=get_vocational_level_dataframe_columns_list())
    df_detail = pd.DataFrame(columns=get_vocational_level_detail_dataframe_columns_list())

    temp = []
    for year in year_list:
        for vocational_level in get_vocational_level_list():
            temp.append(
                pd.DataFrame(
                    [[year, vocational_level,
                      data[year]["在编"]["全区"]["所有学段"]["最高职称"].get(vocational_level, None)]],
                    columns=get_vocational_level_dataframe_columns_list()
                )
            )

    df = pd.concat(temp, ignore_index=True)

    for vocational_level in get_vocational_level_list():
        output[f"{vocational_level}"] = [
            [year, data[year]["在编"]["全区"]["所有学段"]["最高职称"].get(vocational_level, None)] for year in
            year_list]

    temp_detail = []
    for year in year_list:
        for vocational_level_detail in get_vocational_level_detail_list():
            temp_detail.append(
                pd.DataFrame(
                    [[year, vocational_level_detail,
                      data[year]["在编"]["全区"]["所有学段"]["专业技术岗位"].get(vocational_level_detail, None)]],
                    columns=get_vocational_level_detail_dataframe_columns_list()
                )
            )

    df_detail = pd.concat(temp_detail, ignore_index=True)

    with st.container(border=True):
        left, right = st.columns(spec=2)

        with left:
            visual_func.draw_line_chart(data=output, title="", x_axis=year_list, label_list=get_vocational_level_list(),
                                        is_symbol_show=False)

        with right:
            visual_func.draw_unstack_bar_chart(data=df, x_axis=get_vocational_level_dataframe_columns_list()[0],
                                               y_axis=get_vocational_level_dataframe_columns_list()[2],
                                               label=get_vocational_level_dataframe_columns_list()[1])

        visual_func.draw_horizontal_bar_chart(data=df_detail,
                                              x_axis=get_vocational_level_detail_dataframe_columns_list()[0],
                                              y_axis=get_vocational_level_detail_dataframe_columns_list()[2],
                                              label=get_vocational_level_detail_dataframe_columns_list()[1])

    return None


def show_multi_years_teacher_0_discipline(year_list: list) -> None:
    data = visual_func.load_json_data(folder="result", file_name="teacher_info")

    output = {}

    df = pd.DataFrame(columns=get_discipline_dataframe_columns_list())

    temp = []
    for year in year_list:
        for discipline in get_discipline_list():
            temp.append(
                pd.DataFrame(
                    [[year, discipline, data[year]["在编"]["全区"]["所有学段"]["主教学科"].get(discipline, None)]],
                    columns=get_discipline_dataframe_columns_list()
                )
            )

    df = pd.concat(temp, ignore_index=True)

    for discipline in get_discipline_list():
        output[f"{discipline}"] = [[year, data[year]["在编"]["全区"]["所有学段"]["主教学科"].get(discipline, None)] for
                                   year in
                                   year_list]

    with st.container(border=True):

        left, right = st.columns(spec=2)

        with left:
            visual_func.draw_line_chart(data=output, title="", x_axis=year_list, label_list=get_discipline_list(),
                                        is_symbol_show=False)
        with right:
            visual_func.draw_unstack_bar_chart(data=df, x_axis=get_discipline_dataframe_columns_list()[0],
                                               y_axis=get_discipline_dataframe_columns_list()[2],
                                               label=get_discipline_dataframe_columns_list()[1])

        visual_func.draw_horizontal_bar_chart(data=df, x_axis=get_discipline_dataframe_columns_list()[0],
                                              y_axis=get_discipline_dataframe_columns_list()[2],
                                              label=get_discipline_dataframe_columns_list()[1])

    return None


if __name__ == '__main__':
    show_multi_years_teacher_0_vocational_level(year_list=["2023", "2024"])
