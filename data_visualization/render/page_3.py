from data_visualization.render.statistics_and_charts import *


def get_base_data() -> dict:
    """
    获取全区教师数据
    :return:
    """
    return load_json_data(folder="result", file_name="teacher_info")


def show_text_info() -> None:
    """
    用于展示指导中心的基础信息（不查询东西的时候）
    :return:
    """
    st.divider()

    # 展示宣传数据
    with st.container(border=True):
        st.markdown(
            "<h3 style='text-align: center;'>广州市白云区各教育指导中心相关信息</h3>",
            unsafe_allow_html=True
        )

        draw_dataframe(
            data=pd.DataFrame(
                [
                    ["永平教育指导中心", "白云大道北1689号（岭南新世界花园内）",
                     "永平街道、京溪街道、同和街道、嘉禾街道、均禾街道、鹤龙街道", "62189335"],
                    ["石井教育指导中心", "白云区石井石沙路1682号（石井中学旁）",
                     "同德街道、石井街道、白云湖街道、石门街道、松洲街道、金沙街道", "36533012-614"],
                    ["新市教育指导中心", "三元里大道棠安路新市中学东侧教师楼101",
                     "景泰街道、三元里街道、新市街道、云城街道、棠景街道、黄石街道", "86307817"],
                    ["人和教育指导中心", "白云区人和镇鹤龙六路18号", "人和镇", "36042235"],
                    ["江高教育指导中心", "白云区江高镇爱国东路61号", "江高镇", "86604940/86203661"],
                    ["太和教育指导中心", "白云区太和镇政府内", "太和镇、大源街道、龙归街道", "37312198"],
                    ["钟落潭教育指导中心", "白云区钟落潭镇福龙路88号", "钟落潭镇", "87403000"],
                ],
                columns=["教育指导中心", "地址", "服务范围", "联系方式"]
            ),
            height=350
        )

    return None


