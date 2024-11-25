from calculation.retirement import *
from data_visualization.tool.func import *
from teacher_data_processing.read_database.get_database_data import \
    generate_sql_sentence as generate_sql_sentence_teacher


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


def get_area_list() -> list[str]:
    """
    片镇列表：["永平", "石井", "新市", "江高", "人和", "太和", "钟落潭"]
    :return:
    """

    return ["直管", "永平", "石井", "新市", "江高", "人和", "太和", "钟落潭"]


def get_period_list() -> list[str]:
    """
    学段列表：["高中", "初中", "小学", "幼儿园"]
    :return:
    """
    return ["高中", "初中", "小学", "幼儿园"]


def get_edu_bg_list() -> list[str]:
    """
    学历列表：["专科", "本科", "硕士研究生", "博士研究生"]
    :return:
    """
    return ["专科", "本科", "硕士研究生", "博士研究生"]


def get_vocational_level_list() -> list[str]:
    """
    职称列表：["三级教师", "二级教师", "一级教师", "高级教师", "正高级教师"]
    :return:
    """
    return ["三级教师", "二级教师", "一级教师", "高级教师", "正高级教师"]


def get_vocational_level_detail_list() -> list[str]:
    """
    专业技术等级列表：["专业技术十三级", "试用期（未定级）", "专业技术十二级", "专业技术十一级", "专业技术十级", "专业技术九级", "专业技术八级", "专业技术七级", "专业技术六级", "专业技术五级", "专业技术四级", ]
    :return:
    """
    return ["专业技术十三级", "试用期（未定级）", "专业技术十二级", "专业技术十一级", "专业技术十级",
            "专业技术九级", "专业技术八级", "专业技术七级", "专业技术六级", "专业技术五级", "专业技术四级", ]


def get_discipline_list() -> list[str]:
    """
    学科列表：["语文", "数学", "英语", "思想政治", "历史", "地理", "物理", "化学", "生物", "体育", "音乐", "美术", "科学", "信息技术", "通用技术", "劳动", "心理健康"]
    :return:
    """
    return [
        "语文", "数学", "英语", "思想政治", "历史", "地理", "物理", "化学", "生物", "体育", "音乐", "美术",
        "科学", "信息技术", "通用技术", "劳动", "心理健康"
    ]


def get_grad_school_list() -> list[str]:
    """
    毕业院校类型列表：["985院校", "部属师范院校", "211院校"]
    :return:
    """
    return ["985院校", "部属师范院校", "211院校"]


def get_1_year_grad_school_dataframe(year: str) -> DataFrameContainer:
    """
    根据年份多个包含院校名及其频率的dataframe\n
    df_985:985院校名及其数量\n
    df_nettp:国优计划院校名及其数量\n
    df_affiliate:部属师范院校名及其数量\n
    df_211:211院校名及其数量\n
    :param year: 查询的年份
    :return:
    """
    container = DataFrameContainer()

    container.add_dataframe(
        name="df_985",
        df=pd.Series(
            dict(
                execute_sql_sentence(
                    sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0_{year} where "参加工作前毕业院校代码" in {tuple(get_school_codes()["985"])} and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
                )
            )
        )
        .nlargest(20).to_frame()
        .rename(
            index={
                key: value[0] for key, value in load_json_data(folder="source", file_name="院校代码").items()
            },
            columns={0: "人数"}
        )
        .rename_axis(["985院校"])
    )

    container.add_dataframe(
        name="df_nettp",
        df=pd.Series(
            dict(
                execute_sql_sentence(
                    sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0_{year} where "参加工作前毕业院校代码" in {tuple(get_school_codes()["国优计划"])} and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
                )
            )
        )
        .nlargest(20).to_frame()
        .rename(
            index={
                key: value[0] for key, value in load_json_data(folder="source", file_name="院校代码").items()
            },
            columns={0: "人数"}
        )
        .rename_axis(["国优计划院校"])
    )

    container.add_dataframe(
        name="df_affiliate",
        df=pd.Series(
            dict(
                execute_sql_sentence(
                    sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0_{year} where "参加工作前毕业院校代码" in {tuple(get_school_codes()["部属师范"])} and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
                )
            )
        )
        .nlargest(20).to_frame()
        .rename(
            index={
                key: value[0] for key, value in load_json_data(folder="source", file_name="院校代码").items()
            },
            columns={0: "人数"}
        )
        .rename_axis(["部属师范院校"])
    )

    container.add_dataframe(
        name="df_211",
        df=pd.Series(
            dict(
                execute_sql_sentence(
                    sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0_{year} where "参加工作前毕业院校代码" in {tuple(get_school_codes()["211"])} and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
                )
            )
        )
        .nlargest(20).to_frame()
        .rename(
            index={
                key: value[0] for key, value in load_json_data(folder="source", file_name="院校代码").items()
            },
            columns={0: "人数"}
        )
        .rename_axis(["211院校"])
    )

    container.add_dataframe(
        name="df_all",
        df=pd.Series(
            dict(
                execute_sql_sentence(
                    sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0_{year} where "参加工作前毕业院校代码" not in {tuple(["无", "51161", "51315"])} and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
                )
            )
        )
        .nlargest(100).to_frame()
        .rename(
            index={
                key: value[0] for key, value in load_json_data(folder="source", file_name="院校代码").items()
            },
            columns={0: "人数"}
        )
        .rename_axis(["所有院校"])
    )

    return container


