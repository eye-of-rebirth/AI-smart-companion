import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url="https://api.deepseek.com")

st.set_page_config(
    page_title="AI 智能助手",
    page_icon="🤖",
    layout="wide",
    #控制侧边栏
    initial_sidebar_state="expanded",
    menu_items={}
)

#大标题
st.title("AI 智能助手")

#logo
st.logo("resources/sidelogo.png")

# #系统提示词
# system_prompt = "你是一个helpful的助手，请用中文回答问题。"

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

#初始化名字
if "name" not in st.session_state:
    st.session_state.name = "助手"

#初始化系统提示词
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "你是一个helpful的助手，请用中文回答问题。"

#展示聊天信息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

#左侧侧边栏
with st.sidebar:
    st.title("系统提示词")
    ai_name = st.text_input("请输入AI名称", "助手")
    if ai_name:
        st.session_state.name = ai_name
    system_prompt = st.text_area("请输入系统提示词", "你是一个helpful的助手，请用中文回答问题。")
    if system_prompt:
        st.session_state.system_prompt = system_prompt


#聊天框
prompt = st.chat_input("请输入你的问题")
if prompt:
    st.chat_message("user").write(prompt)
    print(f"--------->输出的内容是：{prompt}")
    st.session_state.messages.append({"role": "user", "content": prompt})


    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages,
        ],
        stream=True
    )
    #非流式输出
    # st.chat_message("assistant").write(response.choices[0].message.content)
    # print(f"--------->大模型输出的内容是：{response.choices[0].message.content}")
    # st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

    #流式输出
    response_message = st.empty()
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)

    print(f"--------->大模型输出的内容是：{full_response}")
    st.session_state.messages.append({"role": "assistant", "content": full_response})



