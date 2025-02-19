from data_visualization.render.statistics_and_charts import *
from teacher_data_processing.make_json.school_data.update_data import *
from teacher_data_processing.tool.func import *


def get_base_data() -> dict:
    """
    获取全区教师数据
    :return:
    """
    return load_json_data(folder="result", file_name="teacher_info")


def get_school_list_by_year_list(year_list: list[str]) -> list:
    """
    用于计算选中年份对应的学校列表
    :param year_list: 目前选中的年份列表
    :return:
    """
    output = {}
    dict1 = load_json_data(folder="result", file_name="teacher_info")

    for year in year_list:
        for school in dict1.get(f"{year}", {}).get("学校教师总数", {}).keys():

            if school not in output.keys():
                output[school] = dict1.get(f"{year}", {}).get("学校教师总数", {}).get(f"{school}", {})[5]

            else:
                output[school] = max(
                    dict1.get(f"{year}", {}).get("学校教师总数", {}).get(f"{school}", {})[5], output[school]
                )

    return [key for key, value in sorted(output.items(), key=lambda item: item[1], reverse=True)]


def update_specific_school(school: str, year: str, period: str, kind_0_flag=False, kind_1_flag=False) -> None:
    """
    根据参数更新json文件中的学校数据
    :param school: 校名
    :param year: 年份
    :param period: 学段
    :param kind_0_flag:是否更新在编数据
    :param kind_1_flag: 是否更新编外数据
    :return: 无
    """

    if kind_0_flag:
        update(kind="在编", school_name=school, period=period, year=year)

    if kind_1_flag:
        update(kind="编外", school_name=school, period=period, year=year)

    return None


# 这里要加一个返回值，判断查询的信息属于什么类型
def confirm_input(**kwargs) -> None:
    """
    用于确认输入的组件状态并确定需要查询的信息类型
    :return: 暂无
    """

    if min(len(list(kwargs["year_list"])), len(list(kwargs["school_list"]))) > 1:
        st.toast("年份与学校不能同时多选！", icon="🥺")

    if not kwargs["year_list"] or not kwargs["school_list"]:

        if not kwargs["year_list"]:
            st.toast("需要选择查询的年份", icon="🥱")

        if not kwargs["school_list"]:
            st.toast("需要选择查询的学校", icon="🥱")

    # 这里要判断查询类型并设置flag
    set_flags_and_update_school_data(school_list=kwargs["school_list"], year_list=kwargs["year_list"],
                                     period=kwargs["period"])

    return None


