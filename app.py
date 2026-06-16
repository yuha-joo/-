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
