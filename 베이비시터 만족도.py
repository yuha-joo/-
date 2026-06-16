import streamlit as st
import random
import time
import base64

st.set_page_config(
    page_title="집안일 룰렛 머신",
    page_icon="🎰",
    layout="centered"
)

DEFAULT_TASKS = {
    "설거지": "😐 보통",
    "분리수거": "😊 쉬움",
    "청소기 돌리기": "😐 보통",
    "빨래 개기": "😊 쉬움",
    "화장실 청소": "😭 어려움",
    "먼지 닦기": "😊 쉬움",
    "음식물 쓰레기 버리기": "😐 보통",
    "장보기": "😐 보통"
}

FORTUNES = [
    "오늘은 생각보다 일이 쉽게 끝날 거예요!",
    "집안일 후 시원한 음료 한 잔 어떠세요?",
    "성실함이 빛나는 하루입니다!",
    "작은 노력이 큰 만족으로 돌아옵니다!",
    "끝나고 나면 뿌듯함이 기다리고 있어요!"
]

if "tasks" not in st.session_state:
    st.session_state.tasks = DEFAULT_TASKS.copy()

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🎰 집안일 룰렛 머신")
st.caption("오늘의 집안일을 슬롯머신처럼 뽑아보세요!")

st.divider()

st.subheader("➕ 집안일 추가")

new_task = st.text_input("집안일 이름")

if st.button("추가"):
    task = new_task.strip()

    if not task:
        st.warning("집안일 이름을 입력해주세요.")
    elif task in st.session_state.tasks:
        st.warning("이미 존재합니다.")
    else:
        st.session_state.tasks[task] = "😐 보통"
        st.success(f"{task} 추가 완료!")

st.divider()

st.subheader("📋 집안일 목록")

for task, level in st.session_state.tasks.items():
    st.write(f"• {task} ({level})")

st.divider()

# 효과음 생성 함수
def play_sound(freq=440, duration=0.15):
    html = f"""
    <script>
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    oscillator.frequency.value = {freq};
    oscillator.type = 'sine';

    oscillator.start();

    gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(
        0.0001,
        audioCtx.currentTime + {duration}
    );

    oscillator.stop(audioCtx.currentTime + {duration});
    </script>
    """
    st.components.v1.html(html, height=0)

st.subheader("🎰 룰렛 머신")

slot_placeholder = st.empty()

if st.button("돌리기!", type="primary"):

    try:
        tasks = list(st.session_state.tasks.keys())

        if len(tasks) == 0:
            st.error("집안일이 없습니다.")
            st.stop()

        play_sound(700)

        # 슬롯 회전 연출
        for _ in range(20):
            current = random.choice(tasks)

            slot_placeholder.markdown(
                f"""
                <div style="
                    text-align:center;
                    font-size:40px;
                    padding:25px;
                    border:3px solid orange;
                    border-radius:15px;
                    background:#fff8e1;">
                    🎰 {current}
                </div>
                """,
                unsafe_allow_html=True
            )

            time.sleep(0.08)

        # 면제권 확률
        if random.random() < 0.10:

            result = "🎁 집안일 면제권!"
            level = "🥳 최고 행운"

        else:
            result = random.choice(tasks)
            level = st.session_state.tasks[result]

        play_sound(1000)

        slot_placeholder.markdown(
            f"""
            <div style="
                text-align:center;
                font-size:42px;
                padding:30px;
                border:4px solid green;
                border-radius:15px;
                background:#e8f5e9;">
                🎉 {result}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.success("결과 확정!")

        st.markdown(f"### 난이도: {level}")

        st.info("🍀 " + random.choice(FORTUNES))

        st.session_state.history.insert(
            0,
            result
        )

    except Exception as e:
        st.error(f"오류 발생: {e}")

st.divider()

st.subheader("🕒 최근 기록")

if st.session_state.history:
    for i, item in enumerate(st.session_state.history[:10], 1):
        st.write(f"{i}. {item}")
else:
    st.info("아직 기록이 없습니다.")

st.divider()

if st.button("🔄 초기화"):
    st.session_state.tasks = DEFAULT_TASKS.copy()
    st.session_state.history = []
    st.success("초기화 완료!")
    st.rerun()
