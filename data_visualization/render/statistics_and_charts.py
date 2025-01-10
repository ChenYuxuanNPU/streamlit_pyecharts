from calculation.retirement import *
from data_visualization.tool.func import *


def get_1_year_age_and_gender_dataframe(year: str, area: str = None, school: str = None,
                                        period: str = None) -> DataFrameContainer:
    """
    根据年份生成列为年龄，行为性别的dataframe\n
    data: 二维dataframe，包含性别和年龄\n
    sum: 一维dataframe，包含年龄和人数总和
    :param year: 查询的年份（必填）
    :param area: 查询的片镇（选填）
    :param school: 查询的学校（选填）
    :param period: 查询的学段（选填）
    :return:
    """

    container = DataFrameContainer()

    df_dict = {"男": {}, "女": {}}  # 使用嵌套字典保存数据，外层为性别行，内层为年龄列
    ages = set()  # 用于检查age_dict中是否有对应的年龄

    min_age = 1000
    max_age = -1

    id_list = execute_sql_sentence(
        sentence=f'select "身份证号", "性别" from teacher_data_0_{year} where 1{f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''}'
    )

    for item in id_list:

        age = str(get_age_from_citizen_id(citizen_id=item[0], year=year))

        min_age = int(age) if int(age) < min_age else min_age
        max_age = int(age) if int(age) > max_age else max_age

        if age not in ages:

            for gender in ["男", "女"]:
                df_dict[gender][age] = 0

        df_dict[item[1]][age] += 1

        ages.add(age)

    for age in range(min_age, max_age):

        if str(age) not in df_dict["男"].keys():
            df_dict["男"][str(age)] = 0

        if str(age) not in df_dict["女"].keys():
            df_dict["女"][str(age)] = 0

    container.add_dataframe(name="data", df=sort_dataframe_columns(df=convert_dict_to_dataframe(d=df_dict)))

    df = pd.DataFrame(sort_dataframe_columns(df=convert_dict_to_dataframe(d=df_dict)).sum()).T
    df.index = ["合计"]

    container.add_dataframe("sum", df=df)

    return container


