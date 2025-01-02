import sys
from pathlib import Path

# 加入项目路径
sys.path.append(
    str(
        Path(__file__).resolve().parent.parent.parent
    )
)

from data_visualization.tool.func import *
from data_visualization.render.page_4 import *

# 清空其他页暂用变量
session_state_reset(page=4)

# 设置全局属性
set_page_configuration(title="学校教师数据", icon=":house_with_garden:")


# 标题
st.markdown(
    "<h1 style='text-align: center;'>学校教师数据</h1>",
    unsafe_allow_html=True
)

st.divider()

left, right = st.columns(spec=2)

with left:
    year_0 = st.selectbox(
        label="请选择需要查询的年份",
        options=get_year_list(kind="teacher_info"),
        index=0,
        on_change=reset_self,
        args=[4]
    )

    school_name_0 = st.selectbox(
        label="请输入需要查询的学校",
        options=load_json_data(folder="result", file_name="teacher_info")[year_0]["学校教师总数"].keys(),
        index=None,
        placeholder="必选项",
        on_change=reset_self,
        args=[4]
    )

    period_0 = st.selectbox(
        label="选择查询学段",
        options=[item for item in ["所有学段"] + get_period_list() if item != "幼儿园"],
        on_change=reset_self,
        args=[4]
    )

with right:
    year_1 = st.selectbox(
        label="请选择需要对比的年份",
        options=get_year_list(kind="teacher_info"),
        index=None,
        placeholder="可选项",
        on_change=reset_self,
        args=[4]
    )

    school_name_1 = st.selectbox(
        label="请输入需要对比的学校",
        options=load_json_data(folder="result", file_name="teacher_info")[year_0]["学校教师总数"].keys(),
        index=None,
        placeholder="可选项",
        on_change=reset_self,
        args=[4]
    )

    period_1 = st.selectbox(
        label="选择对比学段",
        options=[item for item in ["所有学段"] + get_period_list() if item != "幼儿园"],
        index=None,
        placeholder="可选项",
        on_change=reset_self,
        args=[4]
    )

left, middle, right = st.columns([4, 1, 4])

with middle:
    st.button("查询学校信息", args=[[year_0, year_1, school_name_0, school_name_1, period_0, period_1]],
              on_click=confirm_input)

# 不查询的时候展示学校云图
if not st.session_state.page4_search_flag:
    show_word_cloud(year=year_0)

if st.session_state.page4_search_flag:
    with st.container(border=True):
        show_school_stream(school_name=school_name_0, year=year_0)

# 展示某一年在编数据
if st.session_state.page4_search_flag and st.session_state.page4_kind_0_flag:
    with st.container(border=True):
        show_teacher_0(year=year_0, school_name=school_name_0, period=period_0)

if st.session_state.page4_kind_0_flag and st.session_state.page4_kind_1_flag:
    st.divider()

# 展示某一年编外数据
if st.session_state.page4_search_flag and st.session_state.page4_kind_1_flag:
    with st.container(border=True):
        show_teacher_1(year=year_0, school_name=school_name_0, period=period_0)
