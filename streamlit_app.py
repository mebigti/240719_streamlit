import streamlit as st
import openai
from streamlit_chat import message
import tempfile
import speech_recognition as sr

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

# 음성 인식 처리
def transcribe_audio():
    recognizer = sr.Recognizer()
    audio_file = st.file_uploader("녹음된 음성을 업로드하세요", type=["wav"])
    if audio_file:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            temp_audio_file.write(audio_file.getvalue())
            temp_audio_file_path = temp_audio_file.name

        with sr.AudioFile(temp_audio_file_path) as source:
            audio = recognizer.record(source)
            try:
                return recognizer.recognize_google(audio, language="ko-KR")
            except sr.UnknownValueError:
                return "음성을 인식할 수 없습니다."
            except sr.RequestError as e:
                return f"음성 인식 서비스 오류: {e}"

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

# 멀티모달 입력과 음성 인식 기능
if multimodal_input:
    st.write("멀티모달 입력 기능이 활성화되었습니다.")

if voice_recognition:
    st.write("음성 인식 기능이 활성화되었습니다.")
    audio_text = transcribe_audio()
    st.text_area("음성 인식 결과", audio_text)

# Run with: streamlit run this_script.py
