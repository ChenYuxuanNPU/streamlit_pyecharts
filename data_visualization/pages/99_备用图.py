import os
import sys

import pyecharts.options as opts
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

from teacher_data_processing.tool import func as tch_proc_func
from screeninfo import get_monitors
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Pie

st.write()

height = int(get_monitors()[0].height / 1080) * 350

c, conn = tch_proc_func.connect_database()

# 查党员
c.execute("select political_status,count(*) from teacher_data_0 group by political_status order by count(*) desc")

party_0 = c.fetchall()

c.execute("select political_status,count(*) from teacher_data_0 where current_administrative_position != '无' and "
          "current_administrative_position != '中层正职' and current_administrative_position != '中层副职' group by "
          "political_status order by count(*) desc")

party_1 = c.fetchall()

with st.container(border=True):
    st_pyecharts(
        chart=(
            Pie()
            .add("", [(k, v) for k, v in dict(party_0).items()],
                 center=["50%", "60%"], radius="65%", percent_precision=1)
            .set_global_opts(title_opts=opts.TitleOpts(title="全区政治面貌统计"),
                             legend_opts=opts.LegendOpts(pos_left='20%' if len("全区政治面貌统计") > 2 else "15%"))
            # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}人,占比{d}%"))
        ),
        height=f"{height}px"
    )

with st.container(border=True):
    st_pyecharts(
        chart=(
            Pie()
            .add("", [(k, v) for k, v in dict(party_1).items()],
                 center=["50%", "60%"], radius="65%", percent_precision=1)
            .set_global_opts(title_opts=opts.TitleOpts(title="校级干部政治面貌统计"),
                             legend_opts=opts.LegendOpts(pos_left='20%' if len("校级干部政治面貌统计") > 2 else "15%"))
            # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}人,占比{d}%"))
        ),
        height=f"{height}px"
    )

tch_proc_func.disconnect_database(conn=conn)