def get_1_year_age_and_gender_dataframe(year: str, ) -> DataFrameContainer:
    """
    根据年份生成列为年龄，行为性别的dataframe
    :param year: 查询的年份
    :return:
    """

    container = DataFrameContainer()

    df_dict = {"男": {}, "女": {}}  # 使用嵌套字典保存数据，外层为性别行，内层为年龄列
    ages = set()  # 用于检查age_dict中是否有对应的年龄

    id_list = execute_sql_sentence(
        sentence=generate_sql_sentence_teacher(kind="在编", info_num=2, info=["身份证号", "性别"], scope="全区",
                                               year=year)
    )

    for item in id_list:

        age = str(get_age_from_citizen_id(citizen_id=item[0], year=year))

        if age not in ages:

            for gender in ["男", "女"]:
                df_dict[gender][age] = 0

        df_dict[item[1]][age] += 1

        ages.add(age)

    container.add_dataframe(name="data", df=sort_dataframe_columns(df=convert_dict_to_dataframe(d=df_dict)))

    df = pd.DataFrame(sort_dataframe_columns(df=convert_dict_to_dataframe(d=df_dict)).sum()).T
    df.index = ["合计"]

    container.add_dataframe("sum", df=df)

    return container


def get_1_year_discipline_and_gender_dataframe(year: str, ) -> DataFrameContainer:
    """
    根据年份生成列为学科，行为性别的dataframe
    :param year: 查询的年份
    :return:
    """

    container = DataFrameContainer()

    df_dict = {"男": {}, "女": {}}  # 使用嵌套字典保存数据，外层为性别行，内层为学科列

    discipline_list = del_tuple_in_list(
        execute_sql_sentence(
            sentence=generate_sql_sentence_teacher(kind="在编", info_num=1, info=["主教学科"], scope="全区",
                                                   year=year, limit=16, order="desc",
                                                   additional_requirement=['"主教学科" != "无"'])
        )
    )

    for discipline in discipline_list:
        data = execute_sql_sentence(
            sentence=generate_sql_sentence_teacher(kind="在编", info_num=1, info=["性别"], scope="全区",
                                                   year=year, additional_requirement=[f'"主教学科" = "{discipline}"'])
        )

        for item in data:
            df_dict[item[0]][discipline] = item[1]

    container.add_dataframe(name="data", df=convert_dict_to_dataframe(d=df_dict))
    df = pd.DataFrame(convert_dict_to_dataframe(d=df_dict).sum()).T
    df.index = ["合计"]
    container.add_dataframe(name="sum", df=df)

    return container


