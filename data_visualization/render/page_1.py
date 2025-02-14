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
        st.markdown(
            body="<h2 style='text-align: center;'>占比数据</h2>",
            unsafe_allow_html=True
        )

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
        st.markdown(
            body="<h2 style='text-align: center;'>合计数据</h2>",
            unsafe_allow_html=True
        )

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

        st.markdown(
            body="<h2 style='text-align: center;'>学段数据</h2>",
            unsafe_allow_html=True
        )

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
        # 小标题
        st.markdown(
            body="<h2 style='text-align: center;'>变化数据</h2>",
            unsafe_allow_html=True
        )
        st.divider()

        left, right = st.columns(spec=2)

        with left:
            st.info("我区在校学生数随年份变化情况")
            df_student = show_multi_years_student(year_list=year_list)

        with right:
            st.info("我区班额数随年份变化情况")
            df_class = show_multi_years_class(year_list=year_list)

        # 这里计算了每个学段平均的班级规模
        # st.write(round(df_student.drop("合计") / df_class.drop("合计"), 1))

        with st.expander("详细信息"):
            left, right = st.columns(spec=2)
            with left:
                st.dataframe(df_student.T)
            with right:
                st.dataframe(df_class.T)

    return None


def show_multi_years_student(year_list: list) -> pd.DataFrame:
    """
    用于展示多年份的学生数量对比
    :param year_list: 需要对比所用的年份列表
    :return:
    """

    line_data = execute_sql_sentence(
        sentence=f'select "采集年份", "学段", "合计学生数" from school_data_sum where "学段" in ("合计", "高级中学", "初级中学", "小学", "幼儿园") and "采集年份" in ({', '.join([f'"{year}"' for year in year_list])})'
    )

    dict_for_df = {year: {} for year in year_list}
    for item in line_data:
        dict_for_df[item[0]][item[1]] = int(item[2])

    with st.container(border=True):
        draw_line_chart(data=convert_dict_to_dataframe(d=dict_for_df).T.reindex(columns=year_list[::-1]), title="",
                        height=400, )

    return convert_dict_to_dataframe(d=dict_for_df).T.reindex(columns=year_list[::-1])


def show_multi_years_class(year_list: list) -> pd.DataFrame:
    """
    用于展示多年份的班额数量对比
    :param year_list: 需要对比所用的年份列表
    :return:
    """

    line_data = execute_sql_sentence(
        sentence=f'select "采集年份", "学段", "合计班额数" from school_data_sum where "学段" in ("合计", "高级中学", "初级中学", "小学", "幼儿园") and "采集年份" in ({', '.join([f'"{year}"' for year in year_list])})'
    )

    dict_for_df = {year: {} for year in year_list}
    for item in line_data:
        dict_for_df[item[0]][item[1]] = int(item[2])

    with st.container(border=True):
        draw_line_chart(data=convert_dict_to_dataframe(d=dict_for_df).T.reindex(columns=year_list[::-1]), title="",
                        height=400, )

    return convert_dict_to_dataframe(d=dict_for_df).T.reindex(columns=year_list[::-1])
