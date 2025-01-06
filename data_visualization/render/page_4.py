from calculation.retirement import *
from data_visualization.tool.func import *
from teacher_data_processing.make_json.school_data.update_data import *
from teacher_data_processing.tool.func import *


def get_base_data() -> dict:
    """
    获取全区教师数据
    :return:
    """
    return load_json_data(folder="result", file_name="teacher_info")


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
        # st.session_state.page4_info_kind = None

        if not kwargs["year_list"]:
            st.toast("需要选择查询的年份", icon="🥱")

        if not kwargs["school_list"]:
            st.toast("需要选择查询的学校", icon="🥱")

    # 这里要判断是否只查询某一所学校
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
        st.session_state.page4_kind_0_flag = \
            school_name_and_period_check(kind="在编", year=year_list[0],
                                         school=school_list[0],
                                         period=period)[0]

        st.session_state.page4_1_year_and_1_school_kind_1_flag = \
            school_name_and_period_check(kind="编外", year=year_list[0],
                                         school=school_list[0],
                                         period=period)[0]

        # 至少展示一类信息
        if st.session_state.page4_kind_0_flag or st.session_state.page4_1_year_and_1_school_kind_1_flag:

            st.toast("查询成功！", icon="✅")

            st.session_state.page4_info_kind = "1"
            st.session_state.page4_year_list = year_list
            st.session_state.page4_school_list = school_list
            st.session_state.page4_period = period

            if not st.session_state.page4_kind_0_flag:
                st.toast(school_name_and_period_check(kind="在编", year=year_list[0],
                                                      school=school_list[0], period=period)[1], icon="⚠️")

            if not st.session_state.page4_1_year_and_1_school_kind_1_flag:
                st.toast(school_name_and_period_check(kind="编外", year=year_list[0],
                                                      school=school_list[0], period=period)[1], icon="⚠️")

            update_specific_school(school=school_list[0], year=year_list[0], period=period,
                                   kind_0_flag=st.session_state.page4_kind_0_flag,
                                   kind_1_flag=st.session_state.page4_1_year_and_1_school_kind_1_flag)

        # 两类信息都找不到
        else:
            st.session_state.page4_info_kind = None
            st.toast(school_name_and_period_check(kind="在编", year=year_list[0],
                                                  school=school_list[0], period=period)[1], icon="⚠️")
            st.toast(school_name_and_period_check(kind="编外", year=year_list[0],
                                                  school=school_list[0], period=period)[1], icon="⚠️")

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
    if st.session_state.page4_info_kind == "1" and st.session_state.page4_kind_0_flag:
        with st.container(border=True):
            show_1_year_and_1_school_teacher_0(year=year, school=school,
                                               period=period if period is not None else None)

    if st.session_state.page4_info_kind == "1" and st.session_state.page4_kind_0_flag and st.session_state.page4_1_year_and_1_school_kind_1_flag:
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
        st.markdown(
            f"<h3 style='text-align: center;'>{school} - 学校基本概况</h3>",
            unsafe_allow_html=True
        )

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
    st.markdown(
        f"<h2 style='text-align: center;'>{year}年{school}{period if period is not None else ""}在编教师统计</h2>" if period != "所有学段" else f"<h2 style='text-align: center;'>{school}在编教师统计</h2>",
        unsafe_allow_html=True
    )

    st.info(
        f"在编总人数：{get_base_data()[year]["在编"]["学校"][school][period if period is not None else "所有学段"]["总人数"]}")

    # st.write(json_data["在编"]["学校"][school][period])

    try:
        df_container = get_1_year_and_1_school_age_and_gender_dataframe(year=year, school=school, period=period)

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

    with st.container(border=True):
        df_container = get_1_year_grad_school_dataframe(year=year, school=school, period=period)
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


def get_1_year_and_1_school_age_and_gender_dataframe(year: str, school: str, period: str) -> DataFrameContainer:
    """
    根据年份生成列为年龄，行为性别的dataframe\n
    data: 二维dataframe，包含性别和年龄\n
    sum: 一维dataframe，包含年龄和人数总和
    :param year: 查询的年份
    :param school: 查询的学校
    :param period: 查询的学段
    :return:
    """

    container = DataFrameContainer()

    df_dict = {"男": {}, "女": {}}  # 使用嵌套字典保存数据，外层为性别行，内层为年龄列
    ages = set()  # 用于检查age_dict中是否有对应的年龄

    min_age = 1000
    max_age = -1

    id_list = execute_sql_sentence(
        sentence=f'select "身份证号", "性别" from teacher_data_0_{year} where "校名" = "{school}"{f' and "任教学段" = "{period}"' if period is not None else ''}'
    )

    for item in id_list:

        age = str(get_age_from_citizen_id(citizen_id=item[0], year=year))

        min_age = int(age) if int(age) < min_age else min_age
        max_age = int(age) if int(age) > max_age else max_age

        if age not in ages:

            for gender in ["男", "女"]:
                df_dict[gender][age] = 0

        df_dict[item[1]][age] += 1

        ages.add(age)

    for age in range(min_age, max_age):

        if str(age) not in df_dict["男"].keys():
            df_dict["男"][str(age)] = 0

        if str(age) not in df_dict["女"].keys():
            df_dict["女"][str(age)] = 0

    container.add_dataframe(name="data", df=sort_dataframe_columns(df=convert_dict_to_dataframe(d=df_dict)))

    df = pd.DataFrame(sort_dataframe_columns(df=convert_dict_to_dataframe(d=df_dict)).sum()).T
    df.index = ["合计"]

    container.add_dataframe("sum", df=df)

    return container


