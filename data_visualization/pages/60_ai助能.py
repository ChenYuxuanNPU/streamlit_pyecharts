import streamlit as st
from openai import OpenAI

st.title("deepseek api测试页面")

# 初始化用于存放问答的列表
if "messages" not in st.session_state:
    st.session_state.messages = []

st.write(st.session_state.messages)

# Set API key from Streamlit secrets
client = OpenAI(api_key=st.secrets['DEEPSEEK_API_KEY'], base_url="https://api.deepseek.com")

# 用于在屏幕上方展示st.session_state.messages中所有历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 获取并确认用户输入
if prompt := st.chat_input("请输入内容"):
    # 添加用户输入至messages
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 在屏幕上方展示用户输入
    with st.chat_message("user"):
        st.markdown(prompt)

    # 在上方展示ai回答内容
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="deepseek-chat",
            messages=st.session_state.messages,
            stream=True
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
