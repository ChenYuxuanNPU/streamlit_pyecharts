import math

import pandas as pd

from calculation.tool import func as cal_func

pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('display.max_columns', None)  # 显示所有列


def custom_round(value: float | int | str | None) -> int | str | None:
    """
    对小数或整数进行四舍五入
    :param value: 四舍五入前的值
    :return:
    """
    # 如果值是浮点数且小数点后有数字，则根据小数点后第一位决定是否向上取整
    if isinstance(value, float) and value != int(value):
        return math.ceil(value) if value - int(value) >= 0.5 else math.floor(value)
    # 对于整数、NaN和其他非浮点数类型，直接返回原始值
    return value


def calculate_exact_grade(classes: int, lessons: int, grade: str, base: pd.DataFrame,
                          subject_list: list) -> pd.DataFrame:
    """
    计算某一年级的应配教师数
    :param classes: 年级班数
    :param lessons: 年级教师平均课时量
    :param grade: 年级
    :param base: 原数据
    :param subject_list: 学科列表
    :return: 插入一条数据后的数据
    """

    df = pd.DataFrame(data=None, columns=["年级"] + subject_list)

    # 插入一条空数据
    df = df._append(pd.Series(dtype=float), ignore_index=True)

    # 给空数据开头加上年级
    df.at[0, "年级"] = grade

    for subject in subject_list:

        # 对初中语数英按两个班满课时量计算（有早读课或自习课）
        if grade in ["七年级", "八年级", "九年级"] and subject in ["语文", "数学", "英语"]:
            df.at[0, subject] = round(classes * 0.5, 1)
        else:
            df.at[0, subject] = round(classes * base.loc[base["学科"] == subject, grade].values[0] / lessons, 1)

    return df


def summarize_row(df: pd.DataFrame, subject_list: list, title: str) -> pd.DataFrame:
    """
    某个学段合计行的生成，可以基于df前几行生成求和行
    :param df: 待求和的Dataframe
    :param subject_list: 学科列表
    :param title: 左侧标题
    :return: 加入求和行后的Dataframe
    """

    match title:
        case "小学" | "初中":
            df.loc[len(df)] = [title] + [df[s].sum() for s in subject_list]

        case "合计":
            df.loc["合计", df.columns.difference(["年级"])] = \
                df[df["年级"].isin(["小学", "初中"])].drop(columns=["年级"]).sum().to_frame().T.iloc[0]
            df.at['合计', '年级'] = "合计"

        case _:
            pass

    return df


def summarize_column(df: pd.DataFrame, subject_list: list) -> pd.DataFrame:
    """
    生成求和列，对每一行的数据进行求和计算
    :param df: 原Dataframe
    :param subject_list: 学科列表
    :return: 插入直接求和列后的Dataframe
    """

    # 对学科教师直接全部加起来
    df["直接求和"] = df[subject_list].sum(axis=1)

    # 对每一门学科四舍五入后求和
    df["取整求和"] = df.apply(
        lambda row: sum(custom_round(row[col]) for col in subject_list if pd.notna(row[col])), axis=1
    )

    return df


# 统计小学的教师需求
def cal_primary_expected_teacher(lessons: int, subject_list: list, base: pd.DataFrame,
                                 grade_1=0, grade_2=0, grade_3=0,
                                 grade_4=0, grade_5=0, grade_6=0) -> pd.DataFrame:
    """
    统计小学学段教师需求
    :param lessons: 教师课时量
    :param subject_list: 学科列表
    :param base: 学段学科对应的课时量
    :param grade_1: 小学一年级班数
    :param grade_2: 小学二年级班数
    :param grade_3: 小学三年级班数
    :param grade_4: 小学四年级班数
    :param grade_5: 小学五年级班数
    :param grade_6: 小学六年级班数
    :return: 返回带有学段汇总行的统计结果
    """

    df = pd.DataFrame(data=None, columns=["年级"] + subject_list)

    if grade_1:
        df = pd.concat(
            [
                df, calculate_exact_grade(classes=grade_1, lessons=lessons, grade="一年级", base=base,
                                          subject_list=subject_list)
            ],
            axis=0
        )

    if grade_2:
        df = pd.concat(
            [
                df, calculate_exact_grade(classes=grade_2, lessons=lessons, grade="二年级", base=base,
                                          subject_list=subject_list)
            ],
            axis=0
        )

    if grade_3:
        df = pd.concat(
            [
                df, calculate_exact_grade(classes=grade_3, lessons=lessons, grade="三年级", base=base,
                                          subject_list=subject_list)
            ],
            axis=0
        )

    if grade_4:
        df = pd.concat(
            [
                df, calculate_exact_grade(classes=grade_4, lessons=lessons, grade="四年级", base=base,
                                          subject_list=subject_list)
            ],
            axis=0
        )

    if grade_5:
        df = pd.concat(
            [
                df, calculate_exact_grade(classes=grade_5, lessons=lessons, grade="五年级", base=base,
                                          subject_list=subject_list)
            ],
            axis=0
        )

    if grade_6:
        df = pd.concat(
            [
                df, calculate_exact_grade(classes=grade_6, lessons=lessons, grade="六年级", base=base,
                                          subject_list=subject_list)
            ],
            axis=0
        )

    df = summarize_row(df=df, subject_list=subject_list, title="小学")

    return df


