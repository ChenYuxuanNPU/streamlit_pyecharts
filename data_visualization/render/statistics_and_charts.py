from calculation.retirement import *
from data_visualization.tool.func import *


def get_base_data() -> dict:
    """
    获取全区学校数据
    :return:
    """
    return load_json_data(folder="result", file_name="school_info")


def get_multi_years_student(year_list: list) -> pd.DataFrame:
    """
    用于获取多年份的学生数量对比
    :param year_list: 需要对比所用的年份列表
    :return:
    """

    data = execute_sql_sentence(
        sentence=f'select "采集年份", "学段", "合计学生数" from school_data_sum where "学段" in ("合计", "高级中学", "初级中学", "小学", "幼儿园") and "采集年份" in ({', '.join([f'"{year}"' for year in year_list])})'
    )

    dict_for_df = {year: {"幼儿园": 0, "小学": 0, "初级中学": 0, "高级中学": 0, "合计": 0} for year in year_list}

    for item in data:
        dict_for_df[item[0]][item[1]] = int(item[2])

    return convert_dict_to_dataframe(d=dict_for_df).T.reindex(columns=year_list[::-1])


def get_multi_years_class(year_list: list) -> pd.DataFrame:
    """
    用于获取多年份的班额数量对比
    :param year_list: 需要对比所用的年份列表
    :return:
    """

    data = execute_sql_sentence(
        sentence=f'select "采集年份", "学段", "合计班额数" from school_data_sum where "学段" in ("合计", "高级中学", "初级中学", "小学", "幼儿园") and "采集年份" in ({', '.join([f'"{year}"' for year in year_list])})'
    )

    dict_for_df = {year: {"幼儿园": 0, "小学": 0, "初级中学": 0, "高级中学": 0, "合计": 0} for year in year_list}

    for item in data:
        dict_for_df[item[0]][item[1]] = int(item[2])

    return convert_dict_to_dataframe(d=dict_for_df).T.reindex(columns=year_list[::-1])


def get_multi_years_full_time_teacher(year_list: list) -> pd.DataFrame:
    """
    用于获取多年份的学年初报表专任教师数
    :param year_list: 需要对比所用的年份列表
    :return:
    """

    data = execute_sql_sentence(
        sentence=f'select "采集年份", "学段", "合计专任教师数" from school_data_sum where "学段" in ("合计", "十二年一贯制学校", "完全中学", "高级中学", "九年一贯制学校", "初级中学", "小学", "幼儿园") and "采集年份" in ({', '.join([f'"{year}"' for year in year_list])})'
    )

    dict_for_df = {year: {"幼儿园": 0, "小学": 0, "初级中学": 0, "高级中学": 0, "合计": 0} for year in year_list}

    for item in data:

        if item[1] in dict_for_df[item[0]].keys():
            dict_for_df[item[0]][item[1]] += int(item[2])

        elif item[1] in ["初级中学", "九年一贯制学校"]:
            dict_for_df[item[0]]["初级中学"] += int(item[2])

        elif item[1] in ["高级中学", "完全中学", "十二年一贯制学校"]:
            dict_for_df[item[0]]["高级中学"] += int(item[2])

        else:
            print_color_text(text=f'学年初报表中专任教师数有误：{item}')

    return convert_dict_to_dataframe(d=dict_for_df).T.reindex(columns=year_list[::-1])


def get_multi_years_full_time_teacher_to_class_ratio(year_list: list) -> pd.DataFrame:
    """
    用于获取多年份的学年初报表班师比（平均每个班拥有多少名教师）
    :param year_list:
    :return:
    """

    return round(get_multi_years_full_time_teacher(year_list=year_list) / get_multi_years_class(year_list=year_list),
                 2).drop("合计")


def get_multi_years_student_to_full_time_teacher_ratio(year_list: list) -> pd.DataFrame:
    """
    用于获取多年份的学年初报表生师比（平均每个教师教多少学生）
    :param year_list:
    :return:
    """

    return round(get_multi_years_student(year_list=year_list) / get_multi_years_full_time_teacher(year_list=year_list),
                 2).drop("合计")