def show_1_year_and_1_area_teacher_0(year: str, area: str, period: str) -> None:
    """
    用于展示某一年某一片镇在编教师信息
    :param year: 年份
    :param area: 片镇
    :param period: 学段
    :return:
    """
    data = get_base_data()

    try:
        st.success(
            f"{area}在编{period if period is not None else ""}教师总人数：{data[year]["在编"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["总人数"]}",
            icon="😋")

    except KeyError as e:

        if e.args[0] == year:
            st.error(f"缺少{year}年的数据", icon="🤣")

        elif e.args[0] == "在编":
            st.error(f"缺少{year}年的在编数据", icon="😆")

        elif e.args[0] == "学校教师总数":
            st.error("缺少在编或编外信息", icon="😆")

        else:
            print(e)
            st.error(str(e), icon="😭")

    with st.container(border=False):

        try:
            df_container = get_1_year_age_and_gender_dataframe(year=year, area=area, period=period)

            draw_mixed_bar_and_line(
                df_bar=df_container.get_dataframe(name="data"),
                df_line=df_container.get_dataframe(name="sum"),
                bar_axis_label="人数", line_axis_label="合计人数",
                mark_line_type="average"
            )

        except Exception as e:
            print_color_text("年龄柱状折线图展示异常")
            print(e)
            st.toast("年龄柱状折线图展示异常", icon="😕")

        c0, c1, c2 = st.columns(spec=3)

        with c0:
            # 在编年龄统计
            draw_pie_chart(
                data=data[year]["在编"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["年龄"],
                title="年龄", pos_left="15%", center_to_bottom="64%")

            # 在编学段统计
            draw_pie_chart(
                data=data[year]["在编"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["学段统计"],
                title="学段统计")

        with c1:
            # 在编学历统计
            draw_pie_chart(
                data=data[year]["在编"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["最高学历"],
                title="最高学历")

            # 在编毕业院校统计
            draw_bar_chart(
                data=data[year]["在编"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["院校级别"],
                title="毕业院校", is_visual_map_show=False)

        with c2:
            # 在编职称统计
            draw_pie_chart(
                data=data[year]["在编"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["最高职称"],
                title="职称")

            # 在编行政职务统计
            draw_pie_chart(
                data=data[year]["在编"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["行政职务"],
                title="行政职务")

        # 最多毕业生数量统计
        with st.container(border=True):
            df_container = get_1_year_grad_school_dataframe(year=year, area=area, period=period)
            a0, a1, a2, a3, a4 = st.columns(spec=5)
            with a0:
                st.dataframe(df_container.get_dataframe("df_985"), height=400, width=300)
            with a1:
                st.dataframe(df_container.get_dataframe("df_nettp"), height=400, width=300)
            with a2:
                st.dataframe(df_container.get_dataframe("df_affiliate"), height=400, width=300)
            with a3:
                st.dataframe(df_container.get_dataframe("df_211"), height=400, width=300)
            with a4:
                st.dataframe(df_container.get_dataframe("df_all"), height=400, width=300)

        # 在编学科统计
        draw_bar_chart(
            data=data[year]["在编"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["主教学科"],
            title="主教学科", is_visual_map_show=False, axis_font_size=10)

        c0, c1, c2 = st.columns(spec=3)  # 不能删，这里删了会影响上下层顺序

        with c0:
            # 在编骨干教师统计
            draw_pie_chart(
                data=data[year]["在编"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["骨干教师"],
                title="骨干教师")

        with c1:
            # 在编教师支教统计
            draw_pie_chart(
                data=data[year]["在编"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["支教地域"],
                title="支教地域")

        with c2:
            # 在编四名教师统计
            draw_pie_chart(
                data=data[year]["在编"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["四名工作室"],
                title="四名统计")

    return None


def show_1_year_and_1_area_teacher_1(year: str, area: str, period: str = None) -> None:
    """
    用于展示某一年某一片镇编外教师信息
    :param year: 年份
    :param area: 片镇
    :param period: 学段
    :return:
    """
    data = get_base_data()

    try:
        st.success(
            f"{area}编外总人数：{data[year]["编外"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["总人数"]}",
            icon="😋")

    except KeyError as e:

        if e.args[0] == year:
            st.error(f"缺少{year}年的数据", icon="🤣")

        elif e.args[0] == "编外":
            st.error(f"缺少{year}年的编外数据", icon="😆")

        elif e.args[0] == "学校教师总数":
            st.error("缺少在编或编外信息", icon="😆")

        else:
            print(e)
            st.error(str(e), icon="😭")

    with st.container(border=False):
        c0, c1, c2 = st.columns(spec=3)

        with c0:
            # 编外学段统计
            draw_pie_chart(
                data=data[year]["编外"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["学段统计"],
                title="学段统计")

            # 编外教师资格统计
            draw_pie_chart(
                data=data[year]["编外"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["教师资格"],
                title="教师资格")

        with c1:
            # 编外学历统计
            draw_pie_chart(
                data=data[year]["编外"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["最高学历"],
                title="最高学历")

            # 编外中小学教师资格统计
            draw_pie_chart(data=data[year]["编外"]["片区"][area]["中小学"]["教师资格"],
                           title="中小学")

        with c2:
            # 编外职称统计
            draw_pie_chart(
                data=data[year]["编外"]["片区"][area][get_trans_period(kind="string_to_option")[period]]["最高职称"],
                title="职称")

            # 编外幼儿园教师资格统计
            draw_pie_chart(data=data[year]["编外"]["片区"][area]["幼儿园"]["教师资格"],
                           title="幼儿园")

    return None


def show_multi_years_and_1_area_teacher_0(year_list: list[str], area: str, period: str) -> None:
    """
    用于展示同一片镇多年的在编教师数据对比信息
    :param year_list: 年份列表
    :param area: 查询的片镇名
    :param period: 任教学段
    :return:
    """

    with st.container(border=True):
        # 小标题
        st.markdown(
            body="<h2 style='text-align: center;'>年份对比</h2>",
            unsafe_allow_html=True
        )
        st.divider()

        st.info(f"{area}在编{period if period is not None else ""}教师数随年份变化情况")
        show_multi_years_and_1_area_teacher_0_age(year_list=year_list, area=area, period=period)

        if period is None:
            st.info(f"{area}在编学段教师数随年份变化情况")
            show_multi_years_and_1_area_teacher_0_period(year_list=year_list, area=area)

        st.info(f"{area}在编{period if period is not None else ""}教师学历水平随年份变化情况")
        show_multi_years_and_1_area_teacher_0_edu_bg(year_list=year_list, area=area, period=period)

        st.info(f"{area}在编{period if period is not None else ""}教师专技职称随年份变化情况")
        show_multi_years_and_1_area_teacher_0_vocational_level(year_list=year_list, area=area, period=period)

        st.info(f"{area}在编{period if period is not None else ""}学科教师数随年份变化情况")
        show_multi_years_and_1_area_teacher_0_discipline(year_list=year_list, area=area, period=period)

        st.info(f"{area}在编{period if period is not None else ""}教师毕业院校水平随年份变化情况")
        show_multi_years_and_1_area_teacher_0_grad_school(year_list=year_list, area=area, period=period)

    return None


def show_multi_years_and_1_area_teacher_0_age(year_list: list[str], area: str, period: str = None) -> None:
    """
    展示多年份教师数对比
    :param year_list: 年份列表
    :param area: 查询的单个片镇名
    :param period: 任教学段
    :return:
    """

    df_container = get_multi_years_and_1_area_age_dataframe(year_list=year_list, area=area, period=period)

    left, right = st.columns(spec=2)

    with left:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="count_by_year"), title="", height=400)

    with right:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="growth_rate_by_year"), title="", height=400,
                            mark_line_y=0, formatter="{value} %")

    draw_mixed_bar_and_line(
        df_bar=df_container.get_dataframe(name="age_and_year"),
        df_line=df_container.get_dataframe(name="age_growth_rate_and_year"),
        bar_axis_label="人数",
        line_axis_label="增长率",
        # line_max_=300,
        # line_min_=-400,
        mark_line_y=0,
        line_formatter="{value} %"
    )

    with st.expander("详细信息"):
        st.dataframe(data=df_container.get_dataframe(name="age_and_year"))

        st.dataframe(data=df_container.get_dataframe(name="age_growth_rate_and_year").map(lambda x: f"{float(x):.1f}%"))

    return None


def get_multi_years_and_1_area_age_dataframe(year_list: list[str], area: str, period: str = None) -> DataFrameContainer:
    """
    根据年份列表生成多个年龄统计dataframe，放置在container中\n
    age_and_year：所有数据，列为年龄，行为年份\n
    age_growth_rate_and_year：所有数据对年龄求增长率，列为年龄，行为年份（存疑）\n
    count_by_year：每年的总人数，列为年份，单行\n
    growth_rate_by_year：原dataframe中每一年相对于上一年的总增长率（年份总人数增长率，不考虑年龄），列为年份，单行\n
    :param year_list: 查询的年份列表
    :param area: 查询的片镇名
    :param period: 任教学段
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为年龄列

    for year in year_list:

        df1[year] = {}  # 初始化该年份的子字典
        """
        df_dict:{
        "2024":{
            25:100,
            26:200
            },
        "2023"：{
            25：50，
            24：100
            }
        }
        """
        id_list = del_tuple_in_list(
            data=execute_sql_sentence(
                sentence=f'select "身份证号" from teacher_data_0_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}"' if period is not None else ''}'
            )
        )

        for item in id_list:

            age = str(get_age_from_citizen_id(citizen_id=item, year=year))

            if age == "0":
                print_color_text(item)
                print_color_text(year)

            if age in df1[year].keys():
                df1[year][age] += 1
            else:
                df1[year][age] = 1

    df1 = sort_dataframe_columns(df=convert_dict_to_dataframe(d=df1))
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="age_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe("age_growth_rate_and_year", df=df2)

    df3 = pd.DataFrame(df1.sum(axis="columns")).T
    df3.index = ["总人数"]
    container.add_dataframe(name="count_by_year", df=df3)

    df4 = get_growth_rate_from_one_row_dataframe(df=df3)
    df4.index = ["增长率"]

    container.add_dataframe(name="growth_rate_by_year", df=df4)

    return container


def show_multi_years_and_1_area_teacher_0_period(year_list: list[str], area: str) -> None:
    """
    展示多年份不同学段教师数对比
    :param year_list: 年份列表
    :param area: 片镇名
    :return:
    """
    df_container = get_multi_years_and_1_area_teacher_0_period_dataframe(year_list=year_list, area=area)

    left, right = st.columns(spec=2)

    with left:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="period_and_year").T, title="", height=400, )

    with right:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="period_growth_rate_and_year").T, title="", height=400,
                            mark_line_y=0, formatter="{value} %")

    draw_mixed_bar_and_line(
        df_bar=df_container.get_dataframe(name="period_and_year"),
        df_line=df_container.get_dataframe(name="period_growth_rate_and_year"),
        bar_axis_label="人数",
        line_axis_label="增长率",
        mark_line_y=0,
        line_formatter="{value} %"
    )

    with st.expander(label="详细信息"):
        left, right = st.columns(spec=2)
        with left:
            st.dataframe(data=df_container.get_dataframe(name="period_and_year"))
        with right:
            st.dataframe(
                data=df_container.get_dataframe(name="period_growth_rate_and_year").map(lambda x: f"{float(x):.1f}%"))

    return None


def get_multi_years_and_1_area_teacher_0_period_dataframe(year_list: list[str], area: str) -> DataFrameContainer:
    """
    根据年份列表生成多个学段统计dataframe，放置在container中\n
    period_and_year：所有数据，列为学段，行为年份\n
    period_growth_rate_and_year：所有数据对学段求增长率，行为增长率对应年份，列为学段，单行\n
    :param year_list: 查询的年份列表
    :param area: 片镇名
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为学段列

    for year in year_list:

        df1[year] = {}  # 初始化该年份的子字典
        """
        df_dict:{
        "2024":{
            "高中":100,
            "初中":200
            },
        "2023"：{
            "高中"：50，
            "初中"：100
            }
        }
        """
        period_count_list = execute_sql_sentence(
            sentence=f'select "任教学段", count(*) from teacher_data_0_{year} where "区域" = "{area}" and "任教学段" in ({', '.join([f'"{period}"' for period in get_period_list() if period != "高中"])}) group by "任教学段"'
        )

        for item in period_count_list:
            df1[year][item[0]] = item[1]

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=[period for period in get_period_list() if period != "高中"])
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="period_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe(name="period_growth_rate_and_year", df=df2)

    return container


def show_multi_years_and_1_area_teacher_0_edu_bg(year_list: list[str], area: str, period: str = None) -> None:
    """
    展示多年份教师学历对比
    :param year_list: 年份列表
    :param area: 片镇名
    :param period: 任教学段
    :return:
    """
    df_container = get_multi_years_and_1_area_teacher_0_edu_bg_dataframe(year_list=year_list, area=area, period=period)

    left, right = st.columns(spec=2)

    with left:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="edu_bg_and_year").T, title="", height=400, )

    with right:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="edu_bg_growth_rate_and_year").T, title="", height=400,
                            mark_line_y=0, formatter="{value} %")

    draw_mixed_bar_and_line(
        df_bar=df_container.get_dataframe(name="edu_bg_and_year"),
        df_line=df_container.get_dataframe(name="edu_bg_growth_rate_and_year"),
        bar_axis_label="人数",
        line_axis_label="增长率",
        line_max_=60,
        line_min_=-100,
        mark_line_y=0,
        line_formatter="{value} %"
    )

    with st.expander(label="详细信息"):
        left, right = st.columns(spec=2)
        with left:
            st.dataframe(data=df_container.get_dataframe(name="edu_bg_and_year"))
        with right:
            st.dataframe(
                data=df_container.get_dataframe(name="edu_bg_growth_rate_and_year").map(lambda x: f"{float(x):.1f}%"))

    return None


def get_multi_years_and_1_area_teacher_0_edu_bg_dataframe(year_list: list[str], area: str,
                                                          period: str = None) -> DataFrameContainer:
    """
    根据年份列表生成多个学历统计dataframe，放置在container中\n
    edu_bg_and_year：所有数据，列为学历，行为年份\n
    edu_bg_growth_rate_and_year：所有数据对学历求增长率，行为增长率对应年份，列为学历，单行\n
    :param year_list: 查询的年份列表
    :param area: 片镇名
    :param period: 任教学段
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为学历列

    for year in year_list:

        df1[year] = {}  # 初始化该年份的子字典
        """
        df_dict:{
        "2024":{
            "本科":100,
            "硕士研究生":200
            },
        "2023"：{
            "本科"：50，
            "硕士研究生"：100
            }
        }
        """
        edu_bg_count_list = execute_sql_sentence(
            sentence=f'select "最高学历", count(*) from teacher_data_0_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "最高学历" in ({', '.join([f'"{bg}"' for bg in get_edu_bg_list()])}) group by "最高学历"'
        )

        for item in edu_bg_count_list:
            df1[year][item[0]] = item[1]

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=get_edu_bg_list())
    df1.fillna(value=0, inplace=True)
    df1 = df1.loc[:, ~(df1 == 0).all()]  # 删除全为0的列
    container.add_dataframe(name="edu_bg_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe("edu_bg_growth_rate_and_year", df=df2)

    return container


def show_multi_years_and_1_area_teacher_0_vocational_level(year_list: list[str], area: str, period: str = None) -> None:
    """
    展示多年份教师专业技术级别对比
    :param year_list: 年份列表
    :param area: 片镇名
    :param period: 任教学段
    :return:
    """
    df_container = get_multi_years_and_1_area_teacher_0_vocational_level_dataframe(year_list=year_list, area=area,
                                                                                   period=period)

    left, right = st.columns(spec=2)

    with left:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="vocational_level_and_year").T, title="", height=400, )

    with right:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="vocational_level_growth_rate_and_year").T, title="",
                            height=400,
                            mark_line_y=0, formatter="{value} %")

    draw_mixed_bar_and_line(
        df_bar=df_container.get_dataframe(name="vocational_level_detail_and_year"),
        df_line=df_container.get_dataframe(name="vocational_level_detail_growth_rate_and_year"),
        bar_axis_label="人数",
        line_axis_label="增长率",
        mark_line_y=0,
        line_formatter="{value} %",
        x_axis_font_size=9
    )

    with st.expander("详细信息"):
        st.dataframe(data=df_container.get_dataframe(name="vocational_level_detail_and_year"))
        st.dataframe(data=df_container.get_dataframe(name="vocational_level_detail_growth_rate_and_year").map(
            lambda x: f"{float(x):.1f}%"))

    return None


def get_multi_years_and_1_area_teacher_0_vocational_level_dataframe(year_list: list[str], area: str,
                                                                    period: str = None) -> DataFrameContainer:
    """
    根据年份列表生成多个教师级别、专业技术级别统计dataframe，放置在container中\n
    vocational_level_and_year：所有数据，列为教师级别，行为年份\n
    vocational_level_growth_rate_and_year：所有数据对教师级别求增长率，行为增长率对应年份，列为教师级别，单行\n
    vocational_level_detail_and_year：所有数据，列为专技级别，行为年份\n
    vocational_level_detail_growth_rate_and_year：所有数据对专技级别求增长率，行为增长率对应年份，列为专技级别，单行\n
    :param year_list: 查询的年份列表
    :param area: 片镇名
    :param period: 任教学段
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为年龄列
    df3 = {}

    for year in year_list:

        df1[year] = {}  # 初始化该年份的子字典
        df3[year] = {}
        """
        df_dict:{
        "2024":{
            "一级教师":100,
            "二级教师":200
            },
        "2023"：{
            "一级教师"：50，
            "二级教师"：100
            }
        }
        """
        vocational_level_count_list = execute_sql_sentence(
            sentence=f'select "最高职称", count(*) from teacher_data_0_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "最高职称" in ({', '.join([f'"{level}"' for level in get_vocational_level_list()])}) group by "最高职称"'
        )

        for item in vocational_level_count_list:
            df1[year][item[0]] = item[1]

        vocational_level_detail_count_list = execute_sql_sentence(
            sentence=f'select "专业技术岗位", count(*) from teacher_data_0_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "专业技术岗位" in ({', '.join([f'"{level}"' for level in get_vocational_level_detail_list()])}) group by "专业技术岗位"'
        )

        for item in vocational_level_detail_count_list:
            df3[year][item[0]] = item[1]

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=get_vocational_level_list())
    df1.fillna(value=0, inplace=True)
    df1 = df1.loc[:, ~(df1 == 0).all()]  # 删除全为0的列
    container.add_dataframe(name="vocational_level_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe("vocational_level_growth_rate_and_year", df=df2)

    df3 = convert_dict_to_dataframe(d=df3).reindex(columns=get_vocational_level_detail_list())
    df3.fillna(value=0, inplace=True)
    df3 = df3.loc[:, ~(df3 == 0).all()]  # 删除全为0的列
    container.add_dataframe(name="vocational_level_detail_and_year", df=df3)

    df4 = get_growth_rate_from_multi_rows_dataframe(df=df3)
    container.add_dataframe("vocational_level_detail_growth_rate_and_year", df=df4)

    return container


def show_multi_years_and_1_area_teacher_0_discipline(year_list: list[str], area: str, period: str = None) -> None:
    """
    展示多年份不同学科教师数对比
    :param year_list: 年份列表
    :param area: 片镇名
    :param period: 任教学段
    :return:
    """
    df_container = get_multi_years_and_1_area_teacher_0_discipline_dataframe(year_list=year_list, area=area,
                                                                             period=period)

    left, right = st.columns(spec=2)

    with left:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="discipline_and_year").T, title="", height=400, )

    with right:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="discipline_growth_rate_and_year").T, title="",
                            height=400,
                            mark_line_y=0, formatter="{value} %")

    draw_mixed_bar_and_line(
        df_bar=df_container.get_dataframe(name="discipline_and_year"),
        df_line=df_container.get_dataframe(name="discipline_growth_rate_and_year"),
        bar_axis_label="人数",
        line_axis_label="增长率",
        # line_max_=50,
        # line_min_=-100,
        mark_line_y=0,
        line_formatter="{value} %"
    )

    with st.expander("详细信息"):
        st.dataframe(data=df_container.get_dataframe(name="discipline_and_year"))
        st.dataframe(
            data=df_container.get_dataframe(name="discipline_growth_rate_and_year").map(lambda x: f"{float(x):.1f}%"))

    return None


