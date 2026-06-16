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
("쓰레기 버리기", "가장 빠르게 완료 가능한 집안일입니다."),
("신발 정리", "현관을 깔끔하게 만들 수 있습니다."),
("물컵 설거지", "부담 없이 시작하기 좋은 집안일입니다.")
],
2: [
("침대 정리", "방 분위기를 깔끔하게 바꿔줍니다."),
("옷 개기", "정리 습관을 만들기 좋습니다."),
("식탁 닦기", "위생 관리에 도움이 됩니다."),
("냉장고 문 정리", "짧은 시간에 할 수 있습니다.")
],
3: [
("설거지", "꾸준히 해야 하는 대표적인 집안일입니다."),
("방 청소기 돌리기", "깨끗한 생활환경을 만듭니다."),
("욕실 세면대 청소", "생각보다 금방 끝납니다."),
("빨래 개기", "20분 내외로 완료 가능합니다.")
],
4: [
("욕실 청소", "시간과 노력이 필요한 작업입니다."),
("주방 정리", "여러 구역을 정리해야 합니다."),
("창문 닦기", "체력이 필요한 집안일입니다."),
("베란다 청소", "먼지 제거에 효과적입니다.")
],
5: [
("냉장고 전체 청소", "대청소 수준의 작업입니다."),
("옷장 정리", "시간이 많이 소요됩니다."),
("집 전체 청소", "가장 난이도가 높은 집안일입니다."),
("창고 정리", "큰 결심이 필요한 작업입니다.")
]
}

if "selected_level" not in st.session_state:
st.session_state.selected_level = None

if "current_chore" not in st.session_state:
st.session_state.current_chore = None

def recommend_chore(level):
try:
return random.choice(CHORES[level])
except Exception:
return ("추천 실패", "다시 시도해주세요.")

st.title("🧹 집안일 난이도별 추천기")
st.write("원하는 난이도를 선택하면 오늘 할 집안일을 추천해드립니다!")

st.divider()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
if st.button("1", use_container_width=True):
st.session_state.selected_level = 1
st.session_state.current_chore = recommend_chore(1)

with col2:
if st.button("2", use_container_width=True):
st.session_state.selected_level = 2
st.session_state.current_chore = recommend_chore(2)

with col3:
if st.button("3", use_container_width=True):
st.session_state.selected_level = 3
st.session_state.current_chore = recommend_chore(3)

with col4:
if st.button("4", use_container_width=True):
st.session_state.selected_level = 4
st.session_state.current_chore = recommend_chore(4)

with col5:
if st.button("5", use_container_width=True):
st.session_state.selected_level = 5
st.session_state.current_chore = recommend_chore(5)

if st.session_state.current_chore:
chore, reason = st.session_state.current_chore

```
st.success(
    f"난이도 {st.session_state.selected_level} 추천 결과"
)

st.markdown(
    f"""
```

### 📌 추천 집안일

## {chore}

💡 {reason}
"""
)

```
if st.button("🔄 같은 난이도에서 다시 추천"):
    st.session_state.current_chore = recommend_chore(
        st.session_state.selected_level
    )
    st.rerun()
```
