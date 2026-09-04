import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# إعدادات الشاشة الكاملة
st.set_page_config(
    page_title="AR HUD Smart Glasses - Ultimate Pro", page_icon="👓", layout="wide"
)

# تصميم واجهة السايبربانك مع أنيميشن خط الليزر المتحرك
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0e14;
    }
    .hud-container {
        position: relative;
        background: linear-gradient(135deg, rgba(13, 27, 42, 0.95), rgba(20, 35, 60, 0.85));
        border: 2px solid #1e90ff;
        border-radius: 16px;
        padding: 22px;
        color: #ffffff;
        font-family: 'Courier New', Courier, monospace;
        box-shadow: 0 0 30px rgba(30, 144, 255, 0.5);
        margin-top: 15px;
        margin-bottom: 15px;
        width: 100%;
        overflow: hidden;
    }
    .hud-header {
        display: flex;
        justify-content: space-between;
        color: #00d2ff;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        border-bottom: 1px solid rgba(30, 144, 255, 0.4);
        padding-bottom: 6px;
        margin-bottom: 12px;
    }
    .hud-content {
        font-size: 16px;
        line-height: 1.7;
        color: #e0f7ff;
        white-space: pre-wrap;
    }
    .hud-footer {
        margin-top: 12px;
        font-size: 11px;
        color: #00ffcc;
        text-align: right;
        letter-spacing: 1px;
    }
    /* أنيميشن خط الليزر للمسح البصري */
    @keyframes scanline {
        0% { transform: translateY(-100%); opacity: 0.8; }
        50% { opacity: 1; }
        100% { transform: translateY(500%); opacity: 0.8; }
    }
    .scan-laser {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: #00ffcc;
        box-shadow: 0 0 12px #00ffcc;
        animation: scanline 1.2s infinite linear;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("👓 AR HUD Smart Glasses [ULTIMATE PRO]")
st.write("نظام الواقع المختلط المتقدم: اختر الوضع عبر الأزرار السريعة أو القائمة والتقط الصورة.")

# جلب مفتاح الـ API بأمان
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

if not api_key:
    api_key = st.text_input("أدخل مفتاح Gemini API:", type="password")

# حفظ الوضع النشط في الجلسة
if "mode" not in st.session_state:
    st.session_state["mode"] = "1. تحليل نفسي وشخصي"

# أزرار اختصار سريعة للتحويل الفوري بين الأوضاع
st.markdown("### ⚡ الأوضاع السريعة")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    if st.button("🧠 نفسي"): st.session_state["mode"] = "1. تحليل نفسي وشخصي"
with c2:
    if st.button("🔍 أشياء"): st.session_state["mode"] = "2. شرح الأشياء المحيطة"
with c3:
    if st.button("⚠️ عوائق"): st.session_state["mode"] = "3. إظهار عوائق الطريق والمخاطر"
with c4:
    if st.button("📡 رادار"): st.session_state["mode"] = "4. كشف الأشخاص (نظام رادار)"
with c5:
    if st.button("🚗 مركبات"): st.session_state["mode"] = "5. معرفة موديل المركبة ونوعها ولونها"

# قائمة الاختيار المتزامنة مع الأزرار
hud_mode = st.selectbox("الوضع الحالي النشط:", [
    "1. تحليل نفسي وشخصي",
    "2. شرح الأشياء المحيطة",
    "3. إظهار عوائق الطريق والمخاطر",
    "4. كشف الأشخاص (نظام رادار)",
    "5. معرفة موديل المركبة ونوعها ولونها"
], index=[
    "1. تحليل نفسي وشخصي",
    "2. شرح الأشياء المحيطة",
    "3. إظهار عوائق الطريق والمخاطر",
    "4. كشف الأشخاص (نظام رادار)",
    "5. معرفة موديل المركبة ونوعها ولونها"
].index(st.session_state["mode"]))

# التقاط الصورة بالكاميرا
image_file = st.camera_input("التقط صورة بالكاميرا")

if image_file and api_key:
    genai.configure(api_key=api_key)
    
    try:
        # استخدام النسخة السريعة والمستقرة جداً لضمان عدم التعليق
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # ضغط مكثف جداً للصورة لتطير بسرعة البرق وتتجنب أي بطء
        img = Image.open(image_file)
        img.thumbnail((320, 320))
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=50)
        img_bytes = buffered.getvalue()

        image_parts = [{"mime_type": "image/jpeg", "data": img_bytes}]

        # تخصيص البرومبت لكل وضع بشكل صارع ومختصر
        if "1." in hud_mode:
            prompt = "حلل الحالة النفسية والمزاج في سطر واحد مختصر جداً."
            mode_title = "PSYCHOLOGICAL SCANNER"
        elif "2." in hud_mode:
            prompt = "اذكر أهم الأشياء الظاهرة باختصار في سطر واحد."
            mode_title = "OBJECT EXPLAINER"
        elif "3." in hud_mode:
            prompt = "هل هناك عوائق أو مخاطر؟ اذكرها باختصار أو قل لا توجد."
            mode_title = "HAZARD DETECTOR"
        elif "4." in hud_mode:
            prompt = "حدد عدد الأشخاص ومواقعهم باختصار شديد."
            mode_title = "RADAR TRACKER"
        else:
            prompt = "اذكر موديل المركبة ولونها باختصار، أو قل لا توجد مركبة."
            mode_title = "VEHICLE RECOGNITION"

        # تنفيذ الطلب بصمت تام وبدون رسائل معلقة لضمان السرعة الفورية
        response = model.generate_content([image_parts[0], prompt])

        if response and response.text:
            st.markdown(
                f"""
                <div class="hud-container">
                    <div class="scan-laser"></div>
                    <div class="hud-header">
                        <span>{mode_title} [ULTRA-TURBO]</span>
                        <span>5G 📶 | 37°C 🌡️ | 99% 🔋</span>
                    </div>
                    <div class="hud-content">
                        {response.text}
                    </div>
                    <div class="hud-footer">
                        STATUS: SECURE & ACTIVE [OK]
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    except Exception as e:
        st.error(f"حدث خطأ أثناء المعالجة: {e}")

elif not api_key and (image_file is not None):
    st.warning("الرجاء إدخال مفتاح Gemini API للمتابعة.")
