import pandas as pd

from calculation.tool import func as cal_func

pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('display.max_columns', None)  # 显示所有列


def calculate_exact_grade(classes: int, lessons: int, grade: str, base: pd.DataFrame, subject_list: list):
    df = pd.DataFrame(data=None, columns=["年级"] + subject_list)

    # 插入一条空数据
    df = df._append(pd.Series(dtype=float), ignore_index=True)

    # 给空数据开头加上年级
    df.at[0, "年级"] = grade

    for s in subject_list:

        # 对初中语数英按两个班满课时量计算（有早读课或自习课）
        if grade in ["七年级", "八年级", "九年级"] and s in ["语文", "数学", "英语"]:
            df.at[0, s] = round(classes * 0.5, 1)
        else:
            df.at[0, s] = round(classes * base.loc[base["学科"] == s, grade].values[0] / lessons, 1)

    return df


def summarize_column(df: pd.DataFrame, subject_list: list, title: str):

    # 插入一行，前面是列名（xx合计），后面是每列求和
    # 小学初中计算完分别的时候都过一遍这里再插入到总的df里
    df.loc[len(df)] = [title] + [df[s].sum() for s in subject_list]

    return df


def summarize_row(df: pd.DataFrame, subject_list: list, title: str):

    df[title] = sum(df[s] for s in subject_list)

    return df


# 统计小学的教师需求
def cal_primary_expected_teacher(lessons: int, subject_list: list, base: pd.DataFrame,
                                 grade_1=0, grade_2=0, grade_3=0,
                                 grade_4=0, grade_5=0, grade_6=0):
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

    df = summarize_column(df=df, subject_list=subject_list, title="小学汇总")

    return df


# 统计初中的教师需求
def cal_junior_expected_teacher(lessons: int, subject_list: list, base: pd.DataFrame,
                                grade_7=0, grade_8=0, grade_9=0):
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

    df = summarize_column(df=df, subject_list=subject_list, title="初中汇总")

    return df


# 计算每个学段需要的教师数量和合计教师数量
# 其中输入量lessons代表了每周课时量
# 输入量grade_x代表了该年级班数
def cal_expected_teacher(lessons: int, grade_1=0, grade_2=0, grade_3=0, grade_4=0,
                         grade_5=0, grade_6=0, grade_7=0, grade_8=0, grade_9=0):

    # 错误处理
    if lessons == 0:
        return pd.DataFrame()

    # 读取各科目课时量
    curriculum_sheet = cal_func.load_json_data(folder="source", file_name="课时量")
    subject_list = list(curriculum_sheet.keys())

    df = pd.DataFrame(data=None, columns=["年级"] + subject_list)

    # 转换为列表插入dataframe中
    base = pd.DataFrame(data=[[key] + value for key, value in curriculum_sheet.items()],
                        columns=["学科", "一年级", "二年级", "三年级", "四年级", "五年级", "六年级", "七年级", "八年级",
                                 "九年级"])

    # 小学
    if grade_1 or grade_2 or grade_3 or grade_4 or grade_5 or grade_6:
        df = pd.concat(
            [
                df, cal_primary_expected_teacher(lessons=lessons, subject_list=subject_list, base=base,
                                                 grade_1=grade_1, grade_2=grade_2, grade_3=grade_3,
                                                 grade_4=grade_4, grade_5=grade_5, grade_6=grade_6)
            ],
            axis=0
        )

    # 初中
    if grade_7 or grade_8 or grade_9:
        df = pd.concat(
            [
                df, cal_junior_expected_teacher(lessons=lessons, subject_list=subject_list, base=base,
                                                grade_7=grade_7, grade_8=grade_8, grade_9=grade_9)
            ],
            axis=0
        )

    df = summarize_row(df=df, subject_list=subject_list, title="合计")

    # 清洗一下索引
    df = df.reset_index(drop=True)

    return df


if __name__ == '__main__':

    print(cal_expected_teacher(lessons=12, grade_7=10, grade_8=10, grade_9=12))

