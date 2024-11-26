from calculation.retirement import *
from data_visualization.tool.func import *


class DataFrameContainer:
    """
    用于动态返回多个dataframe
    """

    def __init__(self):
        # 初始化一个空字典来存储 DataFrame
        self.dataframes = {}

    def add_dataframe(self, name, df):
        # 添加一个 DataFrame 到字典中，使用 name 作为键
        self.dataframes[name] = df

    def get_dataframe(self, name):
        # 根据名称获取 DataFrame
        return self.dataframes.get(name, None)

    def remove_dataframe(self, name):
        # 根据名称移除 DataFrame
        if name in self.dataframes:
            del self.dataframes[name]

    def list_dataframes(self):
        # 列出所有存储的 DataFrame 的名称
        return list(self.dataframes.keys())

    def all_dataframes(self):
        # 返回一个包含所有 DataFrame 的字典
        return self.dataframes.copy()


def get_period_list() -> list[str]:
    """
    学段列表：["高中", "初中", "小学", "幼儿园"]
    :return:
    """
    return ["高中", "初中", "小学", "幼儿园"]


def get_base_data() -> dict:
    """
    获取全区教师数据
    :return:
    """
    return load_json_data(folder="result", file_name="teacher_info")


def show_text_info() -> None:
    """
    用于展示指导中心的基础信息（不查询东西的时候）
    :return:
    """
    st.divider()

    # 展示宣传数据
    with st.container(border=True):
        st.markdown(
            "<h3 style='text-align: center;'>广州市白云区各教育指导中心相关信息</h3>",
            unsafe_allow_html=True
        )

        draw_dataframe(
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


def show_1_year_teacher_0(year: str, area: str) -> None:
    """
    用于展示某一年在编教师信息
    :param year: 年份
    :param area: 片镇
    :return:
    """
    data = get_base_data()

    st.success(f"{area}在编总人数：{data[year]["在编"]["片区"][area]["所有学段"]["总人数"]}", icon="😋")

    with st.container(border=False):
        c0, c1, c2 = st.columns(spec=3)

        with c0:
            # 在编年龄统计
            draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["年龄"],
                           title="年龄", pos_left="15%", center_to_bottom="64%")

            # 在编学段统计
            draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["学段统计"],
                           title="学段统计")

        with c1:
            # 在编学历统计
            draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["最高学历"],
                           title="最高学历")

            # 在编毕业院校统计
            draw_bar_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["院校级别"],
                           title="毕业院校", is_show_visual_map=False)

        with c2:
            # 在编职称统计
            draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["最高职称"],
                           title="职称")

            # 在编行政职务统计
            draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["行政职务"],
                           title="行政职务")

        # 在编学科统计
        draw_bar_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["主教学科"],
                       title="主教学科", is_show_visual_map=False)

        c0, c1, c2 = st.columns(spec=3)  # 不能删，这里删了会影响上下层顺序

        with c0:
            # 在编骨干教师统计
            draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["骨干教师"],
                           title="骨干教师")

        with c1:
            # 在编教师支教统计
            draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["支教地域"],
                           title="支教地域")

        with c2:
            # 在编四名教师统计
            draw_pie_chart(data=data[year]["在编"]["片区"][area]["所有学段"]["四名工作室"],
                           title="四名统计")


def show_1_year_teacher_1(year: str, area: str) -> None:
    """
    用于展示某一年编外教师信息
    :param year: 年份
    :param area: 片镇
    :return:
    """
    data = get_base_data()

    st.success(f"{area}编外总人数：{data[year]["编外"]["片区"][area]["所有学段"]["总人数"]}", icon="😋")

    with st.container(border=False):
        c0, c1, c2 = st.columns(spec=3)

        with c0:
            # 编外学段统计
            draw_pie_chart(data=data[year]["编外"]["片区"][area]["所有学段"]["学段统计"],
                           title="学段统计")

            # 编外教师资格统计
            draw_pie_chart(data=data[year]["编外"]["片区"][area]["所有学段"]["教师资格"],
                           title="教师资格")

        with c1:
            # 编外学历统计
            draw_pie_chart(data=data[year]["编外"]["片区"][area]["所有学段"]["最高学历"],
                           title="最高学历")

            # 编外中小学教师资格统计
            draw_pie_chart(data=data[year]["编外"]["片区"][area]["中小学"]["教师资格"],
                           title="中小学")

        with c2:
            # 编外职称统计
            draw_pie_chart(data=data[year]["编外"]["片区"][area]["所有学段"]["最高职称"],
                           title="职称")

            # 编外幼儿园教师资格统计
            draw_pie_chart(data=data[year]["编外"]["片区"][area]["幼儿园"]["教师资格"],
                           title="幼儿园")


def show_multi_years_and_1_area_teacher_0(year_list: list[str], area: str) -> None:
    """
    用于展示同一片镇多年的在编教师数据对比信息
    :param year_list: 年份列表
    :param area: 查询的片镇名
    :return:
    """

    with st.container(border=True):
        # 小标题
        st.markdown(
            body="<h2 style='text-align: center;'>年份对比</h2>",
            unsafe_allow_html=True
        )
        st.divider()

        st.info("在编教师数随年份变化情况")
        show_multi_years_and_1_area_teacher_0_count(year_list=year_list, area=area)

        st.info("学段教师数随年份变化情况")
        show_multi_years_and_1_area_teacher_0_period(year_list=year_list, area=area)


