from data_visualization.render.statistics_and_charts import *


def show_1_year_teacher_0(year: str, ) -> None:
    """
    在编教师展示框架
    :param year: 年份
    :return:
    """
    data = load_json_data(folder="result", file_name="teacher_info")

    display_centered_title(title="在编教师数据", font_size=2)

    period_list = st.multiselect(
        label="请选择需要查询的学段",
        options=["所有学段"] + get_period_list(),
        default=["所有学段", get_period_list()[0]],  # 所有学段、高中
        placeholder="必选项"
    )

    if "所有学段" in period_list:
        show_1_year_all_period(year=year)

    for item in get_period_list():
        if item in period_list:
            show_1_year_given_period(year=year, period=item)

    return None


def show_1_year_all_period(year: str) -> None:
    """
    展示某一年所有学段的在编教师信息
    :param year: 年份
    :return:
    """
    data = load_json_data(folder="result", file_name="teacher_info")

    st.success(f"在编教职工总人数：{data[year]['在编']['全区']['所有学段']['总人数']}")

    with st.container(border=False):

        # 年龄性别柱状折线图，生成时要查询数据库，所以做个错误处理
        try:
            df_container = get_1_year_teacher_0_age_and_gender_dataframe(year=year)

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
            # 在编片区统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["片区统计"], title="片区统计")

            # 在编学历统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["最高学历"], title="最高学历")

        with c1:
            # 在编学段统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["学段统计"], title="学段统计")

            # 在编职称统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["最高职称"], title="职称")

        with c2:
            # 在编年龄统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["年龄"], title="年龄",
                           pos_left="15%",
                           center_to_bottom="64%")

            # 在编行政职务统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["行政职务"], title="行政职务",
                           center_to_bottom="68%")

        # 学科性别柱状折线图，生成时要查询数据库，所以做个错误处理
        try:
            df_container = get_1_year_teacher_0_discipline_and_gender_dataframe(year=year)

            draw_mixed_bar_and_line(
                df_bar=df_container.get_dataframe(name="data"),
                df_line=df_container.get_dataframe(name="sum"),
                bar_axis_label="人数", line_axis_label="合计人数",
                mark_line_type="average"
            )

        except Exception as e:
            print_color_text("学科柱状折线图展示异常")
            st.toast("学科柱状折线图展示异常", icon="😕")

        # 在编毕业院校统计
        with st.container(border=True):
            draw_line_chart(data=pd.DataFrame([data[year]["在编"]["全区"]["所有学段"]["院校级别"]],
                                              columns=data[year]["在编"]["全区"]["所有学段"]["院校级别"].keys(),
                                              index=["人数"]), title="毕业院校", height=400, is_datazoom_show=True)

        with st.container(border=True):
            df_container = get_1_year_teacher_0_grad_school_dataframe(year=year)
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

        c0, c1, c2 = st.columns(spec=3)

        with c0:
            # 在编骨干教师统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["骨干教师"], title="骨干教师")

        with c1:
            # 在编教师支教统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["支教地域"], title="支教地域")

        with c2:
            # 在编四名教师统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["四名工作室"], title="四名统计")

        # 教师分布前三十统计
        draw_bar_chart(data=data[year]["在编"]["全区"]["所有学段"]["教师分布前三十"], title="最多教师数",
                       is_visual_map_show=True, is_datazoom_show=True, axis_font_size=10)

        # 在编教师数后三十的学校统计
        draw_bar_chart(data=data[year]["在编"]["全区"]["所有学段"]["教师分布后三十"], title="最少教师数",
                       is_visual_map_show=True, is_datazoom_show=True, axis_font_size=10)

    return None


def show_1_year_given_period(year: str, period: str) -> None:
    """
    展示某一年某一学段的在编教师信息
    :param year: 年份
    :param period: 学段
    :return:
    """

    data = load_json_data(folder="result", file_name="teacher_info")

    st.info(f"在编{period}信息", icon="😋")

    with st.container(border=False):

        # 年龄性别柱状折线图，生成时要查询数据库，所以做个错误处理
        try:
            df_container = get_1_year_teacher_0_age_and_gender_dataframe(year=year, period=period)

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

        c0, c1 = st.columns([2, 1])

        with c0:
            draw_bar_chart(data=data[year]["在编"]["全区"][period]["主教学科"], title="主教学科",
                           is_visual_map_show=True, datazoom_end=get_end_dict()[period], axis_font_size=9)

        with c1:
            draw_pie_chart(data=data[year]["在编"]["全区"][period]["年龄"], title="年龄", pos_left="15%",
                           center_to_bottom="64%")

        with st.container(border=True):
            df_container = get_1_year_teacher_0_grad_school_dataframe(year=year, period=period)
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

        if period != "幼儿园":
            try:
                df_container = get_1_year_teacher_0_discipline_and_gender_dataframe(year=year, period=period)

                draw_mixed_bar_and_line(
                    df_bar=df_container.get_dataframe(name="data"),
                    df_line=df_container.get_dataframe(name="sum"),
                    bar_axis_label="人数", line_axis_label="合计人数",
                    mark_line_type="average"
                )

            except Exception as e:
                print_color_text("学科柱状折线图展示异常")
                st.toast("学科柱状折线图展示异常", icon="😕")

        c0, c1, c2 = st.columns(spec=3)

        with c0:
            draw_pie_chart(data=data[year]["在编"]["全区"][period]["最高学历"], title="最高学历")

        with c1:
            draw_bar_chart(data=data[year]["在编"]["全区"][period]["院校级别"], title="毕业院校",
                           is_visual_map_show=False)

        with c2:
            draw_pie_chart(data=data[year]["在编"]["全区"][period]["最高职称"], title="职称")

    return None


