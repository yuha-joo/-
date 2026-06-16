import streamlit as st
import google.generativeai as genai

# ---------------------------
# 🔐 API 키 설정
# ---------------------------
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("❌ API 키가 없습니다. secrets 설정을 확인하세요.")
    st.stop()

# ---------------------------
# 🤖 모델 생성
# ---------------------------
try:
    model = genai.GenerativeModel(model_name="gemini-2.5-flash-lite")
except Exception as e:
    st.error(f"모델 로딩 실패: {e}")
    st.stop()

# ---------------------------
# 💬 채팅 기록
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# 🧠 시스템 프롬프트
# ---------------------------
SYSTEM_PROMPT = """
너는 '베이비시터 만족도 검사기' AI야.

사용자의 경험을 보고 아래 형식으로 답해:
1. 만족도 점수 (1~10)
2. 한줄 평가
3. 👍 좋은 점
4. ⚠️ 아쉬운 점

친절하게 답변해.
"""

# ---------------------------
# 🖥️ UI
# ---------------------------
st.title("👶 베이비시터 만족도 검사기")

# 기존 채팅 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 입력창
user_input = st.chat_input("경험을 입력하세요")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    try:
        # 대화 구성
        prompt = SYSTEM_PROMPT + "\n"
        for m in st.session_state.messages:
            role = "사용자" if m["role"] == "user" else "AI"
            prompt += f"{role}: {m['content']}\n"

        # 모델 호출
        response = model.generate_content(prompt)

        # 안전하게 텍스트 추출
        if hasattr(response, "text") and response.text:
            ai_text = response.text
        elif response.candidates:
            ai_text = response.candidates[0].content.parts[0].text
        else:
            ai_text = "⚠️ 응답을 가져오지 못했습니다."

    except Exception as e:
        ai_text = f"⚠️ 오류 발생: {str(e)}"

    # 저장 및 출력
    st.session_state.messages.append({"role": "assistant", "content": ai_text})

    with st.chat_message("assistant"):
        st.write(ai_text)
