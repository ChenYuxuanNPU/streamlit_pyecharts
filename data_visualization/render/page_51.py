import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from calculation import curriculum as cur

# 加入项目路径
sys.path.append(
    str(
        Path(__file__).resolve().parent.parent.parent
    )
)


def show_result(lessons_pri: int, lessons_jun: int, grade_1=0, grade_2=0, grade_3=0, grade_4=0,
                grade_5=0, grade_6=0, grade_7=0, grade_8=0, grade_9=0) -> pd.DataFrame | None:
    """
    用于计算应配教师数的结果
    :param lessons_pri: 小学教师课时量
    :param lessons_jun: 初中教师课时量
    :param grade_1: 一年级班数
    :param grade_2: 二年级班数
    :param grade_3: 三年级班数
    :param grade_4: 四年级班数
    :param grade_5: 五年级班数
    :param grade_6: 六年级班数
    :param grade_7: 七年级班数
    :param grade_8: 八年级班数
    :param grade_9: 九年级班数
    :return:
    """
    pass
    if lessons_pri == 0 or lessons_jun == 0:
        st.toast("课时量不能为空！", icon="⚠️")
        return None

    df = cur.cal_expected_teacher(lessons_pri=lessons_pri, lessons_jun=lessons_jun,
                                  grade_1=grade_1, grade_2=grade_2, grade_3=grade_3,
                                  grade_4=grade_4, grade_5=grade_5, grade_6=grade_6,
                                  grade_7=grade_7, grade_8=grade_8, grade_9=grade_9)

    st.dataframe(df)

    return df
