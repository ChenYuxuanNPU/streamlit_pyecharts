from data_visualization.tool.func import *


def get_base_data() -> dict:
    """
    获取全区学校数据
    :return:
    """
    return load_json_data(folder="result", file_name="school_info")


def show_pie_chart_info(year: str) -> None:
    """
    使用饼图展示某一年的全区占比数据
    :param year: 年份
    :return:
    """
    # 横向比较
    with st.container(border=True):
        display_centered_title(title="占比数据", font_size=2)

        col0, col1 = st.columns([1, 1])

        with col0:
            # 合计学校数对比
            st.info(f"合计学校数：{get_base_data()[year]["合计"]["合计学校数"]}")
            draw_pie_chart(
                data=dict([
                    [period, get_base_data()[year][period]["合计学校数"]] for period in get_base_data()["学段列表"]
                ]),
                title="合计学校数",
                formatter="{b}--占比{d}%"
            )

            # 公民办学校数对比
            school_kind = st.selectbox(
                label=" ",
                options=["公办学校数", "民办学校数"],
                label_visibility="collapsed"
            )

            draw_pie_chart(
                data=dict([
                    [period, get_base_data()[year][period][school_kind]] for period in get_base_data()["学段列表"]
                ]),
                title=school_kind,
                formatter="{b}--占比{d}%",
                pos_left=f"{len(school_kind) * 3}%"
            )

            st.divider()

            # 合计教职工数对比
            st.info(f"合计教职工数：{get_base_data()[year]["合计"]["合计教职工数"]}")
            draw_pie_chart(
                data=dict([
                    [period, get_base_data()[year][period]["合计教职工数"]] for period in get_base_data()["学段列表"]
                ]),
                title="合计教职工数",
                formatter="{b}--占比{d}%"
            )

            # 公民办教职工数对比
            school_kind = st.selectbox(
                label=" ",
                options=["公办学校教职工数", "民办学校教职工数"],
                label_visibility="collapsed"
            )

            draw_pie_chart(
                data=dict([
                    [period, get_base_data()[year][period][school_kind]] for period in get_base_data()["学段列表"]
                ]),
                title=school_kind,
                formatter="{b}--占比{d}%",
                pos_left=f"{len(school_kind) * 3}%"
            )

        with col1:
            # 合计学生数对比
            st.info(
                f"合计学生数：{get_base_data()[year]["合计"]["合计学生数"]} / 合计班额数：{get_base_data()[year]["合计"]["合计班额数"]}")
            draw_pie_chart(
                data=dict([
                    [period, get_base_data()[year][period]["合计学生数"]] for period in get_base_data()["学段列表"]
                ]),
                title="合计学生数",
                formatter="{b}--占比{d}%"
            )

            # 公民办学生数对比
            school_kind = st.selectbox(
                label=" ",
                options=["合计班额数", "公办学校学生数", "民办学校学生数",
                         "公办学校白云区户籍学生数", "公办学校非白云区户籍学生数",
                         "公办学校广州市户籍学生数", "公办学校非广州市户籍学生数",
                         "民办学校白云区户籍学生数", "民办学校非白云区户籍学生数",
                         "民办学校广州市户籍学生数", "民办学校非广州市户籍学生数"],
                label_visibility="collapsed"
            )

            draw_pie_chart(
                data=dict([
                    [period, get_base_data()[year][period][school_kind]] for period in get_base_data()["学段列表"]
                ]),
                title=school_kind,
                formatter="{b}--占比{d}%",
                pos_left=f"{len(school_kind) * 3}%"
            )

            st.divider()

            # 合计专任教师数对比
            st.info(f"合计专任教师数：{get_base_data()[year]["合计"]["合计专任教师数"]}")
            draw_pie_chart(
                data=dict([
                    [period, get_base_data()[year][period]["合计专任教师数"]] for period in get_base_data()["学段列表"]
                ]),
                title="合计专任教师数",
                formatter="{b}--占比{d}%"
            )

            # 公民办专任教师数对比
            school_kind = st.selectbox(
                label=" ",
                options=["公办学校专任教师数", "民办学校专任教师数"],
                label_visibility="collapsed"
            )

            draw_pie_chart(
                data=dict([
                    [period, get_base_data()[year][period][school_kind]] for period in get_base_data()["学段列表"]
                ]),
                title=school_kind,
                formatter="{b}--占比{d}%",
                pos_left=f"{len(school_kind) * 3}%"
            )

    st.divider()

    return None