def get_multi_years_age_dataframe(year_list: list[str], ) -> DataFrameContainer:
    """
    根据年份列表生成多个年龄统计dataframe，放置在container中\n
    age_and_year：所有数据，列为年龄，行为年份\n
    age_growth_rate_and_year：所有数据对年龄求增长率，列为年龄，行为年份（存疑）\n
    count_by_year：每年的总人数，列为年份，单行\n
    growth_rate_by_year：原dataframe中每一年相对于上一年的总增长率（年份总人数增长率，不考虑年龄），列为年份，单行\n
    :param year_list: 查询的年份列表
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
                sentence=generate_sql_sentence_teacher(kind="在编", info_num=0, info=["身份证号"], scope="全区",
                                                       year=year)
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

    # print("")
    # print("总人数的dataframe：")
    # print("")
    # print(f"df1:{df1}")
    # print("")
    # print(f"df2:{df2}")
    # print("")
    # print(f"df3:{df3}")
    # print("")
    # print(f"df4:{df4}")
    # print("")

    return container


def get_multi_years_area_dataframe(year_list: list[str]) -> DataFrameContainer:
    """
    根据年份列表生成多个片镇统计dataframe，放置在container中\n
    area_and_year：所有数据，列为片镇，行为年份\n
    area_growth_rate_and_year：所有数据对片镇求增长率，行为增长率对应年份，列为片镇名，单行\n
    :param year_list: 查询的年份列表
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为片镇列

    for year in year_list:

        df1[year] = {}  # 初始化该年份的子字典
        """
        df_dict:{
        "2024":{
            "永平":100,
            "江高":200
            },
        "2023"：{
            "永平"：50，
            "江高"：100
            }
        }
        """
        area_count_list = execute_sql_sentence(
            sentence=generate_sql_sentence_teacher(kind="在编", info_num=1, info=["区域"], scope="全区",
                                                   year=year,
                                                   additional_requirement=[f'"区域" in {str(tuple(get_area_list()))}'])
        )

        for item in area_count_list:
            df1[year][item[0]] = item[1]

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=get_area_list())
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="area_and_year", df=df1)
    # print(df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe("area_growth_rate_and_year", df=df2)
    # print(df2)

    return container


def get_multi_years_period_dataframe(year_list: list[str]) -> DataFrameContainer:
    """
    根据年份列表生成多个学段统计dataframe，放置在container中\n
    period_and_year：所有数据，列为学段，行为年份\n
    period_growth_rate_and_year：所有数据对学段求增长率，行为增长率对应年份，列为学段，单行\n
    :param year_list: 查询的年份列表
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
            sentence=generate_sql_sentence_teacher(kind="在编", info_num=1, info=["任教学段"], scope="全区",
                                                   year=year, additional_requirement=[
                    f'"任教学段" in {str(tuple(get_period_list()))}'])
        )

        for item in period_count_list:
            df1[year][item[0]] = item[1]

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=get_period_list())
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="period_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe(name="period_growth_rate_and_year", df=df2)

    return container


def get_multi_years_edu_bg_dataframe(year_list: list[str]) -> DataFrameContainer:
    """
    根据年份列表生成多个学历统计dataframe，放置在container中\n
    edu_bg_and_year：所有数据，列为学历，行为年份\n
    edu_bg_growth_rate_and_year：所有数据对学历求增长率，行为增长率对应年份，列为学历，单行\n
    :param year_list: 查询的年份列表
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为学历列

    for year in year_list:

        df1[year] = {}  # 初始化该年份的子字典
        """
        df_dict:{
        "2024":{
            "本科":100,
            "硕士研究生":200
            },
        "2023"：{
            "本科"：50，
            "硕士研究生"：100
            }
        }
        """
        edu_bg_count_list = execute_sql_sentence(
            sentence=generate_sql_sentence_teacher(kind="在编", info_num=1, info=["最高学历"], scope="全区",
                                                   year=year, additional_requirement=[
                    f'"最高学历" in {str(tuple(get_edu_bg_list()))}'])
        )

        for item in edu_bg_count_list:
            df1[year][item[0]] = item[1]

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=get_edu_bg_list())
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="edu_bg_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe("edu_bg_growth_rate_and_year", df=df2)

    return container


