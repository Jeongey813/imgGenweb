import streamlit as st
from openai import OpenAI

st.title("🖼️ AI 이미지 생성기")
st.write("텍스트를 입력하면, 해당 내용을 바탕으로 이미지를 생성합니다.")

# 사이드바: API 키 입력
st.sidebar.title("🔑 설정")
openai_api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")
if not openai_api_key:
    st.sidebar.warning("OpenAI API 키를 입력하세요.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

prompt = st.text_input("📝 이미지 설명을 입력하세요:", value="A beautiful landscape")

# 스타일 선택
style = st.radio(
    "원하는 이미지 스타일을 선택하세요:",
    options=["hyperrealism", "illustration", "pop-art"],
    horizontal=True
)

# 🆕 이미지 비율 선택 (가로 라디오 버튼)
aspect_ratio = st.radio(
    "이미지 비율을 선택하세요:",
    options=["16:9", "9:16", "1:1"],
    horizontal=True
)

# 비율에 따른 실제 사이즈 매핑
size_map = {
    "16:9": "1792x1024",
    "9:16": "1024x1792",
    "1:1": "1024x1024"
}
selected_size = size_map[aspect_ratio]

# 스타일별 추가 문구
style_phrases = {
    "hyperrealism": "in ultra-realistic hyperrealism style, 8K detail, photographic lighting",
    "illustration": "in colorful hand-drawn illustration style, vector art, soft shading",
    "pop-art": "in vibrant pop-art style, bold lines, halftone dots, bright contrasting colors"
}

if st.button("이미지 생성하기"):
    with st.spinner("이미지를 생성 중입니다..."):
        try:
            styled_prompt = f"{prompt}, {style_phrases[style]}"

            # 이미지 2장 생성
            response1 = client.images.generate(
                prompt=styled_prompt,
                model="dall-e-3",
                size=selected_size
            )
            response2 = client.images.generate(
                prompt=styled_prompt,
                model="dall-e-3",
                size=selected_size
            )

            image_url1 = response1.data[0].url
            image_url2 = response2.data[0].url

            st.subheader(f"🖼️ {style} 스타일 / 비율 {aspect_ratio} 이미지")
            st.image(image_url1, caption="생성된 이미지 1", use_container_width=True)
            st.image(image_url2, caption="생성된 이미지 2", use_container_width=True)

        except Exception as e:
            st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")
