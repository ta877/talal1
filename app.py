import os
import streamlit as st
import google.generativeai as genai

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

st.title("👓 AR HUD Smart Glasses")
st.write("اختر وضع التحليل من القائمة، ثم التقط الصورة ليظهر في واجهة النظارة.")

# جلب مفتاح الـ API بأمان
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

if not api_key:
    api_key = st.text_input("أدخل مفتاح Gemini API:", type="password")

# قائمة الخيارات المتقدمة للنظارة
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
        
        model = genai.GenerativeModel("gemini-3.6-flash")
        
        bytes_data = image_file.getvalue()
        image_parts = [
            {
                "mime_type": "image/jpeg",
                "data": bytes_data
            }
        ]

        # تخصيص البرومبت بناءً على الخيار اللي اختاره
        if "1." in hud_mode:
            prompt = "قم بتحليل الشخص في الصورة تحليلاً نفسياً وسلوكياً سريعاً في نقطتين أو ثلاث مختصرة جداً."
            mode_title = "PSYCHOLOGICAL SCANNER"
        elif "2." in hud_mode:
            prompt = "اشرح أهم الأشياء والمعالم الظاهرة في الصورة باختصار شديد في سطرين."
            mode_title = "OBJECT EXPLAINER"
        elif "3." in hud_mode:
            prompt = "حدد أي عوائق أو مخاطر محتملة في طريق أو محيط الصورة بشكل تحذيري مختصر."
            mode_title = "HAZARD & OBSTACLE DETECTOR"
        elif "4." in hud_mode:
            prompt = "اكشف عن وجود الأشخاص في الصورة وعددهم ومواقعهم كأنك نظام رادار بأسلوب مختصر."
            mode_title = "RADAR / PEOPLE TRACKER"
        else:
            prompt = "إذا كانت هناك سيارة أو مركبة في الصورة، حدد موديلها ونوعها ولونها ولوحتها بدقة. إذا لم توجد قل لا توجد مركبة."
            mode_title = "VEHICLE RECOGNITION HUD"

        with st.spinner("جاري معالجة نظام النظارة..."):
            response = model.generate_content([image_parts[0], prompt])

            st.markdown(
                f"""
                <div class="hud-container">
                    <div class="hud-header">
                        <span>{mode_title}</span>
                        <span>10:56 AM 🔋</span>
                    </div>
                    <div class="hud-content">
                        {response.text}
                    </div>
                    <div class="hud-footer">
                        STATUS: ACTIVE [OK]
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    except Exception as e:
        st.error(f"حدث خطأ أثناء المعالجة: {e}")

elif not api_key and (image_file is not None):
    st.warning("الرجاء إدخال مفتاح Gemini API للمتابعة.")