def show_multi_years_and_1_area_teacher_0_count(year_list: list[str], area: str) -> None:
    """
    展示多年份教师数对比
    :param year_list: 年份列表
    :param area: 查询的单个片镇名
    :return:
    """

    df_container = get_multi_years_age_dataframe(year_list=year_list, area=area)

    left, right = st.columns(spec=2)

    with left:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="count_by_year"), title="", height=400)

    with right:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="growth_rate_by_year"), title="", height=400,
                            mark_line_y=0, formatter="{value} %")

    draw_mixed_bar_and_line(
        df_bar=df_container.get_dataframe(name="age_and_year"),
        df_line=df_container.get_dataframe(name="age_growth_rate_and_year"),
        bar_axis_label="人数",
        line_axis_label="增长率",
        # line_max_=300,
        # line_min_=-400,
        mark_line_y=0,
        line_formatter="{value} %"
    )

    return None


def get_multi_years_age_dataframe(year_list: list[str], area: str) -> DataFrameContainer:
    """
    根据年份列表生成多个年龄统计dataframe，放置在container中\n
    age_and_year：所有数据，列为年龄，行为年份\n
    age_growth_rate_and_year：所有数据对年龄求增长率，列为年龄，行为年份（存疑）\n
    count_by_year：每年的总人数，列为年份，单行\n
    growth_rate_by_year：原dataframe中每一年相对于上一年的总增长率（年份总人数增长率，不考虑年龄），列为年份，单行\n
    :param year_list: 查询的年份列表
    :param area: 查询的片镇名
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为年龄列

    for year in year_list:

        df1[year] = {}  # 初始化该年份的子字典
        """
        df_dict:{
        "2024":{
            25:100,
            26:200
            },
        "2023"：{
            25：50，
            24：100
            }
        }
        """

        id_list = del_tuple_in_list(
            data=execute_sql_sentence(
                sentence=f'select "身份证号" from teacher_data_0_{year} where "区域" = "{area}"'
            )
        )

        for item in id_list:

            age = str(get_age_from_citizen_id(citizen_id=item, year=year))

            if age == "0":
                print_color_text(item)
                print_color_text(year)

            if age in df1[year].keys():
                df1[year][age] += 1
            else:
                df1[year][age] = 1

    df1 = sort_dataframe_columns(df=convert_dict_to_dataframe(d=df1))
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="age_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe("age_growth_rate_and_year", df=df2)

    df3 = pd.DataFrame(df1.sum(axis="columns")).T
    df3.index = ["总人数"]
    container.add_dataframe(name="count_by_year", df=df3)

    df4 = get_growth_rate_from_one_row_dataframe(df=df3)
    df4.index = ["增长率"]

    container.add_dataframe(name="growth_rate_by_year", df=df4)

    return container


def show_multi_years_and_1_area_teacher_0_period(year_list: list[str], area: str) -> None:
    """
    展示多年份不同学段教师数对比
    :param year_list: 年份列表
    :param area: 片镇名
    :return:
    """
    df_container = get_multi_years_and_1_area_period_dataframe(year_list=year_list, area=area)

    left, right = st.columns(spec=2)

    with left:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="period_and_year").T, title="", height=400, )

    with right:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="period_growth_rate_and_year").T, title="", height=400,
                            mark_line_y=0, formatter="{value} %")

    draw_mixed_bar_and_line(
        df_bar=df_container.get_dataframe(name="period_and_year"),
        df_line=df_container.get_dataframe(name="period_growth_rate_and_year"),
        bar_axis_label="人数",
        line_axis_label="增长率",
        line_max_=20,
        line_min_=-20,
        mark_line_y=0,
        line_formatter="{value} %"
    )

    return None


def get_multi_years_and_1_area_period_dataframe(year_list: list[str], area: str) -> DataFrameContainer:
    """
    根据年份列表生成多个学段统计dataframe，放置在container中\n
    period_and_year：所有数据，列为学段，行为年份\n
    period_growth_rate_and_year：所有数据对学段求增长率，行为增长率对应年份，列为学段，单行\n
    :param year_list: 查询的年份列表
    :param area: 片镇名
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为学段列

    for year in year_list:

        df1[year] = {}  # 初始化该年份的子字典
        """
        df_dict:{
        "2024":{
            "高中":100,
            "初中":200
            },
        "2023"：{
            "高中"：50，
            "初中"：100
            }
        }
        """
        period_count_list = execute_sql_sentence(
            sentence=f'select "任教学段", count(*) from teacher_data_0_{year} where "区域" = "{area}" and "任教学段" in ({', '.join([f'"{period}"' for period in get_period_list() if period != "高中"])}) group by "任教学段"'
        )

        for item in period_count_list:
            df1[year][item[0]] = item[1]

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=[period for period in get_period_list() if period != "高中"])
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="period_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe(name="period_growth_rate_and_year", df=df2)

    return container


def show_1_year_and_multi_areas_teacher_0(year_list: list[str]) -> None:
    pass


def show_multi_years_and_multi_areas_teacher_0(year_list: list[str]) -> None:
    pass


if __name__ == '__main__':
    # get_multi_years_and_1_area_period_dataframe(year_list=["2023", "2024"], area="永平")
    pass
