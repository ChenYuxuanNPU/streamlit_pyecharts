import streamlit as st

from data_visualization.tool import func as visual_func
from teacher_data_processing.make_json.school_data import update_data as ud
from teacher_data_processing.tool import func as tch_proc_func


def update_specific_school(school_name: str, year: str, period: str, kind_0_flag=False, kind_1_flag=False) -> None:
    if kind_0_flag:
        ud.update(kind="在编", school_name=school_name, period=period, year=year)

    if kind_1_flag:
        ud.update(kind="编外", school_name=school_name, period=period, year=year)


def set_flags_and_update_school_data(school_name: str, year: str, period: str) -> None:
    if school_name is None:
        st.session_state.page4_search_flag = False
        st.toast("未填写校名", icon="⚠️")

        return None

    # 验证了输入的信息是否有误
    st.session_state.page4_kind_0_flag = tch_proc_func.school_name_and_period_check(kind="在编", year=year,
                                                                                    school_name=school_name,
                                                                                    period=period)[0]

    st.session_state.page4_kind_1_flag = tch_proc_func.school_name_and_period_check(kind="编外", year=year,
                                                                                    school_name=school_name,
                                                                                    period=period)[0]

    # 至少展示一类信息
    if st.session_state.page4_kind_0_flag or st.session_state.page4_kind_1_flag:
        st.session_state.page4_search_flag = True
        st.toast("查询成功！", icon="✅")

        update_specific_school(school_name=school_name, year=year, period=period,
                               kind_0_flag=st.session_state.page4_kind_0_flag,
                               kind_1_flag=st.session_state.page4_kind_1_flag)

    # 两类信息都找不到
    else:
        st.session_state.page4_search_flag = False
        st.toast(tch_proc_func.school_name_and_period_check(kind="在编", year=year,
                                                            school_name=school_name, period=period)[1], icon="⚠️")
        st.toast(tch_proc_func.school_name_and_period_check(kind="编外", year=year,
                                                            school_name=school_name, period=period)[1], icon="⚠️")


# 用于展示学校词云图
def show_word_cloud(year: str, data: dict) -> None:
    with st.container(border=True):
        # # 小标题
        # st.markdown(
        #     "<h2 style='text-align: center;'>区内学校</h2>",
        #     unsafe_allow_html=True
        # )

        visual_func.draw_word_cloud_chart(
            words=[[k, v[3]] for k, v in list(visual_func.simplify_school_name(data[year]["学校教师总数"]).items()) if
                   v[1] != "幼儿园"][:180],
            title="区内学校")


def show_school_stream(school_name: str, year: str, period: str) -> None:
    data = visual_func.load_json_data(folder="result", file_name="teacher_info")

    intro_0 = [
        f"统一社会信用代码：{data[year]["学校教师总数"][school_name][0]}",
        f"学校性质：{data[year]["学校教师总数"][school_name][1]}",
        f"所属区域：{data[year]["学校教师总数"][school_name][2]}",
    ]

    intro_1 = [
        f"学校总教师数：{data[year]["学校教师总数"][school_name][5]}",
        f"学校在编教师数：{data[year]["学校教师总数"][school_name][3]}",
        f"学校编外教师数：{data[year]["学校教师总数"][school_name][4]}",
    ]

    with st.container(border=False):

        # 小标题
        st.markdown(
            f"<h3 style='text-align: center;'>{school_name} - 学校基本概况</h3>",
            unsafe_allow_html=True
        )

        _, top_left, top_right = st.columns([1.7, 3.5, 3])

        with top_left:

            # 流式插入学校基础介绍
            for i in range(len(intro_0)):
                st.write_stream(visual_func.stream_data(sentence=intro_0[i]))

        with top_right:

            # 流式插入学校基础介绍
            for i in range(len(intro_1)):
                st.write_stream(visual_func.stream_data(sentence=intro_1[i]))


