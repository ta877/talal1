import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

st.set_page_config(page_title="AI HUD", layout="centered")
st.title("نظام النظارة (HUD) الذكية")

# تهيئة المفتاح
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.text_input("أدخل مفتاح Google Gemini API Key:", type="password")

img_file_buffer = st.camera_input("التقاط صورة من الكاميرا", key="camera")

if img_file_buffer is not None:
    image = Image.open(img_file_buffer)
    
    st.markdown("### :إصدار الأوامر والأنماط")
    col1, col2 = st.columns(2)
    
    prompt = ""
    with col1:
        if st.button("1 تحليل الأشياء التي أمامي"):
            prompt = "صف لي ما تراه في هذه الصورة بدقة واذكر أهم العناصر الظاهرة."
        if st.button("3 رادار الأفراد والمواقع"):
            prompt = "تعرف على الأشخاص والمواقع أو الأماكن الموجودة في الصورة."
        if st.button("5 موسوعة ومعلومات الشيء"):
            prompt = "قدّم معلومات مفصلة وموسوعية عن المكون الرئيسي في الصورة."

    with col2:
        if st.button("2 تحليل نفسي ولغة الجسد"):
            prompt = "حلل لغة الجسد والانفعالات الظاهرة للأشخاص في الصورة."
        if st.button("4 كاشف العوائق والمخاطر"):
            prompt = "حدد أي عوائق أو مخاطر أو تنبيهات مهمة في المشهد."

    if prompt:
        if not api_key:
            st.error("يرجى إدخال مفتاح GEMINI_API_KEY أولاً.")
        else:
            genai.configure(api_key=api_key)
            try:
                with st.spinner("جاري التحليل..."):
                    model = genai.GenerativeModel('gemini-1.5-flash-latest')
                    response = model.generate_content([prompt, image])
                    st.success("تم التحليل بنجاح!")
                    st.write(response.text)
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
