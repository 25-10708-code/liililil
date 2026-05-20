import streamlit as st
from openai import OpenAI

# 1. 웹 페이지 기본 설정
st.set_page_config(page_title="오늘의 감정 영화 추천", page_icon="🎬", layout="centered")

# 2. OpenAI API 키 설정
# *주의: 테스트용으로 키를 직접 넣을 때는 깃허브가 Public(공개) 상태이므로 키가 유출되지 않도록 주의하세요!
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE" 

# (권장) 깃허브 유출을 막기 위해 Streamlit Cloud의 Advanced Settings -> Secrets 기능을 쓴다면 
# 아래 줄의 주석(#)을 풀고 위 14번째 줄을 지워주시면 됩니다.
# OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

# 3. UI 화면 구성
st.title("🎬 오늘 어떤 하루를 보내셨나요?")
st.subheader("오늘 있었던 일을 한두 줄로 적어주시면, 딱 맞는 영화/드라마를 추천해 드려요.")

st.divider()

# 사용자 입력창
user_diary = st.text_input(
    label="오늘의 하루 요약", 
    placeholder="예: 오늘 회사에서 칭찬을 받아서 너무 기분 좋아!, 하루 종일 비가 와서 울적했어."
)

# 추천받기 버튼
if st.button("나에게 맞는 작품 추천받기 ✨"):
    if not user_diary.strip():
        st.warning("내용을 한 줄이라도 입력해 주세요!")
    elif OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
        st.error("OpenAI API 키를 설정해야 정상 작동합니다.")
    else:
        # 로딩 애니메이션
        with st.spinner("오늘의 하루를 분석하여 완벽한 작품을 고르는 중... 🍿"):
            try:
                # GPT에게 보낼 프롬프트(지시사항) 구성
                system_instruction = (
                    "당신은 세계 최고의 감성 영화 및 드라마 추천 전문가입니다. "
                    "사용자가 작성한 오늘 하루 일기를 바탕으로, 그 감정에 위로가 되거나 "
                    "즐거움을 배가시켜 줄 수 있는 영화 또는 드라마 2~3편을 추천해 주세요. "
                    "응답은 반드시 깔끔한 마크다운 형식을 사용하고, "
                    "각 작품의 [제목], [유형(영화/드라마)], [추천 이유]를 포함해 주세요."
                )
                
                # API 호출
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # 속도가 빠르고 가성비 좋은 모델
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": f"오늘 나의 하루: {user_diary}"}
                    ],
                    temperature=0.7
                )
                
                # 결과 출력
                recommendation = response.choices[0].message.content
                st.success("🎉 이런 작품들은 어떠신가요?")
                st.markdown(recommendation)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# 푸터
st.caption("Powered by Streamlit & OpenAI GPT-4o-mini")