def get_1_year_teacher_0_age_and_gender_dataframe(year: str, area: str = None, school: str = None,
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
        sentence=f'select "身份证号", "性别" from teacher_data_0 where "采集年份" = "{year}"{f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''}'
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


def get_1_year_teacher_0_grad_school_dataframe(year: str, area: str = None, school: str = None,
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
                        sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0 where "采集年份" = "{year}" and "参加工作前毕业院校代码" in ({', '.join([f'"{code}"' for code in get_school_codes()["985"]])}){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
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
                        sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0 where "采集年份" = "{year}" and "参加工作前毕业院校代码" in ({', '.join([f'"{code}"' for code in get_school_codes()["国优计划"]])}){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
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
                        sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0 where "采集年份" = "{year}" and "参加工作前毕业院校代码" in ({', '.join([f'"{code}"' for code in get_school_codes()["部属师范"]])}){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
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
                        sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0 where "采集年份" = "{year}" and "参加工作前毕业院校代码" in ({', '.join([f'"{code}"' for code in get_school_codes()["211"]])}){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
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
                    sentence=f'select "参加工作前毕业院校代码",count(*) from teacher_data_0 where "采集年份" = "{year}" and "参加工作前毕业院校代码" not in ({', '.join([f'"{code}"' for code in ["无", "51161", "51315"]])}){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生") group by "参加工作前毕业院校代码"'
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


def get_1_year_teacher_0_discipline_and_gender_dataframe(year: str, area: str = None, school: str = None,
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
            sentence=f'select "主教学科", count(*) from teacher_data_0 where "采集年份" = "{year}" and "主教学科" != "无"{f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} group by "主教学科" order by count(*) desc limit 16'
        )
    )

    data = execute_sql_sentence(
        sentence=f'select "主教学科", "性别", count(*) from teacher_data_0 where "采集年份" = "{year}" and "主教学科" in ({', '.join([f'"{discipline}"' for discipline in discipline_list])}){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} group by "主教学科", "性别"'
    )

    for item in data:
        df_dict[item[1]][item[0]] = item[2]

    df1 = convert_dict_to_dataframe(d=df_dict).reindex(columns=get_discipline_list())
    df1 = fillnan_and_del_0_lines_in_df(df=df1)
    container.add_dataframe(name="data", df=df1)

    df2 = pd.DataFrame(df1.sum()).T
    df2.index = ["合计"]
    container.add_dataframe(name="sum", df=df2)

    return container


def get_1_year_and_multi_locations_teacher_0_age_dataframe(year: str, area_list: list[str] = None,
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
        sentence=f'select "身份证号", "{'区域' if area_list is not None else '校名'}" from teacher_data_0 where "采集年份" = "{year}" and "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}"' if period is not None else ''}'
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
    df1 = fillnan_and_del_0_lines_in_df(df=df1)
    container.add_dataframe(name="age_and_location", df=df1)

    for location in (area_list if area_list is not None else school_list):
        for age in df2[location].keys():
            df2[location][age] = round(number=100 * float(
                (df2[location][age] / df2_values_sum[location] if df2_values_sum[location] != 0 else 0)), ndigits=1)

    df2 = sort_dataframe_columns(df=convert_dict_to_dataframe(d=df2))
    df2 = fillnan_and_del_0_lines_in_df(df=df2)
    container.add_dataframe(name="age_percentage_and_location", df=df2)

    return container


def get_1_year_and_multi_locations_teacher_0_edu_bg_dataframe(year: str, area_list: list[str] = None,
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
        sentence=f'select "最高学历", "{'区域' if area_list is not None else '校名'}", count(*) from teacher_data_0 where "采集年份" = "{year}" and "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}" ' if period is not None else ' '}and "最高学历" in ({', '.join([f'"{bg}"' for bg in get_edu_bg_list()])}) group by "最高学历", "{'区域' if area_list is not None else '校名'}"'
    )

    count_list = execute_sql_sentence(
        sentence=f'select "{'区域' if area_list is not None else '校名'}", count(*) from teacher_data_0 where "采集年份" = "{year}" and "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}" ' if period is not None else ' '}group by "{'区域' if area_list is not None else '校名'}"'
    )

    for item in edu_bg_list:
        df1[item[1]][item[0]] = item[2]

        df2_values_sum[item[1]][item[0]] = round(
            number=100 * float(item[2] / list(x[1] for x in count_list if x[0] == item[1])[0]),
            ndigits=1
        )

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=get_edu_bg_list())
    df1 = fillnan_and_del_0_lines_in_df(df=df1)
    container.add_dataframe(name="edu_bg_and_location", df=df1)

    df2 = convert_dict_to_dataframe(d=df2_values_sum).reindex(columns=get_edu_bg_list())
    df2 = fillnan_and_del_0_lines_in_df(df=df2)
    container.add_dataframe(name="edu_bg_percentage_and_location", df=df2)

    return container


def get_1_year_and_multi_locations_teacher_0_vocational_level_detail_dataframe(year: str,
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
        sentence=f'select "专业技术岗位", "{'区域' if area_list is not None else '校名'}", count(*) from teacher_data_0 where "采集年份" = "{year}" and "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}" ' if period is not None else ' '}and "专业技术岗位" in ({', '.join([f'"{d}"' for d in get_vocational_level_detail_list()])}) group by "专业技术岗位", "{'区域' if area_list is not None else '校名'}"'
    )

    count_list = execute_sql_sentence(
        sentence=f'select "{'区域' if area_list is not None else '校名'}", count(*) from teacher_data_0 where "采集年份" = "{year}" and "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}" ' if period is not None else ' '}group by "{'区域' if area_list is not None else '校名'}"'
    )

    for item in vocational_level_detail_list:
        df1[item[1]][item[0]] = item[2]

        df2_values_sum[item[1]][item[0]] = round(
            number=100 * float(item[2] / list(x[1] for x in count_list if x[0] == item[1])[0]),
            ndigits=1
        )

    df1 = convert_dict_to_dataframe(d=df1)
    # df1 = df1.reindex(columns=shorten_vocational_level_detail_dict()).rename(
    #     columns=shorten_vocational_level_detail_dict())
    df1 = df1[[col for col in shorten_vocational_level_detail_dict().keys() if col in df1.columns]].rename(
        columns=shorten_vocational_level_detail_dict())
    df1 = fillnan_and_del_0_lines_in_df(df=df1)
    container.add_dataframe(name="vocational_level_detail_and_location", df=df1)

    df2 = convert_dict_to_dataframe(d=df2_values_sum)
    # df2 = df2.reindex(columns=shorten_vocational_level_detail_dict()).rename(
    #     columns=shorten_vocational_level_detail_dict())
    df2 = df2[[col for col in shorten_vocational_level_detail_dict().keys() if col in df2.columns]].rename(
        columns=shorten_vocational_level_detail_dict())
    df2 = fillnan_and_del_0_lines_in_df(df=df2)
    container.add_dataframe(name="vocational_level_detail_percentage_and_location", df=df2)

    return container


