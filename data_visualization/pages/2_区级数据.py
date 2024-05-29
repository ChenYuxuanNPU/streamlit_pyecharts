import sys
import streamlit as st

sys.path.append(
    r'C:\Users\1012986131\Desktop\python\streamlit_pyecharts'
)

from data_visualization.tool import module as m_visual


# 设置全局属性
m_visual.set_page_configuration()

# 读取现有json文件
json_data = m_visual.load_json_data()

# 标题
st.title("全区教师数据")

with st.expander("在编数据展示", expanded=True):

    # 根据选择的学段展示信息
    popover1 = st.popover("学段类别")
    all_period = popover1.checkbox("所有学段", True)
    senior_high_school = popover1.checkbox("高中", False)
    junior_high_school = popover1.checkbox("初中", False)
    primary_school = popover1.checkbox("小学", False)
    kindergarten = popover1.checkbox("幼儿园", False)

    if all_period:
        st.success("全区在编所有学段信息")

        with st.container(border=False):
            col0, col1, col2 = st.columns(spec=3)

            with col0:
                # 在编片区统计
                m_visual.draw_pie(data=json_data["在编"]["全区"]["所有学段"]["片区统计"], title="片区统计")

                # 在编学历统计
                m_visual.draw_pie(data=json_data["在编"]["全区"]["所有学段"]["最高学历"], title="最高学历")

            with col1:
                # 在编学段统计
                m_visual.draw_pie(data=json_data["在编"]["全区"]["所有学段"]["学段统计"], title="学段统计")

                # 在编职称统计
                m_visual.draw_pie(data=json_data["在编"]["全区"]["所有学段"]["最高职称"], title="职称")

            with col2:
                # 在编年龄统计
                m_visual.draw_pie(data=json_data["在编"]["全区"]["所有学段"]["年龄"], title="年龄")

                # 在编行政职务统计
                m_visual.draw_pie(data=json_data["在编"]["全区"]["所有学段"]["行政职务"], title="行政职务")

            # 学科统计占两列
            col0, col1 = st.columns([2, 1])

            with col0:
                # 在编学科统计
                m_visual.draw_2col_bar(data=json_data["在编"]["全区"]["所有学段"]["主教学科"], title="主教学科")

            with col1:
                # 在编毕业院校统计
                m_visual.draw_1col_bar(data=json_data["在编"]["全区"]["所有学段"]["院校级别"], title="毕业院校")

            col0, col1, col2 = st.columns(spec=3)

            with col0:
                # 在编骨干教师统计
                m_visual.draw_pie(data=json_data["在编"]["全区"]["所有学段"]["骨干教师"], title="骨干教师")

            with col1:
                # 在编教师支教统计
                m_visual.draw_pie(data=json_data["在编"]["全区"]["所有学段"]["支教地域"], title="支教地域")

            with col2:
                # 在编三名教师统计
                m_visual.draw_pie(data=json_data["在编"]["全区"]["所有学段"]["三名工作室"], title="三名统计")

            # 教师分布统计
            m_visual.draw_2col_bar(data=json_data["在编"]["全区"]["所有学段"]["教师分布"], title="教师分布", end=50)

    if senior_high_school:
        m_visual.show_period(period="高中", data=json_data)

    if junior_high_school:
        m_visual.show_period(period="初中", data=json_data)

    if primary_school:
        m_visual.show_period(period="小学", data=json_data)

    if kindergarten:
        m_visual.show_period(period="幼儿园", data=json_data)

# 非编数据
with st.expander("编外数据展示", expanded=True):

    st.success("编外所有学段教师信息")

    with st.container(border=False):

        col0, col1, col2 = st.columns(spec=3)

        with col0:

            # 非编片区统计
            m_visual.draw_pie(data=json_data["非编"]["全区"]["所有学段"]["片区统计"], title="片区统计")

            # 非编学段统计
            m_visual.draw_pie(data=json_data["非编"]["全区"]["所有学段"]["学段统计"], title="学段统计")

        with col1:
            # 非编学历统计
            m_visual.draw_pie(data=json_data["非编"]["全区"]["所有学段"]["最高学历"], title="最高学历")

            # 非编职称统计
            m_visual.draw_pie(data=json_data["非编"]["全区"]["所有学段"]["最高职称"], title="职称")

        with col2:
            # 非编骨干教师统计
            m_visual.draw_pie(data=json_data["非编"]["全区"]["所有学段"]["骨干教师"], title="骨干教师")

            # 非编三名教师统计
            m_visual.draw_pie(data=json_data["非编"]["全区"]["所有学段"]["三名工作室"], title="三名统计")

        # 教师分布统计
        m_visual.draw_2col_bar(data=json_data["非编"]["全区"]["所有学段"]["教师分布"], title="教师分布", end=50)

        col0, col1, col2 = st.columns(spec=3)

        with col0:

            # 非编教师资格统计
            m_visual.draw_pie(data=json_data["非编"]["全区"]["所有学段"]["教师资格"], title="教师资格")

        with col1:

            # 非编中小学教师资格统计
            m_visual.draw_pie(data=json_data["非编"]["全区"]["中小学"]["教师资格"], title="中小学")

        with col2:

            # 非编幼儿园教师资格统计
            m_visual.draw_pie(data=json_data["非编"]["全区"]["幼儿园"]["教师资格"], title="幼儿园")
