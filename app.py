import streamlit as st
import random
import time
import base64

st.set_page_config(
    page_title="집안일 운명의 룰렛",
    page_icon="🏠",
    layout="centered"
)

# -----------------------------
# 효과음 (Web Audio API 사용)
# -----------------------------
def play_spin_sound():
    st.components.v1.html("""
    <script>
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    function beep(freq, duration){
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc.frequency.value = freq;
        osc.type = "triangle";

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();

        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(
            0.0001,
            audioCtx.currentTime + duration
        );

        osc.stop(audioCtx.currentTime + duration);
    }

    beep(400, 0.2);
    </script>
    """, height=0)


def play_win_sound():
    st.components.v1.html("""
    <script>
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    function beep(freq, duration){
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc.frequency.value = freq;
        osc.type = "sine";

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();

        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(
            0.0001,
            audioCtx.currentTime + duration
        );

        osc.stop(audioCtx.currentTime + duration);
    }

    beep(600, 0.15);
    setTimeout(() => beep(800, 0.15), 180);
    setTimeout(() => beep(1000, 0.25), 360);
    </script>
    """, height=0)


# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = None


# -----------------------------
# 제목
# -----------------------------
st.title("🏠 집안일 운명의 룰렛")
st.caption("누가 집안일을 할지 운명에 맡겨보세요!")

# -----------------------------
# 기본 집안일
# -----------------------------
default_tasks = [
    "설거지",
    "쓰레기 버리기",
    "분리수거",
    "화장실 청소",
    "방 청소",
    "빨래 개기",
    "빨래 널기",
    "바닥 청소",
    "먼지 제거",
    "주방 정리"
]

# -----------------------------
# 추가 입력
# -----------------------------
st.subheader("➕ 집안일 추가")

new_task = st.text_input("집안일 입력")

col1, col2 = st.columns(2)

with col1:
    if st.button("추가"):
        task = new_task.strip()

        if task:
            if task not in st.session_state.tasks:
                st.session_state.tasks.append(task)
                st.success(f"추가 완료: {task}")
            else:
                st.warning("이미 존재하는 항목입니다.")
        else:
            st.warning("내용을 입력하세요.")

with col2:
    if st.button("기본 집안일 넣기"):
        for item in default_tasks:
            if item not in st.session_state.tasks:
                st.session_state.tasks.append(item)

        st.success("기본 집안일 추가 완료!")

# -----------------------------
# 현재 목록
# -----------------------------
st.subheader("📋 현재 룰렛 목록")

if st.session_state.tasks:

    remove_target = st.selectbox(
        "삭제할 항목 선택",
        st.session_state.tasks
    )

    if st.button("선택 항목 삭제"):
        try:
            st.session_state.tasks.remove(remove_target)
            st.success("삭제 완료")
            st.rerun()
        except ValueError:
            st.error("삭제 중 오류 발생")

    for idx, item in enumerate(st.session_state.tasks, start=1):
        st.write(f"{idx}. {item}")

else:
    st.info("아직 집안일이 없습니다.")

st.divider()

# -----------------------------
# 룰렛
# -----------------------------
st.subheader("🎯 룰렛 돌리기")

if st.button("🎡 운명의 룰렛 시작!", type="primary"):

    if len(st.session_state.tasks) < 2:
        st.warning("최소 2개 이상의 집안일을 넣어주세요.")
    else:

        play_spin_sound()

        spinner = st.empty()

        for _ in range(20):
            spinner.markdown(
                f"# 🎲 {random.choice(st.session_state.tasks)}"
            )
            time.sleep(0.08)

        result = random.choice(st.session_state.tasks)

        st.session_state.result = result
        st.session_state.history.insert(0, result)

        play_win_sound()

        spinner.markdown(
            f"""
            <div style="
                background:#ffef9f;
                padding:20px;
                border-radius:15px;
                text-align:center;
                font-size:36px;
                font-weight:bold;
                color:#d35400;
            ">
            🎉 {result}
            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------------
# 결과 표시
# -----------------------------
if st.session_state.result:

    st.success(
        f"오늘의 집안일 당첨자는 👉 {st.session_state.result}"
    )

# -----------------------------
# 기록
# -----------------------------
st.divider()

st.subheader("📜 최근 당첨 기록")

if st.session_state.history:
    for i, item in enumerate(st.session_state.history[:10], start=1):
        st.write(f"{i}. {item}")
else:
    st.write("아직 기록이 없습니다.")

# -----------------------------
# 초기화
# -----------------------------
if st.button("🗑️ 전체 초기화"):
    st.session_state.tasks = []
    st.session_state.history = []
    st.session_state.result = None
    st.success("초기화 완료!")
    st.rerun()