def show_summarized_info(year: str, ) -> None:
    """
    用于展示全区的合计数据
    :param year: 年份
    :return:
    """

    with st.container(border=True):
        display_centered_title(title="合计数据", font_size=2)

        col0, col1, col2 = st.columns(spec=3)

        with col0:
            draw_pie_chart(
                data=dict([
                    ["公办学校数", get_base_data()[year]["合计"]["公办学校数"]],
                    ["民办学校数", get_base_data()[year]["合计"]["民办学校数"]]
                ]),
                title="学校类型",
                formatter="{c}--占比{d}%"
            )

            draw_pie_chart(
                data=dict([
                    ["白云区", get_base_data()[year]["合计"]["公办学校白云区户籍学生数"]],
                    ["市内外区",
                     get_base_data()[year]["合计"]["公办学校广州市户籍学生数"] - get_base_data()[year]["合计"][
                         "公办学校白云区户籍学生数"]],
                    ["广州市外", get_base_data()[year]["合计"]["公办学校非广州市户籍学生数"]]
                ]),
                title="公办学校户籍分布",
                formatter="{c}--占比{d}%",
                pos_left="35%"
            )

        with col1:
            draw_pie_chart(
                data=dict([
                    ["公办学校教职工数", get_base_data()[year]["合计"]["公办学校教职工数"]],
                    ["民办学校教职工数", get_base_data()[year]["合计"]["民办学校教职工数"]]
                ]),
                title="教职工数",
                formatter="{c}--占比{d}%"
            )

            # st.dataframe(height=385, width=int(1920/3), hide_index=True)

            draw_dataframe(
                data=pd.DataFrame(
                    [
                        ["学校数", "合计", get_base_data()[year]["合计"]["合计学校数"]],
                        ["1.", "公办学校数", get_base_data()[year]["合计"]["公办学校数"]],
                        ["2.", "民办学校数", get_base_data()[year]["合计"]["民办学校数"]],
                        ["学生数", "合计", get_base_data()[year]["合计"]["合计学生数"]],
                        ["公办学校学生数", "小计", get_base_data()[year]["合计"]["公办学校学生数"]],
                        ["1.", "公办学校白云区户籍学生数", get_base_data()[year]["合计"]["公办学校白云区户籍学生数"]],
                        ["2.", "公办学校广州市户籍学生数", get_base_data()[year]["合计"]["公办学校广州市户籍学生数"]],
                        ["3.", "公办学校非白云区户籍学生数",
                         get_base_data()[year]["合计"]["公办学校非白云区户籍学生数"]],
                        ["4.", "公办学校非广州市户籍学生数",
                         get_base_data()[year]["合计"]["公办学校非广州市户籍学生数"]],
                        ["民办学校学生数", "小计", get_base_data()[year]["合计"]["民办学校学生数"]],
                        ["1.", "民办学校白云区户籍学生数", get_base_data()[year]["合计"]["民办学校白云区户籍学生数"]],
                        ["2.", "民办学校广州市户籍学生数", get_base_data()[year]["合计"]["民办学校广州市户籍学生数"]],
                        ["3.", "民办学校非白云区户籍学生数",
                         get_base_data()[year]["合计"]["民办学校非白云区户籍学生数"]],
                        ["4.", "民办学校非广州市户籍学生数",
                         get_base_data()[year]["合计"]["民办学校非广州市户籍学生数"]],
                        ["教职工数", "合计", get_base_data()[year]["合计"]["合计教职工数"]],
                        ["1.", "公办学校教职工数", get_base_data()[year]["合计"]["公办学校教职工数"]],
                        ["2.", "民办学校教职工数", get_base_data()[year]["合计"]["民办学校教职工数"]],
                        ["专任教师数", "合计", get_base_data()[year]["合计"]["合计专任教师数"]],
                        ["1.", "公办学校专任教师数", get_base_data()[year]["合计"]["公办学校专任教师数"]],
                        ["2.", "民办学校专任教师数", get_base_data()[year]["合计"]["民办学校专任教师数"]],
                        ["班额数", "合计", get_base_data()[year]["合计"]["合计班额数"]],
                    ],
                    columns=["项目", "细分项", "人数"]
                )
            )

        with col2:
            draw_pie_chart(
                data=dict([
                    ["公办学校专任教师数", get_base_data()[year]["合计"]["公办学校专任教师数"]],
                    ["民办学校专任教师数", get_base_data()[year]["合计"]["民办学校专任教师数"]]
                ]),
                title="专任教师",
                formatter="{c}--占比{d}%"
            )

            draw_pie_chart(
                data=dict([
                    ["白云区", get_base_data()[year]["合计"]["民办学校白云区户籍学生数"]],
                    ["市内外区",
                     get_base_data()[year]["合计"]["民办学校广州市户籍学生数"] - get_base_data()[year]["合计"][
                         "民办学校白云区户籍学生数"]],
                    ["广州市外", get_base_data()[year]["合计"]["民办学校非广州市户籍学生数"]]
                ]),
                title="民办学校户籍分布",
                formatter="{c}--占比{d}%",
                pos_left="35%"
            )

    st.divider()

    return None