def set_flags_and_update_school_data(year_list: list, school_list: list, period: str or None = None) -> None:
    """
    用于更新json文件中学校数据，设置st的全局变量从而使页面组件展示信息，返回查询类型的列表
    :param year_list: 需要更新的年份列表
    :param school_list: 学校列表
    :param period: 需要更新的学段
    :return:
    """

    if len(year_list) == 1 and len(school_list) == 1:

        # 验证了输入的信息是否有误
        st.session_state.page4_1_year_and_1_school_kind_0_flag = \
            school_name_and_period_check(kind="在编", year=year_list[0],
                                         school=school_list[0],
                                         period=period)[0]

        st.session_state.page4_1_year_and_1_school_kind_1_flag = \
            school_name_and_period_check(kind="编外", year=year_list[0],
                                         school=school_list[0],
                                         period=period)[0]

        # 至少展示一类信息
        if st.session_state.page4_1_year_and_1_school_kind_0_flag or st.session_state.page4_1_year_and_1_school_kind_1_flag:

            st.toast("查询成功！", icon="✅")

            st.session_state.page4_info_kind = "1"
            st.session_state.page4_year_list = year_list
            st.session_state.page4_school_list = school_list
            st.session_state.page4_period = period

            if not st.session_state.page4_1_year_and_1_school_kind_0_flag:
                st.toast(school_name_and_period_check(kind="在编", year=year_list[0],
                                                      school=school_list[0], period=period)[1], icon="⚠️")

            if not st.session_state.page4_1_year_and_1_school_kind_1_flag:
                st.toast(school_name_and_period_check(kind="编外", year=year_list[0],
                                                      school=school_list[0], period=period)[1], icon="⚠️")

            update_specific_school(school=school_list[0], year=year_list[0], period=period,
                                   kind_0_flag=st.session_state.page4_1_year_and_1_school_kind_0_flag,
                                   kind_1_flag=st.session_state.page4_1_year_and_1_school_kind_1_flag)

        # 两类信息都找不到
        else:
            st.session_state.page4_info_kind = None
            st.toast(school_name_and_period_check(kind="在编", year=year_list[0],
                                                  school=school_list[0], period=period)[1], icon="⚠️")
            st.toast(school_name_and_period_check(kind="编外", year=year_list[0],
                                                  school=school_list[0], period=period)[1], icon="⚠️")

    elif len(year_list) > 1 and len(school_list) == 1:

        success_flag = False
        for year in year_list:

            if school_name_and_period_check(kind="在编", year=year, school=school_list[0], period=period)[0]:

                if not success_flag:
                    st.toast("查询成功！", icon="✅")
                    success_flag = True

                st.session_state.page4_info_kind = "2.1"
                st.session_state.page4_year_list = year_list
                st.session_state.page4_school_list = school_list
                st.session_state.page4_period = period

            else:
                st.toast(
                    school_name_and_period_check(kind="在编", year=year, school=school_list[0], period=period)[
                        1], icon="⚠️")

    elif len(year_list) == 1 and len(school_list) > 1:

        success_flag = False
        for school in school_list:
            if school_name_and_period_check(kind="在编", year=year_list[0], school=school, period=period)[0]:

                if not success_flag:
                    st.toast("查询成功！", icon="✅")
                    success_flag = True

                st.session_state.page4_info_kind = "1.2"
                st.session_state.page4_year_list = year_list
                st.session_state.page4_school_list = school_list
                st.session_state.page4_period = period

            else:
                st.toast(
                    school_name_and_period_check(kind="在编", year=year_list[0], school=school, period=period)[
                        1], icon="⚠️")

    return None


# 不搜索学校信息时展示学校词云图
def show_word_cloud(year: str or int = get_year_list(kind="teacher_info")[0]) -> None:
    """
    用于展示学校词云图
    :param year: 年份
    :return: 无
    """

    with st.container(border=True):
        draw_word_cloud_chart(
            words=[[k, v[3]] for k, v in
                   list(simplify_school_name(get_base_data()[str(year)]["学校教师总数"]).items()) \
                   if v[1] != "幼儿园"][:180],
            title="区内学校")

    return None


def show_1_year_and_1_school(year: str, school: str, period: str) -> None:
    """
    展示某一年某一学校教师信息
    :param year: 查询的某一年份
    :param school: 查询的某一学校
    :param period: 可选的查询学段
    :return: 
    """
    with st.container(border=True):
        show_school_stream(year=year,
                           school=school)

    # 展示某一年在编数据
    if st.session_state.page4_info_kind == "1" and st.session_state.page4_1_year_and_1_school_kind_0_flag:
        with st.container(border=True):
            show_1_year_and_1_school_teacher_0(year=year, school=school,
                                               period=period if period is not None else None)

    if st.session_state.page4_info_kind == "1" and st.session_state.page4_1_year_and_1_school_kind_0_flag and st.session_state.page4_1_year_and_1_school_kind_1_flag:
        st.divider()

    # 展示某一年编外数据
    if st.session_state.page4_info_kind == "1" and st.session_state.page4_1_year_and_1_school_kind_1_flag:
        with st.container(border=True):
            show_1_year_and_1_school_teacher_1(year=year, school=school,
                                               period=period if period is not None else None)


