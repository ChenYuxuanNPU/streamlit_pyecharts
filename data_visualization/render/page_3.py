import pandas as pd
import streamlit as st

from data_visualization.tool import func as visual_func


def get_base_data() -> dict:
    return visual_func.load_json_data(folder="result", file_name="teacher_info")


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
                     "永平街道、京溪街道、同和街道、嘉禾街道、均禾街道、鹤龙街道", "62189335"],
                    ["石井教育指导中心", "白云区石井石沙路1682号（石井中学旁）",
                     "同德街道、石井街道、白云湖街道、石门街道、松洲街道、金沙街道", "36533012-614"],
                    ["新市教育指导中心", "三元里大道棠安路新市中学东侧教师楼101",
                     "景泰街道、三元里街道、新市街道、云城街道、棠景街道、黄石街道", "86307817"],
                    ["人和教育指导中心", "白云区人和镇鹤龙六路18号", "人和镇", "36042235"],
                    ["江高教育指导中心", "白云区江高镇爱国东路61号", "江高镇", "86604940/86203661"],
                    ["太和教育指导中心", "白云区太和镇政府内", "太和镇、大源街道、龙归街道", "37312198"],
                    ["钟落潭教育指导中心", "白云区钟落潭镇福龙路88号", "钟落潭镇", "87403000"],
                ],
                columns=["教育指导中心", "地址", "服务范围", "联系方式"]
            ),
            height=350
        )


def show_teacher_0(year: str, area: str) -> None:
    data = get_base_data()

    st.success(f"{area}在编总人数：{data[year]["在编"]["片区"][area]["所有学段"]["总人数"]}", icon="😋")

    with st.container(border=False):
        c0, c1, c2 = st.columns(spec=3)

        with c0:
            # 在编年龄统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["年龄"],
                                       title="年龄", pos_left="15%", center_to_bottom="64%")

            # 在编学段统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["学段统计"],
                                       title="学段统计")

        with c1:
            # 在编学历统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["最高学历"],
                                       title="最高学历")

            # 在编毕业院校统计
            visual_func.draw_bar_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["院校级别"],
                                       title="毕业院校", is_show_visual_map=False)

        with c2:
            # 在编职称统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["最高职称"],
                                       title="职称")

            # 在编行政职务统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["行政职务"],
                                       title="行政职务")

        # 在编学科统计
        visual_func.draw_bar_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["主教学科"],
                                   title="主教学科", is_show_visual_map=False)

        c0, c1, c2 = st.columns(spec=3)  # 不能删，这里删了会影响上下层顺序

        with c0:
            # 在编骨干教师统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["骨干教师"],
                                       title="骨干教师")

        with c1:
            # 在编教师支教统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["支教地域"],
                                       title="支教地域")

        with c2:
            # 在编四名教师统计
            visual_func.draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["四名工作室"],
                                       title="四名统计")


def show_teacher_1(year: str, area: str) -> None:
    data = get_base_data()

    st.success(f"{area}编外总人数：{data[year]["编外"]["片区"][area]["所有学段"]["总人数"]}", icon="😋")

    with st.container(border=False):
        c0, c1, c2 = st.columns(spec=3)

        with c0:
            # 编外学段统计
            visual_func.draw_pie_chart(data=data[year]["编外"]["片区"][area]["所有学段"]["学段统计"],
                                       title="学段统计")

            # 编外教师资格统计
            visual_func.draw_pie_chart(data=data[year]["编外"]["片区"][area]["所有学段"]["教师资格"],
                                       title="教师资格")

        with c1:
            # 编外学历统计
            visual_func.draw_pie_chart(data=data[year]["编外"]["片区"][area]["所有学段"]["最高学历"],
                                       title="最高学历")

            # 编外中小学教师资格统计
            visual_func.draw_pie_chart(data=data[year]["编外"]["片区"][area]["中小学"]["教师资格"],
                                       title="中小学")

        with c2:
            # 编外职称统计
            visual_func.draw_pie_chart(data=data[year]["编外"]["片区"][area]["所有学段"]["最高职称"],
                                       title="职称")

            # 编外幼儿园教师资格统计
            visual_func.draw_pie_chart(data=data[year]["编外"]["片区"][area]["幼儿园"]["教师资格"],
                                       title="幼儿园")
