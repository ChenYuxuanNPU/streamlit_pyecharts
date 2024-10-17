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

# 初始化全局变量
# visual_func.session_state_initial()

# 清空其他页暂用变量
visual_func.session_state_reset(page=2)

# 设置全局属性
visual_func.set_page_configuration(title="区级教师数据", icon=":classical_building:")


# 这里是给片区不同学段的可视化做的，在编信息
def show_1_year_given_period(year: str, period: str) -> None:
    data = visual_func.load_json_data(folder="result", file_name="teacher_info")

    st.info(f"在编{period}信息", icon="😋")

    with st.container(border=False):
        c0, c1 = st.columns([2, 1])

        with c0:
            visual_func.draw_bar_chart(data=data[year]["在编"]["全区"][period]["主教学科"], title="主教学科",
                                       end=visual_func.end_dict[period])

        with c1:
            visual_func.draw_pie_chart(data=data[year]["在编"]["全区"][period]["年龄"], title="年龄", pos_left="15%",
                                       center_to_bottom="64%")

        c0, c1, c2 = st.columns(spec=3)

        with c0:
            visual_func.draw_pie_chart(data=data[year]["在编"]["全区"][period]["最高学历"], title="最高学历")

        with c1:
            visual_func.draw_bar_chart(data=data[year]["在编"]["全区"][period]["院校级别"], title="毕业院校",
                                       is_show_visual_map=False)

        with c2:
            visual_func.draw_pie_chart(data=data[year]["在编"]["全区"][period]["最高职称"], title="职称")


# 展示某一学年所有学段在编教师数据
def show_1_year_all_period(year: str):
    data = visual_func.load_json_data(folder="result", file_name="teacher_info")

    st.success(f"在编教职工总人数：{data[year]['在编']['全区']['所有学段']['总人数']}")

    with st.container(border=False):
        c0, c1, c2 = st.columns(spec=3)

        with c0:
            # 在编片区统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["片区统计"], title="片区统计")

            # 在编学历统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["最高学历"], title="最高学历")

        with c1:
            # 在编学段统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["学段统计"], title="学段统计")

            # 在编职称统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["最高职称"], title="职称")

        with c2:
            # 在编年龄统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["年龄"], title="年龄", pos_left="15%",
                                       center_to_bottom="64%")

            # 在编行政职务统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["行政职务"], title="行政职务",
                                       center_to_bottom="68%")

        # 学科统计占两列
        c0, c1 = st.columns([2, 1])

        with c0:
            # 在编学科统计
            visual_func.draw_bar_chart(data=data[year]["在编"]["全区"]["所有学段"]["主教学科"], title="主教学科",
                                       end=70)

        with c1:
            # 在编毕业院校统计
            visual_func.draw_bar_chart(data=data[year]["在编"]["全区"]["所有学段"]["院校级别"], title="毕业院校",
                                       is_show_visual_map=False)

        c0, c1, c2 = st.columns(spec=3)

        with c0:
            # 在编骨干教师统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["骨干教师"], title="骨干教师")

        with c1:
            # 在编教师支教统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["支教地域"], title="支教地域")

        with c2:
            # 在编四名教师统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["四名工作室"], title="四名统计")

        # 教师分布前三十统计
        visual_func.draw_bar_chart(data=data[year]["在编"]["全区"]["所有学段"]["教师分布前三十"], title="最多教师数", end=100)

        # 在编教师数后三十的学校统计
        visual_func.draw_bar_chart(data=data[year]["在编"]["全区"]["所有学段"]["教师分布后三十"], title="最少教师数", end=100)


