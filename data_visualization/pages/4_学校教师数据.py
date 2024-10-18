import sys
from pathlib import Path

import streamlit as st

# 加入项目路径
sys.path.append(
    str(
        Path(__file__).resolve().parent.parent.parent
    )
)

from data_visualization.tool import func as visual_func
from data_visualization.render import page_4 as r

# 清空其他页暂用变量
visual_func.session_state_reset(page=4)

# 设置全局属性
visual_func.set_page_configuration(title="学校教师数据", icon=":house_with_garden:")


# 这里要加一个返回值，判断查询的信息属于什么类型
def confirm_input(param_list: list):
    # [year_0, year_1, school_name_0, school_name_1, period_0, period_1]
    print(f"4_学校教师数据--页面控件参数列表： {param_list}")

    # 这里要判断是否只查询某一所学校
    r.set_flags_and_update_school_data(school_name=param_list[2], year=param_list[0], period=param_list[4])


# 读取现有json文件
json_data = visual_func.load_json_data(folder="result", file_name="teacher_info")

# 获取查询的年份列表
year_list = set([data[0] for data in visual_func.load_json_data(folder="database", file_name="database_basic_info")[
    "list_for_update_teacher_info"]])

# 标题
st.markdown(
    "<h1 style='text-align: center;'>学校教师数据</h1>",
    unsafe_allow_html=True
)

st.divider()

left, right = st.columns(spec=2)

with left:
    year_0 = st.selectbox(
        "请选择需要查询的年份",
        year_list,
        index=1,
        on_change=visual_func.reset_self,
        args=[4]
    )

    school_name_0 = st.selectbox(
        "请输入需要查询的学校",
        json_data[year_0]["学校教师总数"].keys(),
        index=None,
        placeholder="必选项",
        on_change=visual_func.reset_self,
        args=[4]
    )

    period_0 = st.selectbox(
        "选择查询学段1",
        ("所有学段", "高中", "初中", "小学"),
        on_change=visual_func.reset_self,
        args=[4]
    )

with right:
    year_1 = st.selectbox(
        "请选择需要对比的年份",
        [year for year in year_list if year != year_0],
        index=None,
        placeholder="可选项",
        on_change=visual_func.reset_self,
        args=[4]
    )

    school_name_1 = st.selectbox(
        "请输入需要对比的学校",
        json_data[year_0]["学校教师总数"].keys(),
        index=None,
        placeholder="可选项",
        on_change=visual_func.reset_self,
        args=[4]
    )

    period_1 = st.selectbox(
        "选择对比学段",
        ("所有学段", "高中", "初中", "小学"),
        index=None,
        placeholder="可选项",
        on_change=visual_func.reset_self,
        args=[4]
    )

left, middle, right = st.columns([4, 1, 4])

with middle:
    st.button("查询学校信息", args=[[year_0, year_1, school_name_0, school_name_1, period_0, period_1]],
              on_click=confirm_input)

# 不查询的时候展示学校云图
if not st.session_state.page4_search_flag:
    r.show_word_cloud(year=year_0, data=json_data)

if st.session_state.page4_search_flag:
    with st.container(border=True):
        r.show_school_stream(school_name=school_name_0, year=year_0, period=period_0, )

# 展示某一年在编数据
if st.session_state.page4_search_flag and st.session_state.page4_kind_0_flag:
    with st.container(border=True):
        r.show_teacher_0(year=year_0, school_name=school_name_0, period=period_0)

if st.session_state.page4_kind_0_flag and st.session_state.page4_kind_1_flag:
    st.divider()

# 展示某一年编外数据
if st.session_state.page4_search_flag and st.session_state.page4_kind_1_flag:
    with st.container(border=True):
        r.show_teacher_1(year=year_0, school_name=school_name_0, period=period_0)