def show_school_stream(school: str, year: str) -> None:
    """
    流式展示学校基础信息
    :param school: 校名
    :param year: 年份
    :return: 无
    """

    intro_0 = [
        f"统一社会信用代码：{get_base_data()[year]["学校教师总数"][school][0]}",
        f"学校性质：{get_base_data()[year]["学校教师总数"][school][1]}",
        f"所属区域：{get_base_data()[year]["学校教师总数"][school][2]}",
    ]

    intro_1 = [
        f"学校总教师数：{get_base_data()[year]["学校教师总数"][school][5]}",
        f"学校在编教师数：{get_base_data()[year]["学校教师总数"][school][3]}",
        f"学校编外教师数：{get_base_data()[year]["学校教师总数"][school][4]}",
    ]

    with st.container(border=False):

        # 小标题
        display_centered_title(title=f'{school} - 学校基本概况', font_size=3)

        _, top_left, top_right = st.columns([1.7, 3.5, 3])

        with top_left:

            # 流式插入学校基础介绍
            for i in range(len(intro_0)):
                st.write_stream(stream_data(sentence=intro_0[i]))

        with top_right:

            # 流式插入学校基础介绍
            for i in range(len(intro_1)):
                st.write_stream(stream_data(sentence=intro_1[i]))

    return None


def show_1_year_and_1_school_teacher_0(year: str, school: str, period: str) -> None:
    """
    展示在编数据
    :param year: 年份
    :param school:校名
    :param period: 学段
    :return: 无
    """

    # 标题
    display_centered_title(
        title=f'{year}年{school}{period if period is not None else ""}在编教师统计' if period != "所有学段" else f'{school}在编教师统计',
        font_size=2)

    st.info(
        f"在编总人数：{get_base_data()[year]["在编"]["学校"][school][period if period is not None else "所有学段"]["总人数"]}")

    # st.write(json_data["在编"]["学校"][school][period])

    try:
        df_container = get_1_year_teacher_0_age_and_gender_dataframe(year=year, school=school, period=period)

        draw_mixed_bar_and_line(
            df_bar=df_container.get_dataframe(name="data"),
            df_line=df_container.get_dataframe(name="sum"),
            bar_axis_label="人数", line_axis_label="合计人数",
            mark_line_type="average", multiple_for_border=30
        )

    except Exception as e:
        print_color_text("年龄柱状折线图展示异常")
        print(e)
        st.toast("年龄柱状折线图展示异常", icon="😕")

    col0, col1, col2 = st.columns([1, 1, 1])

    with col0:
        # 在编年龄统计
        draw_pie_chart(
            data=get_base_data()[year]["在编"]["学校"][school][period if period is not None else "所有学段"][
                "年龄"],
            title="年龄", pos_left="15%", center_to_bottom="64%")

    with col1:
        # 在编学历统计
        draw_pie_chart(
            data=get_base_data()[year]["在编"]["学校"][school][period if period is not None else "所有学段"][
                "最高学历"],
            title="最高学历")

    with col2:
        # 在编职称统计
        draw_pie_chart(
            data=get_base_data()[year]["在编"]["学校"][school][period if period is not None else "所有学段"][
                "最高职称"],
            title="职称")

    # 在编学科统计
    draw_bar_chart(
        data=get_base_data()[year]["在编"]["学校"][school][period if period is not None else "所有学段"][
            "主教学科"],
        title="主教学科", is_datazoom_show=True, )

    try:
        df_container = get_1_year_teacher_0_discipline_and_gender_dataframe(year=year, school=school, period=period)

        draw_mixed_bar_and_line(
            df_bar=df_container.get_dataframe(name="data"),
            df_line=df_container.get_dataframe(name="sum"),
            bar_axis_label="人数", line_axis_label="合计人数",
            mark_line_type="average",
            height=0.6
        )

    except Exception as e:
        print_color_text("学科柱状折线图展示异常")
        st.toast("学科柱状折线图展示异常", icon="😕")

    with st.container(border=True):
        df_container = get_1_year_teacher_0_grad_school_dataframe(year=year, school=school, period=period)
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

    col0, col1, col2 = st.columns([1, 1, 1])

    with col0:
        # 在编教资统计
        draw_pie_chart(
            data=get_base_data()[year]["在编"]["学校"][school][period if period is not None else "所有学段"][
                "教师资格"],
            title="教师资格")

        # 在编支教地域统计
        draw_pie_chart(
            data=get_base_data()[year]["在编"]["学校"][school][period if period is not None else "所有学段"][
                "支教地域"],
            title="支教地域")

    with col1:
        # 在编毕业院校统计
        draw_bar_chart(
            data=get_base_data()[year]["在编"]["学校"][school][period if period is not None else "所有学段"][
                "院校级别"],
            title="毕业院校", is_visual_map_show=False)

        # 在编骨干教师统计
        draw_pie_chart(
            data=get_base_data()[year]["在编"]["学校"][school][period if period is not None else "所有学段"][
                "骨干教师"],
            title="骨干教师")

    with col2:
        # 在编性别统计
        draw_pie_chart(
            data=get_base_data()[year]["在编"]["学校"][school][period if period is not None else "所有学段"][
                "性别"],
            title="性别")

        # 在编三名工作室统计
        draw_pie_chart(
            data=get_base_data()[year]["在编"]["学校"][school][period if period is not None else "所有学段"][
                "四名工作室"],
            title="三名统计")

    return None


