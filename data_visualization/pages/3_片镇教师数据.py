import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# 加入项目路径
sys.path.append(
    str(
        Path(__file__).resolve().parent.parent.parent
    )
)

from data_visualization.tool import func as visual_func


# 用于展示指导中心信息
def show_text_info() -> None:

    st.divider()

    # 展示宣传数据
    with st.container(border=True):
        st.markdown(
            "<h3 style='text-align: center;'>广州市白云区各教育指导中心相关信息</h3>",
            unsafe_allow_html=True
        )

        visual_func.draw_dataframe(
            data=pd.DataFrame(
                [
                    ["永平教育指导中心", "白云大道北1689号（岭南新世界花园内）",
                     "永平街、京溪街、同和街、嘉禾街、均禾街、鹤龙街", "62189335"],
                    ["石井教育指导中心", "白云区石井石沙路1682号（石井中学旁）",
                     "同德街、石井街、白云湖街、石门街、松州街、金沙街", "36533012-614"],
                    ["新市教育指导中心", "三元里大道棠安路新市中学东侧教师楼101",
                     "景泰街、三元里街、新市街、云城街、棠景街、黄石街", "86307817"],
                    ["人和教育指导中心", "白云区人和镇鹤龙六路18号", "人和镇", "36042235"],
                    ["江高教育指导中心", "白云区江高镇爱国东路61号", "江高镇", "86604940/86203661"],
                    ["太和教育指导中心", "白云区太和镇政府内", "太和镇", "37312198"],
                    ["钟落潭教育指导中心", "白云区钟落潭镇福龙路88号", "钟落潭镇", "87403000"],
                ],
                columns=["教育指导中心", "地址", "服务范围", "联系方式"]
            ),
            height=350
        )


def show_teacher_0(year: str, area: str, data: dict) -> None:

    st.success(f"{area}在编总人数：{data[year]["在编"]["片区"][area]["所有学段"]["总人数"]}", icon="😋")

    with st.container(border=False):
        c0, c1, c2 = st.columns(spec=3)

        with c0:
            # 在编年龄统计
            visual_func.draw_pie(data=data[year]["在编"]["片区"][area]["所有学段"]["年龄"],
                                 title="年龄", pos_left="15%", center_to_bottom="64%")

            # 在编学段统计
            visual_func.draw_pie(data=data[year]["在编"]["片区"][area]["所有学段"]["学段统计"],
                                 title="学段统计")

        with c1:
            # 在编学历统计
            visual_func.draw_pie(data=data[year]["在编"]["片区"][area]["所有学段"]["最高学历"],
                                 title="最高学历")

            # 在编毕业院校统计
            visual_func.draw_bar(data=data[year]["在编"]["片区"][area]["所有学段"]["院校级别"],
                                 title="毕业院校", is_show_visual_map=False)

        with c2:
            # 在编职称统计
            visual_func.draw_pie(data=data[year]["在编"]["片区"][area]["所有学段"]["最高职称"],
                                 title="职称")

            # 在编行政职务统计
            visual_func.draw_pie(data=data[year]["在编"]["片区"][area]["所有学段"]["行政职务"],
                                 title="行政职务")

        # 在编学科统计
        visual_func.draw_bar(data=data[year]["在编"]["片区"][area]["所有学段"]["主教学科"],
                             title="主教学科", is_show_visual_map=False)

        c0, c1, c2 = st.columns(spec=3)  # 不能删，这里删了会影响上下层顺序

        with c0:
            # 在编骨干教师统计
            visual_func.draw_pie(data=data[year]["在编"]["片区"][area]["所有学段"]["骨干教师"],
                                 title="骨干教师")

        with c1:
            # 在编教师支教统计
            visual_func.draw_pie(data=data[year]["在编"]["片区"][area]["所有学段"]["支教地域"],
                                 title="支教地域")

        with c2:
            # 在编四名教师统计
            visual_func.draw_pie(data=data[year]["在编"]["片区"][area]["所有学段"]["四名工作室"],
                                 title="四名统计")


def show_teacher_1(year: str, area: str, data: dict) -> None:

    st.success(f"{area}编外总人数：{data[year]["编外"]["片区"][area]["所有学段"]["总人数"]}", icon="😋")

    with st.container(border=False):
        c0, c1, c2 = st.columns(spec=3)

        with c0:
            # 编外学段统计
            visual_func.draw_pie(data=data[year]["编外"]["片区"][area]["所有学段"]["学段统计"],
                                 title="学段统计")

            # 编外教师资格统计
            visual_func.draw_pie(data=data[year]["编外"]["片区"][area]["所有学段"]["教师资格"],
                                 title="教师资格")

        with c1:
            # 编外学历统计
            visual_func.draw_pie(data=data[year]["编外"]["片区"][area]["所有学段"]["最高学历"],
                                 title="最高学历")

            # 编外中小学教师资格统计
            visual_func.draw_pie(data=data[year]["编外"]["片区"][area]["中小学"]["教师资格"],
                                 title="中小学")

        with c2:
            # 编外职称统计
            visual_func.draw_pie(data=data[year]["编外"]["片区"][area]["所有学段"]["最高职称"],
                                 title="职称")

            # 编外幼儿园教师资格统计
            visual_func.draw_pie(data=data[year]["编外"]["片区"][area]["幼儿园"]["教师资格"],
                                 title="幼儿园")


# 初始化全局变量
visual_func.session_state_initial()

# 清空其他页暂用变量
visual_func.session_state_reset(page=3)

# 设置页面格式
visual_func.set_page_configuration(title="片镇教师数据", icon=":office:")

# 读取现有json文件
json_data = visual_func.load_json_data(folder="result", file_name="teacher_info")

year_list = set([data[0] for data in visual_func.load_json_data(folder="database", file_name="database_basic_info")["list_for_update_teacher_info"]])

# 标题
st.markdown(
    "<h1 style='text-align: center;'>片镇教师数据</h1>",
    unsafe_allow_html=True
)

st.divider()

with st.container(border=True):

    col0, col1 = st.columns(spec=2)

    with col0:
        year0 = st.selectbox(
            "请选择需要查询的年份",
            year_list,
            index=0,
        )

        area0 = st.selectbox(
            "想查询哪一个片镇的信息？",
            ("永平", "石井", "新市", "人和", "江高", "太和", "钟落潭"),
            index=None,
            placeholder=""
        )

        st.button("点我")

    with col1:
        year1 = st.selectbox(
            "请选择需要对比的年份",
            [year for year in year_list if year != year0],
            index=None,
            placeholder=""
        )

        area1 = st.selectbox(
            "想对比哪一个片镇的信息？",
            [area for area in ["永平", "石井", "新市", "人和", "江高", "太和", "钟落潭"] if area != area0],
            index=None,
            placeholder=""
        )

        st.button("点我1")

    if area0 is not None and year0 is not None:

        try:
            show_teacher_0(year=year0, area=area0, data=json_data)

        except KeyError as e:

            if e.args[0] == year0:
                st.error(f"json文件缺少{year0}年的数据", icon="🤣")

            elif e.args[0] == "在编":
                st.error(f"json文件缺少{year0}年的在编数据", icon="😆")

        try:
            show_teacher_1(year=year0, area=area0, data=json_data)

        except KeyError as e:

            if e.args[0] == year0:
                st.error(f"json文件缺少{year0}年的数据", icon="🤣")

            elif e.args[0] == "编外":
                st.error(f"json文件缺少{year0}年的编外数据", icon="😆")


if area0 is None or year0 is None:

    show_text_info()
