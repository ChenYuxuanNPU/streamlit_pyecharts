import sys
from pathlib import Path

# 加入项目路径
sys.path.append(
    str(
        Path(__file__).resolve().parent.parent.parent
    )
)

from data_visualization.render.page_1 import *

# 清空其他页暂用变量
session_state_reset(page=1)

# 设置全局属性
set_page_configuration(title="教育数字大屏", icon=":sparkler:")


def get_year_list() -> list:
    """
    获取学校信息年份列表并按照年份逆序排序（由后到前）
    :return:
    """

    return sorted(
        load_json_data(folder="database", file_name="database_basic_info")["list_for_update_school_info"],
        reverse=True
    )


st.markdown(
    body="<h1 style='text-align: center;'>学校信息总览</h1>",
    unsafe_allow_html=True
)

st.divider()

left, right = st.columns(spec=2)

with left:
    year_0 = st.selectbox(
        label="请选择需要查询的年份",
        options=get_year_list(),
        index=0,
    )

with right:
    year_1 = st.selectbox(
        label="请选择需要比较的年份",
        options=get_year_list(),
        index=None,
        placeholder="可选项"
    )

show_pie_chart_info(year=year_0)

show_summarized_info(year=year_0)

# 某学段展示

# 展示信息时
if st.session_state.page1_show_detail:

    show_period_detail_info(year=year_0)

# 不展示信息时
else:
    # 放一个展开信息的按钮
    show_detail_button()
