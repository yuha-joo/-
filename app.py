# snack_recommender_app.py
# 실행 방법:
# 1) pip install streamlit
# 2) streamlit run snack_recommender_app.py

import streamlit as st
import random

st.set_page_config(
    page_title="간식 추천기",
    page_icon="🍪",
    layout="centered"
)

st.title("🍿 오늘의 간식 추천")
st.write("기분과 상황에 맞는 간식을 추천해드립니다!")

# 간식 데이터
snacks = {
    "달달한 게 먹고 싶어요": [
        "초코 쿠키 🍪",
        "마카롱 🩷",
        "아이스크림 🍨",
        "허니버터칩 🍯",
        "와플 🧇"
    ],
    "짭짤한 게 좋아요": [
        "감자칩 🥔",
        "나초 🌮",
        "팝콘 🍿",
        "프레첼 🥨",
        "치즈볼 🧀"
    ],
    "건강한 간식이 좋아요": [
        "그릭요거트 🥣",
        "견과류 믹스 🌰",
        "바나나 🍌",
        "고구마 🍠",
        "샐러드 컵 🥗"
    ],
    "배가 꽤 고파요": [
        "핫도그 🌭",
        "떡볶이 🌶️",
        "샌드위치 🥪",
        "김밥 🍙",
        "토스트 🍞"
    ]
}

# 사용자 선택
mood = st.selectbox(
    "지금 어떤 간식이 먹고 싶나요?",
    list(snacks.keys())
)

# 추천 버튼
if st.button("간식 추천받기 🎯"):
    recommendation = random.choice(snacks[mood])

    st.success(f"오늘의 추천 간식은 👉 **{recommendation}**")

    # 추가 메시지
    messages = [
        "맛있게 드세요 😋",
        "오늘 하루도 화이팅 💪",
        "간식 타임은 소중하죠 ✨",
        "행복한 간식 시간이 되길 🍀"
    ]

    st.info(random.choice(messages))

# 사이드바
st.sidebar.title("📌 앱 소개")
st.sidebar.write(
    """
    이 앱은 사용자의 취향에 따라
    랜덤으로 간식을 추천해주는
    간단한 Streamlit 웹앱입니다.
    """
)

st.sidebar.markdown("---")
st.sidebar.write("Made with ❤️ using Streamlit")
