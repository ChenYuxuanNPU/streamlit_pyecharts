from teacher_data_processing.tool.func import *


def update(year: str, kind: str = Literal["在编", "编外"], ) -> dict:
    """
    更新所有片区某一年某一类型教师的统计信息
    :param year: 年份
    :param kind: 在编或编外
    :return: 返回统计后生成的字典
    """

    json_data = load_json_data(folder="result", file_name="teacher_info")

    #  在字典中更新数据库查询结果
    for area in get_area_list():
        #  统计在编人员性别 - 分片区
        json_data = dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/性别",
                                    value=dict(
                                        execute_sql_sentence(
                                            sentence=f'select "性别", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}" group by "性别" order by count(*) asc')
                                    ),
                                    json_data=json_data)

        #  统计片区教师资格

        #  先统计没有教资的
        json_data = dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/教师资格/未持教师资格",
                                    value=execute_sql_sentence(
                                        sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}" and "教师资格学段" = "无"')[
                                        0][0],
                                    json_data=json_data)

        #  再统计有教资的
        json_data = dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/教师资格/持有教师资格",
                                    value=execute_sql_sentence(
                                        sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}" and "教师资格学段" != "无"')[
                                        0][0],
                                    json_data=json_data)

        #  统计片区教师资格 - 幼儿园

        #  先统计没有教资的
        json_data = dict_assignment(route=f"{year}/{kind}/片区/{area}/幼儿园/教师资格/未持教师资格",
                                    value=execute_sql_sentence(
                                        sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}" and "任教学段" = "幼儿园" and "教师资格学段" = "无"')[
                                        0][0],
                                    json_data=json_data)

        #  再统计有教资的
        json_data = dict_assignment(route=f"{year}/{kind}/片区/{area}/幼儿园/教师资格/持有教师资格",
                                    value=execute_sql_sentence(
                                        sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}" and "任教学段" = "幼儿园" and "教师资格学段" != "无"')[
                                        0][0],
                                    json_data=json_data)

        #  统计片区教师资格 - 中小学

        #  先统计没有教资的
        json_data = dict_assignment(route=f"{year}/{kind}/片区/{area}/中小学/教师资格/未持教师资格",
                                    value=execute_sql_sentence(
                                        sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}" and "教师资格学段" = "无" and "任教学段" != "幼儿园"')[
                                        0][0],
                                    json_data=json_data)

        #  再统计有教资的
        json_data = dict_assignment(route=f"{year}/{kind}/片区/{area}/中小学/教师资格/持有教师资格",
                                    value=execute_sql_sentence(
                                        sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}" and "教师资格学段" != "无" and "任教学段" != "幼儿园"')[
                                        0][0],
                                    json_data=json_data)

        #  统计片镇人数分布前十数量
        json_data = dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/教师分布前十",
                                    value=simplify_school_name(
                                        d=dict(
                                            execute_sql_sentence(
                                                sentence=f'select "校名", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}" and "学校类型" != "幼儿园" and "学校类型" != "教学支撑单位" group by "校名" order by count(*) desc limit 10'
                                            )
                                        )
                                    ),
                                    json_data=json_data)

        #  统计片镇人数分布倒数前十数量
        json_data = dict_assignment(route=f"{year}/{kind}/片区/{area}/所有学段/教师分布后十",
                                    value=simplify_school_name(
                                        d=dict(
                                            execute_sql_sentence(
                                                sentence=f'select "校名", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}" and "学校类型" != "幼儿园" and "学校类型" != "教学支撑单位" group by "校名" order by count(*) asc limit 10'
                                            )
                                        )
                                    ),
                                    json_data=json_data)

        json_data = period_update(json_data=json_data, area=area, year=year, kind=kind)

        if kind == "编外":
            json_data = data_01_unique(json_data=json_data, year=year, area=area)

    save_json_data(json_data=json_data, folder="result", file_name="teacher_info")

    return json_data