# 展示编内教师数据
def show_teacher_0(year: str, school_name: str, period: str) -> None:
    # 更新数据
    data = visual_func.load_json_data(folder="result", file_name="teacher_info")

    # 标题
    st.markdown(
        f"<h2 style='text-align: center;'>{school_name}{period}在编教师统计</h2>" if period != "所有学段" else f"<h2 style='text-align: center;'>{school_name}在编教师统计</h2>",
        unsafe_allow_html=True
    )

    st.info(f"在编总人数：{data[year]["在编"]["学校"][school_name][period]["总人数"]}")

    # st.write(json_data["在编"]["学校"][school_name][period])

    col0, col1, col2 = st.columns([1, 1, 1])

    with col0:
        # 在编年龄统计
        visual_func.draw_pie_chart(data=data[year]["在编"]["学校"][school_name][period]["年龄"],
                                   title="年龄", pos_left="15%", center_to_bottom="64%")

    with col1:
        # 在编学历统计
        visual_func.draw_pie_chart(data=data[year]["在编"]["学校"][school_name][period]["最高学历"],
                                   title="最高学历")

    with col2:
        # 在编职称统计
        visual_func.draw_pie_chart(data=data[year]["在编"]["学校"][school_name][period]["最高职称"],
                                   title="职称")

    # 在编学科统计
    visual_func.draw_bar_chart(data=data[year]["在编"]["学校"][school_name][period]["主教学科"],
                               title="主教学科",
                               end=100)

    col0, col1, col2 = st.columns([1, 1, 1])

    with col0:
        # 在编教资统计
        visual_func.draw_pie_chart(data=data[year]["在编"]["学校"][school_name][period]["教师资格"],
                                   title="教师资格")

        # 在编支教地域统计
        visual_func.draw_pie_chart(data=data[year]["在编"]["学校"][school_name][period]["支教地域"],
                                   title="支教地域")

    with col1:
        # 在编毕业院校统计
        visual_func.draw_bar_chart(
            data=data[year]["在编"]["学校"][school_name][period]["院校级别"],
            title="毕业院校", is_show_visual_map=False)

        # 在编骨干教师统计
        visual_func.draw_pie_chart(data=data[year]["在编"]["学校"][school_name][period]["骨干教师"],
                                   title="骨干教师")

    with col2:
        # 在编性别统计
        visual_func.draw_pie_chart(data=data[year]["在编"]["学校"][school_name][period]["性别"],
                                   title="性别")

        # 在编三名工作室统计
        visual_func.draw_pie_chart(data=data[year]["在编"]["学校"][school_name][period]["四名工作室"],
                                   title="三名统计")


# 展示编外教师数据
def show_teacher_1(year: str, school_name: str, period: str) -> None:
    # 更新数据
    data = visual_func.load_json_data(folder="result", file_name="teacher_info")

    # 标题
    st.markdown(
        f"<h2 style='text-align: center;'>{school_name}{period}编外教师统计</h2>" if period != "所有学段" else f"<h2 style='text-align: center;'>{school_name}编外教师统计</h2>",
        unsafe_allow_html=True
    )

    st.info(f"编外总人数：{data[year]["编外"]["学校"][school_name][period]["总人数"]}")

    # st.write(json_data[year]["编外"]["学校"][school_name][period])

    col0, col1 = st.columns(spec=2)

    with col0:
        # 编外学历统计
        visual_func.draw_pie_chart(data=data[year]["编外"]["学校"][school_name][period]["最高学历"],
                                   title="最高学历")

        # 编外教师资格统计
        visual_func.draw_pie_chart(data=data[year]["编外"]["学校"][school_name][period]["教师资格"],
                                   title="教师资格")

    with col1:
        # 编外职称统计
        visual_func.draw_pie_chart(data=data[year]["编外"]["学校"][school_name][period]["最高职称"],
                                   title="职称")

        # 编外骨干教师统计
        visual_func.draw_pie_chart(data=data[year]["编外"]["学校"][school_name][period]["骨干教师"],
                                   title="骨干教师")