def get_multi_years_and_1_area_teacher_0_discipline_dataframe(year_list: list[str], area: str,
                                                              period: str = None) -> DataFrameContainer:
    """
    根据年份列表生成多个学科统计dataframe，放置在container中\n
    discipline_and_year：所有数据，列为学科，行为年份\n
    discipline_growth_rate_and_year：所有数据对学科求增长率，行为增长率对应年份，列为学科，单行\n
    :param year_list: 查询的年份列表
    :param area: 片镇名
    :param period: 任教学段
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为学历列

    for year in year_list:

        df1[year] = {}  # 初始化该年份的子字典
        """
        df_dict:{
        "2024":{
            "语文":100,
            "数学":200
            },
        "2023"：{
            "语文"：50，
            "数学"：100
            }
        }
        """
        discipline_count_list = execute_sql_sentence(
            sentence=f'select "主教学科", count(*) from teacher_data_0_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "主教学科" in ({', '.join([f'"{discipline}"' for discipline in get_discipline_list()])}) group by "主教学科"'
        )

        for item in discipline_count_list:
            df1[year][item[0]] = item[1]

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=get_discipline_list())
    df1.fillna(value=0, inplace=True)
    df1 = df1.loc[:, ~(df1 == 0).all()]  # 删除全为0的列
    container.add_dataframe(name="discipline_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe("discipline_growth_rate_and_year", df=df2)

    return container


def show_multi_years_and_1_area_teacher_0_grad_school(year_list: list[str], area: str, period: str = None) -> None:
    """
    展示多年份教师毕业院校质量对比
    :param year_list: 年份列表
    :param area: 片镇名
    :param period: 任教学段
    :return:
    """

    df_container = get_multi_years_and_1_area_teacher_0_grad_school_dataframe(year_list=year_list, area=area,
                                                                              period=period)

    left, right = st.columns(spec=2)

    with left:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="grad_school_kind_and_year").T, title="", height=400, )

    with right:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="grad_school_kind_growth_rate_and_year").T, title="",
                            height=400,
                            mark_line_y=0, formatter="{value} %")

    draw_mixed_bar_and_line(
        df_bar=df_container.get_dataframe(name="grad_school_kind_and_year"),
        df_line=df_container.get_dataframe(name="grad_school_kind_growth_rate_and_year"),
        bar_axis_label="人数",
        line_axis_label="增长率",
        mark_line_y=0,
        # line_max_=65,
        # line_min_=-65,
        line_formatter="{value} %"
    )

    with st.expander("详细信息"):
        left, right = st.columns(spec=2)
        with left:
            st.dataframe(data=df_container.get_dataframe(name="grad_school_kind_and_year"))
        with right:
            st.dataframe(data=df_container.get_dataframe(name="grad_school_kind_growth_rate_and_year").map(
                lambda x: f"{float(x):.1f}%"))

    if df_container.get_dataframe(name="grad_school_kind_and_year").empty or df_container.get_dataframe(
            name="grad_school_kind_growth_rate_and_year").empty:
        st.error(f'{area}的{period}在编教师工作前全日制最高学历均为大专及以下', icon="😕")

    return None


def get_multi_years_and_1_area_teacher_0_grad_school_dataframe(year_list: list[str], area: str,
                                                               period: str = None) -> DataFrameContainer:
    """
    根据年份列表生成多个学科统计dataframe，放置在container中\n
    grad_school_id_and_year：所有数据，列为院校代码，行为年份\n
    grad_school_kind_and_year：所有数据，列为院校类型，行为年份\n
    grad_school_kind_growth_rate_and_year：所有数据对院校类型求增长率，行为增长率对应年份，列为院校类型，单行\n
    :param year_list: 查询的年份列表
    :param area: 片镇名
    :param period: 任教学段
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df0 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为学历列
    df0.update({y: {} for y in year_list})

    grad_school_id_list = []

    query_parts = []
    for y in year_list:
        query_part = f'select "{y}", "参加工作前毕业院校代码" from teacher_data_0_{y} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生")'
        query_parts.append(query_part)

    final_query = " union all ".join(query_parts)

    grad_school_id_list.extend(
        item for item in execute_sql_sentence(
            sentence=final_query
        )
    )

    for item in grad_school_id_list:
        if item[1] not in df0[item[0]].keys():
            df0[item[0]][item[1]] = 1
        else:
            df0[item[0]][item[1]] += 1

    df1 = convert_dict_to_dataframe(d=df0)
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="grad_school_id_and_year", df=df1)

    df2 = {}
    for year in year_list:
        df2[year] = {item: 0 for item in ["985院校", "国优计划院校", "部属师范院校", "211院校", "其他院校"]}

    for item in grad_school_id_list:
        for kind in distinguish_school_id(school_id=item[1], label_length="long"):
            df2[item[0]][kind] += 1

    df2 = convert_dict_to_dataframe(d=df2)
    df2.fillna(value=0, inplace=True)
    df2 = df2.loc[:, ~(df2 == 0).all()]  # 删除全为0的列
    container.add_dataframe(name="grad_school_kind_and_year", df=df2)

    df3 = get_growth_rate_from_multi_rows_dataframe(df=df2)
    container.add_dataframe("grad_school_kind_growth_rate_and_year", df=df3)

    return container


