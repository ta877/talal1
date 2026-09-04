import os
import streamlit as str_lit
from google import genai
from google.genai import types

# 1. تكبير الشاشة لتستغل المساحة الكاملة للمتصفح باستخدام layout="wide"
str_lit.set_page_config(
    page_title="AR HUD Live Camera", page_icon="👓", layout="wide"
)

str_lit.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0e14;
    }
    /* جعل واجهة النظارة تاخذ عرض أكبر وأوسع على الشاشة */
    .hud-container {
        position: relative;
        background: linear-gradient(135deg, rgba(13, 27, 42, 0.9), rgba(20, 35, 60, 0.8));
        border: 2px solid #1e90ff;
        border-radius: 16px;
        padding: 25px;
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
        font-size: 13px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        border-bottom: 1px solid rgba(30, 144, 255, 0.3);
        padding-bottom: 8px;
        margin-bottom: 15px;
    }
    .hud-content {
        font-size: 18px;
        line-height: 1.8;
        color: #e0f7ff;
        white-space: pre-wrap;
    }
    .hud-footer {
        margin-top: 15px;
        font-size: 12px;
        color: #00ffcc;
        text-align: right;
        letter-spacing: 1px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

str_lit.title("👓 AR HUD Live Camera")
str_lit.write("التقط صورة بالكاميرا ليظهر التحليل بشكل عريض وواضح داخل واجهة النظارة.")

# إدخال مفتاح الـ API
api_key = str_lit.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    api_key = str_lit.text_input("أدخل مفتاح Gemini API:", type="password")

# استخدام أعمدة لتنظيم الشاشة العريضة (مثلاً قسم للإعدادات والكاميرا وقسم للنتيجة)
col1, col2 = str_lit.columns([1, 1])

with col1:
    model_choice = str_lit.selectbox(
        "اختر نموذج Gemini:",
        ["gemini-2.5-flash", "gemini-2.5-pro"],
        index=0,
    )
    image_file = str_lit.camera_input("التقط صورة بالكاميرا")

with col2:
    if image_file and api_key:
        try:
            client = genai.Client(api_key=api_key)
            image_bytes = image_file.getvalue()

            with str_lit.spinner("جاري التحليل وعرض البيانات..."):
                prompt = (
                    "قم بتحليل الصورة بدقة تامة. أخرج النتيجة بشكل تعداد مختصر ونظيف جداً "
                    "(مثال: 1. [اسم العنصر] — [العدد أو الوصف]). "
                    "ممنوع نهائياً كتابة مقدمات أو شرح طويل، فقط العناصر والنتيجة مباشرة."
                )

                response = client.models.generate_content(
                    model=model_choice,
                    contents=[
                        types.Part.from_bytes(
                            data=image_bytes,
                            mime_type="image/jpeg",
                        ),
                        prompt,
                    ],
                )

                # عرض النتائج في شاشة النظارة العريضة
                str_lit.markdown(
                    f"""
                    <div class="hud-container">
                        <div class="hud-header">
                            <span>OBJECT DETECTED / COUNTING INTERFACE</span>
                            <span>10:42 AM 🔋</span>
                        </div>
                        <div class="hud-content">
                            {response.text}
                        </div>
                        <div class="hud-footer">
                            NE — E [INVENTORY COUNT]
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        except Exception as e:
            str_lit.error(f"حدث خطأ أثناء المعالجة: {e}")

    elif not api_key and (image_file is not None):
        str_lit.warning("الرجاء إدخال مفتاح Gemini API للمتابعة.")
