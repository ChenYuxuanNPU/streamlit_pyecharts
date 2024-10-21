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
from data_visualization.render import page_2 as r

# 清空其他页暂用变量
visual_func.session_state_reset(page=2)

# 设置全局属性
visual_func.set_page_configuration(title="区级教师数据", icon=":classical_building:")


def get_year_list() -> list:
    return list(
        set(
            [data[0] for data in visual_func.load_json_data(folder="database", file_name="database_basic_info")["list_for_update_teacher_info"]]
        )
    )


# 标题
st.markdown(
    body="<h1 style='text-align: center;'>区级教师数据</h1>",
    unsafe_allow_html=True
)

st.divider()

col0, col1 = st.columns(spec=2)
with col0:
    year_0 = st.selectbox(
        label="请选择需要查询的年份",
        options=sorted(get_year_list(), reverse=True),
        index=0,
    )

with col1:
    year_1 = sorted(
        st.multiselect(
            label="请选择需要比较的年份",
            # [year for year in year_list if year != year_0],
            options=sorted(get_year_list(), reverse=True),
            default=[],
            placeholder="可选项"
        )
    )

# 只是展示某一年的数据
if year_0 is not None and len(year_1) < 2:

    with st.container(border=True):

        try:
            r.show_1_year_teacher_0(year=year_0)

        except KeyError as e:

            if e.args[0] == year_0:
                st.error(f"缺少{year_0}年的数据", icon="🤣")

            elif e.args[0] == "在编":
                st.error(f"缺少{year_0}年的在编数据", icon="😆")

            elif e.args[0] == "学校教师总数":
                st.error("缺少在编或编外信息", icon="😆")

            else:
                print(e)
                st.toast(str(e))

    st.divider()

    # 编外数据
    with st.container(border=True):

        try:
            r.show_1_year_teacher_1(year=year_0)

        except KeyError as e:

            if e.args[0] == year_0:
                st.error(f"缺少{year_0}年的数据", icon="🤣")

            elif e.args[0] == "编外":
                st.error(f"缺少{year_0}年的编外数据", icon="😆")

            elif e.args[0] == "学校教师总数":
                st.error("缺少在编或编外信息", icon="😆")

            else:
                print(e)
                st.error(str(e), icon="😭")

# 展示对比数据
elif year_0 is not None and len(year_1) >= 2:

    r.show_multi_years_teacher_0(year_list=year_1)

else:
    st.toast("?")