def show_1_year_and_1_school_teacher_1(year: str, school: str, period: str) -> None:
    """
    展示编外数据
    :param year: 年份
    :param school:校名
    :param period: 学段
    :return: 无
    """

    # 标题
    display_centered_title(
        title=f'{year}年{school}{period if period is not None else ""}编外教师统计' if period != "所有学段" else f'{school}编外教师统计',
        font_size=2)

    st.info(
        f"编外总人数：{get_base_data()[year]["编外"]["学校"][school][period if period is not None else "所有学段"]["总人数"]}")

    # st.write(json_data[year]["编外"]["学校"][school][period])

    col0, col1 = st.columns(spec=2)

    with col0:
        # 编外学历统计
        draw_pie_chart(
            data=get_base_data()[year]["编外"]["学校"][school][period if period is not None else "所有学段"][
                "最高学历"],
            title="最高学历")

        # 编外教师资格统计
        draw_pie_chart(
            data=get_base_data()[year]["编外"]["学校"][school][period if period is not None else "所有学段"][
                "教师资格"],
            title="教师资格")

    with col1:
        # 编外职称统计
        draw_pie_chart(
            data=get_base_data()[year]["编外"]["学校"][school][period if period is not None else "所有学段"][
                "最高职称"],
            title="职称")

        # 编外骨干教师统计
        draw_pie_chart(
            data=get_base_data()[year]["编外"]["学校"][school][period if period is not None else "所有学段"][
                "骨干教师"],
            title="骨干教师")

    return None


def show_1_year_and_multi_schools(year: str, school_list: list[str], period: str) -> None:
    """
    展示某一年某一学校教师信息
    :param year: 查询的某一年份
    :param school_list: 查询的学校列表
    :param period: 可选的查询学段
    :return:
    """

    with st.container(border=True):
        # 小标题
        display_centered_title(title="学校对比", font_size=2)
        st.divider()

        show_1_year_and_multi_schools_teacher_0(year=year, school_list=school_list, period=period)


def show_1_year_and_multi_schools_teacher_0(year: str, school_list: list[str], period: str) -> None:
    """
    展示某一年某一学校教师信息
    :param year: 查询的某一年份
    :param school_list: 查询的学校列表
    :param period: 可选的查询学段
    :return:
    """

    display_centered_title(title="在编教师信息", font_size=3)
    st.divider()

    st.info(f"{year}年不同学校在编教师数情况")
    show_1_year_and_multi_schools_teacher_0_age(year=year, school_list=school_list, period=period)

    st.info(f"{year}年不同学校学历水平情况")
    show_1_year_and_multi_schools_teacher_0_edu_bg(year=year, school_list=school_list, period=period)

    st.info(f"{year}年不同学校专技职称情况")
    show_1_year_and_multi_schools_teacher_0_vocational_level_detail(year=year, school_list=school_list,
                                                                    period=period)

    st.info(f"{year}年不同学校学科教师数情况")
    show_1_year_and_multi_schools_teacher_0_discipline(year=year, school_list=school_list, period=period)

    st.info(f"{year}年不同学校教师毕业院校水平情况")
    show_1_year_and_multi_schools_teacher_0_grad_school_level(year=year, school_list=school_list, period=period)