def get_multi_years_vocational_level_dataframe(year_list: list[str]) -> DataFrameContainer:
    """
    根据年份列表生成多个教师级别、专业技术级别统计dataframe，放置在container中\n
    vocational_level_and_year：所有数据，列为教师级别，行为年份\n
    vocational_level_growth_rate_and_year：所有数据对教师级别求增长率，行为增长率对应年份，列为教师级别，单行\n
    vocational_level_detail_and_year：所有数据，列为专技级别，行为年份\n
    vocational_level_detail_growth_rate_and_year：所有数据对专技级别求增长率，行为增长率对应年份，列为专技级别，单行\n
    :param year_list: 查询的年份列表
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为年龄列
    df3 = {}

    for year in year_list:

        df1[year] = {}  # 初始化该年份的子字典
        df3[year] = {}
        """
        df_dict:{
        "2024":{
            "一级教师":100,
            "二级教师":200
            },
        "2023"：{
            "一级教师"：50，
            "二级教师"：100
            }
        }
        """
        vocational_level_count_list = execute_sql_sentence(
            sentence=generate_sql_sentence_teacher(kind="在编", info_num=1, info=["最高职称"], scope="全区",
                                                   year=year, additional_requirement=[
                    f'"最高职称" in {str(tuple(get_vocational_level_list()))}'])
        )

        for item in vocational_level_count_list:
            df1[year][item[0]] = item[1]

        vocational_level_detail_count_list = execute_sql_sentence(
            sentence=generate_sql_sentence_teacher(kind="在编", info_num=1, info=["专业技术岗位"], scope="全区",
                                                   year=year, additional_requirement=[
                    f'"专业技术岗位" in {str(tuple(get_vocational_level_detail_list()))}'])
        )

        for item in vocational_level_detail_count_list:
            df3[year][item[0]] = item[1]

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=get_vocational_level_list())
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="vocational_level_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe("vocational_level_growth_rate_and_year", df=df2)

    df3 = convert_dict_to_dataframe(d=df3).reindex(columns=get_vocational_level_detail_list())
    df3.fillna(value=0, inplace=True)
    container.add_dataframe(name="vocational_level_detail_and_year", df=df3)

    df4 = get_growth_rate_from_multi_rows_dataframe(df=df3)
    container.add_dataframe("vocational_level_detail_growth_rate_and_year", df=df4)

    return container


def get_multi_years_discipline_dataframe(year_list: list[str]) -> DataFrameContainer:
    """
    根据年份列表生成多个学科统计dataframe，放置在container中\n
    discipline_and_year：所有数据，列为学科，行为年份\n
    discipline_growth_rate_and_year：所有数据对学科求增长率，行为增长率对应年份，列为学科，单行\n
    :param year_list: 查询的年份列表
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为学历列

    for year in year_list:

        df1[year] = {}  # 初始化该年份的子字典
        """
        df_dict:{
        "2024":{
            "语文":100,
            "数学":200
            },
        "2023"：{
            "语文"：50，
            "数学"：100
            }
        }
        """
        discipline_count_list = execute_sql_sentence(
            sentence=generate_sql_sentence_teacher(kind="在编", info_num=1, info=["主教学科"], scope="全区",
                                                   year=year, additional_requirement=[
                    f'"主教学科" in {str(tuple(get_discipline_list()))}'])
        )

        for item in discipline_count_list:
            df1[year][item[0]] = item[1]

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=get_discipline_list())
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="discipline_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe("discipline_growth_rate_and_year", df=df2)

    return container