def get_1_year_grad_school_dataframe(year: str, area: str = None, school: str = None,
                                     period: str = None) -> DataFrameContainer:
    """
    根据年份多个包含院校名及其频率的dataframe\n
    df_985:985院校名及其数量\n
    df_nettp:国优计划院校名及其数量\n
    df_affiliate:部属师范院校名及其数量\n
    df_211:211院校名及其数量\n
    :param year: 查询的年份（必填）
    :param area: 查询的片镇（选填）
    :param school: 查询的学校（选填）
    :param period: 查询的学段（选填）
    :return:
    """
    container = DataFrameContainer()

    try:
        container.add_dataframe(
            name="df_985",
            df=pd.Series(
                dict(
                    execute_sql_sentence(
                        sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0_{year} where "参加工作前毕业院校代码" in ({', '.join([f'"{code}"' for code in get_school_codes()["985"]])}){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
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

    except TypeError as e:
        if "Cannot use method 'nlargest' with dtype object" in str(e):
            st.toast(f'无985院校毕业生', icon="😟")
            container.add_dataframe(
                name="df_985",
                df=pd.DataFrame(data=["0"], columns=["人数"], index=["无"]).rename_axis(["985院校"])
            )
        else:
            print(e)

    try:
        container.add_dataframe(
            name="df_nettp",
            df=pd.Series(
                dict(
                    execute_sql_sentence(
                        sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0_{year} where "参加工作前毕业院校代码" in ({', '.join([f'"{code}"' for code in get_school_codes()["国优计划"]])}){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
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

    except TypeError as e:
        if "Cannot use method 'nlargest' with dtype object" in str(e):
            st.toast(f'无国优计划院校毕业生', icon="😟")
            container.add_dataframe(
                name="df_nettp",
                df=pd.DataFrame(data=["0"], columns=["人数"], index=["无"]).rename_axis(["国优计划院校"])
            )
        else:
            print(e)

    try:
        container.add_dataframe(
            name="df_affiliate",
            df=pd.Series(
                dict(
                    execute_sql_sentence(
                        sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0_{year} where "参加工作前毕业院校代码" in ({', '.join([f'"{code}"' for code in get_school_codes()["部属师范"]])}){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
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

    except TypeError as e:
        if "Cannot use method 'nlargest' with dtype object" in str(e):
            st.toast(f'无部属师范院校毕业生', icon="😟")
            container.add_dataframe(
                name="df_affiliate",
                df=pd.DataFrame(data=["0"], columns=["人数"], index=["无"]).rename_axis(["部属师范院校"])
            )
        else:
            print(e)

    try:
        container.add_dataframe(
            name="df_211",
            df=pd.Series(
                dict(
                    execute_sql_sentence(
                        sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0_{year} where "参加工作前毕业院校代码" in ({', '.join([f'"{code}"' for code in get_school_codes()["211"]])}){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
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

    except TypeError as e:
        if "Cannot use method 'nlargest' with dtype object" in str(e):
            st.toast(f'无211院校毕业生', icon="😟")
            container.add_dataframe(
                name="df_211",
                df=pd.DataFrame(data=["0"], columns=["人数"], index=["无"]).rename_axis(["211院校"])
            )
        else:
            print(e)

    container.add_dataframe(
        name="df_all",
        df=pd.Series(
            dict(
                execute_sql_sentence(
                    sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0_{year} where "参加工作前毕业院校代码" not in ({', '.join([f'"{code}"' for code in ["无", "51161", "51315"]])}){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
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


def get_1_year_discipline_and_gender_dataframe(year: str, area: str = None, school: str = None,
                                               period: str = None) -> DataFrameContainer:
    """
    根据年份生成列为学科，行为性别的dataframe
    :param year: 查询的年份（必填）
    :param area: 查询的片镇（选填）
    :param school: 查询的学校（选填）
    :param period: 查询的学段（选填）
    :return:
    """

    container = DataFrameContainer()

    df_dict = {"男": {}, "女": {}}  # 使用嵌套字典保存数据，外层为性别行，内层为学科列

    discipline_list = del_tuple_in_list(
        execute_sql_sentence(
            sentence=f'select "主教学科", count(*) from teacher_data_0_{year} where "主教学科" != "无"{f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} group by "主教学科" order by count(*) desc limit 16'
        )
    )

    for discipline in discipline_list:
        data = execute_sql_sentence(
            sentence=f'select "性别", count(*) from teacher_data_0_{year} where "主教学科" = "{discipline}"{f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} group by "性别"'
        )

        for item in data:
            df_dict[item[0]][discipline] = item[1]

    container.add_dataframe(name="data", df=convert_dict_to_dataframe(d=df_dict))
    df = pd.DataFrame(convert_dict_to_dataframe(d=df_dict).sum()).T
    df.index = ["合计"]
    container.add_dataframe(name="sum", df=df)

    return container


def get_1_year_and_multi_areas_or_schools_teacher_0_age_dataframe(year: str, area_list: list[str] = None,
                                                                  school_list: list[str] = None,
                                                                  period: str = None) -> DataFrameContainer:
    """
    根据给定的范围列表生成单个年龄统计dataframe，放置在container中\n
    age_and_location：所有数据，列为年龄，行为片镇或学校\n
    age_percentage_and_location: 所有年龄占片镇占比，列为年龄，行为片镇
    :param year: 查询的年份
    :param area_list: 查询的片镇列表
    :param school_list: 查询的学校列表
    :param period: 任教学段
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()

    min_age = 1000
    max_age = -1

    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为年龄列
    df1.update({location: {} for location in (area_list if area_list is not None else school_list)})  # 初始化该年份的子字典

    df2_values_sum = {}
    df2_values_sum.update(
        {a: 0 for a in (area_list if area_list is not None else school_list)})  # 计算每一个范围当年的总人数，用于计算某个年龄的占比

    id_list = execute_sql_sentence(
        sentence=f'select "身份证号", "{'区域' if area_list is not None else '校名'}" from teacher_data_0_{year} where "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}"' if period is not None else ''}'
    )

    """
    df_dict:{
    "永平":{
        25:100,
        26:200
        },
    "石井"：{
        25：50，
        24：100
        }
    }
    """

    for item in id_list:

        age = str(get_age_from_citizen_id(citizen_id=item[0], year=year))

        min_age = int(age) if int(age) < min_age else min_age
        max_age = int(age) if int(age) > max_age else max_age

        if age == "0":
            print_color_text(item[0])
            print_color_text(year)

        if age in df1[item[1]].keys():
            df1[item[1]][age] += 1
        else:
            df1[item[1]][age] = 1

        df2_values_sum[item[1]] += 1

    for location in (area_list if area_list is not None else school_list):
        for age in range(min_age, max_age + 1):

            if str(age) not in df1[location].keys():
                df1[location][str(age)] = 0

    df2 = df1
    df1 = sort_dataframe_columns(df=convert_dict_to_dataframe(d=df1))
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="age_and_location", df=df1)

    for location in (area_list if area_list is not None else school_list):
        for age in df2[location].keys():
            df2[location][age] = round(number=100 * float(
                (df2[location][age] / df2_values_sum[location] if df2_values_sum[location] != 0 else 0)), ndigits=1)

    df2 = sort_dataframe_columns(df=convert_dict_to_dataframe(d=df2))
    df2.fillna(value=0, inplace=True)
    container.add_dataframe(name="age_percentage_and_location", df=df2)

    return container


def get_1_year_and_multi_areas_or_schools_teacher_0_edu_bg_dataframe(year: str, area_list: list[str] = None,
                                                                     school_list: list[str] = None,
                                                                     period: str = None) -> DataFrameContainer:
    """
    根据片镇列表生成单个学历统计dataframe，放置在container中\n
    edu_bg_and_location：所有数据，列为学历，行为范围\n
    edu_bg_percentage_and_location: 所有学历占范围占比，列为学历，行为范围
    :param year: 查询的年份
    :param area_list: 查询的片镇列表
    :param school_list: 查询的学校列表
    :param period: 任教学段
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()

    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为学历列
    """
    df_dict:{
    "永平":{
        "本科":100,
        "硕士研究生":200
        },
    "石井"：{
        "本科"：50，
        "硕士研究生"：100
        }
    }
    """
    df1.update({location: {} for location in (area_list if area_list is not None else school_list)})  # 初始化该年份的子字典

    df2_values_sum = {}
    df2_values_sum.update({location: {} for location in
                           (area_list if area_list is not None else school_list)})  # 计算每一个范围当年的总人数，用于计算某个学历的占比

    edu_bg_list = execute_sql_sentence(
        sentence=f'select "最高学历", "{'区域' if area_list is not None else '校名'}", count(*) from teacher_data_0_{year} where "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}" ' if period is not None else ' '}and "最高学历" in ({', '.join([f'"{bg}"' for bg in get_edu_bg_list()])}) group by "最高学历", "{'区域' if area_list is not None else '校名'}"'
    )

    count_list = execute_sql_sentence(
        sentence=f'select "{'区域' if area_list is not None else '校名'}", count(*) from teacher_data_0_{year} where "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}" ' if period is not None else ' '}group by "{'区域' if area_list is not None else '校名'}"'
    )

    for item in edu_bg_list:
        df1[item[1]][item[0]] = item[2]

        df2_values_sum[item[1]][item[0]] = round(
            number=100 * float(item[2] / list(x[1] for x in count_list if x[0] == item[1])[0]),
            ndigits=1
        )

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=get_edu_bg_list())
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="edu_bg_and_location", df=df1)

    df2 = convert_dict_to_dataframe(d=df2_values_sum).reindex(columns=get_edu_bg_list())
    df2.fillna(value=0, inplace=True)
    container.add_dataframe(name="edu_bg_percentage_and_location", df=df2)

    return container


def get_1_year_and_multi_areas_or_schools_teacher_0_vocational_level_detail_dataframe(year: str,
                                                                                      area_list: list[str] = None,
                                                                                      school_list: list[str] = None,
                                                                                      period: str = None) -> DataFrameContainer:
    """
    根据范围列表生成单个专技等级统计dataframe，放置在container中\n
    vocational_level_detail_and_location：所有数据，列为专技等级，行为范围\n
    vocational_level_detail_percentage_and_location: 所有专技等级占范围占比，列为专技等级，行为范围
    :param year: 查询的年份
    :param area_list: 查询的片镇列表
    :param school_list: 查询的学校列表
    :param period: 任教学段
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()

    df1 = {}
    df1.update({location: {} for location in (area_list if area_list is not None else school_list)})  # 初始化该年份的子字典

    df2_values_sum = {}
    df2_values_sum.update({location: {} for location in (area_list if area_list is not None else school_list)})

    vocational_level_detail_list = execute_sql_sentence(
        sentence=f'select "专业技术岗位", "{'区域' if area_list is not None else '校名'}", count(*) from teacher_data_0_{year} where "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}" ' if period is not None else ' '}and "专业技术岗位" in ({', '.join([f'"{d}"' for d in get_vocational_level_detail_list()])}) group by "专业技术岗位", "{'区域' if area_list is not None else '校名'}"'
    )

    count_list = execute_sql_sentence(
        sentence=f'select "{'区域' if area_list is not None else '校名'}", count(*) from teacher_data_0_{year} where "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}" ' if period is not None else ' '}group by "{'区域' if area_list is not None else '校名'}"'
    )

    for item in vocational_level_detail_list:
        df1[item[1]][item[0]] = item[2]

        df2_values_sum[item[1]][item[0]] = round(
            number=100 * float(item[2] / list(x[1] for x in count_list if x[0] == item[1])[0]),
            ndigits=1
        )

    df1 = convert_dict_to_dataframe(d=df1)
    df1.fillna(value=0, inplace=True)
    df1 = df1.reindex(columns=shorten_vocational_level_detail_dict()).rename(
        columns=shorten_vocational_level_detail_dict())
    container.add_dataframe(name="vocational_level_detail_and_location", df=df1)

    df2 = convert_dict_to_dataframe(d=df2_values_sum)
    df2.fillna(value=0, inplace=True)
    df2 = df2.reindex(columns=shorten_vocational_level_detail_dict()).rename(
        columns=shorten_vocational_level_detail_dict())
    container.add_dataframe(name="vocational_level_detail_percentage_and_location", df=df2)

    return container


def get_1_year_and_multi_areas_or_schools_teacher_0_discipline_dataframe(year: str,
                                                                         area_list: list[str] = None,
                                                                         school_list: list[str] = None,
                                                                         period: str = None) -> DataFrameContainer:
    """
    根据范围列表生成学科人数统计dataframe，放置在container中\n
    discipline_and_location：所有数据，列为学科，行为范围\n
    discipline_percentage_and_location: 所有学科占范围占比，列为学科，行为范围
    :param year: 查询的年份
    :param area_list: 查询的片镇列表
    :param school_list: 查询的学校列表
    :param period: 任教学段
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()

    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为学科列
    df1.update({location: {} for location in (area_list if area_list is not None else school_list)})  # 初始化该年份的子字典

    df2_values_sum = {}
    df2_values_sum.update({location: {} for location in
                           (area_list if area_list is not None else school_list)})  # 计算每一个范围当年的总人数，用于计算某个学科的占比

    discipline_detail_list = execute_sql_sentence(
        sentence=f'select "主教学科", "{'区域' if area_list is not None else '校名'}", count(*) from teacher_data_0_{year} where "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}" ' if period is not None else ' '}and "主教学科" in ({', '.join([f'"{d}"' for d in get_discipline_list()])}) group by "主教学科", "{'区域' if area_list is not None else '校名'}"'
    )

    count_list = execute_sql_sentence(
        sentence=f'select "{'区域' if area_list is not None else '校名'}", count(*) from teacher_data_0_{year} where "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}" ' if period is not None else ' '}group by "{'区域' if area_list is not None else '校名'}"'
    )

    for item in discipline_detail_list:
        df1[item[1]][item[0]] = item[2]

        df2_values_sum[item[1]][item[0]] = round(
            number=100 * float(item[2] / list(x[1] for x in count_list if x[0] == item[1])[0]),
            ndigits=1
        )

    df1 = convert_dict_to_dataframe(d=df1)
    df1 = df1.reindex(columns=get_discipline_list())
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="discipline_and_location", df=df1)

    df2 = convert_dict_to_dataframe(d=df2_values_sum)
    df2 = df2.reindex(columns=get_discipline_list())
    df2.fillna(value=0, inplace=True)
    df2 = df2.loc[:, ~(df2 == 0).all()]
    container.add_dataframe(name="discipline_percentage_and_location", df=df2)

    return container


def get_1_year_and_multi_areas_or_schools_teacher_0_grad_school_level_dataframe(year: str,
                                                                                area_list: list[str] = None,
                                                                                school_list: list[str] = None,
                                                                                period: str = None) -> DataFrameContainer:
    """
    根据范围列表生成毕业院校类型人数统计dataframe，放置在container中\n
    grad_school_id_and_location: 所有数据，列为毕业院校id，行为范围\n
    grad_school_kind_and_location: 分类数据，列为毕业院校级别，行为范围\n
    grad_school_percentage_and_location: 所有学科占范围占比，列为毕业院校级别，行为范围
    :param year: 查询的年份
    :param area_list: 查询的片镇列表
    :param school_list: 查询的学校列表
    :param period: 任教学段
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()

    df0 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为学历列
    df0.update({location: {} for location in (area_list if area_list is not None else school_list)})

    grad_school_id_list = []

    query_parts = []
    for location in (area_list if area_list is not None else school_list):
        query_part = f'select "{location}", "参加工作前毕业院校代码" from teacher_data_0_{year} where "{'区域' if area_list is not None else '校名'}" = "{location}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生")'
        query_parts.append(query_part)

    final_query = " union all ".join(query_parts)

    grad_school_id_list.extend(
        item for item in execute_sql_sentence(
            sentence=final_query
        )
    )

    count_dict = dict(
        execute_sql_sentence(
            sentence=f'select "{'区域' if area_list is not None else '校名'}", count(*) from teacher_data_0_{year} where "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}" ' if period is not None else ' '}group by "{'区域' if area_list is not None else '校名'}"'
        )
    )

    for item in grad_school_id_list:
        if item[1] not in df0[item[0]].keys():
            df0[item[0]][item[1]] = 1
        else:
            df0[item[0]][item[1]] += 1

    df1 = convert_dict_to_dataframe(d=df0)
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="grad_school_id_and_location", df=df1)

    df2 = {}
    df3 = {}
    for location in (area_list if area_list is not None else school_list):
        df2[location] = {item: 0. for item in ["985院校", "国优计划院校", "部属师范院校", "211院校", "其他院校"]}
        df3[location] = {item: 0. for item in ["985院校", "国优计划院校", "部属师范院校", "211院校", "其他院校"]}

    for item in grad_school_id_list:
        for kind in distinguish_school_id(school_id=item[1], label_length="long"):
            df2[item[0]][kind] += 1

    for location, item in df2.items():
        for key, value in item.items():
            if location in count_dict.keys():
                df3[location][key] = round(
                    number=100 * float(value / count_dict[location]),
                    ndigits=1
                )

    df2 = convert_dict_to_dataframe(d=df2)
    df2.fillna(value=0, inplace=True)
    df2 = df2.loc[:, ~(df2 == 0).all()]  # 删除全为0的列
    container.add_dataframe(name="grad_school_kind_and_location", df=df2)

    df3 = convert_dict_to_dataframe(d=df3)
    df3.fillna(value=0, inplace=True)
    df3 = df3.loc[:, ~(df3 == 0).all()]  # 删除全为0的列
    container.add_dataframe(name="grad_school_percentage_and_location", df=df3)

    return container


if __name__ == '__main__':
    container1 = get_1_year_and_multi_areas_or_schools_teacher_0_age_dataframe(year="2024",
                                                                               school_list=["广州市培英中学",
                                                                                            "广州市实验外语学校"])
    print(container1.get_dataframe("age_and_location"))