def show_1_year_and_multi_schools_teacher_0_age(year: str, school_list: list[str], period: str):
    """
    展示某一年某一学校教师信息
    :param year: 查询的某一年份
    :param school_list: 查询的学校列表
    :param period: 可选的查询学段
    :return:
    """

    df_container = get_1_year_and_multi_locations_teacher_0_age_dataframe(year=year, school_list=school_list,
                                                                          period=period)

    with st.container(border=True):
        display_centered_title(title=f'{period if period is not None else "所有学段"}教师人数对比', font_size=4)

        draw_line_chart(data=df_container.get_dataframe(name="age_and_location"), title="", height=600,
                        is_datazoom_show=True)

    with st.container(border=True):
        display_centered_title(title=f'{period if period is not None else "所有学段"}教师人数占比对比', font_size=4)

        draw_line_chart(data=df_container.get_dataframe(name="age_percentage_and_location"), title="", height=600,
                        is_datazoom_show=True, formatter="{value} %")

    with st.expander("详细信息"):
        st.dataframe(data=df_container.get_dataframe(name="age_and_location"))

        st.dataframe(
            data=df_container.get_dataframe(name="age_percentage_and_location").map(lambda x: f"{float(x):.1f}%"))

    return None


def show_1_year_and_multi_schools_teacher_0_edu_bg(year: str, school_list: list[str], period: str = None) -> None:
    """
    展示多学校教师学历情况对比
    :param year: 年份
    :param school_list: 查询的片镇列表
    :param period: 任教学段
    :return:
    """

    df_container = get_1_year_and_multi_locations_teacher_0_edu_bg_dataframe(year=year, school_list=school_list,
                                                                             period=period)

    with st.container(border=True):
        display_centered_title(title=f'{period if period is not None else "所有学段"}教师最高学历占比对比', font_size=4)

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


def show_1_year_and_multi_schools_teacher_0_vocational_level_detail(year: str, school_list: list[str],
                                                                    period: str = None) -> None:
    """
    展示多学校教师专业技术等级对比
    :param year: 年份
    :param school_list: 查询的片镇列表
    :param period: 任教学段
    :return:
    """

    df_container = get_1_year_and_multi_locations_teacher_0_vocational_level_detail_dataframe(year=year,
                                                                                              school_list=school_list,
                                                                                              period=period)

    with st.container(border=True):
        display_centered_title(title=f'{period if period is not None else "所有学段"}教师专业技术等级占比对比',
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


def show_1_year_and_multi_schools_teacher_0_discipline(year: str, school_list: list[str], period: str = None) -> None:
    """
    展示多学校教师学科数量对比
    :param year: 年份
    :param school_list: 查询的片镇列表
    :param period: 任教学段
    :return:
    """

    df_container = get_1_year_and_multi_locations_teacher_0_discipline_dataframe(year=year,
                                                                                 school_list=school_list,
                                                                                 period=period)

    with st.container(border=True):
        display_centered_title(title=f'{period if period is not None else "所有学段"}教师学科占比对比', font_size=4)

        draw_line_chart(data=df_container.get_dataframe(name="discipline_percentage_and_location"), title="",
                        height=600,
                        is_datazoom_show=True, formatter="{value} %")

        with st.expander("详细信息"):
            st.dataframe(data=df_container.get_dataframe(name="discipline_and_location"))

            st.dataframe(data=df_container.get_dataframe(name="discipline_percentage_and_location").map(
                lambda x: f"{float(x):.1f}%"))

    return None


def show_1_year_and_multi_schools_teacher_0_grad_school_level(year: str, school_list: list[str],
                                                              period: str = None) -> None:
    """
    展示不同学校教师毕业院校情况对比
    :param year: 年份
    :param school_list: 查询的片镇列表
    :param period: 任教学段
    :return:
    """

    df_container = get_1_year_and_multi_locations_teacher_0_grad_school_level_dataframe(year=year,
                                                                                        school_list=school_list,
                                                                                        period=period)

    with st.container(border=True):
        display_centered_title(title=f'{period if period is not None else "所有学段"}教师毕业院校占比对比', font_size=4)

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


def show_multi_years_and_1_school(year_list: list[str], school: str, period: str) -> None:
    """
    展示某一年某一学校教师信息
    :param year_list: 查询的年份列表
    :param school: 查询的某一学校
    :param period: 可选的查询学段
    :return:
    """

    with st.container(border=True):
        # 小标题
        display_centered_title(title="学年对比", font_size=2)
        st.divider()

        show_multi_years_and_1_school_teacher_0(year_list=year_list, school=school, period=period)


def show_multi_years_and_1_school_teacher_0(year_list: list[str], school: str, period: str) -> None:
    """
    展示某一年某一学校教师信息
    :param year_list: 查询的年份列表
    :param school: 查询的某一学校
    :param period: 可选的查询学段
    :return:
    """

    display_centered_title(title="在编教师信息", font_size=3)
    st.divider()

    st.info(f"{school}在编{period if period is not None else ""}教师数随年份变化情况")
    show_multi_years_and_1_school_teacher_0_age(year_list=year_list, school=school, period=period)

    st.info(f"{school}在编{period if period is not None else ""}教师学历水平随年份变化情况")
    show_multi_years_and_1_school_teacher_0_edu_bg(year_list=year_list, school=school, period=period)

    st.info(f"{school}在编{period if period is not None else ""}教师专技职称随年份变化情况")
    show_multi_years_and_1_school_teacher_0_vocational_level(year_list=year_list, school=school, period=period)

    st.info(f"{school}在编{period if period is not None else ""}学科教师数随年份变化情况")
    show_multi_years_and_1_school_teacher_0_discipline(year_list=year_list, school=school, period=period)

    st.info(f"{school}在编{period if period is not None else ""}教师毕业院校水平随年份变化情况")
    show_multi_years_and_1_school_teacher_0_grad_school(year_list=year_list, school=school, period=period)


def show_multi_years_and_1_school_teacher_0_age(year_list: list[str], school: str, period: str = None) -> None:
    """
    展示多年份教师数对比
    :param year_list: 年份列表
    :param school: 查询的单个校名
    :param period: 任教学段
    :return:
    """

    df_container = get_multi_years_teacher_0_age_dataframe(year_list=year_list, school=school, period=period)

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
        mark_line_y=0,
        line_formatter="{value} %"
    )

    with st.expander("详细信息"):
        st.dataframe(data=df_container.get_dataframe(name="age_and_year"))

        st.dataframe(data=df_container.get_dataframe(name="age_growth_rate_and_year").map(lambda x: f"{float(x):.1f}%"))

    return None


