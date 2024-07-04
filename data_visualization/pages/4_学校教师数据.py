import sys

import streamlit as st

sys.path.append(
    r'C:\Users\1012986131\Desktop\python\streamlit_pyecharts'
)

from teacher_data_processing.tool import func as tch_proc_func
from data_visualization.tool import func as visual_func
from teacher_data_processing.make_json.school_data import update_data as ud

# 初始化全局变量
visual_func.session_state_initial()

# 清空其他页暂用变量
visual_func.session_state_reset(page=4)

# 设置全局属性
visual_func.set_page_configuration(title="学校教师数据", icon=":house_with_garden:")

# 判断是否查询成功
st.session_state.page4_search_flag = False

# 判断kind_list的元素个数
st.session_state.page4_kind_0_flag = False
st.session_state.page4_kind_1_flag = False

# 读取现有json文件
json_data = visual_func.load_json_data(folder="result", file_name="teacher_info")

# 标题
st.markdown(
    "<h1 style='text-align: center;'>学校教师数据</h1>",
    unsafe_allow_html=True
)

st.divider()

with st.container(border=True):
    col0, col1 = st.columns([2, 3])

    with col0:

        col01, col10, col11 = st.columns([1, 4, 1])

        with col10:

            # 校名搜索栏下拉框
            page4_school_name = st.selectbox(
                "请输入完整校名",
                json_data["学校教师总数"].keys(),
                index=None,
                placeholder="校名全称",
            )

            raw_period = st.selectbox(
                "选择查询学段",
                ("所有学段", "高中", "初中", "小学"),
            )
            # 对空代指的所有学段进行预处理
            period = visual_func.trans_period[raw_period]

        col99, col88 = st.columns([2, 3])

        with col88:

            if st.button("查询"):

                if page4_school_name is None:
                    st.session_state.page4_search_flag = False
                    st.toast("校名为空", icon="⚠️")

                else:

                    # 验证了输入的信息是否有误
                    check_result_0 = tch_proc_func.school_name_and_period_check(kind="在编",
                                                                                school_name=page4_school_name,
                                                                                period=period)

                    check_result_1 = tch_proc_func.school_name_and_period_check(kind="编外",
                                                                                school_name=page4_school_name,
                                                                                period=period)
                    st.session_state.page4_kind_0_flag = check_result_0[0]
                    st.session_state.page4_kind_1_flag = check_result_1[0]

                    # 至少展示一类信息
                    if st.session_state.page4_kind_0_flag or st.session_state.page4_kind_1_flag:
                        st.session_state.page4_search_flag = True
                        st.toast("查询成功！", icon="✅")

                        if st.session_state.page4_kind_0_flag:
                            ud.update(kind="在编", school_name=page4_school_name, period=period)

                        if st.session_state.page4_kind_1_flag:
                            ud.update(kind="编外", school_name=page4_school_name, period=period)

                        intro_0 = [
                            f"统一社会信用代码：{json_data["学校教师总数"][page4_school_name][0]}",
                            f"学校性质：{json_data["学校教师总数"][page4_school_name][1]}",
                            f"所属区域：{json_data["学校教师总数"][page4_school_name][2]}",
                        ]

                        intro_1 = [
                            f"学校总教师数：{json_data["学校教师总数"][page4_school_name][5]}",
                            f"学校在编教师数：{json_data["学校教师总数"][page4_school_name][3]}",
                            f"学校编外教师数：{json_data["学校教师总数"][page4_school_name][4]}",
                        ]

                        with col1:

                            with st.container(border=False):

                                # 小标题
                                st.markdown(
                                    f"<h3 style='text-align: center;'>{page4_school_name} - 学校基本概况</h3>",
                                    unsafe_allow_html=True
                                )

                                _, col0, col1 = st.columns([1, 3, 3])

                                with col0:

                                    # 流式插入学校基础介绍
                                    for i in range(len(intro_0)):
                                        st.write_stream(visual_func.stream_data(sentence=intro_0[i]))

                                with col1:

                                    # 流式插入学校基础介绍
                                    for i in range(len(intro_1)):
                                        st.write_stream(visual_func.stream_data(sentence=intro_1[i]))

                    # 一类信息都找不到
                    else:
                        st.session_state.page4_search_flag = False
                        st.toast(check_result_0[1], icon="⚠️")
                        st.toast(check_result_1[1], icon="⚠️")