def show_1_year_and_multi_areas_teacher_0(year: str, area_list: list, period: str = None) -> None:
    """
    用于展示同一片镇多年的在编教师数据对比信息
    :param year: 年份
    :param area_list: 查询的片镇列表
    :param period: 任教学段
    :return:
    """

    with st.container(border=True):
        # 小标题
        st.markdown(
            body="<h2 style='text-align: center;'>片镇对比</h2>",
            unsafe_allow_html=True
        )
        st.divider()

        st.info(f"{year}年不同片镇在编教师数情况")
        show_1_year_and_multi_areas_teacher_0_age(year=year, area_list=area_list, period=period)

        st.info(f"{year}年不同片镇学历水平情况")
        show_1_year_and_multi_areas_teacher_0_edu_bg(year=year, area_list=area_list, period=period)

        st.info(f"{year}年不同片镇专技职称情况")
        show_1_year_and_multi_areas_teacher_0_vocational_level_detail(year=year, area_list=area_list, period=period)

        st.info(f"{year}年不同片镇学科教师数情况")
        show_1_year_and_multi_areas_teacher_0_discipline(year=year, area_list=area_list, period=period)

        st.info(f"{year}年不同片镇教师毕业院校水平情况")
        show_1_year_and_multi_areas_teacher_0_grad_school_level(year=year, area_list=area_list, period=period)

    return None


