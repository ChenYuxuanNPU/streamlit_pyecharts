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
from data_visualization.render import page_1 as r

# 清空其他页暂用变量
visual_func.session_state_reset(page=1)

# 设置全局属性
visual_func.set_page_configuration(title="教育数字大屏", icon=":sparkler:")


def get_year_list() -> list:
    return visual_func.load_json_data(folder="database", file_name="database_basic_info")["list_for_update_school_info"]


st.markdown(
    body="<h1 style='text-align: center;'>学校信息总览</h1>",
    unsafe_allow_html=True
)

st.divider()

left, right = st.columns(spec=2)

with left:
    year_0 = st.selectbox(
        label="请选择需要查询的年份",
        options=sorted(get_year_list(), reverse=True),
        index=0,
    )

with right:
    year_1 = st.selectbox(
        label="请选择需要比较的年份",
        options=sorted(get_year_list(), reverse=True),
        index=None,
        placeholder="可选项"
    )

r.show_pie_chart_info(year=year_0)

r.show_summarized_info(year=year_0)

# 某学段展示

# 展示信息时
if st.session_state.page1_show_detail:

    r.show_period_detail_info(year=year_0)

# 不展示信息时
else:
    # 放一个展开信息的按钮
    r.show_detail_button()