def get_multi_years_grad_school_dataframe(year_list: list[str]) -> DataFrameContainer:
    """
    根据年份列表生成多个学科统计dataframe，放置在container中\n
    grad_school_id_and_year：所有数据，列为院校代码，行为年份\n
    grad_school_kind_and_year：所有数据，列为院校类型，行为年份\n
    grad_school_kind_growth_rate_and_year：所有数据对院校类型求增长率，行为增长率对应年份，列为院校类型，单行\n
    :param year_list: 查询的年份列表
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df0 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为学历列
    grad_school_id_list = []

    for year in year_list:
        df0[year] = {}  # 初始化该年份的子字典
        """
        df_dict:{
        "2024":{
            "10699":100,
            "10558":200
            },
        "2023"：{
            "10699"：50，
            "10558"：100
            }
        }
        """

        grad_school_id_list.extend(item for item in execute_sql_sentence(
            # todo:以后改了sql生成函数记得改这里
            # sentence=generate_sql_sentence_teacher(kind="在编", info_num=0, info=["参加工作前毕业院校代码"],
            #                                        scope="全区", year=year,
            #                                        additional_requirement=['("参加工作前学历" in ("本科", "硕士研究生", "博士研究生"))'])
            sentence=f'select  "{year}","参加工作前毕业院校代码"  from teacher_data_0_{year}  where ("参加工作前学历" in ("本科", "硕士研究生", "博士研究生"))'
        ))

    for item in grad_school_id_list:
        if item[1] not in df0[item[0]].keys():
            df0[item[0]][item[1]] = 1
        else:
            df0[item[0]][item[1]] += 1

    df1 = convert_dict_to_dataframe(d=df0)
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="grad_school_id_and_year", df=df1)

    df2 = {}
    for year in year_list:
        df2[year] = {item: 0 for item in ["985院校", "国优计划院校", "部属师范院校", "211院校", "其他院校"]}

    for item in grad_school_id_list:
        for kind in distinguish_school_id(item[1]):
            df2[item[0]][kind] += 1

    df2 = convert_dict_to_dataframe(d=df2)
    df2.fillna(value=0, inplace=True)
    container.add_dataframe(name="grad_school_kind_and_year", df=df2)
    # print(df2)

    df3 = get_growth_rate_from_multi_rows_dataframe(df=df2)
    container.add_dataframe("grad_school_kind_growth_rate_and_year", df=df3)
    # print(df3)

    return container


def show_1_year_given_period(year: str, period: str) -> None:
    """
    展示某一年某一学段的在编教师信息
    :param year: 年份
    :param period: 学段
    :return:
    """

    data = load_json_data(folder="result", file_name="teacher_info")

    st.info(f"在编{period}信息", icon="😋")

    with st.container(border=False):
        c0, c1 = st.columns([2, 1])

        with c0:
            draw_bar_chart(data=data[year]["在编"]["全区"][period]["主教学科"], title="主教学科",
                           end=get_end_dict()[period])

        with c1:
            draw_pie_chart(data=data[year]["在编"]["全区"][period]["年龄"], title="年龄", pos_left="15%",
                           center_to_bottom="64%")

        c0, c1, c2 = st.columns(spec=3)

        with c0:
            draw_pie_chart(data=data[year]["在编"]["全区"][period]["最高学历"], title="最高学历")

        with c1:
            draw_bar_chart(data=data[year]["在编"]["全区"][period]["院校级别"], title="毕业院校",
                           is_show_visual_map=False)

        with c2:
            draw_pie_chart(data=data[year]["在编"]["全区"][period]["最高职称"], title="职称")


def show_1_year_all_period(year: str):
    """
    展示某一年所有学段的在编教师信息
    :param year: 年份
    :return:
    """
    data = load_json_data(folder="result", file_name="teacher_info")

    st.success(f"在编教职工总人数：{data[year]['在编']['全区']['所有学段']['总人数']}")

    with st.container(border=False):

        # 年龄性别柱状折线图，生成时要查询数据库，所以做个错误处理
        try:
            df_container = get_1_year_age_and_gender_dataframe(year=year)

            draw_mixed_bar_and_line(
                df_bar=df_container.get_dataframe(name="data"),
                df_line=df_container.get_dataframe(name="sum"),
                bar_axis_label="人数", line_axis_label="合计人数",
                mark_line_type="average"
            )
        except Exception as e:
            print_color_text("年龄柱状折线图展示异常")
            print(e)
            st.toast("年龄柱状折线图展示异常", icon="😕")

        c0, c1, c2 = st.columns(spec=3)

        with c0:
            # 在编片区统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["片区统计"], title="片区统计")

            # 在编学历统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["最高学历"], title="最高学历")

        with c1:
            # 在编学段统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["学段统计"], title="学段统计")

            # 在编职称统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["最高职称"], title="职称")

        with c2:
            # 在编年龄统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["年龄"], title="年龄",
                           pos_left="15%",
                           center_to_bottom="64%")

            # 在编行政职务统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["行政职务"], title="行政职务",
                           center_to_bottom="68%")

        # 学科性别柱状折线图，生成时要查询数据库，所以做个错误处理
        try:
            df_container = get_1_year_discipline_and_gender_dataframe(year=year)

            draw_mixed_bar_and_line(
                df_bar=df_container.get_dataframe(name="data"),
                df_line=df_container.get_dataframe(name="sum"),
                bar_axis_label="人数", line_axis_label="合计人数",
                mark_line_type="average"
            )
        except Exception as e:
            print_color_text("学科柱状折线图展示异常")
            st.toast("学科柱状折线图展示异常", icon="😕")

        # 在编毕业院校统计
        draw_line_chart(data=pd.DataFrame([data["2023"]["在编"]["全区"]["所有学段"]["院校级别"]],
                                          columns=data["2023"]["在编"]["全区"]["所有学段"]["院校级别"].keys(),
                                          index=["人数"]), title="毕业院校", height=400)

        with st.container(border=True):
            df_container = get_1_year_grad_school_dataframe(year=year)
            a0, a1, a2, a3, a4 = st.columns(spec=5)
            with a0:
                st.dataframe(df_container.get_dataframe("df_985"), height=400, width=300)
            with a1:
                st.dataframe(df_container.get_dataframe("df_nettp"), height=400, width=300)
            with a2:
                st.dataframe(df_container.get_dataframe("df_affiliate"), height=400, width=300)
            with a3:
                st.dataframe(df_container.get_dataframe("df_211"), height=400, width=300)
            with a4:
                st.dataframe(df_container.get_dataframe("df_all"), height=400, width=300)

        c0, c1, c2 = st.columns(spec=3)

        with c0:
            # 在编骨干教师统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["骨干教师"], title="骨干教师")

        with c1:
            # 在编教师支教统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["支教地域"], title="支教地域")

        with c2:
            # 在编四名教师统计
            draw_pie_chart(data=data[year]["在编"]["全区"]["所有学段"]["四名工作室"], title="四名统计")

        # 教师分布前三十统计
        draw_bar_chart(data=data[year]["在编"]["全区"]["所有学段"]["教师分布前三十"], title="最多教师数",
                       end=100)

        # 在编教师数后三十的学校统计
        draw_bar_chart(data=data[year]["在编"]["全区"]["所有学段"]["教师分布后三十"], title="最少教师数",
                       end=100)


def show_1_year_teacher_0(year: str, ):
    """
    在编教师展示框架
    :param year: 年份
    :return:
    """
    data = load_json_data(folder="result", file_name="teacher_info")

    # 小标题
    st.markdown(
        body="<h2 style='text-align: center;'>在编教师数据</h2>",
        unsafe_allow_html=True
    )

    period_list = st.multiselect(
        label="请选择需要查询的学段",
        options=["所有学段"] + get_period_list(),
        default=["所有学段", get_period_list()[0]]  # 所有学段、高中
    )

    if "所有学段" in period_list:
        show_1_year_all_period(year=year)

    for item in get_period_list():
        if item in period_list:
            show_1_year_given_period(year=year, period=item)


def show_1_year_teacher_1(year: str):
    """
    展示某一年编外教师信息
    :param year: 年份
    :return:
    """
    data = load_json_data(folder="result", file_name="teacher_info")

    # 小标题
    st.markdown(
        body="<h2 style='text-align: center;'>编外教师数据</h2>",
        unsafe_allow_html=True
    )

    st.info(f"编外教职工总人数：{data[year]['编外']['全区']['所有学段']['总人数']}")

    c0, c1, c2 = st.columns(spec=3)

    with c0:
        # 编外片区统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["片区统计"], title="片区统计")

        # 编外学段统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["学段统计"], title="学段统计")

    with c1:
        # 编外学历统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["最高学历"], title="最高学历")

        # 编外职称统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["最高职称"], title="职称")

    with c2:
        # 编外骨干教师统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["骨干教师"], title="骨干教师")

        # 编外四名教师统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["四名工作室"], title="四名统计")

    # 教师分布统计
    draw_bar_chart(data=data[year]["编外"]["全区"]["所有学段"]["教师分布前三十"], title="最多教师数",
                   end=100)

    c0, c1, c2 = st.columns(spec=3)

    with c0:
        # 编外教师资格统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["所有学段"]["教师资格"], title="教师资格")

    with c1:
        # 编外中小学教师资格统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["中小学"]["教师资格"], title="中小学")

    with c2:
        # 编外幼儿园教师资格统计
        draw_pie_chart(data=data[year]["编外"]["全区"]["幼儿园"]["教师资格"], title="幼儿园")


def show_multi_years_teacher_0(year_list: list[str]) -> None:
    """
    展示年份对比功能中在编教师的信息
    :param year_list: 年份列表
    :return:
    """
    data = load_json_data(folder="result", file_name="teacher_info")

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


def show_multi_years_teacher_0_count(year_list: list[str]) -> None:
    """
    展示多年份教师数对比
    :param year_list: 年份列表
    :return:
    """

    df_container = get_multi_years_age_dataframe(year_list=year_list)

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


def show_multi_years_teacher_0_area(year_list: list[str]) -> None:
    """
    展示多年份片镇教师数对比
    :param year_list: 年份列表
    :return:
    """

    df_container = get_multi_years_area_dataframe(year_list=year_list)

    left, right = st.columns(spec=2)

    with left:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="area_and_year").T, title="", height=400, )

    with right:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="area_growth_rate_and_year").T, title="", height=400,
                            mark_line_y=0, formatter="{value} %")

    draw_mixed_bar_and_line(
        df_bar=df_container.get_dataframe(name="area_and_year"),
        df_line=df_container.get_dataframe(name="area_growth_rate_and_year"),
        bar_axis_label="人数",
        line_axis_label="增长率",
        line_max_=20,
        line_min_=-20,
        mark_line_y=0,
        line_formatter="{value} %"
    )

    return None


def show_multi_years_teacher_0_period(year_list: list[str]) -> None:
    """
    展示多年份不同学段教师数对比
    :param year_list: 年份列表
    :return:
    """
    df_container = get_multi_years_period_dataframe(year_list=year_list)

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


def show_multi_years_teacher_0_edu_bg(year_list: list[str]) -> None:
    """
    展示多年份教师学历对比
    :param year_list: 年份列表
    :return:
    """
    df_container = get_multi_years_edu_bg_dataframe(year_list=year_list)

    left, right = st.columns(spec=2)

    with left:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="edu_bg_and_year").T, title="", height=400, )

    with right:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="edu_bg_growth_rate_and_year").T, title="", height=400,
                            mark_line_y=0, formatter="{value} %")

    draw_mixed_bar_and_line(
        df_bar=df_container.get_dataframe(name="edu_bg_and_year"),
        df_line=df_container.get_dataframe(name="edu_bg_growth_rate_and_year"),
        bar_axis_label="人数",
        line_axis_label="增长率",
        line_max_=60,
        line_min_=-100,
        mark_line_y=0,
        line_formatter="{value} %"
    )

    return None


def show_multi_years_teacher_0_vocational_level(year_list: list[str]) -> None:
    """
    展示多年份教师专业技术级别对比
    :param year_list: 年份列表
    :return:
    """
    df_container = get_multi_years_vocational_level_dataframe(year_list=year_list)

    left, right = st.columns(spec=2)

    with left:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="vocational_level_and_year").T, title="", height=400, )

    with right:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="vocational_level_growth_rate_and_year").T, title="",
                            height=400,
                            mark_line_y=0, formatter="{value} %")

    draw_mixed_bar_and_line(
        df_bar=df_container.get_dataframe(name="vocational_level_detail_and_year"),
        df_line=df_container.get_dataframe(name="vocational_level_detail_growth_rate_and_year"),
        bar_axis_label="人数",
        line_axis_label="增长率",
        line_max_=60,
        line_min_=-100,
        mark_line_y=0,
        line_formatter="{value} %",
        x_axis_font_size=9
    )

    return None


def show_multi_years_teacher_0_discipline(year_list: list[str]) -> None:
    """
    展示多年份不同学科教师数对比
    :param year_list: 年份列表
    :return:
    """
    df_container = get_multi_years_discipline_dataframe(year_list=year_list)

    left, right = st.columns(spec=2)

    with left:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="discipline_and_year").T, title="", height=400, )

    with right:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="discipline_growth_rate_and_year").T, title="",
                            height=400,
                            mark_line_y=0, formatter="{value} %")

    draw_mixed_bar_and_line(
        df_bar=df_container.get_dataframe(name="discipline_and_year"),
        df_line=df_container.get_dataframe(name="discipline_growth_rate_and_year"),
        bar_axis_label="人数",
        line_axis_label="增长率",
        line_max_=50,
        line_min_=-100,
        mark_line_y=0,
        line_formatter="{value} %"
    )

    return None


def show_multi_years_teacher_0_grad_school(year_list: list[str]) -> None:
    """
    展示多年份教师毕业院校质量对比
    :param year_list: 年份列表
    :return:
    """

    df_container = get_multi_years_grad_school_dataframe(year_list=year_list)

    left, right = st.columns(spec=2)

    with left:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="grad_school_kind_and_year").T, title="", height=400, )

    with right:
        with st.container(border=True):
            draw_line_chart(data=df_container.get_dataframe(name="grad_school_kind_growth_rate_and_year").T, title="",
                            height=400,
                            mark_line_y=0, formatter="{value} %")

    draw_mixed_bar_and_line(
        df_bar=df_container.get_dataframe(name="grad_school_kind_and_year"),
        df_line=df_container.get_dataframe(name="grad_school_kind_growth_rate_and_year"),
        bar_axis_label="人数",
        line_axis_label="增长率",
        mark_line_y=0,
        # line_max_=65,
        # line_min_=-65,
        line_formatter="{value} %"
    )

    return None


if __name__ == '__main__':
    # container = get_1_year_grad_school_dataframe(year="2024")
    # print(container.get_dataframe("df_985"))
    pass