def cal_junior_expected_teacher(lessons: int, subject_list: list, base: pd.DataFrame,
                                grade_7=0, grade_8=0, grade_9=0) -> pd.DataFrame:
    """
    统计初中学段教师需求
    :param lessons: 教师课时量
    :param subject_list: 学科列表
    :param base: 学段学科对应的课时量
    :param grade_7: 初中一年级班数
    :param grade_8: 初中二年级班数
    :param grade_9: 初中三年级班数
    :return: 返回带有学段汇总行的统计结果
    """

    df = pd.DataFrame(data=None, columns=["年级"] + subject_list)

    if grade_7:
        df = pd.concat(
            [
                df, calculate_exact_grade(classes=grade_7, lessons=lessons, grade="七年级", base=base,
                                          subject_list=subject_list)
            ],
            axis=0
        )

    if grade_8:
        df = pd.concat(
            [
                df, calculate_exact_grade(classes=grade_8, lessons=lessons, grade="八年级", base=base,
                                          subject_list=subject_list)
            ],
            axis=0
        )

    if grade_9:
        df = pd.concat(
            [
                df, calculate_exact_grade(classes=grade_9, lessons=lessons, grade="九年级", base=base,
                                          subject_list=subject_list)
            ],
            axis=0
        )

    df = summarize_row(df=df, subject_list=subject_list, title="初中")

    return df


def cal_expected_teacher(lessons_pri: int, lessons_jun: int,
                         grade_1=0, grade_2=0, grade_3=0,
                         grade_4=0, grade_5=0, grade_6=0,
                         grade_7=0, grade_8=0, grade_9=0) -> pd.DataFrame:
    """
    计算预期需要的教师数量
    :param lessons_pri: 小学课时量
    :param lessons_jun: 初中课时量
    :param grade_1: 小学一年级班数
    :param grade_2: 小学二年级班数
    :param grade_3: 小学三年级班数
    :param grade_4: 小学四年级班数
    :param grade_5: 小学五年级班数
    :param grade_6: 小学六年级班数
    :param grade_7: 初中一年级班数
    :param grade_8: 初中二年级班数
    :param grade_9: 初中三年级班数
    :return: 返回Dataframe类型的查询结果
    """

    # 读取各科目课时量
    curriculum_sheet = cal_func.load_json_data(folder="source", file_name="课时量")
    subject_list = list(curriculum_sheet.keys())

    df = pd.DataFrame(data=None, columns=["年级"] + subject_list)

    # 转换为列表插入dataframe中
    base = pd.DataFrame(data=[[key] + value for key, value in curriculum_sheet.items()],
                        columns=["学科", "一年级", "二年级", "三年级", "四年级", "五年级", "六年级", "七年级", "八年级",
                                 "九年级"])

    # 小学
    if (grade_1 or grade_2 or grade_3 or grade_4 or grade_5 or grade_6) and lessons_pri:
        df = pd.concat(
            [
                df, cal_primary_expected_teacher(lessons=lessons_pri, subject_list=subject_list, base=base,
                                                 grade_1=grade_1, grade_2=grade_2, grade_3=grade_3,
                                                 grade_4=grade_4, grade_5=grade_5, grade_6=grade_6)
            ],
            axis=0
        )

    # 初中
    if (grade_7 or grade_8 or grade_9) and lessons_jun:
        df = pd.concat(
            [
                df, cal_junior_expected_teacher(lessons=lessons_jun, subject_list=subject_list, base=base,
                                                grade_7=grade_7, grade_8=grade_8, grade_9=grade_9)
            ],
            axis=0
        )

    df = summarize_column(df=df, subject_list=subject_list)

    df = summarize_row(df=df, subject_list=subject_list, title="合计")

    # 清洗一下索引
    df = df.reset_index(drop=True)

    return df


if __name__ == '__main__':
    pass
