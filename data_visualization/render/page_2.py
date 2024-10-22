import pandas as pd
import streamlit as st

from data_visualization.tool import func as visual_func


def get_area_list() -> list:
    """
    片镇列表：["永平", "石井", "新市", "江高", "人和", "太和", "钟落潭"]
    :return:
    """

    return ["永平", "石井", "新市", "江高", "人和", "太和", "钟落潭"]


def get_area_dataframe_columns_list() -> list:
    return ["年份", "片镇", "人数"]


def get_period_list() -> list:
    return ["高中", "初中", "小学", "幼儿园"]


def get_period_dataframe_columns_list() -> list:
    return ["年份", "学段", "人数"]


def get_edu_bg_list() -> list:
    return ["博士研究生", "硕士研究生", "本科", "专科"]


def get_edu_bg_dataframe_columns_list() -> list:
    return ["年份", "最高学历", "人数"]


def get_vocational_level_list() -> list:
    return ["正高级教师", "高级教师", "一级教师", "二级教师", "三级教师"]


def get_vocational_level_dataframe_columns_list() -> list:
    return ["年份", "聘用职称", "人数"]


def get_vocational_level_detail_list() -> list:
    return ["试用期（未定级）", "专业技术十三级", "专业技术十二级", "专业技术十一级", "专业技术十级",
            "专业技术九级", "专业技术八级", "专业技术七级", "专业技术六级", "专业技术五级", "专业技术四级", ]


def get_vocational_level_detail_dataframe_columns_list() -> list:
    return ["年份", "专业技术等级", "人数"]


def get_discipline_list() -> list:
    return [
        "语文", "数学", "英语", "思想政治", "历史", "地理", "物理", "化学", "生物", "体育", "音乐", "美术",
        "科学", "信息技术", "通用技术", "劳动", "心理健康"
    ]


def get_discipline_dataframe_columns_list() -> list:
    return ["年份", "学科", "人数"]


def get_grad_school_list() -> list:
    return ["985院校", "部属师范院校", "211院校"]


def get_grad_school_dataframe_columns_list() -> list:
    return ["年份", "院校级别", "人数"]


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
        options=["所有学段"] + get_period_list(),
        default=["所有学段", get_period_list()[0]]
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

        st.info("在编教师数随年份变化情况")
        show_multi_years_teacher_0_count(year_list=year_list)

        st.info("片镇教师数随年份变化情况")
        show_multi_years_teacher_0_area(year_list=year_list)

        st.info("学段教师数随年份变化情况")
        show_multi_years_teacher_0_period(year_list=year_list)

        st.info("学历水平随年份变化情况")
        show_multi_years_teacher_0_edu_bg(year_list=year_list)

        st.info("专技职称随年份变化情况")
        show_multi_years_teacher_0_vocational_level(year_list=year_list)

        st.info("学科教师数随年份变化情况")
        show_multi_years_teacher_0_discipline(year_list=year_list)

        st.info("教师毕业院校水平随年份变化情况")
        show_multi_years_teacher_0_grad_school(year_list=year_list)


