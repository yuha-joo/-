import streamlit as st
import random

st.set_page_config(
    page_title="집안일 난이도별 추천기",
    page_icon="🧹",
    layout="centered"
)

CHORES = {
    1: [
        ("책상 정리", "5분 안에 끝낼 수 있는 간단한 정리입니다."),
        ("쓰레기 버리기", "가장 빠르게 완료 가능한 집안일입니다.")
    ],
    2: [
        ("침대 정리", "방 분위기를 깔끔하게 바꿔줍니다."),
        ("옷 개기", "정리 습관을 만들기 좋습니다.")
    ],
    3: [
        ("설거지", "꾸준히 해야 하는 대표적인 집안일입니다."),
        ("방 청소기 돌리기", "깨끗한 생활환경을 만듭니다.")
    ],
    4: [
        ("욕실 청소", "시간과 노력이 필요한 작업입니다."),
        ("주방 정리", "여러 구역을 정리해야 합니다.")
    ],
    5: [
        ("냉장고 전체 청소", "대청소 수준의 작업입니다."),
        ("집 전체 청소", "가장 난이도가 높은 집안일입니다.")
    ]
}

if "selected_level" not in st.session_state:
    st.session_state.selected_level = None

if "current_chore" not in st.session_state:
    st.session_state.current_chore = None

def recommend_chore(level):
    return random.choice(CHORES[level])

st.title("🧹 집안일 난이도별 추천기")
st.write("원하는 난이도를 선택하세요.")

cols = st.columns(5)

for i in range(5):
    level = i + 1

    if cols[i].button(str(level), use_container_width=True):
        st.session_state.selected_level = level
        st.session_state.current_chore = recommend_chore(level)

if st.session_state.current_chore:
    chore, reason = st.session_state.current_chore

    st.success(
        f"난이도 {st.session_state.selected_level} 추천 결과"
    )

    st.markdown(
        f"""
### 📌 추천 집안일

## {chore}

💡 {reason}
"""
    )

    if st.button("🔄 같은 난이도에서 다시 추천"):
        st.session_state.current_chore = recommend_chore(
            st.session_state.selected_level
        )
        st.rerun()
