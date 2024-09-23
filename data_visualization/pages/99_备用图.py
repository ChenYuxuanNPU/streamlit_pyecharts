import os
import sys

import streamlit as st


# 返回给定的第n层的父目录路径
def get_nth_parent_dir(n):
    path = os.path.abspath(__file__)

    for _ in range(n):
        path = os.path.dirname(path)

    return path


sys.path.append(
    get_nth_parent_dir(n=3)
)

from screeninfo import get_monitors
from data_visualization.tool import func as visual_func

st.write()

height = int(get_monitors()[0].height / 1080) * 350

# c, conn = tch_proc_func.connect_database()
#
# # 查党员
# c.execute("select political_status,count(*) from teacher_data_0 group by political_status order by count(*) desc")
#
# party_0 = c.fetchall()
#
# c.execute("select political_status,count(*) from teacher_data_0 where current_administrative_position != '无' and "
#           "current_administrative_position != '中层正职' and current_administrative_position != '中层副职' group by "
#           "political_status order by count(*) desc")
#
# party_1 = c.fetchall()
#
# with st.container(border=True):
#     c0, c1 = st.columns(spec=2)
#
#     with c0:
#
#         with st.container(border=True):
#             st_pyecharts(
#                 chart=(
#                     Pie()
#                     .add("", [(k, v) for k, v in dict(party_0).items()],
#                          center=["50%", "60%"], radius="65%", percent_precision=1)
#                     .set_global_opts(title_opts=opts.TitleOpts(title="政治面貌"),
#                                      legend_opts=opts.LegendOpts(pos_left='20%' if len("全区政治面貌统计") > 2 else "15%"))
#                     # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
#                     .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}人,占比{d}%"))
#                 ),
#                 height=f"{height}px"
#             )
#
#     with c1:
#
#         with st.container(border=True):
#             st_pyecharts(
#                 chart=(
#                     Pie()
#                     .add("", [(k, v) for k, v in dict(party_1).items()],
#                          center=["50%", "60%"], radius="65%", percent_precision=1)
#                     .set_global_opts(title_opts=opts.TitleOpts(title="校级干部"),
#                                      legend_opts=opts.LegendOpts(pos_left='20%' if len("校级干部政治面貌统计") > 2 else "15%"))
#                     # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
#                     .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}人,占比{d}%"))
#                 ),
#                 height=f"{height}px"
#             )
#
# tch_proc_func.disconnect_database(conn=conn)


st.markdown(
    "<h1 style='text-align: center;'>2024学年部分人事数据</h1>",
    unsafe_allow_html=True
)

st.divider()

with st.container(border=True):
    c0, c1 = st.columns(spec=2)

    with c0:
        visual_func.draw_pie(data={
            "博士研究生": 1,
            "硕士研究生": 1,
            "本科": 1,
            "专科": 1,
            "中专": 1,
            "中师": 1,
            "高中": 1,
            "初中": 1,
        }, title="学历统计", height=450)

        visual_func.draw_pie(data={
            "正高级教师": 1,
            "高级教师": 1,
            "一级教师": 1,
            "二级教师": 1,
            "三级教师": 1,
            "高级职称（非中小学系列）": 1,
            "中级职称（非中小学系列）": 1,
            "初级职称（非中小学系列）": 1,
            "试用期未聘": 1,
            "未取得职称": 1
        }, title="现聘职称", height=450)

        visual_func.draw_pie(data={
            "高中": 1,
            "初中": 1,
            "小学": 1,
            "中职": 1,
            "幼儿园": 1,
            "其他": 1,
        }, title="任教学段", height=450)

        visual_func.draw_pie(data={
            "直管": 1,
            "永平": 1,
            "石井": 1,
            "新市": 1,
            "江高": 1,
            "人和": 1,
            "太和": 1,
            "钟落潭": 1,
        }, title="区域统计", height=450)

    with c1:
        visual_func.draw_pie(data={
            "语文": 1,
            "数学": 1,
            "英语": 1,
            "专科": 1,
            "思想政治": 1,
            "历史": 1,
            "地理": 1,
            "物理": 1,
            "化学": 1,
            "生物": 1,
            "体育": 1,
            "音乐": 1,
            "美术": 1,
            "书法": 1,
            "舞蹈": 1,
            "科学": 1,
            "信息技术": 1,
            "通用技术": 1,
            "劳动": 1,
            "综合实践": 1,
            "心理健康": 1,
            "人工智能": 1,
            "汽修": 1,
            "烹饪": 1,
            "幼儿教育": 1,
        }, title="学科统计", height=450)

        visual_func.draw_pie(data={
            "广东省骨干教师": 1,
            "广州市骨干教师": 1,
            "白云区骨干教师": 1,
            "其他": 1,
            "无": 1
        }, title="骨干教师", height=450)

        visual_func.draw_pie(data={
            "片内": 1,
            "区内": 1,
            "外市": 1,
            "外省": 1,
            "无": 1
        }, title="支教情况", height=450)

        visual_func.draw_pie(data={
            "在职在岗": 1,
            "区内其他单位跟岗或借调": 1,
            "区内交流": 1,
            "外市支教": 1,
            "长期事假": 1,
            "产假":1,
            "公假":1,
            "长期病休":1,
            "其他":1
        }, title="在岗情况", height=450)
