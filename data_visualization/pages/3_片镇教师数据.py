import sys
import streamlit as st

sys.path.append(
    r'C:\Users\1012986131\Desktop\python\streamlit_pyecharts'
)

from data_visualization.tool import module as m_visual


# 设置页面格式
m_visual.set_page_configuration(title="片镇教师数据", icon=":office:")

# 读取现有json文件
json_data = m_visual.load_json_data(file_name="output")

# 标题
st.title("各片镇教师数据")

with st.container(border=True):
    area = st.selectbox(
        "想查询哪一个片镇的信息？",
        ("永平", "石井", "新市", "人和", "江高", "太和", "钟落潭"),
        index=None,
        placeholder="单击选择区域",
    )

    if area is not None:
        st.success(f"{area}在编所有学段信息")

        with st.container(border=False):
            col0, col1, col2 = st.columns(spec=3)

            with col0:
                # 在编年龄统计
                m_visual.draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["年龄"], title="年龄")

                # 在编学段统计
                m_visual.draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["学段统计"], title="学段统计")

            with col1:
                # 在编学历统计
                m_visual.draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["最高学历"], title="最高学历")

                # 在编毕业院校统计
                m_visual.draw_1col_bar(data=json_data["在编"]["片区"][area]["所有学段"]["院校级别"], title="毕业院校")

            with col2:
                # 在编职称统计
                m_visual.draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["最高职称"], title="职称")

                # 在编行政职务统计
                m_visual.draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["行政职务"], title="行政职务")

            # 在编学科统计
            m_visual.draw_1col_bar(data=json_data["在编"]["片区"][area]["所有学段"]["主教学科"], title="主教学科")

            # 在编教师数少的学校统计
            temp_all = sorted(list(json_data["学校教师总数"].items()), key=lambda x: (x[1][3], x[1][5]))
            temp = []
            temp_for_bar = {}

            for item in temp_all:
                if item[1][2] == area and item[1][3] != 0 and item[1][1] != "幼儿园" and item[1][1] != "教育辅助单位":
                    temp.append(item)

            for i in range(0, min(15, len(temp))):
                temp_for_bar[temp[i][0]] = temp[i][1][3]

            m_visual.draw_1col_bar(data=m_visual.simplify_school_name(temp_for_bar), title="在编教师数较少的学校")

            # 统计完在编教师数少的学校了

            col0, col1, col2 = st.columns(spec=3)

            with col0:
                # 在编骨干教师统计
                m_visual.draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["骨干教师"], title="骨干教师")

            with col1:
                # 在编教师支教统计
                m_visual.draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["支教地域"], title="支教地域")

            with col2:
                # 在编三名教师统计
                m_visual.draw_pie(data=json_data["在编"]["片区"][area]["所有学段"]["三名工作室"], title="三名统计")

        st.success("编外所有学段教师信息")

        with st.container(border=False):
            col0, col1, col2 = st.columns(spec=3)

            with col0:
                # 非编学段统计
                m_visual.draw_pie(data=json_data["非编"]["片区"][area]["所有学段"]["学段统计"], title="学段统计")

                # 非编教师资格统计
                m_visual.draw_pie(data=json_data["非编"]["片区"][area]["所有学段"]["教师资格"], title="教师资格")

            with col1:
                # 非编学历统计
                m_visual.draw_pie(data=json_data["非编"]["片区"][area]["所有学段"]["最高学历"], title="最高学历")

                # 非编中小学教师资格统计
                m_visual.draw_pie(data=json_data["非编"]["片区"][area]["中小学"]["教师资格"], title="中小学")

            with col2:
                # 非编职称统计
                m_visual.draw_pie(data=json_data["非编"]["片区"][area]["所有学段"]["最高职称"], title="职称")

                # 非编幼儿园教师资格统计
                m_visual.draw_pie(data=json_data["非编"]["片区"][area]["幼儿园"]["教师资格"], title="幼儿园")
