import sys
import time
import streamlit as st

sys.path.append(
    r'C:\Users\1012986131\Desktop\python\streamlit_pyecharts'
)

from data_processing.tool import module as m_proc
from data_visualization.tool import module as m_visual
from data_processing.make_json.school_data import update_data as ud
from data_processing.read_database import get_database_data as gd

# 设置全局属性
m_visual.set_page_configuration(title="学校教师数据", icon=":house_with_garden:")

# 判断是否查询成功
search_flag = False

# 判断kind_list的元素个数
kind_0_flag = False
kind_1_flag = False

# 读取基础数据
json_data = m_visual.load_json_data(file_name="teacher_info")

# 标题
st.title("学校教师数据")

with st.container(border=True):
    col0, col1 = st.columns([2, 3])

    with col0:

        col01, col10, col11 = st.columns([1, 4, 1])

        with col10:

            # 校名搜索栏下拉框
            school_name = st.selectbox(
                "请输入校名",
                json_data["学校教师总数"].keys(),
                index=None,
                placeholder=" ",
            )

            raw_period = st.selectbox(
                "选择查询学段",
                ("所有学段", "高中", "初中", "小学"),
            )
            # 对空代指的所有学段进行预处理
            period = m_visual.trans_period[raw_period]

        # kind = st.selectbox(
        #     "选择类型",
        #     ("在编", "非编"),
        # )

        col99, col88 = st.columns([2, 3])

        with col88:

            if st.button("查询"):

                if school_name is None or school_name == "":
                    search_flag = False
                    st.toast("校名为空", icon="⚠️")

                else:

                    # 验证了输入的信息是否有误
                    check_result_0 = m_proc.school_name_and_period_check(kind="在编", school_name=school_name,
                                                                         period=period)

                    check_result_1 = m_proc.school_name_and_period_check(kind="非编", school_name=school_name,
                                                                         period=period)
                    kind_0_flag = check_result_0[0]
                    kind_1_flag = check_result_1[0]

                    # 至少展示一类信息
                    if kind_0_flag or kind_1_flag:
                        search_flag = True
                        st.toast("查询成功！", icon="✅")

                        if kind_0_flag:
                            ud.update(kind="在编", school_name=school_name, period=period)

                        if kind_1_flag:
                            ud.update(kind="非编", school_name=school_name, period=period)

                        intro_0 = [
                            f"统一社会信用代码：{json_data["学校教师总数"][school_name][0]}",
                            f"学校性质：{json_data["学校教师总数"][school_name][1]}",
                            f"所属区域：{json_data["学校教师总数"][school_name][2]}",
                        ]

                        intro_1 = [
                            f"学校总教师数：{json_data["学校教师总数"][school_name][5]}",
                            f"学校在编教师数：{json_data["学校教师总数"][school_name][3]}",
                            f"学校编外教师数：{json_data["学校教师总数"][school_name][4]}",
                        ]

                        with col1:

                            with st.container(border=False):

                                col00, col11 = st.columns([1, 3.5])

                                with col11:

                                    st.subheader(f"{school_name} - 学校基本概况")

                                c0lm1, col01, col10 = st.columns([1, 3, 3])

                                with col01:

                                    # 流式插入学校基础介绍
                                    for i in range(len(intro_0)):
                                        st.write_stream(m_visual.stream_data(sentence=intro_0[i]))

                                with col10:

                                    # 流式插入学校基础介绍
                                    for i in range(len(intro_1)):
                                        st.write_stream(m_visual.stream_data(sentence=intro_1[i]))

                    # 一类信息都找不到
                    else:
                        search_flag = False
                        st.toast(check_result_0[1], icon="⚠️")
                        st.toast(check_result_1[1], icon="⚠️")

# 展示在编数据
with st.container(border=True):
    if search_flag and kind_0_flag:
        # 更新数据
        json_data = m_visual.load_json_data(file_name="teacher_info")

        st.subheader(f"{school_name}{period}在编教师统计" if period is not None else f"{school_name}在编教师统计")

        st.info(f"在编总人数：{json_data["在编"]["学校"][school_name][raw_period]["总人数"]}")

        # st.write(json_data["在编"]["学校"][school_name][raw_period])

        col0, col1, col2 = st.columns([1, 1, 1])

        with col0:
            # 在编年龄统计
            m_visual.draw_pie(data=json_data["在编"]["学校"][school_name][raw_period]["年龄"], title="年龄")

        with col1:
            # 在编学历统计
            m_visual.draw_pie(data=json_data["在编"]["学校"][school_name][raw_period]["最高学历"], title="最高学历")

        with col2:
            # 在编职称统计
            m_visual.draw_pie(data=json_data["在编"]["学校"][school_name][raw_period]["最高职称"], title="职称")

        # 在编学科统计
        m_visual.draw_2col_bar(data=json_data["在编"]["学校"][school_name][raw_period]["主教学科"], title="主教学科", end=100)

        col0, col1, col2 = st.columns([1, 1, 1])

        with col0:
            # 在编教资统计
            m_visual.draw_pie(data=json_data["在编"]["学校"][school_name][raw_period]["教师资格"], title="教师资格")

            # 在编支教地域统计
            m_visual.draw_pie(data=json_data["在编"]["学校"][school_name][raw_period]["支教地域"], title="支教地域")

        with col1:
            # 在编毕业院校统计
            m_visual.draw_1col_bar(data=json_data["在编"]["学校"][school_name][raw_period]["院校级别"], title="毕业院校")

            # 在编骨干教师统计
            m_visual.draw_pie(data=json_data["在编"]["学校"][school_name][raw_period]["骨干教师"], title="骨干教师")

        with col2:
            # 在编性别统计
            m_visual.draw_pie(data=json_data["在编"]["学校"][school_name][raw_period]["性别"], title="性别")

            # 在编三名工作室统计
            m_visual.draw_pie(data=json_data["在编"]["学校"][school_name][raw_period]["三名工作室"], title="三名统计")

# 展示编外数据
with st.container(border=True):
    if search_flag and kind_1_flag:
        # 更新数据
        json_data = m_visual.load_json_data(file_name="teacher_info")

        st.subheader(f"{school_name}{period}编外教师统计" if period is not None else f"{school_name}编外教师统计")

        st.info(f"编外总人数：{json_data["非编"]["学校"][school_name][raw_period]["总人数"]}")

        # st.write(json_data["非编"]["学校"][school_name][raw_period])

        col0, col1 = st.columns(spec=2)

        with col0:
            # 编外学历统计
            m_visual.draw_pie(data=json_data["非编"]["学校"][school_name][raw_period]["最高学历"], title="最高学历")

            # 编外教师资格统计
            m_visual.draw_pie(data=json_data["非编"]["学校"][school_name][raw_period]["教师资格"], title="教师资格")

        with col1:
            # 编外职称统计
            m_visual.draw_pie(data=json_data["非编"]["学校"][school_name][raw_period]["最高职称"], title="职称")

            # 编外骨干教师统计
            m_visual.draw_pie(data=json_data["非编"]["学校"][school_name][raw_period]["骨干教师"], title="骨干教师")

