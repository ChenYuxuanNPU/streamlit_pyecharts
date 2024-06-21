import sys

import pandas as pd
import streamlit as st

sys.path.append(
    r'C:\Users\1012986131\Desktop\python\streamlit_pyecharts'
)

from data_visualization.tool import func as visual_func

# 设置全局属性
visual_func.set_page_configuration(title="教育数字大屏", icon=":sparkler:")

if 'show_detail' not in st.session_state:
    st.session_state.show_detail = 0


def show_detail_info():
    st.session_state.show_detail += 1


json_data = visual_func.load_json_data(file_name="school_info")

_, col_mid, _ = st.columns([2, 1, 2])
with col_mid:
    st.title("学校信息总览")

# todo 横向比较
with st.container(border=True):
    _, col_mid, _ = st.columns([5, 1, 5])
    with col_mid:
        st.subheader("对比数据")

    col0, col1 = st.columns([1, 1])

    with col0:
        # 合计学校数对比
        st.info(f"合计学校数：{json_data["合计"]["合计学校数"]}")
        visual_func.draw_pie(
            data=dict([
                [period, json_data[period]["合计学校数"]] for period in json_data["学段列表"]
            ]),
            title="合计学校数",
            formatter="{b}--占比{d}%"
        )

        # 公民办学校数对比
        school_kind = st.selectbox(
            " ",
            ["公办学校数", "民办学校数"],
            label_visibility="collapsed"
        )

        visual_func.draw_pie(
            data=dict([
                [period, json_data[period][school_kind]] for period in json_data["学段列表"]
            ]),
            title=school_kind,
            formatter="{b}--占比{d}%",
            pos_left=f"{len(school_kind) * 3}%"
        )

        st.divider()

        # 合计教职工数对比
        st.info(f"合计教职工数：{json_data["合计"]["合计教职工数"]}")
        visual_func.draw_pie(
            data=dict([
                [period, json_data[period]["合计教职工数"]] for period in json_data["学段列表"]
            ]),
            title="合计教职工数",
            formatter="{b}--占比{d}%"
        )

        # 公民办教职工数对比
        school_kind = st.selectbox(
            " ",
            ["公办学校教职工数", "民办学校教职工数"],
            label_visibility="collapsed"
        )

        visual_func.draw_pie(
            data=dict([
                [period, json_data[period][school_kind]] for period in json_data["学段列表"]
            ]),
            title=school_kind,
            formatter="{b}--占比{d}%",
            pos_left=f"{len(school_kind) * 3}%"
        )

    with col1:
        # 合计学生数对比
        st.info(f"合计学生数：{json_data["合计"]["合计学生数"]} / 合计班额数：{json_data["合计"]["合计班额数"]}")
        visual_func.draw_pie(
            data=dict([
                [period, json_data[period]["合计学生数"]] for period in json_data["学段列表"]
            ]),
            title="合计学生数",
            formatter="{b}--占比{d}%"
        )

        # 公民办学生数对比
        school_kind = st.selectbox(
            " ",
            ["合计班额数", "公办学校学生数", "民办学校学生数",
             "公办学校白云区户籍学生数", "公办学校非白云区户籍学生数",
             "公办学校广州市户籍学生数", "公办学校非广州市户籍学生数",
             "民办学校白云区户籍学生数", "民办学校非白云区户籍学生数",
             "民办学校广州市户籍学生数", "民办学校非广州市户籍学生数"],
            label_visibility="collapsed"
        )

        visual_func.draw_pie(
            data=dict([
                [period, json_data[period][school_kind]] for period in json_data["学段列表"]
            ]),
            title=school_kind,
            formatter="{b}--占比{d}%",
            pos_left=f"{len(school_kind) * 3}%"
        )

        st.divider()

        # 合计专任教师数对比
        st.info(f"合计专任教师数：{json_data["合计"]["合计专任教师数"]}")
        visual_func.draw_pie(
            data=dict([
                [period, json_data[period]["合计专任教师数"]] for period in json_data["学段列表"]
            ]),
            title="合计专任教师数",
            formatter="{b}--占比{d}%"
        )

        # 公民办专任教师数对比
        school_kind = st.selectbox(
            " ",
            ["公办学校专任教师数", "民办学校专任教师数"],
            label_visibility="collapsed"
        )

        visual_func.draw_pie(
            data=dict([
                [period, json_data[period][school_kind]] for period in json_data["学段列表"]
            ]),
            title=school_kind,
            formatter="{b}--占比{d}%",
            pos_left=f"{len(school_kind) * 3}%"
        )

st.divider()

