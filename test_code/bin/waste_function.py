def if_school_and_period_exist(kind: str, school_name: str, period=None):
    if kind not in ["在编", '非编']:
        raise MyError("kind参数错误")

    if period not in [None, "高中", "初中", "小学", "幼儿园", ""]:
        raise MyError("period参数错误")

    with open(r"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\result\output.json",
              "r", encoding="UTF-8") as file:
        json_data = json.load(file)

    if school_name not in json_data[kind]["学校"]:
        return False

    if (period if period is not None else "所有学段") not in json_data[kind]["学校"][school_name]:
        return False

    if "总人数" not in json_data[kind]["学校"][school_name][period if period is not None else "所有学段"]:
        return False

    if json_data[kind]["学校"][school_name][period if period is not None else "所有学段"]["总人数"] <= 0:
        return False

    return True


def json_school_and_period_initialization(kind: str, school_name: str, period=None):
    if kind not in ["在编", '非编']:
        raise MyError("kind参数错误")

    if period not in [None, "高中", "初中", "小学", "幼儿园", ""]:
        raise MyError("period参数错误")

    with open(r"C:\Users\1012986131\Desktop\python\streamlit_pyecharts\json\result\output.json",
              "r", encoding="UTF-8") as file:
        json_data = json.load(file)

    # 不考虑分学段的情况
    if period is None:

        if school_name not in json_data[kind]["学校"]:
            json_data[kind]["学校"][school_name] = {}

        json_data[kind]["学校"][school_name]["所有学段"] = {}

    if period is not None:

        if school_name not in json_data[kind]["学校"]:
            json_data[kind]["学校"][school_name] = {}

        if period not in json_data[kind]["学校"][school_name]:
            json_data[kind]["学校"][school_name][period] = {}

    return json_data