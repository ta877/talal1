import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# تكبير الشاشة لتستغل المساحة الكاملة للمتصفح
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
        background: linear-gradient(135deg, rgba(13, 27, 42, 0.9), rgba(20, 35, 60, 0.8));
        border: 2px solid #1e90ff;
        border-radius: 16px;
        padding: 22px;
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

st.title("👓 AR HUD Smart Glasses (Turbo)")
st.write("وضع السرعة القصوى: اختر الوضع والتقط الصورة لتحليل فوري.")

# جلب مفتاح الـ API بأمان
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

if not api_key:
    api_key = st.text_input("أدخل مفتاح Gemini API:", type="password")

hud_mode = st.selectbox(
    "اختر وضع نظام النظارة:",
    [
        "1. تحليل نفسي وشخصي",
        "2. شرح الأشياء المحيطة",
        "3. إظهار عوائق الطريق والمخاطر",
        "4. كشف الأشخاص (نظام رادار)",
        "5. معرفة موديل المركبة ونوعها ولونها"
    ]
)

image_file = st.camera_input("التقط صورة بالكاميرا")

if image_file and api_key:
    try:
        genai.configure(api_key=api_key)
        
        # استخدام إعدادات تسريع الاستجابة وضغط الصورة لتطير بالسرعة
        model = genai.GenerativeModel("gemini-3.6-flash")
        
        # فتح وضغط الصورة لترسل للنموذج بأسرع وقت ممكن وبدون حجم ثقيل
        img = Image.open(image_file)
        img.thumbnail((640, 640)) # ضغط الأبعاد لسرعة خارقة
        
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=80)
        img_bytes = buffered.getvalue()

        image_parts = [
            {
                "mime_type": "image/jpeg",
                "data": img_bytes
            }
        ]

        if "1." in hud_mode:
            prompt = "حلل الحالة النفسية والمزاج في سطرين بحد أقصى وبدون مقدمات."
            mode_title = "PSYCHOLOGICAL SCANNER"
        elif "2." in hud_mode:
            prompt = "اذكر أهم الأشياء في الصورة في سطرين باختصار شديد."
            mode_title = "OBJECT EXPLAINER"
        elif "3." in hud_mode:
            prompt = "حدد المخاطر أو العوائق في الصورة إن وجدت باختصار شديد."
            mode_title = "HAZARD DETECTOR"
        elif "4." in hud_mode:
            prompt = "حدد عدد الأشخاص ومواقعهم باختصار شديد كأنك رادار."
            mode_title = "RADAR / PEOPLE TRACKER"
        else:
            prompt = "اذكر موديل المركبة، لونها، ونوعها باختصار، وإن لم توجد قل لا توجد مركبة."
            mode_title = "VEHICLE RECOGNITION"

        with st.spinner("⚡ جاري التحليل الفوري..."):
            response = model.generate_content([image_parts[0], prompt])

            st.markdown(
                f"""
                <div class="hud-container">
                    <div class="hud-header">
                        <span>{mode_title} [TURBO]</span>
                        <span>11:02 AM 🔋</span>
                    </div>
                    <div class="hud-content">
                        {response.text}
                    </div>
                    <div class="hud-footer">
                        STATUS: ULTRA-FAST [OK]
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    except Exception as e:
        st.error(f"حدث خطأ أثناء المعالجة: {e}")

elif not api_key and (image_file is not None):
    st.warning("الرجاء إدخال مفتاح Gemini API للمتابعة.")
