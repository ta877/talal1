import os
from flask import Flask, render_template_string, request, jsonify
from google import genai
from google.genai import types
from PIL import Image
import io
import base64

app = Flask(__name__)

# قالب الصفحة الواحدة (Frontend + Backend في ملف واحد لسهولة الاستخدام)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live Camera - تحليل النظارة</title>
    <style>
        body { background-color: #121212; color: #ffffff; font-family: Tahoma, sans-serif; text-align: center; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; background: #1e1e1e; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        input, select, button { width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #444; background: #2a2a2a; color: #fff; }
        button { background: #007bff; border: none; cursor: pointer; font-weight: bold; }
        button:hover { background: #0056b3; }
        #result { margin-top: 20px; padding: 15px; background: #252525; border-radius: 5px; text-align: right; white-space: pre-wrap; }
        .preview { max-width: 100%; height: auto; border-radius: 5px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Live Camera Analysis</h2>
        <p>التقط صورة أو ارفعها لعرض التحليل المختصر:</p>
        
        <label>Gemini API Key:</label>
        <input type="password" id="apiKey" placeholder="أدخل مفتاح الـ API هنا">

        <label>اختر وضع نظام النظارة:</label>
        <select id="mode">
            <option value="تحليل نفسي وشخصي">1. تحليل نفسي وشخصي</option>
            <option value="تحليل عام ومحيطي">2. تحليل عام ومحيطي</option>
        </select>

        <label>اختر صورة:</label>
        <input type="file" id="imageInput" accept="image/*" onchange="previewImage(event)">
        <br>
        <img id="imagePreview" class="preview" style="display:none;">
        
        <button onclick="analyzeImage()">بدء التحليل</button>

        <h3>النتيجة:</h3>
        <div id="result">في انتظار التحليل...</div>
    </div>

    <script>
        let base64Image = "";

        function previewImage(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    base64Image = e.target.result;
                    const preview = document.getElementById('imagePreview');
                    preview.src = base64Image;
                    preview.style.display = 'block';
                }
                reader.readAsDataURL(file);
            }
        }

        async function analyzeImage() {
            const apiKey = document.getElementById('apiKey').value;
            const mode = document.getElementById('mode').value;
            const resultDiv = document.getElementById('result');

            if (!apiKey) {
                alert('الرجاء إدخال مفتاح الـ API');
                return;
            }
            if (!base64Image) {
                alert('الرجاء اختيار صورة أولاً');
                return;
            }

            resultDiv.innerText = "جاري تحليل الصورة، يرجى الانتظار...";

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ apiKey, mode, image: base64Image })
                });

                const data = await response.json();
                if (data.success) {
                    resultDiv.innerText = data.result;
                } else {
                    resultDiv.innerText = "خطأ: " + data.error;
                }
            } catch (err) {
                resultDiv.innerText = "حدث خطأ في الاتصال بالسيرفر: " + err.message;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        api_key = data.get('apiKey')
        mode = data.get('mode')
        image_data = data.get('image')

        if not api_key or not image_data:
            return jsonify({'success': False, 'error': 'المفتاح أو الصورة غير متوفرة'})

        # فصل رأس الـ Base64 عن البيانات الفعلية للصورة
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(image_bytes))

        # تهيئة عميل Google GenAI بالطريقة الحديثة
        client = genai.Client(api_key=api_key)

        prompt = f"قم بتحليل هذه الصورة بناءً على الوضع التالي: {mode}. اعطني نتيجة مختصرة ومفيدة باللغة العربية."

        # استدعاء الموديل الصحيح والسريع
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[image, prompt]
        )

        return jsonify({'success': True, 'result': response.text})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