def show_multi_years_and_1_school_teacher_0_edu_bg(year_list: list[str], school: str, period: str = None) -> None:
    """
    展示多年份教师学历对比
    :param year_list: 年份列表
    :param school: 查询的单个校名
    :param period: 任教学段
    :return:
    """
    df_container = get_multi_years_teacher_0_edu_bg_dataframe(year_list=year_list, school=school, period=period)

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


def show_multi_years_and_1_school_teacher_0_vocational_level(year_list: list[str], school: str,
                                                             period: str = None) -> None:
    """
    展示多年份教师专业技术级别对比
    :param year_list: 年份列表
    :param school: 查询的单个校名
    :param period: 任教学段
    :return:
    """
    df_container = get_multi_years_teacher_0_vocational_level_dataframe(year_list=year_list, school=school,
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


def show_multi_years_and_1_school_teacher_0_discipline(year_list: list[str], school: str, period: str = None) -> None:
    """
    展示多年份不同学科教师数对比
    :param year_list: 年份列表
    :param school: 查询的单个校名
    :param period: 任教学段
    :return:
    """
    df_container = get_multi_years_teacher_0_discipline_dataframe(year_list=year_list, school=school, period=period)

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
        st.dataframe(data=df_container.get_dataframe(name="discipline_and_year"))
        st.dataframe(
            data=df_container.get_dataframe(name="discipline_growth_rate_and_year").map(lambda x: f"{float(x):.1f}%"))

    return None


def show_multi_years_and_1_school_teacher_0_grad_school(year_list: list[str], school: str, period: str = None) -> None:
    """
    展示多年份教师毕业院校质量对比
    :param year_list: 年份列表
    :param school: 查询的单个校名
    :param period: 任教学段
    :return:
    """

    df_container = get_multi_years_teacher_0_grad_school_dataframe(year_list=year_list, school=school, period=period)

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
        st.error(f'{school}的{period}在编教师工作前全日制最高学历均为大专及以下', icon="😕")

    return None
