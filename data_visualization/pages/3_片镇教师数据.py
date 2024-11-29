import sys
from pathlib import Path

# 加入项目路径
sys.path.append(
    str(
        Path(__file__).resolve().parent.parent.parent
    )
)

from data_visualization.render.page_3 import *

# 清空其他页暂用变量
session_state_reset(page=3)

# 设置页面格式
set_page_configuration(title="片镇教师数据", icon=":office:")


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


def get_area_list() -> list:
    """
    获取片镇列表：["永平", "石井", "新市", "江高", "人和", "太和", "钟落潭"]
    :return:
    """

    return ["永平", "石井", "新市", "人和", "江高", "太和", "钟落潭"]


def get_area_order() -> dict:
    """
    片镇排序（直管为首位）
    :return:
    """

    return {"直管": 1, "永平": 2, "石井": 3, "新市": 4, "江高": 5, "人和": 6, "太和": 7, "钟落潭": 8, None: 9}


# 标题
st.markdown(
    "<h1 style='text-align: center;'>片镇教师数据</h1>",
    unsafe_allow_html=True
)

st.divider()

with st.container(border=True):
    col0, col1 = st.columns(spec=2)

    with col0:
        year_0 = st.selectbox(
            label="请选择需要查询的年份",
            options=get_year_list(),
            index=0,
        )

        area_0 = st.selectbox(
            label="想查询哪一个片镇的信息？",
            options=get_area_list(),
            index=None,
            placeholder="必选项"
        )

    with col1:
        year_1 = sorted(
            st.multiselect(
                label="请选择需要比较的年份",
                # [year for year in year_list if year != year_0],
                options=get_year_list(),
                default=[],
                placeholder="可选项"
            )
        )

        area_1 = sorted(
            st.multiselect(
                label="请选择需要比较的片镇",
                options=get_area_list(),
                default=[],
                placeholder="可选项"
            ),
            key=lambda x: get_area_order()[x]
        )

    # 查询某一年某片镇的教师信息
    if year_0 and area_0 and len(year_1) <= 1 and len(area_1) <= 1:

        show_1_year_and_1_area_teacher_0(year=year_0, area=area_0)

        show_1_year_and_1_area_teacher_1(year=year_0, area=area_0)

    # 对比不同年份不同片镇的教师信息
    elif len(year_1) > 1 and len(area_1) > 1:

        st.info("对比不同年份不同片镇的教师信息")

        show_multi_years_and_multi_areas_teacher_0(year_list=year_1)

    # 对比某一片镇不同年份的教师信息
    elif len(year_1) > 1 and area_0:

        show_multi_years_and_1_area_teacher_0(year_list=year_1, area=area_0)

    # 对比同一年份不同片镇的教师信息
    elif len(area_1) > 1 and year_0:

        st.info("对比同一年份不同片镇的教师信息")

        show_1_year_and_multi_areas_teacher_0(year=year_0, area_list=area_1)

    else:
        show_text_info()
