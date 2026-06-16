import streamlit as st
import random

# ---------------------------
# 🔐 Gemini API 설정
# ---------------------------
use_ai = False
try:
    import google.generativeai as genai
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    use_ai = True
except:
    use_ai = False

# ---------------------------
# 🎨 기본 설정
# ---------------------------
st.set_page_config(page_title="베이비시터 만족도 조사", page_icon="👶")

st.title("👶 베이비시터 만족도 조사")
st.write("솔직한 경험을 알려주세요! 🎯")

# ---------------------------
# 💬 재미 요소
# ---------------------------
fun_messages = [
    "🤔 음… 이건 중요한 포인트네요!",
    "😲 오! 흥미로운 경험이에요!",
    "😂 이건 공감되네요!",
    "👀 더 자세히 알고 싶어요!",
]

# ---------------------------
# 📋 설문 시작
# ---------------------------
try:
    with st.form("survey_form"):
        st.subheader("📋 설문 시작")

        q1 = st.slider("베이비시터의 전반적인 만족도는?", 1, 10, 5)
        st.write(random.choice(fun_messages))

        q2 = st.slider("아이 돌봄 능력은 어땠나요?", 1, 10, 5)
        st.write(random.choice(fun_messages))

        q3 = st.slider("시간 약속은 잘 지켰나요?", 1, 10, 5)
        st.write(random.choice(fun_messages))

        q4 = st.slider("의사소통은 원활했나요?", 1, 10, 5)

        comment = st.text_area("추가로 하고 싶은 말이 있나요?")

        submitted = st.form_submit_button("결과 보기")

    # ---------------------------
    # 📊 결과 처리
    # ---------------------------
    if submitted:
        avg_score = round((q1 + q2 + q3 + q4) / 4, 1)

        st.subheader("📊 결과")

        st.metric("⭐ 평균 만족도", avg_score)

        # 기본 평가
        if avg_score >= 8:
            st.success("매우 만족 👍")
        elif avg_score >= 5:
            st.info("보통 🙂")
        else:
            st.warning("아쉬움 있음 😥")

        # ---------------------------
        # 🤖 AI 분석
        # ---------------------------
        st.subheader("🤖 AI 분석")

        if use_ai:
            try:
                prompt = f"""
                베이비시터 만족도 분석:

                점수:
                - 전반적 만족도: {q1}
                - 돌봄 능력: {q2}
                - 시간 준수: {q3}
                - 소통: {q4}

                사용자 의견: {comment}

                아래 형식으로 분석:
                1. 한줄 평가
                2. 장점
                3. 개선점
                """

                response = model.generate_content(prompt)

                if hasattr(response, "text") and response.text:
                    st.write(response.text)
                else:
                    st.write("⚠️ AI 응답을 불러오지 못했습니다.")

            except Exception as e:
                st.error(f"AI 오류: {e}")
        else:
            st.write("⚠️ AI 기능이 비활성화되어 기본 결과만 제공합니다.")

        # ---------------------------
        # 🔁 다시하기 버튼
        # ---------------------------
        if st.button("🔄 다시 하기"):
            st.rerun()

except Exception as e:
    st.error(f"❌ 오류 발생: {e}")