def show_1_year_teacher_1(year: str) -> None:
    """
    展示某一年编外教师信息
    :param year: 年份
    :return:
    """
    data = load_json_data(folder="result", file_name="teacher_info")

    display_centered_title(title="编外教师数据", font_size=2)

    st.info(f"编外教职工总人数：{data[year]['编外']['全区']['所有学段']['总人数']}")

    c0, c1, c2 = st.columns(spec=3)

    with c0:
        # 编外片区统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["片区统计"], title="片区统计")

        # 编外学段统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["学段统计"], title="学段统计")

    with c1:
        # 编外学历统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["最高学历"], title="最高学历")

        # 编外职称统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["最高职称"], title="职称")

    with c2:
        # 编外骨干教师统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["骨干教师"], title="骨干教师")

        # 编外四名教师统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["四名工作室"], title="四名统计")

    # 教师分布统计
    draw_bar_chart(data=data[year]["编外"]["全区"]["所有学段"]["教师分布前三十"], title="最多教师数",
                   is_visual_map_show=True, axis_font_size=10)

    c0, c1, c2 = st.columns(spec=3)

    with c0:
        # 编外教师资格统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["教师资格"], title="教师资格")

    with c1:
        # 编外中小学教师资格统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["中小学"]["教师资格"], title="中小学")

    with c2:
        # 编外幼儿园教师资格统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["幼儿园"]["教师资格"], title="幼儿园")

    return None


def show_multi_years_teacher_0(year_list: list[str]) -> None:
    """
    展示年份对比功能中在编教师的信息
    :param year_list: 年份列表
    :return:
    """

    with st.container(border=True):
        display_centered_title(title="年份对比", font_size=2)
        st.divider()

        st.info("在编教师数随年份变化情况")
        show_multi_years_teacher_0_age(year_list=year_list)

        st.info("片镇教师数随年份变化情况")
        show_multi_years_teacher_0_area(year_list=year_list)

        st.info("学段教师数随年份变化情况")
        show_multi_years_teacher_0_period(year_list=year_list)

        st.info("学历水平随年份变化情况")
        show_multi_years_teacher_0_edu_bg(year_list=year_list)

        st.info("专技职称随年份变化情况")
        show_multi_years_teacher_0_vocational_level(year_list=year_list)

        st.info("学科教师数随年份变化情况")
        show_multi_years_teacher_0_discipline(year_list=year_list)

        st.info("教师毕业院校水平随年份变化情况")
        show_multi_years_teacher_0_grad_school(year_list=year_list)

    return None


def show_multi_years_teacher_0_age(year_list: list[str]) -> None:
    """
    展示多年份教师数对比
    :param year_list: 年份列表
    :return:
    """

    df_container = get_multi_years_teacher_0_age_dataframe(year_list=year_list)

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


def show_multi_years_teacher_0_area(year_list: list[str]) -> None:
    """
    展示多年份片镇教师数对比
    :param year_list: 年份列表
    :return:
    """

    df_container = get_multi_years_teacher_0_area_dataframe(year_list=year_list)

    left, right = st.columns(spec=2)

    with left:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="area_and_year").T, title="", height=400, )

    with right:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="area_growth_rate_and_year").T, title="", height=400,
                            mark_line_y=0, formatter="{value} %")

    draw_mixed_bar_and_line(
        df_bar=df_container.get_dataframe(name="area_and_year"),
        df_line=df_container.get_dataframe(name="area_growth_rate_and_year"),
        bar_axis_label="人数",
        line_axis_label="增长率",
        line_max_=20,
        line_min_=-20,
        mark_line_y=0,
        line_formatter="{value} %"
    )

    with st.expander(label="详细信息"):
        left, right = st.columns(spec=2)

        with left:
            display_centered_title(title="片镇人数", font_size=5)
            display_centered_dataframe(df=df_container.get_dataframe(name="area_and_year"),
                                       margin_bottom=20)

        with right:
            display_centered_title(title="片镇增长率", font_size=5)
            display_centered_dataframe(df=df_container.get_dataframe(name="area_growth_rate_and_year").map(
                lambda x: f"{float(x):.1f}%"), margin_top=20)

    return None


