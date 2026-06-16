import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="집안일 난이도 추천기",
    page_icon="🏠",
    layout="centered"
)

# CSS
st.markdown("""
<style>
div.stButton > button {
    border-radius: 50%;
    width: 80px;
    height: 80px;
    font-size: 24px;
    font-weight: bold;
}

.result-box {
    padding: 20px;
    border-radius: 15px;
    background-color: #f0f8ff;
    border: 2px solid #4CAF50;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🏠 집안일 난이도 추천기")
st.write("원하는 난이도를 선택하면 해당 수준의 집안일을 추천해드립니다!")

# 집안일 데이터
chores = {
    1: [
        "책상 정리하기",
        "쓰레기 버리기",
        "물컵 설거지하기",
        "신발 정리하기",
        "침대 정돈하기"
    ],
    2: [
        "식탁 닦기",
        "분리수거 정리하기",
        "욕실 세면대 청소",
        "전자레인지 닦기",
        "냉장고 정리하기"
    ],
    3: [
        "설거지하기",
        "청소기 돌리기",
        "빨래 개기",
        "화장실 청소",
        "창틀 먼지 제거"
    ],
    4: [
        "바닥 물걸레질",
        "주방 전체 청소",
        "창문 청소",
        "이불 세탁",
        "베란다 청소"
    ],
    5: [
        "대청소 진행하기",
        "냉장고 전체 비우고 청소",
        "옷장 정리 및 정돈",
        "집 전체 정리정돈",
        "창고 정리하기"
    ]
}

difficulty_info = {
    1: "⭐ 매우 쉬움",
    2: "⭐⭐ 쉬움",
    3: "⭐⭐⭐ 보통",
    4: "⭐⭐⭐⭐ 어려움",
    5: "⭐⭐⭐⭐⭐ 매우 어려움"
}

# 세션 상태 초기화
if "selected_task" not in st.session_state:
    st.session_state.selected_task = None

if "selected_level" not in st.session_state:
    st.session_state.selected_level = None

st.subheader("난이도 선택")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("1"):
        st.session_state.selected_level = 1
        st.session_state.selected_task = random.choice(chores[1])

with col2:
    if st.button("2"):
        st.session_state.selected_level = 2
        st.session_state.selected_task = random.choice(chores[2])

with col3:
    if st.button("3"):
        st.session_state.selected_level = 3
        st.session_state.selected_task = random.choice(chores[3])

with col4:
    if st.button("4"):
        st.session_state.selected_level = 4
        st.session_state.selected_task = random.choice(chores[4])

with col5:
    if st.button("5"):
        st.session_state.selected_level = 5
        st.session_state.selected_task = random.choice(chores[5])

st.markdown("---")

# 결과 표시
if st.session_state.selected_task:
    level = st.session_state.selected_level

    st.markdown(
        f"""
        <div class="result-box">
        추천 집안일<br><br>
        {st.session_state.selected_task}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.success(f"난이도 {level} - {difficulty_info[level]}")

    if st.button("🔄 다시 추천받기"):
        st.session_state.selected_task = random.choice(chores[level])
        st.rerun()

st.markdown("---")

# 오늘의 추천
st.subheader("🎲 오늘의 랜덤 집안일")

if st.button("오늘의 집안일 뽑기"):
    random_level = random.randint(1, 5)
    task = random.choice(chores[random_level])

    st.info(
        f"""
난이도: {random_level}

{difficulty_info[random_level]}

추천 집안일: {task}
"""
    )

# 하단 안내
with st.expander("ℹ️ 난이도 기준 보기"):
    st.write("""
    - 1 : 금방 끝나는 간단한 집안일
    - 2 : 가벼운 정리 및 청소
    - 3 : 일반적인 집안일
    - 4 : 체력이 필요한 집안일
    - 5 : 시간이 많이 드는 대규모 정리
    """)