def show_1_year_and_multi_areas_teacher_0_age(year: str, area_list: list[str], period: str = None) -> None:
    """
    展示多年份教师数对比
    :param year: 年份
    :param area_list: 查询的片镇列表
    :param period: 任教学段
    :return:
    """

    df_container = get_1_year_and_multi_areas_or_schools_teacher_0_age_dataframe(year=year, area_list=area_list,
                                                                                 period=period)

    with st.container(border=True):
        st.markdown(
            f"<h4 style='text-align: center;'>{period if period is not None else "高中以下"}教师人数对比</h4>",
            unsafe_allow_html=True
        )

        draw_line_chart(data=df_container.get_dataframe(name="age_and_location"), title="", height=600,
                        is_datazoom_show=True)

    with st.container(border=True):
        st.markdown(
            f"<h4 style='text-align: center;'>{period if period is not None else "高中以下"}教师人数占比对比</h4>",
            unsafe_allow_html=True
        )

        draw_line_chart(data=df_container.get_dataframe(name="age_percentage_and_location"), title="", height=600,
                        is_datazoom_show=True, formatter="{value} %")

    with st.expander("详细信息"):
        st.dataframe(data=df_container.get_dataframe(name="age_and_location"), height=282)

        st.dataframe(
            data=df_container.get_dataframe(name="age_percentage_and_location").map(lambda x: f"{float(x):.1f}%"),
            height=282)

    return None