def show_multi_years_teacher_0_period(year_list: list[str]) -> None:
    """
    展示多年份不同学段教师数对比
    :param year_list: 年份列表
    :return:
    """
    df_container = get_multi_years_teacher_0_period_dataframe(year_list=year_list)

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
        line_max_=20,
        line_min_=-20,
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
            display_centered_title(title="学段增长率", font_size=5)
            display_centered_dataframe(df=df_container.get_dataframe(name="period_growth_rate_and_year").map(
                lambda x: f"{float(x):.1f}%"), margin_top=20)

    return None


def show_multi_years_teacher_0_edu_bg(year_list: list[str]) -> None:
    """
    展示多年份教师学历对比
    :param year_list: 年份列表
    :return:
    """
    df_container = get_multi_years_teacher_0_edu_bg_dataframe(year_list=year_list)

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
            display_centered_title(title="学历增长率", font_size=5)
            display_centered_dataframe(df=df_container.get_dataframe(name="edu_bg_growth_rate_and_year").map(
                lambda x: f"{float(x):.1f}%"), margin_top=20)

    return None


def show_multi_years_teacher_0_vocational_level(year_list: list[str]) -> None:
    """
    展示多年份教师专业技术级别对比
    :param year_list: 年份列表
    :return:
    """
    df_container = get_multi_years_teacher_0_vocational_level_dataframe(year_list=year_list)

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
        line_max_=60,
        line_min_=-100,
        mark_line_y=0,
        line_formatter="{value} %",
        x_axis_font_size=9
    )

    with st.expander("详细信息"):
        display_centered_title(title="专业技术职称人数", font_size=5)
        display_centered_dataframe(df=df_container.get_dataframe(name="shorten_vocational_level_detail_and_year"),
                                   margin_bottom=20)

        display_centered_title(title="专业技术职称增长率", font_size=5)
        display_centered_dataframe(
            df=df_container.get_dataframe(name="shorten_vocational_level_detail_growth_rate_and_year").map(
                lambda x: f"{float(x):.1f}%"))

    return None


def show_multi_years_teacher_0_discipline(year_list: list[str]) -> None:
    """
    展示多年份不同学科教师数对比
    :param year_list: 年份列表
    :return:
    """
    df_container = get_multi_years_teacher_0_discipline_dataframe(year_list=year_list)

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
        line_max_=50,
        line_min_=-100,
        mark_line_y=0,
        line_formatter="{value} %"
    )

    with st.expander("详细信息"):
        display_centered_title(title="学科人数", font_size=5)
        display_centered_dataframe(df=df_container.get_dataframe(name="discipline_and_year"),
                                   margin_bottom=20)

        display_centered_title(title="学科增长率", font_size=5)
        display_centered_dataframe(df=df_container.get_dataframe(name="discipline_growth_rate_and_year").map(
            lambda x: f"{float(x):.1f}%"), margin_bottom=20)

    return None


def show_multi_years_teacher_0_grad_school(year_list: list[str]) -> None:
    """
    展示多年份教师毕业院校质量对比
    :param year_list: 年份列表
    :return:
    """

    df_container = get_multi_years_teacher_0_grad_school_dataframe(year_list=year_list)

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
            display_centered_title(title="毕业院校层次增长情况", font_size=5)
            display_centered_dataframe(df=df_container.get_dataframe(name="grad_school_kind_growth_rate_and_year").map(
                lambda x: f"{float(x):.1f}%"), margin_top=20)

    return None


@st.fragment
def ai_module(year_list: list) -> None:
    _, col_mid, _ = st.columns([4, 1, 4])

    col_wide = st.columns(spec=1)

    with col_mid:
        if st.button(label="DeepSeek自动分析数据"):
            with col_wide[0]:
                show_ai_explain(year_list=year_list)


@st.fragment
def show_ai_explain(year_list: list) -> None:
    list_data = []

    for df_container in [get_multi_years_teacher_0_age_dataframe(year_list=year_list),
                         get_multi_years_teacher_0_area_dataframe(year_list=year_list),
                         get_multi_years_teacher_0_period_dataframe(year_list=year_list),
                         get_multi_years_teacher_0_edu_bg_dataframe(year_list=year_list),
                         get_multi_years_teacher_0_vocational_level_dataframe(year_list=year_list),
                         get_multi_years_teacher_0_discipline_dataframe(year_list=year_list),
                         get_multi_years_teacher_0_grad_school_dataframe(year_list=year_list)]:

        for df_name in [n for n in df_container.list_dataframes() if
                        n not in excluded_df_name_in_df_container(param="district_multi_years")]:
            list_data.append([df_name, df_container.get_dataframe(name=df_name).to_json(force_ascii=False)])
            print(df_name, df_container.get_dataframe(name=df_name).to_json(force_ascii=False))

    # print(str(list_data))


if __name__ == '__main__':
    # container = get_1_year_grad_school_dataframe(year="2024")
    # print(container.get_dataframe("df_985"))
    pass
