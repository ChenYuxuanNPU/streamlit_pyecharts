import sys
from pathlib import Path

# 加入项目路径
sys.path.append(
    str(
        Path(__file__).resolve().parent.parent.parent
    )
)

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

left, mid, right = st.columns(spec=3)

with left:
    year = list(
        st.multiselect(
            label="请选择需要查询的年份",
            placeholder="必选项",
            options=get_year_list(kind="teacher_info"),
            default=[],
        )
    )
    st.write(st.session_state.page4_year_list)

with mid:
    school = list(
        st.multiselect(
            label="请输入需要查询的学校",
            options=get_school_list_by_year_list(year_list=year),
            placeholder="必选项",
        )
    )
    st.write(st.session_state.page4_school_list)

with right:
    period = st.selectbox(
        label="选择查询学段",
        placeholder="可选项",
        index=None,
        options=[item for item in get_period_list() if item != "幼儿园"],
    )
    st.write(st.session_state.page4_period)

_, middle, _ = st.columns([4, 1, 4])

with middle:
    st.button("查询学校信息", kwargs={"year_list": year, "school_list": school, "period": period},
              on_click=confirm_input)

# 不查询的时候展示学校云图
if not st.session_state.page4_info_kind:
    show_word_cloud()

elif st.session_state.page4_info_kind == "1":

    show_1_year_and_1_school(year=st.session_state.page4_year_list[0], school=st.session_state.page4_school_list[0],
                             period=st.session_state.page4_period)

elif st.session_state.page4_info_kind == "2.1":
    pass

elif st.session_state.page4_info_kind == "1.2":
    pass

else:
    show_word_cloud()