def get_1_year_and_multi_locations_teacher_0_discipline_dataframe(year: str,
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
        sentence=f'select "主教学科", "{'区域' if area_list is not None else '校名'}", count(*) from teacher_data_0 where "采集年份" = "{year}" and "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}" ' if period is not None else ' '}and "主教学科" in ({', '.join([f'"{d}"' for d in get_discipline_list()])}) group by "主教学科", "{'区域' if area_list is not None else '校名'}"'
    )

    count_list = execute_sql_sentence(
        sentence=f'select "{'区域' if area_list is not None else '校名'}", count(*) from teacher_data_0 where "采集年份" = "{year}" and "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}" ' if period is not None else ' '}group by "{'区域' if area_list is not None else '校名'}"'
    )

    for item in discipline_detail_list:
        df1[item[1]][item[0]] = item[2]

        df2_values_sum[item[1]][item[0]] = round(
            number=100 * float(item[2] / list(x[1] for x in count_list if x[0] == item[1])[0]),
            ndigits=1
        )

    df1 = convert_dict_to_dataframe(d=df1)
    df1 = df1.reindex(columns=get_discipline_list())
    df1 = fillnan_and_del_0_lines_in_df(df=df1)
    container.add_dataframe(name="discipline_and_location", df=df1)

    df2 = convert_dict_to_dataframe(d=df2_values_sum)
    df2 = df2.reindex(columns=get_discipline_list())
    df2 = fillnan_and_del_0_lines_in_df(df=df2)
    container.add_dataframe(name="discipline_percentage_and_location", df=df2)

    return container


