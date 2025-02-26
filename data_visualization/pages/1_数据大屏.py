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

display_centered_title(title="学校信息总览", font_size=1)

st.divider()

year = st.multiselect(
    label="请选择需要查询的年份",
    placeholder="必选项",
    options=get_year_list(kind="school_info"),
    default=[get_year_list(kind="school_info")[0]],
)

if len(list(year)) == 0:
    st.info("111")

elif len(list(year)) == 1:
    show_pie_chart_info(year=year[0])

    show_summarized_info(year=year[0])

else:
    show_multi_years_info(year_list=year)
