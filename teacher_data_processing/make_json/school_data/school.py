from teacher_data_processing.tool.func import *


def update(kind: str, school_name: str, year: str, period: str = None) -> None:
    """
    根据校名、学段、是否在编进行某所学校内教师信息统计
    :param kind: 是否在编
    :param school_name: 校名
    :param year: 年份
    :param period: 学段
    :return: 无
    """

    if kind not in ["在编", '编外']:
        raise MyError("kind参数错误")

    if period not in [None, "所有学段", "高中", "初中", "小学", "幼儿园", ""]:
        raise MyError("period参数错误")

    else:
        period = period if period not in ["所有学段", ""] else None

    json_data = load_json_data(folder="result", file_name="teacher_info")

    #  检查一下有没有这个学校和学段，没有的话就报错
    check_result = school_name_and_period_check(kind=kind, school=school_name, period=period,
                                                year=year)
    if not check_result[0]:
        print(check_result[1])
        return None

    #  统计总人数 - 分学校
    json_data = dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/总人数",
        value=execute_sql_sentence(
            sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "校名" = "{school_name}"{f' and "任教学段" = "{period}"' if period is not None else ''}')[
            0][0],
        json_data=json_data)

    #  统计最高学历 - 分学校
    json_data = dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/最高学历",
        value=dict(
            sorted(
                execute_sql_sentence(
                    sentence=f'select "最高学历", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "校名" = "{school_name}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}group by "最高学历"'
                ),
                key=lambda x: get_educational_background_order()[x[0]]
            )
        ),
        json_data=json_data)

    #  统计性别 - 分学校
    json_data = dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/性别",
        value=dict(
            execute_sql_sentence(
                sentence=f'select "性别", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "校名" = "{school_name}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}group by "性别" order by count(*) asc'
            )
        ),
        json_data=json_data)

    #  统计最高职称 - 分学校
    json_data = dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/最高职称",
        value=combine_highest_title(
            sorted(
                execute_sql_sentence(
                    sentence=f'select "最高职称", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "校名" = "{school_name}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}group by "最高职称"'
                ),
                key=lambda x: get_highest_title_order()[x[0]]
            )
        ),
        json_data=json_data)

    #  统计在编人员骨干教师 - 分学校
    json_data = dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/骨干教师",
        value=combine_none_and_others(
            dict(
                sorted(
                    execute_sql_sentence(
                        sentence=f'select "骨干教师", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "校名" = "{school_name}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}group by "骨干教师"'
                    ),
                    key=lambda x: get_cadre_teacher_order()[x[0]]
                )
            )
        ),
        json_data=json_data)

    #  统计学校教师资格

    #  先统计没有教资的
    json_data = dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/教师资格/未持教师资格",
        value=execute_sql_sentence(
            sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "校名" = "{school_name}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "教师资格学段" = "无"')[
            0][0],
        json_data=json_data)

    #  再统计有教资的
    json_data = dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/教师资格/持有教师资格",
        value=execute_sql_sentence(
            sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "校名" = "{school_name}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "教师资格学段" != "无"')[
            0][0],
        json_data=json_data)

    #  统计一下在编编外的独有信息
    if kind == "在编":
        json_data = data_00_unique(json_data=json_data, school_name=school_name, period=period,
                                   year=year, kind=kind)

    elif kind == "编外":
        json_data = data_01_unique(json_data=json_data, school_name=school_name, period=period,
                                   year=year, kind=kind)

    save_json_data(json_data=json_data, folder="result", file_name="teacher_info")

    return None


def data_00_unique(json_data: dict, school_name: str, year: str, kind: str = "在编", period: str = None) -> dict:
    """
    根据校名、学段、是否在编进行某所学校内在编特有的教师信息统计
    :param json_data: 经过更新在编编外都有的信息后的json文件
    :param school_name: 校名
    :param year: 年份
    :param kind: 是否在编
    :param period: 学段
    :return: 更新后生成的字典
    """

    #  统计在编人员年龄 - 分学校
    json_data = dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/年龄",
        value=age_statistics(
            age_count_list=execute_sql_sentence(
                sentence=f'select "年龄", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "校名" = "{school_name}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}group by "年龄"')
        ),
        json_data=json_data)

    #  统计在编人员主教学科 - 分学校
    json_data = dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/主教学科",
        value=dict(
            execute_sql_sentence(
                sentence=f'select "主教学科", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "校名" = "{school_name}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "主教学科" != "无" group by "主教学科" order by count(*) desc limit 20'
            )
        ),
        json_data=json_data)

    #  统计在编人员院校级别 - 分学校
    json_data = dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/院校级别",
        value=count_school_id(
            data=execute_sql_sentence(
                sentence=f'select "参加工作前毕业院校代码" from teacher_data_{0 if kind == "在编" else 1}_{year} where "校名" = "{school_name}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and ("参加工作前学历" in ("本科", "硕士研究生", "博士研究生"))'
            ),
            label_length="long"
        ),
        json_data=json_data)

    #  统计在编人员三名工作室主持人 - 分学校

    #  这里统计有多少是主持人
    json_data = dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/四名工作室/四名工作室主持人",
        value=execute_sql_sentence(
            sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "校名" = "{school_name}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "四名工作室主持人" != "无"')[
            0][0],
        json_data=json_data)

    #  这里统计有多少不是主持人
    json_data = dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/四名工作室/无",
        value=execute_sql_sentence(
            sentence=f'select count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "校名" = "{school_name}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}and "四名工作室主持人" = "无"')[
            0][0],
        json_data=json_data)

    #  统计在编人员支教地域 - 分学校
    json_data = dict_assignment(
        route=f"{year}/{kind}/学校/{school_name}/{period if period is not None else "所有学段"}/支教地域",
        value=dict(
            sorted(
                execute_sql_sentence(
                    sentence=f'select "支教地域", count(*) from teacher_data_{0 if kind == "在编" else 1}_{year} where "校名" = "{school_name}"{f' and "任教学段" = "{period}" ' if period is not None else ' '}group by "支教地域"'),
                key=lambda x: get_area_of_supporting_education_order()[x[0]]
            )
        ),
        json_data=json_data)

    return json_data


#  更新一些非在编特有的信息
def data_01_unique(json_data: dict, school_name: str, year: str, kind: str, period: str = None) -> dict:
    """
    根据校名、学段、是否在编进行某所学校内在编教师信息统计
    :param json_data: 经过更新在编编外都有的信息后的json文件
    :param school_name: 校名
    :param year: 年份
    :param kind: 是否在编
    :param period: 学段
    :return: 更新后生成的字典
    """
    return json_data


if __name__ == '__main__':
    pass
    update(kind="在编", school_name="广州市白云中学", period="高中", year="2023")
    update(kind="在编", school_name="广州市白云区广州空港实验中学", year="2023")
    update(kind="编外", school_name="广州市实验外语学校", period="高中", year="2023")
    update(kind="在编", school_name="广州市培英中学", year="2023")
    update(kind="在编", school_name="广州市培英中学", year="2024")
    update(kind="在编", school_name="广州市白云中学", period="初中", year="2024")
