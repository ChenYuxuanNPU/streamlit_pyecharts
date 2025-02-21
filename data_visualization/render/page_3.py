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
        display_centered_title(title="广州市白云区各教育指导中心相关信息", font_size=3)

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
            df_container = get_1_year_teacher_0_age_and_gender_dataframe(year=year, area=area, period=period)

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
            df_container = get_1_year_teacher_0_grad_school_dataframe(year=year, area=area, period=period)
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
            title="主教学科", is_visual_map_show=False, axis_font_size=10, is_datazoom_show=True)

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
        display_centered_title(title="年份对比", font_size=2)
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

    df_container = get_multi_years_teacher_0_age_dataframe(year_list=year_list, area=area, period=period)

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


def show_multi_years_and_1_area_teacher_0_period(year_list: list[str], area: str) -> None:
    """
    展示多年份不同学段教师数对比
    :param year_list: 年份列表
    :param area: 片镇名
    :return:
    """
    df_container = get_multi_years_teacher_0_period_dataframe(year_list=year_list, area=area)

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
            display_centered_title(title="学段人数", font_size=5)
            display_centered_dataframe(df=df_container.get_dataframe(name="period_and_year"),
                                       margin_bottom=20)

        with right:
            display_centered_title(title="学段占比", font_size=5)
            display_centered_dataframe(df=df_container.get_dataframe(name="period_growth_rate_and_year").map(
                lambda x: f"{float(x):.1f}%"), margin_top=20)

    return None


def show_multi_years_and_1_area_teacher_0_edu_bg(year_list: list[str], area: str, period: str = None) -> None:
    """
    展示多年份教师学历对比
    :param year_list: 年份列表
    :param area: 片镇名
    :param period: 任教学段
    :return:
    """
    df_container = get_multi_years_teacher_0_edu_bg_dataframe(year_list=year_list, area=area, period=period)

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
            display_centered_title(title="学历人数", font_size=5)
            display_centered_dataframe(df=df_container.get_dataframe(name="edu_bg_and_year"),
                                       margin_bottom=20)

        with right:
            display_centered_title(title="学历占比", font_size=5)
            display_centered_dataframe(df=df_container.get_dataframe(name="edu_bg_growth_rate_and_year").map(
                lambda x: f"{float(x):.1f}%"), margin_top=20, margin_bottom=20)

    return None


def show_multi_years_and_1_area_teacher_0_vocational_level(year_list: list[str], area: str, period: str = None) -> None:
    """
    展示多年份教师专业技术级别对比
    :param year_list: 年份列表
    :param area: 片镇名
    :param period: 任教学段
    :return:
    """
    df_container = get_multi_years_teacher_0_vocational_level_dataframe(year_list=year_list, area=area, period=period)

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
        # st.dataframe(data=df_container.get_dataframe(name="vocational_level_detail_and_year"))
        # st.dataframe(data=df_container.get_dataframe(name="vocational_level_detail_growth_rate_and_year").map(
        #     lambda x: f"{float(x):.1f}%"))

        display_centered_title(title="专技职称人数", font_size=5)
        display_centered_dataframe(df=df_container.get_dataframe(name="shorten_vocational_level_detail_and_year"),
                                   margin_bottom=20)

        display_centered_title(title="专技占比", font_size=5)
        display_centered_dataframe(
            df=df_container.get_dataframe(name="shorten_vocational_level_detail_growth_rate_and_year").map(
                lambda x: f"{float(x):.1f}%"))

    return None


def show_multi_years_and_1_area_teacher_0_discipline(year_list: list[str], area: str, period: str = None) -> None:
    """
    展示多年份不同学科教师数对比
    :param year_list: 年份列表
    :param area: 片镇名
    :param period: 任教学段
    :return:
    """
    df_container = get_multi_years_teacher_0_discipline_dataframe(year_list=year_list, area=area, period=period)

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
        mark_line_y=0,
        line_formatter="{value} %"
    )

    with st.expander("详细信息"):
        display_centered_title(title="学科人数", font_size=5)
        display_centered_dataframe(df=df_container.get_dataframe(name="discipline_and_year"),
                                   margin_bottom=20)

        display_centered_title(title="学科占比", font_size=5)
        display_centered_dataframe(df=df_container.get_dataframe(name="discipline_growth_rate_and_year").map(
            lambda x: f"{float(x):.1f}%"), margin_bottom=20)

    return None


def show_multi_years_and_1_area_teacher_0_grad_school(year_list: list[str], area: str, period: str = None) -> None:
    """
    展示多年份教师毕业院校质量对比
    :param year_list: 年份列表
    :param area: 片镇名
    :param period: 任教学段
    :return:
    """

    df_container = get_multi_years_teacher_0_grad_school_dataframe(year_list=year_list, area=area, period=period)

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
            display_centered_title(title="毕业院校层次", font_size=5)
            display_centered_dataframe(df=df_container.get_dataframe(name="grad_school_kind_and_year"),
                                       margin_bottom=20)

        with right:
            display_centered_title(title="毕业院校层次占比", font_size=5)
            display_centered_dataframe(df=df_container.get_dataframe(name="grad_school_kind_growth_rate_and_year").map(
                lambda x: f"{float(x):.1f}%"), margin_top=20)

    if df_container.get_dataframe(name="grad_school_kind_and_year").empty or df_container.get_dataframe(
            name="grad_school_kind_growth_rate_and_year").empty:
        st.error(f'{area}的{period}在编教师工作前全日制最高学历均为大专及以下', icon="😕")

    return None


