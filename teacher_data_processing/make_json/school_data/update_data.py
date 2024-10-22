from teacher_data_processing.make_json.school_data import school


def update(kind: str, school_name: str, year: str, period: str = None) -> None:
    """
    根据教师类型、校名、年份以及可选填项学段更新json文件中的教师数据
    :param kind: 在编或编外
    :param school_name: 校名
    :param year: 年份
    :param period: 学段
    :return: 无
    """
    school.update(kind=kind, school_name=school_name, year=year, period=period)