# 展示在编数据
with st.container(border=True):
    if st.session_state.page4_search_flag and st.session_state.page4_kind_0_flag:
        # 更新数据
        json_data = visual_func.load_json_data(folder="result", file_name="teacher_info")

        # 标题
        st.markdown(
            f"<h2 style='text-align: center;'>{page4_school_name}{period}在编教师统计</h2>" if period is not None else f"<h2 style='text-align: center;'>{page4_school_name}在编教师统计</h2>",
            unsafe_allow_html=True
        )

        st.info(f"在编总人数：{json_data["在编"]["学校"][page4_school_name][raw_period]["总人数"]}")

        # st.write(json_data["在编"]["学校"][school_name][raw_period])

        col0, col1, col2 = st.columns([1, 1, 1])

        with col0:
            # 在编年龄统计
            visual_func.draw_pie(data=json_data["在编"]["学校"][page4_school_name][raw_period]["年龄"],
                                 title="年龄")

        with col1:
            # 在编学历统计
            visual_func.draw_pie(data=json_data["在编"]["学校"][page4_school_name][raw_period]["最高学历"],
                                 title="最高学历")

        with col2:
            # 在编职称统计
            visual_func.draw_pie(data=json_data["在编"]["学校"][page4_school_name][raw_period]["最高职称"],
                                 title="职称")

        # 在编学科统计
        visual_func.draw_bar(data=json_data["在编"]["学校"][page4_school_name][raw_period]["主教学科"],
                                  title="主教学科",
                                  end=100)

        col0, col1, col2 = st.columns([1, 1, 1])

        with col0:
            # 在编教资统计
            visual_func.draw_pie(data=json_data["在编"]["学校"][page4_school_name][raw_period]["教师资格"],
                                 title="教师资格")

            # 在编支教地域统计
            visual_func.draw_pie(data=json_data["在编"]["学校"][page4_school_name][raw_period]["支教地域"],
                                 title="支教地域")

        with col1:
            # 在编毕业院校统计
            visual_func.draw_bar(
                data=json_data["在编"]["学校"][page4_school_name][raw_period]["院校级别"],
                title="毕业院校", is_show_visual_map=False)

            # 在编骨干教师统计
            visual_func.draw_pie(data=json_data["在编"]["学校"][page4_school_name][raw_period]["骨干教师"],
                                 title="骨干教师")

        with col2:
            # 在编性别统计
            visual_func.draw_pie(data=json_data["在编"]["学校"][page4_school_name][raw_period]["性别"],
                                 title="性别")

            # 在编三名工作室统计
            visual_func.draw_pie(data=json_data["在编"]["学校"][page4_school_name][raw_period]["三名工作室"],
                                 title="三名统计")

        st.divider()

# 展示编外数据
with st.container(border=True):
    if st.session_state.page4_search_flag and st.session_state.page4_kind_1_flag:
        # 更新数据
        json_data = visual_func.load_json_data(folder="result", file_name="teacher_info")

        # 标题
        st.markdown(
            f"<h2 style='text-align: center;'>{page4_school_name}{period}编外教师统计</h2>" if period is not None else f"<h2 style='text-align: center;'>{page4_school_name}编外教师统计</h2>",
            unsafe_allow_html=True
        )

        st.info(f"编外总人数：{json_data["编外"]["学校"][page4_school_name][raw_period]["总人数"]}")

        # st.write(json_data["编外"]["学校"][school_name][raw_period])

        col0, col1 = st.columns(spec=2)

        with col0:
            # 编外学历统计
            visual_func.draw_pie(data=json_data["编外"]["学校"][page4_school_name][raw_period]["最高学历"],
                                 title="最高学历")

            # 编外教师资格统计
            visual_func.draw_pie(data=json_data["编外"]["学校"][page4_school_name][raw_period]["教师资格"],
                                 title="教师资格")

        with col1:
            # 编外职称统计
            visual_func.draw_pie(data=json_data["编外"]["学校"][page4_school_name][raw_period]["最高职称"],
                                 title="职称")

            # 编外骨干教师统计
            visual_func.draw_pie(data=json_data["编外"]["学校"][page4_school_name][raw_period]["骨干教师"],
                                 title="骨干教师")

# 展示学校云图
if not st.session_state.page4_search_flag:

    with st.container(border=True):

        # 小标题
        st.markdown(
            "<h2 style='text-align: center;'>区内学校</h2>",
            unsafe_allow_html=True
        )

        visual_func.draw_word_cloud(words=[[k, v[3]] for k, v in list(visual_func.simplify_school_name(json_data["学校教师总数"]).items()) if v[1] != "幼儿园"],
                                    title="")

        