def show_1_year_and_multi_areas_teacher_0(year: str, area_list: list, period: str = None) -> None:
    """
    用于展示同一片镇多年的在编教师数据对比信息
    :param year: 年份
    :param area_list: 查询的片镇列表
    :param period: 任教学段
    :return:
    """

    with st.container(border=True):
        display_centered_title(title="片镇对比", font_size=2)
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

    df_container = get_1_year_and_multi_locations_teacher_0_age_dataframe(year=year, area_list=area_list, period=period)

    with st.container(border=True):
        display_centered_title(title=f"{period if period is not None else "高中以下"}教师人数对比", font_size=4)

        draw_line_chart(data=df_container.get_dataframe(name="age_and_location"), title="", height=600,
                        is_datazoom_show=True)

    with st.container(border=True):
        display_centered_title(title=f"{period if period is not None else "高中以下"}教师人数中占比对比", font_size=4)

        draw_line_chart(data=df_container.get_dataframe(name="age_percentage_and_location"), title="", height=600,
                        is_datazoom_show=True, formatter="{value} %")

    with st.expander("详细信息"):
        st.dataframe(data=df_container.get_dataframe(name="age_and_location"), )  # height=282

        st.dataframe(
            data=df_container.get_dataframe(name="age_percentage_and_location").map(lambda x: f"{float(x):.1f}%"), )

    return None


def show_1_year_and_multi_areas_teacher_0_edu_bg(year: str, area_list: list[str], period: str = None) -> None:
    """
    展示多年份教师学历情况对比
    :param year: 年份
    :param area_list: 查询的片镇列表
    :param period: 任教学段
    :return:
    """

    df_container = get_1_year_and_multi_locations_teacher_0_edu_bg_dataframe(year=year, area_list=area_list,
                                                                             period=period)

    with st.container(border=True):
        display_centered_title(title=f"{period if period is not None else "高中以下"}教师最高学历占比对比", font_size=4)

        draw_line_chart(data=df_container.get_dataframe(name="edu_bg_percentage_and_location"), title="", height=600,
                        is_datazoom_show=True, formatter="{value} %")

        with st.expander("详细信息"):
            left, right = st.columns(spec=2)
            with left:
                display_centered_title(title="学历人数", font_size=5)
                display_centered_dataframe(df=df_container.get_dataframe(name="edu_bg_and_location"), margin_bottom=20)

            with right:
                display_centered_title(title="学科占比", font_size=5)
                display_centered_dataframe(df=df_container.get_dataframe(name="edu_bg_percentage_and_location").map(
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

    df_container = get_1_year_and_multi_locations_teacher_0_vocational_level_detail_dataframe(year=year,
                                                                                              area_list=area_list,
                                                                                              period=period)

    with st.container(border=True):
        display_centered_title(title=f"{period if period is not None else "高中以下"}教师专业技术等级占比对比",
                               font_size=4)

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

    df_container = get_1_year_and_multi_locations_teacher_0_discipline_dataframe(year=year, area_list=area_list,
                                                                                 period=period)

    with st.container(border=True):
        display_centered_title(title=f"{period if period is not None else "高中以下"}教师学科占比对比",
                               font_size=4)

        draw_line_chart(data=df_container.get_dataframe(name="discipline_percentage_and_location"), title="",
                        height=600,
                        is_datazoom_show=True, formatter="{value} %")

        with st.expander("详细信息"):
            # st.dataframe(data=df_container.get_dataframe(name="discipline_and_location"))
            display_centered_title(title="学科人数", font_size=5)
            display_centered_dataframe(df=df_container.get_dataframe(name="discipline_and_location"), margin_bottom=40)

            # st.dataframe(data=df_container.get_dataframe(name="discipline_percentage_and_location").map(
            #     lambda x: f"{float(x):.1f}%"))

            display_centered_title(title="学科占比", font_size=5)
            display_centered_dataframe(df=df_container.get_dataframe(name="discipline_percentage_and_location").map(
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

    df_container = get_1_year_and_multi_locations_teacher_0_grad_school_level_dataframe(year=year, area_list=area_list,
                                                                                        period=period)

    with st.container(border=True):
        display_centered_title(title=f"{period if period is not None else "高中以下"}教师毕业院校占比对比",
                               font_size=4)

        draw_line_chart(data=df_container.get_dataframe(name="grad_school_percentage_and_location"), title="",
                        height=600,
                        is_datazoom_show=True, formatter="{value} %")

        with st.expander("详细信息"):
            left, right = st.columns(spec=2)

            with left:
                display_centered_title(title="毕业院校层次", font_size=5)
                display_centered_dataframe(df=df_container.get_dataframe(name="grad_school_kind_and_location"),
                                           margin_bottom=20)

            with right:
                display_centered_title(title="毕业院校层次占比", font_size=5)
                display_centered_dataframe(
                    df=df_container.get_dataframe(name="grad_school_percentage_and_location").map(
                        lambda x: f"{float(x):.1f}%"))

    return None


if __name__ == '__main__':
    pass
