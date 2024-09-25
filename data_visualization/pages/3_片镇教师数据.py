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

# 初始化全局变量
visual_func.session_state_initial()

# 清空其他页暂用变量
visual_func.session_state_reset(page=3)

# 设置页面格式
visual_func.set_page_configuration(title="片镇教师数据", icon=":office:")

# 读取现有json文件
json_data = visual_func.load_json_data(folder="result", file_name="teacher_info")

# 标题
st.markdown(
    "<h1 style='text-align: center;'>片镇教师数据</h1>",
    unsafe_allow_html=True
)

st.divider()

with st.container(border=True):
    page3_area = st.selectbox(
        "想查询哪一个片镇的信息？",
        ("永平", "石井", "新市", "人和", "江高", "太和", "钟落潭"),
        index=None,
        placeholder="单击选择区域",
    )

    if page3_area is not None:

        st.success(f"{page3_area}在编所有学段信息")

        with st.container(border=False):
            col0, col1, col2 = st.columns(spec=3)

            with col0:
                # 在编年龄统计
                visual_func.draw_pie(data=json_data["在编"]["片区"][page3_area]["所有学段"]["年龄"],
                                     title="年龄")

                # 在编学段统计
                visual_func.draw_pie(data=json_data["在编"]["片区"][page3_area]["所有学段"]["学段统计"],
                                     title="学段统计")

            with col1:
                # 在编学历统计
                visual_func.draw_pie(data=json_data["在编"]["片区"][page3_area]["所有学段"]["最高学历"],
                                     title="最高学历")

                # 在编毕业院校统计
                visual_func.draw_bar(data=json_data["在编"]["片区"][page3_area]["所有学段"]["院校级别"],
                                     title="毕业院校", is_show_visual_map=False)

            with col2:
                # 在编职称统计
                visual_func.draw_pie(data=json_data["在编"]["片区"][page3_area]["所有学段"]["最高职称"],
                                     title="职称")

                # 在编行政职务统计
                visual_func.draw_pie(data=json_data["在编"]["片区"][page3_area]["所有学段"]["行政职务"],
                                     title="行政职务")

            # 在编学科统计
            visual_func.draw_bar(data=json_data["在编"]["片区"][page3_area]["所有学段"]["主教学科"],
                                 title="主教学科", is_show_visual_map=False)

            # 在编教师数少的学校统计
            temp_all = sorted(list(json_data["学校教师总数"].items()), key=lambda x: (x[1][3], x[1][5]))
            temp = []
            temp_for_bar = {}

            for item in temp_all:
                if item[1][2] == page3_area and item[1][3] != 0 and item[1][1] != "幼儿园" and item[1][
                    1] != "教育辅助单位":
                    temp.append(item)

            for i in range(0, min(15, len(temp))):
                temp_for_bar[temp[i][0]] = temp[i][1][3]

            visual_func.draw_bar(data=visual_func.simplify_school_name(temp_for_bar), title="在编教师数较少的学校",
                                 is_show_visual_map=False)

            # 统计完在编教师数少的学校了

            col0, col1, col2 = st.columns(spec=3)

            with col0:
                # 在编骨干教师统计
                visual_func.draw_pie(data=json_data["在编"]["片区"][page3_area]["所有学段"]["骨干教师"],
                                     title="骨干教师")

            with col1:
                # 在编教师支教统计
                visual_func.draw_pie(data=json_data["在编"]["片区"][page3_area]["所有学段"]["支教地域"],
                                     title="支教地域")

            with col2:
                # 在编三名教师统计
                visual_func.draw_pie(data=json_data["在编"]["片区"][page3_area]["所有学段"]["三名工作室"],
                                     title="三名统计")

        st.success("编外所有学段教师信息")

        with st.container(border=False):
            col0, col1, col2 = st.columns(spec=3)

            with col0:
                # 编外学段统计
                visual_func.draw_pie(data=json_data["编外"]["片区"][page3_area]["所有学段"]["学段统计"],
                                     title="学段统计")

                # 编外教师资格统计
                visual_func.draw_pie(data=json_data["编外"]["片区"][page3_area]["所有学段"]["教师资格"],
                                     title="教师资格")

            with col1:
                # 编外学历统计
                visual_func.draw_pie(data=json_data["编外"]["片区"][page3_area]["所有学段"]["最高学历"],
                                     title="最高学历")

                # 编外中小学教师资格统计
                visual_func.draw_pie(data=json_data["编外"]["片区"][page3_area]["中小学"]["教师资格"],
                                     title="中小学")

            with col2:
                # 编外职称统计
                visual_func.draw_pie(data=json_data["编外"]["片区"][page3_area]["所有学段"]["最高职称"],
                                     title="职称")

                # 编外幼儿园教师资格统计
                visual_func.draw_pie(data=json_data["编外"]["片区"][page3_area]["幼儿园"]["教师资格"],
                                     title="幼儿园")

if page3_area is None:
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