def show_period_detail_info(year: str) -> None:
    """
    展示单一学段所用的框架
    :param year: 年份
    :return:
    """

    with (st.container(border=True)):

        display_centered_title(title="学段数据", font_size=2)

        period = st.selectbox(
            label="选择需要查询的学段",
            options=get_base_data()["学段列表"],
            index=4,
            placeholder="单击选择学段",
        )

        if period is not None:

            # st.write(get_base_data()[period])

            # 可视化只展示学校多的学段
            if int(get_base_data()[year][period]["合计学校数"]) > 1 \
                    and get_base_data()[year][period]["公办学校数"] > 0 \
                    and get_base_data()[year][period]["民办学校数"] > 0:

                st.info(f'白云区内{period}统计信息如下', icon="ℹ️")

                col0, col1, col2 = st.columns(spec=3)

                with col0:
                    draw_pie_chart(
                        data=dict([
                            ["公办学校数", get_base_data()[year][period]["公办学校数"]],
                            ["民办学校数", get_base_data()[year][period]["民办学校数"]]
                        ]),
                        title="学校类型",
                        formatter="{c}--占比{d}%"
                    )

                    draw_pie_chart(
                        data=dict([
                            ["白云区", get_base_data()[year][period]["公办学校白云区户籍学生数"]],
                            ["市内外区",
                             get_base_data()[year][period]["公办学校广州市户籍学生数"] - get_base_data()[year][period][
                                 "公办学校白云区户籍学生数"]],
                            ["广州市外", get_base_data()[year][period]["公办学校非广州市户籍学生数"]]
                        ]),
                        title="公办学校户籍分布",
                        formatter="{c}--占比{d}%",
                        pos_left="35%"
                    )

                with col1:
                    draw_pie_chart(
                        data=dict([
                            ["公办学校教职工数", get_base_data()[year][period]["公办学校教职工数"]],
                            ["民办学校教职工数", get_base_data()[year][period]["民办学校教职工数"]]
                        ]),
                        title="教职工数",
                        formatter="{c}--占比{d}%"
                    )

                    # st.dataframe(height=385, width=int(1920/3), hide_index=True)

                    draw_dataframe(
                        data=pd.DataFrame(
                            [
                                ["合计学校数", get_base_data()[year][period]["合计学校数"]],
                                ["合计学生数", get_base_data()[year][period]["合计学生数"]],
                                ["公办学校学生数", get_base_data()[year][period]["公办学校学生数"]],
                                ["民办学校学生数", get_base_data()[year][period]["民办学校学生数"]],
                                ["合计教职工数", get_base_data()[year][period]["合计教职工数"]],
                                ["合计专任教师数", get_base_data()[year][period]["合计专任教师数"]],
                                ["合计班额数", get_base_data()[year][period]["合计班额数"]],
                            ],
                            columns=["项目", "人数"]
                        )
                    )

                with col2:
                    draw_pie_chart(
                        data=dict([
                            ["公办学校专任教师数", get_base_data()[year][period]["公办学校专任教师数"]],
                            ["民办学校专任教师数", get_base_data()[year][period]["民办学校专任教师数"]]
                        ]),
                        title="专任教师",
                        formatter="{c}--占比{d}%"
                    )

                    draw_pie_chart(
                        data=dict([
                            ["白云区", get_base_data()[year][period]["民办学校白云区户籍学生数"]],
                            ["市内外区",
                             get_base_data()[year][period]["民办学校广州市户籍学生数"] - get_base_data()[year][period][
                                 "民办学校白云区户籍学生数"]],
                            ["广州市外", get_base_data()[year][period]["民办学校非广州市户籍学生数"]]
                        ]),
                        title="民办学校户籍分布",
                        formatter="{c}--占比{d}%",
                        pos_left="35%"
                    )

                # 某几个学段的某几条信息是相同的，这里给个提示
                if period in ["初级中学", "九年一贯制学校"]:
                    st.warning('注：初级中学与九年一贯制学校的学生数与班额数已汇总统计', icon="⚠️")

                elif period in ["高级中学", "完全中学", "十二年一贯制学校"]:
                    st.warning('注：高级中学、完全中学与十二年一贯制学校的学生数与班额数已汇总统计', icon="⚠️")

            # 纯公/民办
            elif get_base_data()[year][period]["公办学校数"] > 0 or get_base_data()[year][period]["民办学校数"] > 0:

                st.warning(
                    f"由于白云区内的{period}均为{'公办' if get_base_data()[year][period]["公办学校数"] > 0 else '民办'}学校，数据将通过表格的形式展示",
                    icon='⚠️')

                _, col_mid, _ = st.columns([1, 1, 1])

                with col_mid:

                    draw_dataframe(
                        data=pd.DataFrame(
                            [
                                ["办学类型",
                                 f"{'公办' if get_base_data()[year][period]["公办学校数"] > 0 else '民办'}"],
                                ["合计学校数", str(get_base_data()[year][period]["合计学校数"])],
                                ["合计班额数", str(get_base_data()[year][period]["合计班额数"])],
                                ["合计学生数", str(get_base_data()[year][period]["合计学生数"])],
                                ["合计教职工数", str(get_base_data()[year][period]["合计教职工数"])],
                                ["合计专任教师数", str(get_base_data()[year][period]["合计专任教师数"])],
                            ],
                            columns=["项目", "信息"]
                        ),
                        hide_index=False,
                        height=280
                    )

            else:
                st.error("看代码")

            # 收起按钮
            hide_detail_button()

    return None


