import sys
from pathlib import Path

import streamlit as st

# 加入项目路径
sys.path.append(
    str(
        Path(__file__).resolve().parent.parent.parent
    )
)

from screeninfo import get_monitors

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


# 标题
# st.markdown(
#     "<h1 style='text-align: center;'>2024年10月人事例会</h1>",
#     unsafe_allow_html=True
# )
#
# st.markdown(
#     "<h3>1.在编人员数据汇总情况</h3>",
#     unsafe_allow_html=True
# )
#
#
# st.markdown(
#     "<h3>2.编外人员数据收集指引</h3>",
#     unsafe_allow_html=True
# )