# todo 汇总展示
with st.container(border=True):
    _, col_mid, _ = st.columns([5, 1, 5])
    with col_mid:
        st.subheader("合计数据")

    col0, col1, col2 = st.columns(spec=3)

    with col0:
        visual_func.draw_pie(
            data=dict([
                ["公办学校数", json_data["合计"]["公办学校数"]],
                ["民办学校数", json_data["合计"]["民办学校数"]]
            ]),
            title="学校类型",
            formatter="{c}--占比{d}%"
        )

        visual_func.draw_pie(
            data=dict([
                ["白云区", json_data["合计"]["公办学校白云区户籍学生数"]],
                ["市内外区",
                 json_data["合计"]["公办学校广州市户籍学生数"] - json_data["合计"]["公办学校白云区户籍学生数"]],
                ["广州市外", json_data["合计"]["公办学校非广州市户籍学生数"]]
            ]),
            title="公办学校户籍分布",
            formatter="{c}--占比{d}%",
            pos_left="35%"
        )

    with col1:
        visual_func.draw_pie(
            data=dict([
                ["公办学校教职工数", json_data["合计"]["公办学校教职工数"]],
                ["民办学校教职工数", json_data["合计"]["民办学校教职工数"]]
            ]),
            title="教职工数",
            formatter="{c}--占比{d}%"
        )

        # st.dataframe(height=385, width=int(1920/3), hide_index=True)

        visual_func.draw_dataframe(
            data=pd.DataFrame(
                [
                    ["学校数", "合计", json_data["合计"]["合计学校数"]],
                    ["1.", "公办学校数", json_data["合计"]["公办学校数"]],
                    ["2.", "民办学校数", json_data["合计"]["民办学校数"]],
                    ["学生数", "合计", json_data["合计"]["合计学生数"]],
                    ["公办学校学生数", "小计", json_data["合计"]["公办学校学生数"]],
                    ["1.", "公办学校白云区户籍学生数", json_data["合计"]["公办学校白云区户籍学生数"]],
                    ["2.", "公办学校广州市户籍学生数", json_data["合计"]["公办学校广州市户籍学生数"]],
                    ["3.", "公办学校非白云区户籍学生数", json_data["合计"]["公办学校非白云区户籍学生数"]],
                    ["4.", "公办学校非广州市户籍学生数", json_data["合计"]["公办学校非广州市户籍学生数"]],
                    ["民办学校学生数", "小计", json_data["合计"]["民办学校学生数"]],
                    ["1.", "民办学校白云区户籍学生数", json_data["合计"]["民办学校白云区户籍学生数"]],
                    ["2.", "民办学校广州市户籍学生数", json_data["合计"]["民办学校广州市户籍学生数"]],
                    ["3.", "民办学校非白云区户籍学生数", json_data["合计"]["民办学校非白云区户籍学生数"]],
                    ["4.", "民办学校非广州市户籍学生数", json_data["合计"]["民办学校非广州市户籍学生数"]],
                    ["教职工数", "合计", json_data["合计"]["合计教职工数"]],
                    ["1.", "公办学校教职工数", json_data["合计"]["公办学校教职工数"]],
                    ["2.", "民办学校教职工数", json_data["合计"]["民办学校教职工数"]],
                    ["专任教师数", "合计", json_data["合计"]["合计专任教师数"]],
                    ["1.", "公办学校专任教师数", json_data["合计"]["公办学校专任教师数"]],
                    ["2.", "民办学校专任教师数", json_data["合计"]["民办学校专任教师数"]],
                    ["班额数", "合计", json_data["合计"]["合计班额数"]],
                ],
                columns=["项目", "细分项", "人数"]
            )
        )

    with col2:
        visual_func.draw_pie(
            data=dict([
                ["公办学校专任教师数", json_data["合计"]["公办学校专任教师数"]],
                ["民办学校专任教师数", json_data["合计"]["民办学校专任教师数"]]
            ]),
            title="专任教师",
            formatter="{c}--占比{d}%"
        )

        visual_func.draw_pie(
            data=dict([
                ["白云区", json_data["合计"]["民办学校白云区户籍学生数"]],
                ["市内外区",
                 json_data["合计"]["民办学校广州市户籍学生数"] - json_data["合计"]["民办学校白云区户籍学生数"]],
                ["广州市外", json_data["合计"]["民办学校非广州市户籍学生数"]]
            ]),
            title="民办学校户籍分布",
            formatter="{c}--占比{d}%",
            pos_left="35%"
        )

# todo 某学段展示
st.divider()

