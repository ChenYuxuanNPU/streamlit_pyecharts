import sys
from pathlib import Path

# 加入项目路径
sys.path.append(
    str(
        Path(__file__).resolve().parent.parent.parent
    )
)

from data_visualization.render.page_2 import *

# 清空其他页暂用变量
session_state_reset(page=2)

# 设置全局属性
set_page_configuration(title="区级教师数据", icon=":classical_building:")


def get_year_list() -> list:
    """
    获取教师信息年份列表并按照年份逆序排序（由后到前）
    :return:
    """

    return sorted(
        list(
            set(
                [data[0] for data in load_json_data(folder="database", file_name="database_basic_info")[
                    "list_for_update_teacher_info"]]
            )
        ),
        reverse=True
    )


# 标题
st.markdown(
    body="<h1 style='text-align: center;'>区级教师数据</h1>",
    unsafe_allow_html=True
)

st.divider()

year = sorted(
    st.multiselect(
        label="请选择需要查询的年份",
        # [year for year in year_list if year != year_0],
        options=get_year_list(),
        default=get_year_list()[0],
        placeholder="必选项"
    )
)

# 只是展示某一年的数据
if len(year) == 1:

    with st.container(border=True):

        try:
            show_1_year_teacher_0(year=year[0])

        except KeyError as e:

            if e.args[0] == year[0]:
                st.error(f"缺少{year[0]}年的数据", icon="🤣")

            elif e.args[0] == "在编":
                st.error(f"缺少{year[0]}年的在编数据", icon="😆")

            elif e.args[0] == "学校教师总数":
                st.error("缺少在编或编外信息", icon="😆")

            else:
                print(e)
                st.toast(str(e))

    st.divider()

    # 编外数据
    with st.container(border=True):

        try:
            show_1_year_teacher_1(year=year[0])

        except KeyError as e:

            if e.args[0] == year[0]:
                st.error(f"缺少{year[0]}年的数据", icon="🤣")

            elif e.args[0] == "编外":
                st.error(f"缺少{year[0]}年的编外数据", icon="😆")

            elif e.args[0] == "学校教师总数":
                st.error("缺少在编或编外信息", icon="😆")

            else:
                print(e)
                st.error(str(e), icon="😭")

# 展示对比数据
elif len(year) >= 2:

    show_multi_years_teacher_0(year_list=year)

else:
    st.toast("?")
