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


def get_period_list() -> list:
    """
    需要统计的学段列表\n
    返回：["初中", "小学", "幼儿园"]
    :return:
    """
    return ["初中", "小学", "幼儿园"]


def get_period_order() -> dict:
    """
    学段排序
    :return:
    """
    return {"初中": 1, "小学": 2, "幼儿园": 3, "None": 4}


# 标题
st.markdown(
    "<h1 style='text-align: center;'>片镇教师数据</h1>",
    unsafe_allow_html=True
)

st.divider()

with st.container(border=True):
    st.warning("年份和片镇均为必选多选项，且不能同时多选；学段为可选单选项，不选择时则显示所有学段信息")

    col0, col1, col2 = st.columns(spec=3)

    with col0:
        year = sorted(
            st.multiselect(
                label="请选择需要查询的年份",
                # [year for year in year_list if year != year_0],
                options=get_year_list(),
                default=[],
                placeholder="必选项",
                # on_change=page3_hide_info,
            )
        )

    with col1:
        area = sorted(
            st.multiselect(
                label="请选择需要查询的片镇",
                options=get_area_list(),
                default=[],
                placeholder="必选项",
                # on_change=page3_hide_info,
            ),
            key=lambda x: get_area_order()[x]
        )

    with col2:
        period = st.selectbox(
            label="请选择需要查询的学段",
            options=get_period_list(),
            index=None,
            placeholder="可选项"
        )

    _, mid, _ = st.columns([4, 1, 4])

    with mid:
        st.button("查询信息", on_click=page3_show_info, args=[year, len(list(year)), area, len(list(area)), period])

if st.session_state.page3_search_flag:
    # 查询某一年某片镇的教师信息
    if st.session_state.page3_year_length == 1 and st.session_state.page3_area_length == 1:

        show_1_year_and_1_area_teacher_0(year=st.session_state.page3_year_list[0],
                                         area=st.session_state.page3_area_list[0], period=st.session_state.page3_period)

        if st.session_state.page3_period is None:
            show_1_year_and_1_area_teacher_1(year=st.session_state.page3_year_list[0],
                                             area=st.session_state.page3_area_list[0],
                                             period=st.session_state.page3_period)

    # 对比某一片镇不同年份的教师信息
    elif st.session_state.page3_year_length > 1 and st.session_state.page3_area_length == 1:

        show_multi_years_and_1_area_teacher_0(year_list=st.session_state.page3_year_list,
                                              area=st.session_state.page3_area_list[0],
                                              period=st.session_state.page3_period)

    # 对比同一年份不同片镇的教师信息
    elif st.session_state.page3_year_length == 1 and st.session_state.page3_area_length > 1:

        st.info("对比同一年份不同片镇的教师信息")

        show_1_year_and_multi_areas_teacher_0(year=st.session_state.page3_year_list[0],
                                              area_list=st.session_state.page3_area_list,
                                              period=st.session_state.page3_period)

    elif st.session_state.page3_year_length == 0 or st.session_state.page3_area_length == 0:

        if st.session_state.page3_year_length == 0:
            st.toast("需要选择查询年份", icon="🥱")

        if st.session_state.page3_area_length == 0:
            st.toast("需要选择查询片镇", icon="🥱")

        show_text_info()

    else:
        st.error("???")
        show_text_info()

else:
    show_text_info()
