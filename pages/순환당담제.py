import streamlit as st
from google import genai

# -------------------------
# 페이지 설정
# -------------------------
st.set_page_config(
    page_title="집안일 순환 담당제 챗봇",
    page_icon="🏠",
)

st.title("🏠 집안일 순환 담당제 챗봇")
st.caption("가족 구성원들의 집안일을 공평하게 분배해주는 AI 도우미")

# -------------------------
# API 키 확인
# -------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("GEMINI_API_KEY가 Secrets에 설정되어 있지 않습니다.")
    st.stop()

# Gemini Client 생성
client = genai.Client(api_key=api_key)

# -------------------------
# 채팅 기록 초기화
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 😊\n\n"
                "저는 집안일 순환 담당제 도우미입니다.\n"
                "가족 구성원 수와 해야 할 집안일을 알려주시면 "
                "공평한 순환 스케줄을 만들어 드릴게요."
            ),
        }
    ]

# -------------------------
# 이전 대화 출력
# -------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# 사용자 입력
# -------------------------
prompt = st.chat_input("예: 가족 4명, 설거지·청소·분리수거를 순환 배정해줘")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):

            try:
                # 시스템 프롬프트
                system_prompt = """
                당신은 집안일 순환 담당제 전문가입니다.

                역할:
                - 가족 구성원 간 집안일을 공평하게 배분
                - 주간/월간 순환표 제안
                - 갈등을 줄일 수 있는 규칙 추천
                - 친절하고 실용적으로 답변

                답변은 한국어로 작성하세요.
                """

                # 대화 이력 구성
                history_text = ""

                for msg in st.session_state.messages:
                    role = "사용자" if msg["role"] == "user" else "AI"
                    history_text += f"{role}: {msg['content']}\n"

                full_prompt = f"""
                {system_prompt}

                아래는 지금까지의 대화입니다.

                {history_text}

                마지막 사용자 요청에 답변하세요.
                """

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=full_prompt,
                )

                answer = response.text

            except Exception as e:
                answer = (
                    "⚠️ 오류가 발생했습니다.\n\n"
                    f"오류 내용: {str(e)}"
                )

            st.markdown(answer)

    # 응답 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
