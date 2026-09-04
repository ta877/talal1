import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(
    page_title="AR HUD Smart Glasses", page_icon="👓", layout="wide"
)

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
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("👓 AR HUD Live Camera")
st.write("التقط صورة لعرض التحليل المختصر داخل النظارة.")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

if not api_key:
    api_key = st.text_input("أدخل مفتاح Gemini API:", type="password")

hud_mode = st.selectbox("اختر وضع نظام النظارة:", [
    "1. تحليل نفسي وشخصي",
    "2. شرح الأشياء المحيطة",
    "3. إظهار عوائق الطريق والمخاطر",
    "4. كشف الأشخاص (نظام رادار)",
    "5. معرفة موديل المركبة ونوعها ولونها"
])

image_file = st.camera_input("التقط صورة بالكاميرا")

if image_file and api_key:
    genai.configure(api_key=api_key)
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        img = Image.open(image_file)
        img.thumbnail((320, 320))
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=50)
        img_bytes = buffered.getvalue()

        if "1." in hud_mode:
            prompt = "Analyze this image and describe the mood or psychological state in one short sentence."
            mode_title = "PSYCHOLOGICAL SCANNER"
        elif "2." in hud_mode:
            prompt = "What are the main objects visible in this image? Answer in one short sentence."
            mode_title = "OBJECT EXPLAINER"
        elif "3." in hud_mode:
            prompt = "Are there any hazards or obstacles in this image? Answer briefly."
            mode_title = "HAZARD DETECTOR"
        elif "4." in hud_mode:
            prompt = "Count the people and describe their positions briefly."
            mode_title = "RADAR TRACKER"
        else:
            prompt = "Identify the vehicle model, color, and type if present. Answer briefly."
            mode_title = "VEHICLE RECOGNITION"

        response = model.generate_content([prompt, img])

        if response and response.text:
            st.markdown(
                f"""
                <div class="hud-container">
                    <div class="hud-header">
                        <span>{mode_title} [ACTIVE]</span>
                        <span>5G 📶 | 37°C 🌡️ | 99% 🔋</span>
                    </div>
                    <div class="hud-content">
                        {response.text}
                    </div>
                    <div class="hud-footer">
                        STATUS: SUCCESS [OK]
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.warning("لم يتم استلام رد، حاول التقاط صورة واضحة مرة أخرى.")

    except Exception as e:
        st.error(f"حدث خطأ في الاتصال: {e}")

elif not api_key and (image_file is not None):
    st.warning("الرجاء إدخال مفتاح Gemini API للمتابعة.")
