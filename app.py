import streamlit as st
from google import genai
import os

# --- 1. API 키 설정 및 클라이언트 초기화 ---
# 환경 변수에서 API 키를 불러옵니다. Streamlit Cloud에 설정한 이름과 동일해야 합니다.
# (이름: GEMINI_API_KEY)
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("오류: GEMINI API 키가 설정되지 않았습니다. Streamlit Cloud의 Secrets에 키를 등록해주세요.")
    st.stop()

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"API 클라이언트 초기화 오류: {e}")
    st.stop()

# --- 2. Streamlit 웹 페이지 구성 ---
st.set_page_config(page_title="✈️ AI 여행 플래너", layout="wide")
st.title("AI 여행 플래너")
st.markdown("여행 정보를 입력하면 Gemini AI가 맞춤형 일정을 만들어 드립니다.")

# --- 3. 사용자 입력 섹션 (사이드바) ---
with st.sidebar:
    st.header("여행 정보 입력")
    # 텍스트 입력 필드
    destination = st.text_input("여행지", "제주도")
    # 숫자 입력 필드 (최소 1일)
    duration = st.text_input("여행 기간 (일)", "3" )
    # 넓은 텍스트 영역 (테마 및 상세 요청)
    theme = st.text_area("여행 테마 및 선호사항", "사진 찍기 좋은 카페, 맛집 위주로 계획해 줘.", height=150)

    # 4. 모델 호출 버튼
    if st.button("일정 생성 시작"):
        # 입력된 여행 기간을 정수로 변환
        try:
            duration = int(duration_str)
        except ValueError:
            st.error("오류: 여행 기간은 숫자로만 입력해야 합니다.")
            st.stop()
            
        if not destination or not theme or duration<1;
            st.error("여행지와 테마를 입력하고 기간은 1일 이상으로 설정해주세")
        else:
            # 5. 프롬프트 구성
            prompt = f"""
            당신은 최고의 여행 플래너입니다. 다음 정보를 바탕으로 상세하고 매력적인 {duration}일 여행 일정을 생성해 주세요.
            - 여행지: {destination}
            - 기간: {duration}일
            - 테마/선호사항: {theme}
            - 응답 형식: 각 일자별 오전/오후/저녁 활동을 구체적인 장소 추천과 함께 Markdown 형식으로 정리해 주세요.
            """

            # 6. 모델 호출 및 결과 처리
            with st.spinner("최고의 일정을 설계하는 중입니다..."):
                try:
                    # 'gemini-2.5-flash' 모델을 사용합니다.
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt
                    )
                    # 생성된 텍스트를 세션 상태에 저장하여 화면에 표시
                    st.session_state['travel_plan'] = response.text
                except Exception as e:
                    st.error(f"AI 모델 호출 중 오류가 발생했습니다. API 키나 설정 상태를 확인해주세요. 오류: {e}")

# --- 7. 결과 표시 ---
if 'travel_plan' in st.session_state:
    st.header("✨ 완성된 여행 일정")

    st.markdown(st.session_state['travel_plan']) # Markdown 형식으로 예쁘게 표시
