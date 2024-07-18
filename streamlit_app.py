import streamlit as st
import openai

# 사이드바에 API 키 입력란 추가
st.sidebar.header('API Key 입력')
api_key = st.sidebar.text_input('OpenAI API Key', type='password')

# 사이드바에 모델 선택란 추가
st.sidebar.header('모델 선택')
model = st.sidebar.selectbox(
    'OpenAI 모델을 선택하세요',
    ['gpt-4', 'gpt-4-turbo', 'gpt-4o', 'gpt-3-turbo']
)

# API 키가 입력되었는지 확인
if api_key:
    openai.api_key = api_key

    # 사용자가 입력할 메시지
    st.header('챗봇과 대화하기')
    user_input = st.text_input('당신의 메시지:')

    if user_input:
        # OpenAI API를 사용하여 응답 생성
        response = openai.Completion.create(
            engine=model,
            prompt=user_input,
            max_tokens=4000
        )

        # 응답 출력
        st.write('챗봇:', response.choices[0].text.strip())
else:
    st.write('API Key를 사이드바에 입력하세요.')

# Streamlit 앱 실행 명령어
# streamlit run app.py
