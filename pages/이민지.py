import streamlit as st
import google.generativeai as genai

# ---------------------------
# 🔐 API 키 불러오기 (secrets)
# ---------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("API 키를 불러오지 못했습니다. Secrets 설정을 확인하세요.")
    st.stop()

# ---------------------------
# 🤖 모델 설정
# ---------------------------
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# ---------------------------
# 💬 채팅 기록 유지
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# 🧠 시스템 프롬프트
# ---------------------------
SYSTEM_PROMPT = """
너는 '베이비시터 만족도 검사기' AI야.

사용자의 경험을 기반으로 만족도를 분석하고 아래 형식으로 답해:
1. 만족도 점수 (1~10)
2. 한줄 평가
3. 긍정 요소
4. 개선 필요 요소

친절하고 이해하기 쉽게 답변해.
"""

# ---------------------------
# 🖥️ UI
# ---------------------------
st.title("👶 베이비시터 만족도 검사기")
st.write("베이비시터 이용 경험을 자유롭게 입력해보세요!")

# 기존 메시지 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 입력
user_input = st.chat_input("예: 아이를 잘 돌봐줬지만 약속 시간을 자주 어겼어요")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    try:
        # 전체 대화 맥락 만들기
        conversation = SYSTEM_PROMPT + "\n"
        for msg in st.session_state.messages:
            role = "사용자" if msg["role"] == "user" else "AI"
            conversation += f"{role}: {msg['content']}\n"

        # 모델 호출
        response = model.generate_content(conversation)

        ai_response = response.text

    except Exception as e:
        ai_response = f"⚠️ 오류가 발생했습니다: {str(e)}"

    # AI 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    # 출력
    with st.chat_message("assistant"):
        st.write(ai_response)