def show_multi_years_teacher_0_basic(year_list: list, json_field: str,
                                     dataframe_columns_list: list, info_list: list,
                                     block_left_img: bool = False, block_right_img: bool = False,
                                     block_bottom_img: bool = False) -> None:
    """
    年份对比中基础三张图的生成
    :param year_list: 对比所用的年份列表
    :param json_field: json文件对应的子字典对应的字段
    :param dataframe_columns_list: 生成pd.Dataframe的列名
    :param info_list: 需要统计的选项列表
    :param block_left_img: 是否屏蔽左侧图，默认False不屏蔽，True则屏蔽
    :param block_right_img: 是否屏蔽右侧图，默认False不屏蔽，True则屏蔽
    :param block_bottom_img: 是否屏蔽底部图，默认False不屏蔽，True则屏蔽
    :return: 无
    """
    data = visual_func.load_json_data(folder="result", file_name="teacher_info")

    left, right = st.columns(spec=2)

    # 展示左侧折线图
    if not block_left_img:
        output = {}

        for area in info_list:
            output[f"{area}"] = [[year, data[year]["在编"]["全区"]["所有学段"][json_field].get(area, None)] for year in
                                 year_list]

        with left:
            visual_func.draw_line_chart(data=output, title="", x_axis=year_list, label_list=info_list,
                                        is_symbol_show=False)

    if not block_right_img or not block_bottom_img:
        df = pd.DataFrame(columns=dataframe_columns_list)
        temp = []

        for year in year_list:
            for info in info_list:
                temp.append(
                    pd.DataFrame(
                        [[year, info, data[year]["在编"]["全区"]["所有学段"][json_field].get(info, None)]],
                        columns=dataframe_columns_list
                    )
                )

        df = pd.concat(temp, ignore_index=True)

        # 展示右侧分散柱状图
        if not block_right_img:
            with right:
                visual_func.draw_unstack_bar_chart(data=df, x_axis=dataframe_columns_list[0],
                                                   y_axis=dataframe_columns_list[2],
                                                   label=dataframe_columns_list[1])
        # 展示底部水平柱状图
        if not block_bottom_img:
            visual_func.draw_horizontal_bar_chart(data=df, x_axis=dataframe_columns_list[0],
                                                  y_axis=dataframe_columns_list[2],
                                                  label=dataframe_columns_list[1])

    return None


def show_multi_years_teacher_0_count(year_list: list) -> None:
    with st.container(border=True):
        data = visual_func.load_json_data(folder="result", file_name="teacher_info")

        output = {"教师数": []}

        for year in year_list:
            output["教师数"].append([f"{year}", data[year]["在编"]["全区"]["所有学段"]["总人数"]])

        visual_func.draw_line_chart(data=output, title="", x_axis=year_list, label_list=["教师数"])


def show_multi_years_teacher_0_area(year_list: list) -> None:
    with st.container(border=True):
        show_multi_years_teacher_0_basic(year_list=year_list, json_field="片区统计",
                                         dataframe_columns_list=get_area_dataframe_columns_list(),
                                         info_list=get_area_list())

    return None


def show_multi_years_teacher_0_period(year_list: list) -> None:
    with st.container(border=True):
        show_multi_years_teacher_0_basic(year_list=year_list, json_field="学段统计",
                                         dataframe_columns_list=get_period_dataframe_columns_list(),
                                         info_list=get_period_list())

    return None


def show_multi_years_teacher_0_edu_bg(year_list: list) -> None:
    with st.container(border=True):
        show_multi_years_teacher_0_basic(year_list=year_list, json_field="最高学历",
                                         dataframe_columns_list=get_edu_bg_dataframe_columns_list(),
                                         info_list=get_edu_bg_list())

    return None


def show_multi_years_teacher_0_vocational_level(year_list: list) -> None:
    with st.container(border=True):
        show_multi_years_teacher_0_basic(year_list=year_list, json_field="最高职称",
                                         dataframe_columns_list=get_vocational_level_dataframe_columns_list(),
                                         info_list=get_vocational_level_list(),
                                         block_bottom_img=True)

        show_multi_years_teacher_0_basic(year_list=year_list, json_field="专业技术岗位",
                                         dataframe_columns_list=get_vocational_level_detail_dataframe_columns_list(),
                                         info_list=get_vocational_level_detail_list(),
                                         block_left_img=True, block_right_img=True)

    return None


def show_multi_years_teacher_0_discipline(year_list: list) -> None:
    with st.container(border=True):
        show_multi_years_teacher_0_basic(year_list=year_list, json_field="主教学科",
                                         dataframe_columns_list=get_discipline_dataframe_columns_list(),
                                         info_list=get_discipline_list())
    return None


def show_multi_years_teacher_0_grad_school(year_list: list) -> None:
    with st.container(border=True):
        show_multi_years_teacher_0_basic(year_list=year_list, json_field="院校级别",
                                         dataframe_columns_list=get_grad_school_dataframe_columns_list(),
                                         info_list=get_grad_school_list())
    return None


if __name__ == '__main__':
    show_multi_years_teacher_0_vocational_level(year_list=["2023", "2024"])
