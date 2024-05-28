import json
import streamlit as st
import pyecharts.options as opts
from screeninfo import get_monitors
from streamlit_echarts import st_echarts
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType

# 读取现有json文件
with open(r"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\result\output.json",
          "r", encoding="UTF-8") as file:
    json_data = json.load(file)

# 设置全局属性
st.set_page_config(
    page_title='我是标题',
    page_icon='',
    layout='wide'
)

st.title("全区教师数据")

col0, col1 = st.columns(spec=2, gap="small")

col0.title('This is Column Ⅰ')
col1.title('This is Column Ⅱ')

with col0:
    st_echarts(
        options={
            "title": {"text": "在编教师身高图"},
            "xAxis": {
                "data": [keys for keys in dict(json_data["在编"]["全区"]["所有学段"]["主教学科"]).keys()],
            },
            "yAxis": {},
            "series": [
                {
                    "type": "bar",
                    "data": [values for values in dict(json_data["在编"]["全区"]["所有学段"]["主教学科"]).values()]
                }
            ]
        }
    )

    st_pyecharts(
        chart=(
            Pie()
            .add("", [(k, v) for k, v in json_data["在编"]["全区"]["所有学段"]["最高学历"].items()],
                 center=["50%", "60%"], radius="65%")
            .set_global_opts(title_opts=opts.TitleOpts(title="骨干教师"), legend_opts=opts.LegendOpts())
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}, {d}%"))
        )
    )

    st_pyecharts(
        chart=(
            Pie()
            .add("", [list(z) for z in zip(["q", "w", "e"], [10, 50, 70])],
                 center=["50%", "60%"], radius="65%")
            .set_global_opts(title_opts=opts.TitleOpts(title="在编教师"), legend_opts=opts.LegendOpts())
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}, {d}%"))
        )
    )

with col1:
    st_pyecharts(
        chart=(
            Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(["a", "b", "c"])
            .add_yaxis("总人数", [100, 200, 300])
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(title_opts=opts.TitleOpts(title="主教学科"), legend_opts=opts.LegendOpts(is_show=False))
        )
    )

    st_pyecharts(
        chart=(
            Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(["aaaa", "bbbbb", "cccccccc"])
            .add_yaxis("总人数", [100, 200, 300])
            .set_series_opts(label_opts=opts.LabelOpts(position="top"))
            .set_global_opts(title_opts=opts.TitleOpts(title="主教学科"), legend_opts=opts.LegendOpts(is_show=False))
        ),
        height="500%"
    )

    c00, c11 = st.columns(spec=2)

    with c00:
        st_pyecharts(
            chart=(
                Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
                .add_xaxis(["k", "b", "c"])
                .add_yaxis("总人数", [100, 200, 300])
                .set_series_opts(label_opts=opts.LabelOpts(position="top"))
                .set_global_opts(title_opts=opts.TitleOpts(title="主教学科"),
                                 legend_opts=opts.LegendOpts(is_show=False))
            ),
            height="450px"
        )

    with c11:
        st_pyecharts(
            chart=(
                Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
                .add_xaxis(["ty", "b", "c"])
                .add_yaxis("总人数", [100, 200, 300])
                .set_series_opts(label_opts=opts.LabelOpts(position="top"))
                .set_global_opts(title_opts=opts.TitleOpts(title="主教学科"),
                                 legend_opts=opts.LegendOpts(is_show=False))
            ),
        )

        for monitor in get_monitors():
            height = monitor.height