def show_1_year_and_multi_areas_teacher_0_edu_bg(year: str, area_list: list[str], period: str = None) -> None:
    """
    展示多年份教师学历情况对比
    :param year: 年份
    :param area_list: 查询的片镇列表
    :param period: 任教学段
    :return:
    """

    df_container = get_1_year_and_multi_areas_or_schools_teacher_0_edu_bg_dataframe(year=year, area_list=area_list,
                                                                                    period=period)

    with st.container(border=True):
        st.markdown(
            f"<h4 style='text-align: center;'>{period if period is not None else "高中以下"}教师最高学历占比对比</h4>",
            unsafe_allow_html=True
        )

        draw_line_chart(data=df_container.get_dataframe(name="edu_bg_percentage_and_location"), title="", height=600,
                        is_datazoom_show=True, formatter="{value} %")

        with st.expander("详细信息"):
            left, right = st.columns(spec=2)
            with left:
                st.dataframe(data=df_container.get_dataframe(name="edu_bg_and_location"))
            with right:
                st.dataframe(data=df_container.get_dataframe(name="edu_bg_percentage_and_location").map(
                    lambda x: f"{float(x):.1f}%"))

    return None


def show_1_year_and_multi_areas_teacher_0_vocational_level_detail(year: str, area_list: list[str],
                                                                  period: str = None) -> None:
    """
    展示多年份教师专业技术等级对比
    :param year: 年份
    :param area_list: 查询的片镇列表
    :param period: 任教学段
    :return:
    """

    df_container = get_1_year_and_multi_areas_or_schools_teacher_0_vocational_level_detail_dataframe(year=year,
                                                                                                     area_list=area_list,
                                                                                                     period=period)

    with st.container(border=True):
        st.markdown(
            f"<h4 style='text-align: center;'>{period if period is not None else "高中以下"}教师专业技术等级占比对比</h4>",
            unsafe_allow_html=True
        )

        draw_line_chart(data=df_container.get_dataframe(name="vocational_level_detail_percentage_and_location"),
                        title="",
                        height=600,
                        is_datazoom_show=True, formatter="{value} %")

        with st.expander("详细信息"):
            left, right = st.columns(spec=2)
            with left:
                st.dataframe(data=df_container.get_dataframe(name="vocational_level_detail_and_location"))
            with right:
                st.dataframe(
                    data=df_container.get_dataframe(name="vocational_level_detail_percentage_and_location").map(
                        lambda x: f"{float(x):.1f}%"))

    return None


