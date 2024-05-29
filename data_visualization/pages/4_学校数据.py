import sys
import streamlit as st

sys.path.append(
    r'C:\Users\1012986131\Desktop\python\streamlit_pyecharts'
)

from data_processing.tool import module as m_proc
from data_visualization.tool import module as m_visual
from data_processing.make_json.school_data import school as s


# 设置全局属性
m_visual.set_page_configuration()

# 读取现有json文件
json_data = m_visual.load_json_data()

# 标题
st.title("学校教师数据")

with st.container(border=True):
    col0, col1 = st.columns([1, 1.5])

    with col0:
        school_name = st.text_input("请输入校名")
        period = st.selectbox(
            "选择学段（默认所有学段）",
            ("", "高中", "初中", "小学"),
        )
        kind = st.selectbox(
            "选择类型",
            ("在编", "非编"),
        )

        if st.button("查询"):

            if school_name is None or school_name == "":
                st.warning("校名为空", icon="⚠️")

            else:

                check_result = m_proc.school_name_and_period_check(kind=kind, school_name=school_name, period=period)
                if not check_result[0]:
                    st.warning(check_result[1], icon="⚠️")

                else:
                    st.success("查询成功", icon="✅")

                    intro = [
                        f"11111111111111",
                        f"22222222222",
                        f"2333333333333"
                    ]

                    with col1:
                        st.subheader(f"{school_name} - 学校概况")

                        # 流式插入学校基础介绍
                        for i in range(len(intro)):
                            st.write_stream(m_visual.stream_data(sentence=intro[i]))
