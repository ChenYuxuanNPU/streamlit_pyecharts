import sys

import pandas as pd
import pyecharts.options as opts
import streamlit as st

sys.path.append(
    r'C:\Users\1012986131\Desktop\python\streamlit_pyecharts'
)

from data_visualization.tool import func as visual_func
from teacher_data_processing.tool import func as tch_proc_func
from screeninfo import get_monitors
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Pie

if 'count' not in st.session_state:
    st.session_state.count = 0

for monitor in get_monitors():
    height = int(monitor.height / 1080) * 350

# 读取现有json文件
json_data = visual_func.load_json_data(file_name="teacher_info")

# 设置全局属性
visual_func.set_page_configuration(title="义务教育优质均衡", icon=":star:")

col3, col0, col1 = st.columns([1, 2.75, 2.75], gap="small")

col0.title('公民办学历情况')
col1.title('公民办教师资格持有率')

col0, col1 = st.columns([1, 1], gap="small")

# with col0:
#     st_echarts(
#         options={
#             "title": {"text": "在编教师学科图"},
#             "xAxis": {
#                 "data": [keys for keys in dict(json_data["在编"]["全区"]["所有学段"]["主教学科"]).keys()],
#             },
#             "yAxis": {},
#             "series": [
#                 {
#                     "type": "bar",
#                     "data": [values for values in dict(json_data["在编"]["全区"]["所有学段"]["主教学科"]).values()]
#                 }
#             ]
#         }
#     )

c, conn = tch_proc_func.connect_database()
c.execute("select distinct school_name from teacher_data_0")
school_list_0 = tch_proc_func.del_tuple_in_list(c.fetchall())

c.execute("select distinct school_name from teacher_data_1")
school_list_1 = tch_proc_func.del_tuple_in_list(c.fetchall())

for i in range(len(school_list_1) - 1, -1, -1):
    if school_list_1[i] in school_list_0:
        del school_list_1[i]

c.execute(
    "select educational_background_highest, count(*) from teacher_data_0 where period = '初中' or period = '小学' group by educational_background_highest")
result0 = dict(
    sorted(
        c.fetchall(), key=lambda x: tch_proc_func.educational_background_order[x[0]]
    )

)

c.execute(
    "select educational_background_highest, count(*) from teacher_data_1 where (period = '初中' or period = '小学') and is_teacher = '是' group by educational_background_highest")
result1 = dict(
    sorted(
        c.fetchall(), key=lambda x: tch_proc_func.educational_background_order[x[0]]
    )

)

merge_edu = result0
for key, value in result1.items():
    if key in merge_edu.keys():
        merge_edu[key] += value
    else:
        merge_edu[key] = value

merge_edu["高中及以下"] += (merge_edu["高中"] + merge_edu["中专"])
del merge_edu["高中"]
del merge_edu["中专"]

with col0:
    # visual_func.draw_pie(data=merge_edu, title="学历统计")
    with st.container(border=True):
        st_pyecharts(
            chart=(
                Pie()
                .add("", [(k, v) for k, v in merge_edu.items()],
                     center=["50%", "60%"], radius="65%", percent_precision=1)
                .set_global_opts(title_opts=opts.TitleOpts(title="学历统计"),
                                 legend_opts=opts.LegendOpts(pos_left='20%' if len("学历统计") > 2 else "15%"))
                # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}人,占比{d}%"))
            ),
            height=f"{height}px"
        )

merge_qua = {}

c.execute(
    "select count(*) from teacher_data_0  where level_of_teacher_certification == '无' and (period == '初中' or period == '小学')")
merge_qua["未持教资"] = c.fetchall()[0][0]

c.execute(
    "select count(*) from teacher_data_1  where level_of_teacher_certification == '无' and (period == '初中' or period == '小学') and is_teacher == '是'")
merge_qua["未持教资"] += c.fetchall()[0][0]

c.execute(
    "select count(*) from teacher_data_0  where level_of_teacher_certification != '无' and (period == '初中' or period == '小学')")
merge_qua["持有教资"] = c.fetchall()[0][0]

c.execute(
    "select count(*) from teacher_data_1  where level_of_teacher_certification != '无' and (period == '初中' or period == '小学') and is_teacher == '是'")
merge_qua["持有教资"] += c.fetchall()[0][0]

with col1:
    # visual_func.draw_pie(data=merge_qua, title="教资持证情况")
    with st.container(border=True):
        st_pyecharts(
            chart=(
                Pie()
                .add("", [(k, v) for k, v in merge_qua.items()],
                     center=["50%", "60%"], radius="65%", percent_precision=1)
                .set_global_opts(title_opts=opts.TitleOpts(title="教资持证情况"),
                                 legend_opts=opts.LegendOpts(pos_left='20%' if len("教资持证情况") > 2 else "15%"))
                # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}人,占比{d}%"))
            ),
            height=f"{height}px"
        )

# 最高学历
c.execute(
    "select educational_background_highest, school_name from teacher_data_0 where period = '初中' or period = '小学'")
result0 = sorted(c.fetchall(), key=lambda x: tch_proc_func.educational_background_order[x[0]])

c.execute(
    "select educational_background_highest, school_name from teacher_data_1 where (period = '初中' or period = '小学') and is_teacher == '是'")
result1 = sorted(c.fetchall(), key=lambda x: tch_proc_func.educational_background_order[x[0]])

# 公办
result0_0 = {}