if st.session_state.show_detail > 0:

    # 单一学段展示
    with (st.container(border=True)):
        period = st.selectbox(
            "选择需要查询的学段",
            json_data["学段列表"],
            index=None,
            placeholder="单击选择学段",
        )

        if period is not None:

            # st.write(json_data[period])

            # 可视化只展示学校多的学段
            if int(json_data[period]["合计学校数"]) > 1 and json_data[period]["公办学校数"] > 0 and json_data[
                period]["民办学校数"] > 0:

                st.info(f'白云区内{period}统计信息如下', icon="ℹ️")

                col0, col1, col2 = st.columns(spec=3)

                with col0:
                    visual_func.draw_pie(
                        data=dict([
                            ["公办学校数", json_data[period]["公办学校数"]],
                            ["民办学校数", json_data[period]["民办学校数"]]
                        ]),
                        title="学校类型",
                        formatter="{c}--占比{d}%"
                    )

                    visual_func.draw_pie(
                        data=dict([
                            ["白云区", json_data[period]["公办学校白云区户籍学生数"]],
                            ["市内外区",
                             json_data[period]["公办学校广州市户籍学生数"] - json_data[period][
                                 "公办学校白云区户籍学生数"]],
                            ["广州市外", json_data[period]["公办学校非广州市户籍学生数"]]
                        ]),
                        title="公办学校户籍分布",
                        formatter="{c}--占比{d}%",
                        pos_left="35%"
                    )

                with col1:
                    visual_func.draw_pie(
                        data=dict([
                            ["公办学校教职工数", json_data[period]["公办学校教职工数"]],
                            ["民办学校教职工数", json_data[period]["民办学校教职工数"]]
                        ]),
                        title="教职工数",
                        formatter="{c}--占比{d}%"
                    )

                    # st.dataframe(height=385, width=int(1920/3), hide_index=True)

                    visual_func.draw_dataframe(
                        data=pd.DataFrame(
                            [
                                ["合计学校数", json_data[period]["合计学校数"]],
                                ["合计学生数", json_data[period]["合计学生数"]],
                                ["公办学校学生数", json_data[period]["公办学校学生数"]],
                                ["民办学校学生数", json_data[period]["民办学校学生数"]],
                                ["合计教职工数", json_data[period]["合计教职工数"]],
                                ["合计专任教师数", json_data[period]["合计专任教师数"]],
                                ["合计班额数", json_data[period]["合计班额数"]],
                            ],
                            columns=["项目", "人数"]
                        )
                    )

                with col2:
                    visual_func.draw_pie(
                        data=dict([
                            ["公办学校专任教师数", json_data[period]["公办学校专任教师数"]],
                            ["民办学校专任教师数", json_data[period]["民办学校专任教师数"]]
                        ]),
                        title="专任教师",
                        formatter="{c}--占比{d}%"
                    )

                    visual_func.draw_pie(
                        data=dict([
                            ["白云区", json_data[period]["民办学校白云区户籍学生数"]],
                            ["市内外区",
                             json_data[period]["民办学校广州市户籍学生数"] - json_data[period][
                                 "民办学校白云区户籍学生数"]],
                            ["广州市外", json_data[period]["民办学校非广州市户籍学生数"]]
                        ]),
                        title="民办学校户籍分布",
                        formatter="{c}--占比{d}%",
                        pos_left="35%"
                    )

                # 某几个学段的某几条信息是相同的，这里给个提示
                if period in ["初级中学", "九年一贯制学校"]:
                    st.warning('注：初级中学与九年一贯制学校的学生数与班额数已汇总统计', icon="⚠️")

                elif period in ["高级中学", "完全中学", "十二年一贯制学校"]:
                    st.warning('注：高级中学、完全中学与十二年一贯制学校的学生数与班额数已汇总统计', icon="⚠️")

            # 纯公/民办
            elif json_data[period]["公办学校数"] > 0 or json_data[period]["民办学校数"] > 0:

                st.info(f'白云区内{period}统计信息如下', icon="ℹ️")

                _, col_mid, _ = st.columns([1, 1, 1])

                with col_mid:

                    visual_func.draw_dataframe(
                        data=pd.DataFrame(
                            [
                                ["办学类型", f"{'公办' if json_data[period]["公办学校数"] > 0 else '民办'}"],
                                ["合计学校数", str(json_data[period]["合计学校数"])],
                                ["合计班额数", str(json_data[period]["合计班额数"])],
                                ["合计学生数", str(json_data[period]["合计学生数"])],
                                ["合计教职工数", str(json_data[period]["合计教职工数"])],
                                ["合计专任教师数", str(json_data[period]["合计专任教师数"])],
                            ],
                            columns=["项目", "信息"]
                        ),
                        hide_index=False,
                        height=280
                    )

            else:
                st.error("看代码")

# 展示详细信息的按钮
# 一定要
_, col_mid, _ = st.columns([4, 1, 4])

with col_mid:
    if st.session_state.show_detail == 0:
        st.button(
            "查看详细信息？",
            on_click=show_detail_info()
        )
