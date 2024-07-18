import streamlit as st
import openai
from streamlit_chat import message

# OpenAI API 키 설정
openai.api_key = 'OPENAI_API_KEY'

# 사이드 메뉴 구성
st.sidebar.title("ChatGPT Interface")
model_selection = st.sidebar.selectbox("모델 선택", ["gpt-3.5-turbo", "text-davinci-003"])
candidate_prompts = st.sidebar.text_area("후보 프롬프트", "예시 프롬프트를 입력하세요")

# 멀티모달 입력 버튼과 음성 인식 버튼
multimodal_input = st.sidebar.button("멀티모달 입력")
voice_recognition = st.sidebar.button("음성 인식")

# 채팅 기록 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# 사용자가 메시지를 입력하는 텍스트 상자
user_input = st.text_input("당신의 메시지를 입력하세요", "")

# 사용자가 메시지를 제출할 때
if st.button("보내기"):
    if user_input:
        st.session_state['messages'].append({"role": "user", "content": user_input})
        # OpenAI API 호출
        try:
            response = openai.ChatCompletion.create(
                model=model_selection,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state['messages']]
            )
            # 모델 응답 저장
            st.session_state['messages'].append({"role": "assistant", "content": response.choices[0].message['content']})
        except Exception as e:
            st.error(f"Error: {e}")

# 채팅 기록 표시
for msg in st.session_state['messages']:
    if msg['role'] == 'user':
        message(msg['content'], is_user=True)
    else:
        message(msg['content'])

# 멀티모달 입력과 음성 인식 기능 (여기서는 단순히 로그를 출력)
if multimodal_input:
    st.write("멀티모달 입력 기능이 활성화되었습니다.")

if voice_recognition:
    st.write("음성 인식 기능이 활성화되었습니다.")

# Run with: streamlit run this_script.py
