import os
import streamlit as st
import google.generativeai as genai

# تكبير الشاشة لتستغل المساحة الكاملة للمتصفح
st.set_page_config(
    page_title="AR HUD Live Camera", page_icon="👓", layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0e14;
    }
    .hud-container {
        position: relative;
        background: linear-gradient(135deg, rgba(13, 27, 42, 0.9), rgba(20, 35, 60, 0.8));
        border: 2px solid #1e90ff;
        border-radius: 16px;
        padding: 20px;
        color: #ffffff;
        font-family: 'Courier New', Courier, monospace;
        box-shadow: 0 0 25px rgba(30, 144, 255, 0.4);
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
        border-bottom: 1px solid rgba(30, 144, 255, 0.3);
        padding-bottom: 6px;
        margin-bottom: 12px;
    }
    .hud-content {
        font-size: 16px;
        line-height: 1.5;
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

# جلب مفتاح الـ API بأمان
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

if not api_key:
    api_key = st.text_input("أدخل مفتاح Gemini API:", type="password")

image_file = st.camera_input("التقط صورة بالكاميرا")

if image_file and api_key:
    try:
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel("gemini-3.6-flash")
        
        bytes_data = image_file.getvalue()
        image_parts = [
            {
                "mime_type": "image/jpeg",
                "data": bytes_data
            }
        ]

        with st.spinner("جاري التحليل..."):
            # برومبت صارم جداً يمنع التفاصيل الطويلة ويخليه سطر واحد مركز
            prompt = (
                "أعطني تحليلاً مختصراً جداً من سطر واحد فقط (مثال: المزاج: هادئ | البيئة: غرفة داخلية). "
                "لا تكتب فقرات طويلة أبداً، فقط كلمات مركزة ومختصرة جداً لتظهر في شاشة نظارة ذكية."
            )

            response = model.generate_content([image_parts[0], prompt])

            st.markdown(
                f"""
                <div class="hud-container">
                    <div class="hud-header">
                        <span>HUD SCANNER / ACTIVE</span>
                        <span>10:42 AM 🔋</span>
                    </div>
                    <div class="hud-content">
                        {response.text}
                    </div>
                    <div class="hud-footer">
                        STATUS: OK [LOCKED]
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    except Exception as e:
        st.error(f"حدث خطأ أثناء المعالجة: {e}")

elif not api_key and (image_file is not None):
    st.warning("الرجاء إدخال مفتاح Gemini API للمتابعة.")