def data_00_unique(json_data: dict, year: str, area: str, kind: Literal["在编"] = "在编", period: str = None, ) -> dict:
    """
    更新在编特有的信息
    :param json_data: 更新基础数据后的字典
    :param year: 年份
    :param area: 片镇
    :param period: 学段
    :param kind: 是否在编
    :return: 更新在编特有数据后的字典
    """

    #  统计片区在编人员年龄
    json_data = dict_assignment(route=f"{year}/{kind}/片区/{area}/{period if period is not None else "所有学段"}/年龄",
                                value=age_statistics(
                                    age_count_list=execute_sql_sentence(
                                        sentence=f'select "年龄", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else " "}group by "年龄"')
                                ),
                                json_data=json_data)

    #  统计片区在编人员主教学科
    json_data = dict_assignment(
        route=f"{year}/{kind}/片区/{area}/{period if period is not None else "所有学段"}/主教学科",
        value=dict(
            execute_sql_sentence(
                sentence=f'select "主教学科", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else " "}and "主教学科" != "无" group by "主教学科" order by count(*) desc limit 20')
        ),
        json_data=json_data)

    #  统计全区在编人员专业技术岗位
    json_data = dict_assignment(
        route=f"{year}/{kind}/片区/{area}/{period if period is not None else "所有学段"}/专业技术岗位",
        value=dict(
            execute_sql_sentence(
                sentence=f'select "专业技术岗位", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else " "}group by "专业技术岗位"')
        ),
        json_data=json_data)

    #  统计片区在编人员行政职务
    json_data = dict_assignment(
        route=f"{year}/{kind}/片区/{area}/{period if period is not None else "所有学段"}/行政职务",
        value=dict(
            sorted(
                execute_sql_sentence(
                    sentence=f'select "行政职务", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else " "}group by "行政职务"'),
                key=lambda x: get_current_administrative_position_order()[x[0]]
            )
        ),
        json_data=json_data)

    #  统计片区在编人员院校级别
    json_data = dict_assignment(
        route=f"{year}/{kind}/片区/{area}/{period if period is not None else "所有学段"}/院校级别",
        value=count_school_id(
            data=execute_sql_sentence(
                sentence=f'select "参加工作前毕业院校代码" from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else " "}and ("参加工作前学历" in ("本科", "硕士研究生", "博士研究生"))'
            ),
            label_length="short"
        ),
        json_data=json_data)

    #  统计片区在编人员支教地域
    json_data = dict_assignment(
        route=f"{year}/{kind}/片区/{area}/{period if period is not None else "所有学段"}/支教地域",
        value=dict(
            sorted(
                execute_sql_sentence(
                    sentence=f'select "支教地域", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else " "}group by "支教地域"'
                ),
                key=lambda x: get_area_of_supporting_education_order()[x[0]]
            )
        ),
        json_data=json_data)

    #  统计片区四名工作室主持人

    #  这里统计有多少是主持人
    json_data = dict_assignment(
        route=f"{year}/{kind}/片区/{area}/{period if period is not None else "所有学段"}/四名工作室/四名工作室主持人",
        value=execute_sql_sentence(
            sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year}  where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else " "}and "四名工作室主持人" != "无"')[
            0][0],
        json_data=json_data)

    #  这里统计有多少不是主持人
    json_data = dict_assignment(
        route=f"{year}/{kind}/片区/{area}/{period if period is not None else "所有学段"}/四名工作室/无",
        value=execute_sql_sentence(
            sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else " "}and "四名工作室主持人" = "无"')[
            0][0],
        json_data=json_data)

    #  统计片区骨干教师
    json_data = dict_assignment(
        route=f"{year}/{kind}/片区/{area}/{period if period is not None else "所有学段"}/骨干教师",
        value=combine_none_and_others(
            dict(
                sorted(
                    execute_sql_sentence(
                        sentence=f'select "骨干教师", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else " "}group by "骨干教师"'
                    ),
                    key=lambda x: get_cadre_teacher_order()[x[0]]
                )
            )
        ),
        json_data=json_data)

    return json_data


def data_01_unique(json_data: dict, year: str, area: str, kind: Literal["编外"] = "编外") -> dict:
    """
    更新编外特有的信息
    :param json_data: 更新基础数据后的字典
    :param year: 年份
    :param area: 片镇
    :param kind: 是否在编
    :return: 更新编外特有数据后的字典
    """

    return json_data


def period_update(json_data: dict, area: str, year: str, kind: str = "在编") -> dict:
    """
    更新在编不同学段的统计信息
    :param json_data: 基础数据更新后的字典
    :param area: 片镇
    :param year: 年份
    :param kind: 在编或编外，默认在编
    :return:
    """
    for period in [item for item in [None] + get_period_list() if item not in ["高中"]]:

        #  先统计下总人数
        json_data = dict_assignment(
            route=f"{year}/{kind}/片区/{area}/{period if period is not None else "所有学段"}/总人数",
            value=execute_sql_sentence(
                sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else " "}')[
                0][0],
            json_data=json_data)

        #  统计在编人员最高学历 - 分片区
        json_data = dict_assignment(
            route=f"{year}/{kind}/片区/{area}/{period if period is not None else "所有学段"}/最高学历",
            value=dict(
                sorted(
                    execute_sql_sentence(
                        sentence=f'select "最高学历", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else " "}group by "最高学历"'),
                    key=lambda x: get_educational_background_order()[x[0]]
                )
            ),
            json_data=json_data)

        #  统计片区学段分布
        json_data = dict_assignment(
            route=f"{year}/{kind}/片区/{area}/{period if period is not None else "所有学段"}/学段统计",
            value=dict(
                sorted(
                    execute_sql_sentence(
                        sentence=f'select "任教学段", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else " "}and "任教学段" != "其他" group by "任教学段"'
                    ),
                    key=lambda x: get_period_order()[x[0]]
                )
            ),
            json_data=json_data)

        #  统计片区最高职称
        json_data = dict_assignment(
            route=f"{year}/{kind}/片区/{area}/{period if period is not None else "所有学段"}/最高职称",
            value=combine_highest_title(
                sorted(
                    execute_sql_sentence(
                        sentence=f'select "最高职称", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "区域" = "{area}"{f' and "任教学段" = "{period}" ' if period is not None else " "}group by "最高职称"'
                    ),
                    key=lambda x: get_highest_title_order()[x[0]]
                )
            ),
            json_data=json_data)

        #  更新一下在编和编外的特殊信息
        if kind == "在编":
            json_data = data_00_unique(json_data=json_data, year=year, area=area, period=period)

    return json_data


if __name__ == '__main__':
    update(kind="在编", year="2023")
    update(kind="在编", year="2024")