def get_1_year_grad_school_dataframe(year: str, school: str, period: str = None) -> DataFrameContainer:
    """
    根据年份多个包含院校名及其频率的dataframe\n
    df_985:985院校名及其数量\n
    df_nettp:国优计划院校名及其数量\n
    df_affiliate:部属师范院校名及其数量\n
    df_211:211院校名及其数量\n
    :param year: 查询的年份
    :param school: 查询的学校
    :param period: 查询的学段
    :return:
    """
    container = DataFrameContainer()

    try:
        container.add_dataframe(
            name="df_985",
            df=pd.Series(
                dict(
                    execute_sql_sentence(
                        sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0_{year} where "参加工作前毕业院校代码" in ({', '.join([f'"{code}"' for code in get_school_codes()["985"]])}) and "校名" = "{school}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
                    )
                )
            )
            .nlargest(20).to_frame()
            .rename(
                index={
                    key: value[0] for key, value in load_json_data(folder="source", file_name="院校代码").items()
                },
                columns={0: "人数"}
            )
            .rename_axis(["985院校"])
        )

    except TypeError as e:
        if "Cannot use method 'nlargest' with dtype object" in str(e):
            st.toast(f'无985院校毕业生', icon="😟")
            container.add_dataframe(
                name="df_985",
                df=pd.DataFrame(data=["0"], columns=["人数"], index=["无"]).rename_axis(["985院校"])
            )
        else:
            print(e)

    try:
        container.add_dataframe(
            name="df_nettp",
            df=pd.Series(
                dict(
                    execute_sql_sentence(
                        sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0_{year} where "参加工作前毕业院校代码" in ({', '.join([f'"{code}"' for code in get_school_codes()["国优计划"]])}) and "校名" = "{school}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
                    )
                )
            )
            .nlargest(20).to_frame()
            .rename(
                index={
                    key: value[0] for key, value in load_json_data(folder="source", file_name="院校代码").items()
                },
                columns={0: "人数"}
            )
            .rename_axis(["国优计划院校"])
        )

    except TypeError as e:
        if "Cannot use method 'nlargest' with dtype object" in str(e):
            st.toast(f'无国优计划院校毕业生', icon="😟")
            container.add_dataframe(
                name="df_nettp",
                df=pd.DataFrame(data=["0"], columns=["人数"], index=["无"]).rename_axis(["国优计划院校"])
            )
        else:
            print(e)

    try:
        container.add_dataframe(
            name="df_affiliate",
            df=pd.Series(
                dict(
                    execute_sql_sentence(
                        sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0_{year} where "参加工作前毕业院校代码" in ({', '.join([f'"{code}"' for code in get_school_codes()["部属师范"]])}) and "校名" = "{school}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
                    )
                )
            )
            .nlargest(20).to_frame()
            .rename(
                index={
                    key: value[0] for key, value in load_json_data(folder="source", file_name="院校代码").items()
                },
                columns={0: "人数"}
            )
            .rename_axis(["部属师范院校"])
        )

    except TypeError as e:
        if "Cannot use method 'nlargest' with dtype object" in str(e):
            st.toast(f'无部属师范院校毕业生', icon="😟")
            container.add_dataframe(
                name="df_affiliate",
                df=pd.DataFrame(data=["0"], columns=["人数"], index=["无"]).rename_axis(["部属师范院校"])
            )
        else:
            print(e)

    try:
        container.add_dataframe(
            name="df_211",
            df=pd.Series(
                dict(
                    execute_sql_sentence(
                        sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0_{year} where "参加工作前毕业院校代码" in ({', '.join([f'"{code}"' for code in get_school_codes()["211"]])}) and "校名" = "{school}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
                    )
                )
            )
            .nlargest(20).to_frame()
            .rename(
                index={
                    key: value[0] for key, value in load_json_data(folder="source", file_name="院校代码").items()
                },
                columns={0: "人数"}
            )
            .rename_axis(["211院校"])
        )

    except TypeError as e:
        if "Cannot use method 'nlargest' with dtype object" in str(e):
            st.toast(f'无211院校毕业生', icon="😟")
            container.add_dataframe(
                name="df_211",
                df=pd.DataFrame(data=["0"], columns=["人数"], index=["无"]).rename_axis(["211院校"])
            )
        else:
            print(e)

    container.add_dataframe(
        name="df_all",
        df=pd.Series(
            dict(
                execute_sql_sentence(
                    sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0_{year} where "参加工作前毕业院校代码" not in ({', '.join([f'"{code}"' for code in ["无", "51161", "51315"]])}) and "校名" = "{school}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
                )
            )
        )
        .nlargest(100).to_frame()
        .rename(
            index={
                key: value[0] for key, value in load_json_data(folder="source", file_name="院校代码").items()
            },
            columns={0: "人数"}
        )
        .rename_axis(["所有院校"])
    )

    return container


def show_1_year_and_1_school_teacher_1(year: str, school: str, period: str) -> None:
    """
    展示编外数据
    :param year: 年份
    :param school:校名
    :param period: 学段
    :return: 无
    """

    # 标题
    st.markdown(
        f"<h2 style='text-align: center;'>{year}年{school}{period if period is not None else ""}编外教师统计</h2>" if period != "所有学段" else f"<h2 style='text-align: center;'>{school}编外教师统计</h2>",
        unsafe_allow_html=True
    )

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
