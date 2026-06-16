import streamlit as st
import google.generativeai as genai

# ---------------------------
# 🔐 API 키 설정
# ---------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("❌ API 키를 불러오지 못했습니다. secrets 설정을 확인하세요.")
    st.stop()

# ---------------------------
# 🤖 모델 설정
# ---------------------------
try:
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
except Exception as e:
    st.error(f"❌ 모델 생성 오류: {e}")
    st.stop()

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

사용자의 경험을 분석해서 아래 형식으로 답해:
1. 만족도 점수 (1~10)
2. 한줄 평가
3. 👍 좋은 점
4. ⚠️ 개선할 점

간결하고 친절하게 작성해.
"""

# ---------------------------
# 🖥️ UI
# ---------------------------
st.title("👶 베이비시터 만족도 검사기")
st.caption("베이비시터 이용 경험을 입력하면 만족도를 분석해줘요!")

# 기존 채팅 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 입력
user_input = st.chat_input("예: 아이를 잘 돌봤지만 늦는 경우가 많았어요")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    try:
        # 🔗 대화 맥락 구성
        prompt = SYSTEM_PROMPT + "\n"
        for m in st.session_state.messages:
            role = "사용자" if m["role"] == "user" else "AI"
            prompt += f"{role}: {m['content']}\n"

        # 🤖 모델 호출
        response = model.generate_content(prompt)

        # ✅ 안전한 응답 처리
        if hasattr(response, "text") and response.text:
            ai_response = response.text
        elif hasattr(response, "candidates") and response.candidates:
            ai_response = response.candidates[0].content.parts[0].text
        else:
            ai_response = "⚠️ 응답을 생성하지 못했습니다."

    except Exception as e:
        ai_response = f"⚠️ 오류 발생: {str(e)}"

    # AI 메시지 저장
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })

    # 출력
    with st.chat_message("assistant"):
        st.write(ai_response)