def show_detail_button() -> None:
    """
    用于放置展开详细信息的按钮
    :return:
    """

    _, col_mid, _ = st.columns([4, 1, 4])

    with col_mid:
        st.button(
            label="学段详细信息",
            on_click=page1_show_detail_info
        )

    return None


def hide_detail_button() -> None:
    """
    用于放置收起详细信息的按钮
    :return:
    """

    _, col_mid, _ = st.columns([8, 1, 8])
    with col_mid:
        st.button(
            label="收起",
            on_click=page1_hide_detail_info,
            type="primary"
        )

    return None


def show_multi_years_info(year_list: list) -> None:
    """
    用于展示多年份的数量对比
    :param year_list: 需要对比所用的年份列表
    :return:
    """

    with st.container(border=True):
        display_centered_title(title="变化数据", font_size=2)
        st.divider()

        st.info("我区在校学生数及师生比随年份变化情况")
        show_multi_years_student(year_list=year_list)

        show_multi_years_student_to_full_time_teacher_ratio(year_list=year_list)

        with st.expander("详细信息"):
            left, right = st.columns(spec=2)
            with left:
                display_centered_title(title="学生数变化情况", font_size=6)
                display_centered_dataframe(df=get_multi_years_student(year_list=year_list).T)

            with right:
                display_centered_title(title="生师比变化情况", font_size=6)
                display_centered_dataframe(df=get_multi_years_student_to_full_time_teacher_ratio(year_list=year_list).T)

        st.info("我区班额数及班师比随年份变化情况")
        show_multi_years_class(year_list=year_list)

        show_multi_years_full_time_teacher_to_class_ratio(year_list=year_list)

        # 这里计算了每个学段平均的班级规模
        # st.write(round(df_student.drop("合计") / df_class.drop("合计"), 1))

        with st.expander("详细信息"):
            left, right = st.columns(spec=2)
            with left:
                display_centered_title(title="班额数变化情况", font_size=6)
                display_centered_dataframe(df=get_multi_years_class(year_list=year_list).T)

            with right:
                display_centered_title(title="班师比变化情况", font_size=6)
                display_centered_dataframe(df=get_multi_years_full_time_teacher_to_class_ratio(year_list=year_list).T)

    return None


def show_multi_years_student(year_list: list) -> None:
    """
    用于展示多年份的学生数量对比
    :param year_list: 需要对比所用的年份列表
    :return:
    """

    with st.container(border=True):
        draw_line_chart(data=get_multi_years_student(year_list=year_list), title="", height=400, )

    return None