def get_1_year_and_multi_locations_teacher_0_grad_school_level_dataframe(year: str,
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
        query_part = f'select "{location}", "参加工作前毕业院校代码" from teacher_data_0 where "采集年份" = "{year}" and "{'区域' if area_list is not None else '校名'}" = "{location}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生")'
        query_parts.append(query_part)

    final_query = " union all ".join(query_parts)

    grad_school_id_list.extend(
        item for item in execute_sql_sentence(
            sentence=final_query
        )
    )

    count_dict = dict(
        execute_sql_sentence(
            sentence=f'select "{'区域' if area_list is not None else '校名'}", count(*) from teacher_data_0 where "采集年份" = "{year}" and "{'区域' if area_list is not None else '校名'}" in ({', '.join([f'"{location}"' for location in (area_list if area_list is not None else school_list)])}){f' and "任教学段" = "{period}" ' if period is not None else ' '}group by "{'区域' if area_list is not None else '校名'}"'
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
        df2[location] = {item: 0 for item in ["985院校", "国优计划院校", "部属师范院校", "211院校", "其他院校"]}
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
    df2 = fillnan_and_del_0_lines_in_df(df=df2)
    container.add_dataframe(name="grad_school_kind_and_location", df=df2)

    df3 = convert_dict_to_dataframe(d=df3)
    df3 = fillnan_and_del_0_lines_in_df(df=df3)
    container.add_dataframe(name="grad_school_percentage_and_location", df=df3)

    return container


def get_multi_years_teacher_0_age_dataframe(year_list: list[str], area: str = None, school: str = None,
                                            period: str = None) -> DataFrameContainer:
    """
    根据年份列表生成多个年龄统计dataframe，放置在container中\n
    age_and_year：所有数据，列为年龄，行为年份\n
    age_growth_rate_and_year：所有数据对年龄求增长率，列为年龄，行为年份（存疑）\n
    count_by_year：每年的总人数，列为年份，单行\n
    growth_rate_by_year：原dataframe中每一年相对于上一年的总增长率（年份总人数增长率，不考虑年龄），列为年份，单行\n
    :param year_list: 查询的年份列表
    :param area: 查询的片镇名
    :param school: 查询的校名
    :param period: 查询的学段
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为年龄列

    min_age = 1000
    max_age = -1

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

    id_list = execute_sql_sentence(
        sentence=f'select "采集年份", "身份证号" from teacher_data_0 where "采集年份" in ({", ".join([f'"{year}"' for year in year_list])}){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''}'
    )

    for item in id_list:

        age = str(get_age_from_citizen_id(citizen_id=item[1], year=item[0]))

        min_age = int(age) if int(age) < min_age else min_age
        max_age = int(age) if int(age) > max_age else max_age

        if age == "0":
            print_color_text(item)

        if age in df1[item[0]].keys():
            df1[item[0]][age] += 1
        else:
            df1[item[0]][age] = 1

    #  填充空年龄列
    for year in year_list:

        for age in range(min_age, max_age):

            if str(age) not in df1[year].keys():
                df1[year][str(age)] = 0

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


def get_multi_years_teacher_0_area_dataframe(year_list: list[str]) -> DataFrameContainer:
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
        df1[year] = {item: 0 for item in get_area_list()}  # 初始化该年份的子字典
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
        sentence=f'select "采集年份", "区域", count(*) from teacher_data_0 where "采集年份" in ({", ".join([f'"{year}"' for year in year_list])}) and "区域" in ({", ".join([f'"{area}"' for area in get_area_list()])}) group by "采集年份", "区域"'
    )

    for item in area_count_list:
        df1[item[0]][item[1]] = item[2]

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=get_area_list())
    df1.fillna(value=0, inplace=True)
    container.add_dataframe(name="area_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe("area_growth_rate_and_year", df=df2)

    return container


def get_multi_years_teacher_0_period_dataframe(year_list: list[str], area: str = None,
                                               school: str = None, ) -> DataFrameContainer:
    """
    根据年份列表生成多个学段统计dataframe，放置在container中\n
    period_and_year：所有数据，列为学段，行为年份\n
    period_growth_rate_and_year：所有数据对学段求增长率，行为增长率对应年份，列为学段，单行\n
    :param year_list: 查询的年份列表
    :param area: 查询的片镇
    :param school: 查询的学校
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为学段列

    for year in year_list:
        df1[year] = {item: 0 for item in get_period_list()}  # 初始化该年份的子字典
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
        sentence=f'select "采集年份", "任教学段", count(*) from teacher_data_0 where "采集年份" in ({", ".join([f'"{year}"' for year in year_list])}) and "任教学段" in ({', '.join([f'"{period}"' for period in get_period_list()])}){f' and "区域" = "{area}" ' if area is not None else ' '}{f' and "校名" = "{school}" ' if school is not None else ' '}group by "采集年份", "任教学段"'
    )

    for item in period_count_list:
        df1[item[0]][item[1]] = item[2]

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=get_period_list())
    df1 = fillnan_and_del_0_lines_in_df(df=df1)
    container.add_dataframe(name="period_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe(name="period_growth_rate_and_year", df=df2)

    return container


def get_multi_years_teacher_0_edu_bg_dataframe(year_list: list[str], area: str = None, school: str = None,
                                               period: str = None) -> DataFrameContainer:
    """
    根据年份列表生成多个学历统计dataframe，放置在container中\n
    edu_bg_and_year：所有数据，列为学历，行为年份\n
    edu_bg_growth_rate_and_year：所有数据对学历求增长率，行为增长率对应年份，列为学历，单行\n
    :param year_list: 查询的年份列表
    :param area: 查询的片镇
    :param school: 查询的学校
    :param period: 查询的学段
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为学历列

    for year in year_list:
        df1[year] = {item: 0 for item in get_edu_bg_list()}  # 初始化该年份的子字典
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
        sentence=f'select "采集年份", "最高学历", count(*) from teacher_data_0 where "采集年份" in ({", ".join([f'"{year}"' for year in year_list])}) and "最高学历" in ({', '.join([f'"{bg}"' for bg in get_edu_bg_list()])}){f' and "区域" = "{area}" ' if area is not None else ' '}{f' and "校名" = "{school}" ' if school is not None else ' '}{f' and "任教学段" = "{period}" ' if period is not None else ' '}group by "采集年份", "最高学历"'
    )

    for item in edu_bg_count_list:
        df1[item[0]][item[1]] = item[2]

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=get_edu_bg_list())
    df1 = fillnan_and_del_0_lines_in_df(df=df1)
    container.add_dataframe(name="edu_bg_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe("edu_bg_growth_rate_and_year", df=df2)

    return container


def get_multi_years_teacher_0_vocational_level_dataframe(year_list: list[str], area: str = None, school: str = None,
                                                         period: str = None) -> DataFrameContainer:
    """
    根据年份列表生成多个教师级别、专业技术级别统计dataframe，放置在container中\n
    vocational_level_and_year：所有数据，列为教师级别，行为年份\n
    vocational_level_growth_rate_and_year：所有数据对教师级别求增长率，行为增长率对应年份，列为教师级别，单行\n
    vocational_level_detail_and_year：所有数据，列为专技级别，行为年份\n
    vocational_level_detail_growth_rate_and_year：所有数据对专技级别求增长率，行为增长率对应年份，列为专技级别，单行\n
    :param year_list: 查询的年份列表
    :param area: 查询的片镇
    :param school: 查询的学校
    :param period: 查询的学段
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df1 = {}  # 使用嵌套字典保存数据，外层为年份行，内层为年龄列
    df3 = {}

    for year in year_list:
        df1[year] = {item: 0 for item in get_vocational_level_list()}
        df3[year] = {item: 0 for item in get_vocational_level_detail_list()}
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
        sentence=f'select "采集年份", "最高职称", count(*) from teacher_data_0 where "采集年份" in ({", ".join([f'"{year}"' for year in year_list])}) and "最高职称" in ({', '.join([f'"{level}"' for level in get_vocational_level_list()])}){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} group by "采集年份", "最高职称"'
    )

    vocational_level_detail_count_list = execute_sql_sentence(
        sentence=f'select "采集年份", "专业技术岗位", count(*) from teacher_data_0 where "采集年份" in ({", ".join([f'"{year}"' for year in year_list])}) and "专业技术岗位" in ({', '.join([f'"{level}"' for level in get_vocational_level_detail_list()])}){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} group by "采集年份", "专业技术岗位"'
    )

    for item in vocational_level_count_list:
        df1[item[0]][item[1]] = item[2]

    for item in vocational_level_detail_count_list:
        df3[item[0]][item[1]] = item[2]

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=get_vocational_level_list())
    df1 = fillnan_and_del_0_lines_in_df(df=df1)
    container.add_dataframe(name="vocational_level_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe("vocational_level_growth_rate_and_year", df=df2)

    df3 = convert_dict_to_dataframe(d=df3).reindex(columns=get_vocational_level_detail_list())
    df3 = fillnan_and_del_0_lines_in_df(df=df3)
    container.add_dataframe(name="vocational_level_detail_and_year", df=df3)

    df4 = df3[[col for col in shorten_vocational_level_detail_dict().keys() if col in df3.columns]].rename(
        columns=shorten_vocational_level_detail_dict())
    df4 = fillnan_and_del_0_lines_in_df(df=df4)
    container.add_dataframe(name="shorten_vocational_level_detail_and_year", df=df4)

    df5 = get_growth_rate_from_multi_rows_dataframe(df=df3)
    container.add_dataframe("vocational_level_detail_growth_rate_and_year", df=df5)

    df6 = df5[[col for col in shorten_vocational_level_detail_dict().keys() if col in df5.columns]].rename(
        columns=shorten_vocational_level_detail_dict())
    # df6 = fillnan_and_del_0_lines_in_df(df=df6)
    container.add_dataframe(name="shorten_vocational_level_detail_growth_rate_and_year", df=df6)

    return container


def get_multi_years_teacher_0_discipline_dataframe(year_list: list[str], area: str = None, school: str = None,
                                                   period: str = None) -> DataFrameContainer:
    """
    根据年份列表生成多个学科统计dataframe，放置在container中\n
    discipline_and_year：所有数据，列为学科，行为年份\n
    discipline_growth_rate_and_year：所有数据对学科求增长率，行为增长率对应年份，列为学科，单行\n
    :param year_list: 查询的年份列表
    :param area: 查询的片镇
    :param school: 查询的学校
    :param period: 查询的学段
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
        sentence=f'select "采集年份", "主教学科", count(*) from teacher_data_0 where "采集年份" in ({", ".join([f'"{year}"' for year in year_list])}) and "主教学科" in ({', '.join([f'"{discipline}"' for discipline in get_discipline_list()])}){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''} group by "采集年份", "主教学科"'
    )

    for item in discipline_count_list:
        df1[item[0]][item[1]] = item[2]

    df1 = convert_dict_to_dataframe(d=df1).reindex(columns=get_discipline_list())
    df1 = fillnan_and_del_0_lines_in_df(df=df1)
    container.add_dataframe(name="discipline_and_year", df=df1)

    df2 = get_growth_rate_from_multi_rows_dataframe(df=df1)
    container.add_dataframe("discipline_growth_rate_and_year", df=df2)

    return container


def get_multi_years_teacher_0_grad_school_dataframe(year_list: list[str], area: str = None, school: str = None,
                                                    period: str = None) -> DataFrameContainer:
    """
    根据年份列表生成多个学科统计dataframe，放置在container中\n
    grad_school_id_and_year：所有数据，列为院校代码，行为年份\n
    grad_school_kind_and_year：所有数据，列为院校类型，行为年份\n
    grad_school_kind_growth_rate_and_year：所有数据对院校类型求增长率，行为增长率对应年份，列为院校类型，单行\n
    :param year_list: 查询的年份列表
    :param area: 查询的片镇
    :param school: 查询的学校
    :param period: 查询的学段
    :return: DataFrameContainer，包含若干个dataframe
    """
    container = DataFrameContainer()
    df0 = {year: {} for year in year_list}  # 使用嵌套字典保存数据，外层为年份行，内层为学历列

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

    grad_school_id_list = execute_sql_sentence(
        sentence=f'select "采集年份", "参加工作前毕业院校代码" from teacher_data_0 where "采集年份" in ({", ".join([f'"{year}"' for year in year_list])}) and "参加工作前学历" in ("本科", "硕士研究生", "博士研究生"){f' and "区域" = "{area}"' if area is not None else ''}{f' and "校名" = "{school}"' if school is not None else ''}{f' and "任教学段" = "{period}"' if period is not None else ''}'
    )

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
        for kind in distinguish_school_id(school_id=item[1], label_length="long"):
            df2[item[0]][kind] += 1

    df2 = convert_dict_to_dataframe(d=df2)
    df2.fillna(value=0, inplace=True)
    container.add_dataframe(name="grad_school_kind_and_year", df=df2)

    df3 = get_growth_rate_from_multi_rows_dataframe(df=df2)
    container.add_dataframe("grad_school_kind_growth_rate_and_year", df=df3)

    return container


if __name__ == '__main__':
    pass