def show_1_year_teacher_0(year: str, ):
    data = visual_func.load_json_data(folder="result", file_name="teacher_info")

    # 小标题
    st.markdown(
        body="<h2 style='text-align: center;'>在编教师数据</h2>",
        unsafe_allow_html=True
    )

    period_list = st.multiselect(
        label="请选择需要查询的学段",
        options=["所有学段", "高中", "初中", "小学", "幼儿园"],
        default=["所有学段", "高中"]
    )

    if "所有学段" in period_list:
        show_1_year_all_period(year=year)

    if "高中" in period_list:
        show_1_year_given_period(year=year, period="高中")

    if "初中" in period_list:
        show_1_year_given_period(year=year, period="初中")

    if "小学" in period_list:
        show_1_year_given_period(year=year, period="小学")

    if "幼儿园" in period_list:
        show_1_year_given_period(year=year, period="幼儿园")


def show_1_year_teacher_1(year: str):
    data = visual_func.load_json_data(folder="result", file_name="teacher_info")

    # 小标题
    st.markdown(
        body="<h2 style='text-align: center;'>编外教师数据</h2>",
        unsafe_allow_html=True
    )

    st.info(f"编外教职工总人数：{data[year]['编外']['全区']['所有学段']['总人数']}")

    c0, c1, c2 = st.columns(spec=3)

    with c0:
        # 编外片区统计
        visual_func.draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["片区统计"], title="片区统计")

        # 编外学段统计
        visual_func.draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["学段统计"], title="学段统计")

    with c1:
        # 编外学历统计
        visual_func.draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["最高学历"], title="最高学历")

        # 编外职称统计
        visual_func.draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["最高职称"], title="职称")

    with c2:
        # 编外骨干教师统计
        visual_func.draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["骨干教师"], title="骨干教师")

        # 编外四名教师统计
        visual_func.draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["四名工作室"], title="四名统计")

    # 教师分布统计
    visual_func.draw_bar_chart(data=data[year]["编外"]["全区"]["所有学段"]["教师分布前三十"], title="最多教师数", end=100)

    c0, c1, c2 = st.columns(spec=3)

    with c0:
        # 编外教师资格统计
        visual_func.draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["教师资格"], title="教师资格")

    with c1:
        # 编外中小学教师资格统计
        visual_func.draw_pie_chart(data=data[year]["编外"]["全区"]["中小学"]["教师资格"], title="中小学")

    with c2:
        # 编外幼儿园教师资格统计
        visual_func.draw_pie_chart(data=data[year]["编外"]["全区"]["幼儿园"]["教师资格"], title="幼儿园")


def show_multi_years_teacher_0(year_list: list) -> None:
    data = visual_func.load_json_data(folder="result", file_name="teacher_info")

    with st.container(border=True):
        # 小标题
        st.markdown(
            body="<h2 style='text-align: center;'>年份对比</h2>",
            unsafe_allow_html=True
        )
        st.divider()

        st.info("教师数随年份变化情况")
        r.show_multi_years_teacher_0_area(year_list=year_list)

        st.info("学段人数随年份变化情况")
        r.show_multi_years_teacher_0_period(year_list=year_list)

        st.info("学历水平随年份变化情况")
        r.show_multi_years_teacher_0_edu_bg(year_list=year_list)

        st.info("专技职称随年份变化情况")
        r.show_multi_years_teacher_0_vocational_level(year_list=year_list)

        st.info("学科教师数随年份变化情况")
        r.show_multi_years_teacher_0_discipline(year_list=year_list)


year_list = set([data[0] for data in visual_func.load_json_data(folder="database", file_name="database_basic_info")[
    "list_for_update_teacher_info"]])

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
        options=year_list,
        index=0,
    )

with col1:
    year_1 = sorted(
        st.multiselect(
            label="请选择需要比较的年份",
            # [year for year in year_list if year != year_0],
            options=year_list,
            default=[],
            placeholder="可选项"
        )
    )

# 只是展示某一年的数据
if year_0 is not None and len(year_1) < 2:

    with st.container(border=True):

        try:
            show_1_year_teacher_0(year=year_0)

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
            show_1_year_teacher_1(year=year_0)

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

    show_multi_years_teacher_0(year_list=year_1)

else:
    st.toast("?")
