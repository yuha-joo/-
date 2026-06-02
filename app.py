import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="🍪 간식 추천기",
    page_icon="🍪",
)

st.title("🍪 AI 간식 추천기")
st.write("먹고 싶은 상황을 말하면 간식을 추천해 드립니다!")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("GEMINI_API_KEY가 Secrets에 설정되어 있지 않습니다.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 🍩\n\n"
                "상황이나 취향을 말해주시면 간식을 추천해드릴게요.\n"
                "예시:\n"
                "- 공부하면서 먹을 간식 추천\n"
                "- 다이어트 중 먹을 간식\n"
                "- 편의점에서 살 수 있는 간식\n"
                "- 달달한 간식 추천"
            ),
        }
    ]

# 기존 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("어떤 간식을 찾고 있나요?"):
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("간식을 찾는 중..."):

                # 최근 대화 컨텍스트 구성
                history_text = ""
                for msg in st.session_state.messages[-10:]:
                    role = "사용자" if msg["role"] == "user" else "AI"
                    history_text += f"{role}: {msg['content']}\n"

                system_prompt = """
너는 친절한 간식 추천 전문가다.

규칙:
1. 사용자의 상황과 취향을 고려해 추천한다.
2. 추천 이유를 함께 설명한다.
3. 가능하면 3~5개의 간식을 추천한다.
4. 답변은 한국어로 한다.
5. 간결하면서도 도움이 되게 답변한다.
"""

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.8,
                    ),
                    contents=history_text,
                )

                answer = response.text

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

        except Exception as e:
            error_msg = (
                "죄송합니다. 응답 생성 중 오류가 발생했습니다.\n\n"
                f"오류 내용: {str(e)}"
            )

            st.error(error_msg)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_msg,
                }
            )