def show_1_year_and_multi_areas_teacher_0_discipline(year: str, area_list: list[str], period: str = None) -> None:
    """
    展示多年份教师学科数量对比
    :param year: 年份
    :param area_list: 查询的片镇列表
    :param period: 任教学段
    :return:
    """

    df_container = get_1_year_and_multi_areas_or_schools_teacher_0_discipline_dataframe(year=year,
                                                                                        area_list=area_list,
                                                                                        period=period)

    with st.container(border=True):
        st.markdown(
            f"<h4 style='text-align: center;'>{period if period is not None else "高中以下"}教师学科占比对比</h4>",
            unsafe_allow_html=True
        )

        draw_line_chart(data=df_container.get_dataframe(name="discipline_percentage_and_location"), title="",
                        height=600,
                        is_datazoom_show=True, formatter="{value} %")

        with st.expander("详细信息"):
            st.dataframe(data=df_container.get_dataframe(name="discipline_and_location"))

            st.dataframe(data=df_container.get_dataframe(name="discipline_percentage_and_location").map(
                lambda x: f"{float(x):.1f}%"))

    return None


def show_1_year_and_multi_areas_teacher_0_grad_school_level(year: str, area_list: list[str],
                                                            period: str = None) -> None:
    """
    展示多年份教师毕业院校情况对比
    :param year: 年份
    :param area_list: 查询的片镇列表
    :param period: 任教学段
    :return:
    """

    df_container = get_1_year_and_multi_areas_or_schools_teacher_0_grad_school_level_dataframe(year=year,
                                                                                               area_list=area_list,
                                                                                               period=period)

    with st.container(border=True):
        st.markdown(
            f"<h4 style='text-align: center;'>{period if period is not None else "高中以下"}教师毕业院校占比对比</h4>",
            unsafe_allow_html=True
        )

        draw_line_chart(data=df_container.get_dataframe(name="grad_school_percentage_and_location"), title="",
                        height=600,
                        is_datazoom_show=True, formatter="{value} %")

        with st.expander("详细信息"):
            left, right = st.columns(spec=2)
            with left:
                st.dataframe(data=df_container.get_dataframe(name="grad_school_kind_and_location"))
            with right:
                st.dataframe(data=df_container.get_dataframe(name="grad_school_percentage_and_location").map(
                    lambda x: f"{float(x):.1f}%"))

    return None


if __name__ == '__main__':
    pass
