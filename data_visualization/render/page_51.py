import sys
from pathlib import Path

import streamlit as st

# 加入项目路径
sys.path.append(
    str(
        Path(__file__).resolve().parent.parent.parent
    )
)

from calculation import curriculum as cur


def show_result(lessons: int, grade_1=0, grade_2=0, grade_3=0, grade_4=0, grade_5=0, grade_6=0, grade_7=0, grade_8=0,
                grade_9=0):
    if lessons == 0 or lessons is None:
        st.toast("课时量不能为空！", icon="⚠️")
        return None

    df = cur.cal_expected_teacher(lessons=lessons, grade_1=grade_1, grade_2=grade_2, grade_3=grade_3,
                                  grade_4=grade_4, grade_5=grade_5, grade_6=grade_6, grade_7=grade_7,
                                  grade_8=grade_8, grade_9=grade_9)

    st.dataframe(df)
