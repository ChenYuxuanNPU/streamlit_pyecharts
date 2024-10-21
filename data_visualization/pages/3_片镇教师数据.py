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
from data_visualization.render import page_3 as r

# 清空其他页暂用变量
visual_func.session_state_reset(page=3)

# 设置页面格式
visual_func.set_page_configuration(title="片镇教师数据", icon=":office:")


def get_year_list() -> list:
    return list(
        set(
            [
                data[0] for data in visual_func.load_json_data(folder="database", file_name="database_basic_info")["list_for_update_teacher_info"]
            ]
        )
    )


def get_area_list() -> list:
    return ["永平", "石井", "新市", "人和", "江高", "太和", "钟落潭"]


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
        year_1 = st.selectbox(
            label="请选择需要对比的年份",
            options=get_year_list(),
            index=None,
            placeholder="可选项"
        )

        area_1 = st.selectbox(
            label="想对比哪一个片镇的信息？",
            options=get_area_list(),
            index=None,
            placeholder="可选项"
        )

    # 查询某一年某片镇的教师信息
    if year_0 is not None and year_1 is None and area_0 is not None and area_1 is None:

        try:
            r.show_teacher_0(year=year_0, area=area_0)

        except KeyError as e:

            if e.args[0] == year_0:
                st.error(f"缺少{year_0}年的数据", icon="🤣")

            elif e.args[0] == "在编":
                st.error(f"缺少{year_0}年的在编数据", icon="😆")

            elif e.args[0] == "学校教师总数":
                st.error("缺少在编或编外信息", icon="😆")

            else:
                print(e)
                st.error(str(e), icon="😭")

        try:
            r.show_teacher_1(year=year_0, area=area_0)

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

    # 对比某一片镇不同年份的教师信息
    elif year_0 is not None and year_1 is not None and area_0 is not None and area_1 is None:
        st.info("对比某一片镇不同年份的教师信息")

    # 对比同一年份不同片镇的教师信息
    elif year_0 is not None and year_1 is None and area_0 is not None and area_1 is not None:
        st.info("对比同一年份不同片镇的教师信息")

    # 对比不同年份不同片镇的教师信息
    elif year_0 is not None and year_1 is not None and area_0 is not None and area_1 is not None:
        st.info("对比不同年份不同片镇的教师信息")

    else:
        st.error("?")

if (visual_func.count_empty_values(lst=[year_0, year_1, area_0, area_1]) >= 2 and not (
        year_0 is not None and area_0 is not None)
        or visual_func.count_empty_values(lst=[year_0, year_1, area_0, area_1]) == 1 and not (
                year_1 is None or area_1 is None)):
    r.show_text_info()