# 民办
result0_1 = {}

for item in result0:
    if item[1] in school_list_0:
        if item[0] not in result0_0.keys():
            result0_0[item[0]] = 0
        result0_0[item[0]] += 1

    else:
        print("?")

for item in result1:
    if item[1] in school_list_0:
        if item[0] not in result0_0.keys():
            result0_0[item[0]] = 0
        result0_0[item[0]] += 1

    else:
        if item[0] not in result0_1.keys():
            result0_1[item[0]] = 0
        result0_1[item[0]] += 1

result0_0["高中及以下"] += (result0_0["高中"] + result0_0["中专"])
del result0_0["高中"]
del result0_0["中专"]

with col0:
    c1, c2 = st.columns(spec=2)

    with c1:
        # visual_func.draw_pie(data=result0_0, title="公办")
        with st.container(border=True):
            st_pyecharts(
                chart=(
                    Pie()
                    .add("", [(k, v) for k, v in result0_0.items()],
                         center=["50%", "60%"], radius="65%", percent_precision=1)
                    .set_global_opts(title_opts=opts.TitleOpts(title="公办"),
                                     legend_opts=opts.LegendOpts(pos_left='20%' if len("公办") > 2 else "15%"))
                    # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}人,占比{d}%"))
                ),
                height=f"{height}px"
            )

    with c2:
        # visual_func.draw_pie(data=result0_1, title="民办")
        with st.container(border=True):
            st_pyecharts(
                chart=(
                    Pie()
                    .add("", [(k, v) for k, v in result0_1.items()],
                         center=["50%", "60%"], radius="65%", percent_precision=1)
                    .set_global_opts(title_opts=opts.TitleOpts(title="民办"),
                                     legend_opts=opts.LegendOpts(pos_left='20%' if len("民办") > 2 else "15%"))
                    # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}人,占比{d}%"))
                ),
                height=f"{height}px"
            )

# 公办
merge_qua_0 = {"未持教资": 0, "持有教资": 0}
# 民办
merge_qua_1 = {"未持教资": 0, "持有教资": 0}

c.execute(
    "select school_name from teacher_data_0  where level_of_teacher_certification == '无' and (period == '初中' or period == '小学')")
schlist_none_0 = tch_proc_func.del_tuple_in_list(c.fetchall())
schlist_none_1 = []
merge_qua_0["未持教资"] += len(schlist_none_0)

c.execute(
    "select school_name from teacher_data_1  where level_of_teacher_certification == '无' and (period == '初中' or period == '小学') and is_teacher == '是'")

result = tch_proc_func.del_tuple_in_list(c.fetchall())
for school in result:
    if school in school_list_0:
        schlist_none_0.append(school)
        merge_qua_0["未持教资"] += 1
    else:
        schlist_none_1.append(school)
        merge_qua_1["未持教资"] += 1

c.execute(
    "select school_name from teacher_data_0  where level_of_teacher_certification != '无' and (period == '初中' or period == '小学')")
merge_qua_0["持有教资"] = len(tch_proc_func.del_tuple_in_list(c.fetchall()))

c.execute(
    "select school_name from teacher_data_1  where level_of_teacher_certification != '无' and (period == '初中' or period == '小学') and is_teacher == '是'")
result = tch_proc_func.del_tuple_in_list(c.fetchall())
for school in result:
    if school in school_list_0:
        merge_qua_0["持有教资"] += 1
    else:
        merge_qua_1["持有教资"] += 1

with col1:
    c1, c2 = st.columns(spec=2)

    with c1:
        # visual_func.draw_pie(data=merge_qua_0, title="公办")
        with st.container(border=True):
            st_pyecharts(
                chart=(
                    Pie()
                    .add("", [(k, v) for k, v in merge_qua_0.items()],
                         center=["50%", "60%"], radius="65%", percent_precision=1)
                    .set_global_opts(title_opts=opts.TitleOpts(title="公办"),
                                     legend_opts=opts.LegendOpts(pos_left='20%' if len("公办") > 2 else "15%"))
                    # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}人,占比{d}%"))
                ),
                height=f"{height}px"
            )

        # 无教资公办名单
        dict0 = {}
        for item in schlist_none_0:
            if item in dict0.keys():
                dict0[item] += 1
            else:
                dict0[item] = 1

        st.dataframe(
            pd.DataFrame(sorted(list(dict0.items()), key=lambda x: x[1], reverse=True), columns=["校名", "人数"]))

    with c2:
        # visual_func.draw_pie(data=merge_qua_1, title="民办")
        with st.container(border=True):
            st_pyecharts(
                chart=(
                    Pie()
                    .add("", [(k, v) for k, v in merge_qua_1.items()],
                         center=["50%", "60%"], radius="65%", percent_precision=1)
                    .set_global_opts(title_opts=opts.TitleOpts(title="民办"),
                                     legend_opts=opts.LegendOpts(pos_left='20%' if len("民办") > 2 else "15%"))
                    # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}人,占比{d}%"))
                ),
                height=f"{height}px"
            )

        # 无教资民办名单
        dict1 = {}
        for item in schlist_none_1:
            if item in dict1.keys():
                dict1[item] += 1
            else:
                dict1[item] = 1

        st.dataframe(
            pd.DataFrame(sorted(list(dict1.items()), key=lambda x: x[1], reverse=True), columns=["校名", "人数"]))

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


def fuck():
    print("fuck!!!")



