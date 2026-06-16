import random
import streamlit as st

st.set_page_config(
    page_title="집안일 랜덤 돌리기",
    page_icon="🎲",
    layout="centered"
)

# 초기 데이터
DEFAULT_TASKS = [
    "설거지",
    "분리수거",
    "청소기 돌리기",
    "빨래 개기",
    "화장실 청소",
    "먼지 닦기",
    "음식물 쓰레기 버리기",
    "장보기"
]

# 세션 상태 초기화
if "tasks" not in st.session_state:
    st.session_state.tasks = DEFAULT_TASKS.copy()

if "history" not in st.session_state:
    st.session_state.history = []

if "used_tasks" not in st.session_state:
    st.session_state.used_tasks = []

st.title("🎲 집안일 랜덤 돌리기")
st.caption("오늘의 집안일을 랜덤으로 정해보세요!")

st.divider()

# 집안일 추가
st.subheader("➕ 집안일 추가")

new_task = st.text_input("새 집안일 입력")

if st.button("추가"):
    task = new_task.strip()

    if not task:
        st.warning("집안일 이름을 입력해주세요.")
    elif task in st.session_state.tasks:
        st.warning("이미 존재하는 집안일입니다.")
    else:
        st.session_state.tasks.append(task)
        st.success(f"'{task}' 추가 완료!")

st.divider()

# 현재 목록
st.subheader("📋 현재 집안일 목록")

if st.session_state.tasks:
    for idx, task in enumerate(st.session_state.tasks, start=1):
        st.write(f"{idx}. {task}")
else:
    st.error("등록된 집안일이 없습니다.")

st.divider()

# 옵션
st.subheader("⚙️ 추첨 옵션")

no_repeat = st.checkbox(
    "중복 방지 모드 (모든 집안일이 한 번씩 나올 때까지 중복 없음)",
    value=True
)

st.divider()

# 랜덤 추첨
st.subheader("🎯 집안일 뽑기")

if st.button("집안일 뽑기!", type="primary"):

    if not st.session_state.tasks:
        st.error("집안일을 먼저 등록해주세요.")
    else:
        try:
            available_tasks = st.session_state.tasks.copy()

            if no_repeat:
                available_tasks = [
                    task
                    for task in st.session_state.tasks
                    if task not in st.session_state.used_tasks
                ]

                if not available_tasks:
                    st.session_state.used_tasks = []
                    available_tasks = st.session_state.tasks.copy()

            selected = random.choice(available_tasks)

            if no_repeat:
                st.session_state.used_tasks.append(selected)

            st.session_state.history.insert(0, selected)

            st.success(f"🎉 오늘의 집안일: {selected}")

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

st.divider()

# 기록
st.subheader("🕒 최근 추첨 기록")

if st.session_state.history:
    for i, item in enumerate(st.session_state.history[:10], start=1):
        st.write(f"{i}. {item}")
else:
    st.info("아직 추첨 기록이 없습니다.")

st.divider()

# 초기화
if st.button("🔄 전체 초기화"):
    st.session_state.tasks = DEFAULT_TASKS.copy()
    st.session_state.history = []
    st.session_state.used_tasks = []
    st.success("초기화 완료!")
    st.rerun()
