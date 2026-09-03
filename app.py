import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="Smart Glasses HUD", page_icon="🕶️", layout="centered")

st.title("🕶️ نظام النظارة الذكية (HUD)")
st.caption("أدخل مفتاح API، ثم التقط صورة من كاميرا الآيفون للتحليل الفوري")

api_key = st.text_input("مفتاح Google Gemini API Key:", type="password")

picture = st.camera_input("📸 التقاط صورة من الكاميرا")

def analyze_image(pil_img, prompt_text):
    if not api_key:
        st.error("⚠️ يرجى إدخال مفتاح الـ API أولاً.")
        return
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        with st.spinner("🧠 جاري التحليل عبر Gemini..."):
            response = model.generate_content([prompt_text, pil_img])
            st.success("✅ تم التحليل بنجاح!")
            st.markdown("### 🖥️ شاشة النظارة (HUD)")
            st.info(response.text)
    except Exception as e:
        st.error(f"❌ حدث خطأ: {str(e)}")

if picture and api_key:
    pil_img = Image.open(picture)

    st.subheader("إصدار الأوامر والأنماط:")
    
    col1, col2 = st.columns(2)

    with col1:
        if st.button("1️⃣ تحليل الأشياء التي أمامي", use_container_width=True):
            prompt = "أنت محرك نظارة ذكية HUD. حلل الصورة وتعرف فوراً على أهم الأشياء والعناصر الموجودة أمام الكاميرا باختصار شديد في نقاط."
            analyze_image(pil_img, prompt)

        if st.button("3️⃣ رادار الأفراد والمواقع", use_container_width=True):
            prompt = "أنت نظام رادار لنظارة ذكية HUD. رصد الأشخاص في المشهد، عددهم، مواقعهم (يمين/يسار/قريب)، ونشاطهم باختصار شديد."
            analyze_image(pil_img, prompt)

        if st.button("5️⃣ موسوعة ومعلومات الشيء", use_container_width=True):
            prompt = "أنت موسوعة معرفية لنظارة ذكية HUD. تعرف على الشيء الرئيسي المكتشف واذكر اسمه، استخدامه، ومعلومة قيمة عنه باختصار."
            analyze_image(pil_img, prompt)

    with col2:
        if st.button("2️⃣ تحليل نفسي ولغة الجسد", use_container_width=True):
            prompt = "أنت خبير لغة جسد لنظارة ذكية HUD. حلل الأشخاص نفسياً بناءً على تعبيرات الوجه ولغة الجسد (المزاج والانطباع) باختصار شديد."
            analyze_image(pil_img, prompt)

        if st.button("4️⃣ كاشف العوائق والمخاطر", use_container_width=True):
            prompt = "أنت نظام سلامة لنظارة ذكية HUD. امسح الطريق وحدد أي عائق أو خطر قريب يسبب التعثر أو الاصطدام، واكتب التنبيه فوراً وبسطرين."
            analyze_image(pil_img, prompt)