def get_multi_years_student(year_list: list) -> pd.DataFrame:
    """
    用于获取多年份的学生数量对比
    :param year_list: 需要对比所用的年份列表
    :return:
    """

    data = execute_sql_sentence(
        sentence=f'select "采集年份", "学段", "合计学生数" from school_data_sum where "学段" in ("合计", "高级中学", "初级中学", "小学", "幼儿园") and "采集年份" in ({', '.join([f'"{year}"' for year in year_list])})'
    )

    dict_for_df = {year: {"幼儿园": 0, "小学": 0, "初级中学": 0, "高级中学": 0, "合计": 0} for year in year_list}

    for item in data:
        dict_for_df[item[0]][item[1]] = int(item[2])

    return convert_dict_to_dataframe(d=dict_for_df).T.reindex(columns=year_list[::-1])


def show_multi_years_class(year_list: list) -> None:
    """
    用于展示多年份的班额数量对比
    :param year_list: 需要对比所用的年份列表
    :return:
    """

    with st.container(border=True):
        draw_line_chart(data=get_multi_years_class(year_list=year_list), title="", height=400, )

    return None


def get_multi_years_class(year_list: list) -> pd.DataFrame:
    """
    用于获取多年份的班额数量对比
    :param year_list: 需要对比所用的年份列表
    :return:
    """

    data = execute_sql_sentence(
        sentence=f'select "采集年份", "学段", "合计班额数" from school_data_sum where "学段" in ("合计", "高级中学", "初级中学", "小学", "幼儿园") and "采集年份" in ({', '.join([f'"{year}"' for year in year_list])})'
    )

    dict_for_df = {year: {"幼儿园": 0, "小学": 0, "初级中学": 0, "高级中学": 0, "合计": 0} for year in year_list}

    for item in data:
        dict_for_df[item[0]][item[1]] = int(item[2])

    return convert_dict_to_dataframe(d=dict_for_df).T.reindex(columns=year_list[::-1])


def get_multi_years_full_time_teacher(year_list: list) -> pd.DataFrame:
    """
    用于获取多年份的学年初报表专任教师数
    :param year_list: 需要对比所用的年份列表
    :return:
    """

    data = execute_sql_sentence(
        sentence=f'select "采集年份", "学段", "合计专任教师数" from school_data_sum where "学段" in ("合计", "十二年一贯制学校", "完全中学", "高级中学", "九年一贯制学校", "初级中学", "小学", "幼儿园") and "采集年份" in ({', '.join([f'"{year}"' for year in year_list])})'
    )

    dict_for_df = {year: {"幼儿园": 0, "小学": 0, "初级中学": 0, "高级中学": 0, "合计": 0} for year in year_list}

    for item in data:

        if item[1] in dict_for_df[item[0]].keys():
            dict_for_df[item[0]][item[1]] += int(item[2])

        elif item[1] in ["初级中学", "九年一贯制学校"]:
            dict_for_df[item[0]]["初级中学"] += int(item[2])

        elif item[1] in ["高级中学", "完全中学", "十二年一贯制学校"]:
            dict_for_df[item[0]]["高级中学"] += int(item[2])

        else:
            print_color_text(text=f'学年初报表中专任教师数有误：{item}')

    return convert_dict_to_dataframe(d=dict_for_df).T.reindex(columns=year_list[::-1])


def show_multi_years_full_time_teacher_to_class_ratio(year_list: list) -> None:
    """
    用于展示多年份班师比变化情况
    :param year_list:
    :return:
    """
    with st.container(border=True):
        draw_line_chart(data=get_multi_years_full_time_teacher_to_class_ratio(year_list=year_list), title="",
                        height=400, )

    return None


def get_multi_years_full_time_teacher_to_class_ratio(year_list: list) -> pd.DataFrame:
    """
    用于获取多年份的学年初报表班师比（平均每个班拥有多少名教师）
    :param year_list:
    :return:
    """

    return round(get_multi_years_full_time_teacher(year_list=year_list) / get_multi_years_class(year_list=year_list),
                 2).drop("合计")


def show_multi_years_student_to_full_time_teacher_ratio(year_list: list) -> None:
    """
    用于展示多年份师生比变化情况
    :param year_list:
    :return:
    """
    with st.container(border=True):
        draw_line_chart(data=get_multi_years_student_to_full_time_teacher_ratio(year_list=year_list), title="",
                        height=400, )

    return None


def get_multi_years_student_to_full_time_teacher_ratio(year_list: list) -> pd.DataFrame:
    """
    用于获取多年份的学年初报表生师比（平均每个教师教多少学生）
    :param year_list:
    :return:
    """

    return round(get_multi_years_student(year_list=year_list) / get_multi_years_full_time_teacher(year_list=year_list),
                 2).drop("合计")


if __name__ == '__main__':
    pass
    # print(get_multi_years_student_to_full_time_teacher_ratio(year_list=["2023", "2024"]))
