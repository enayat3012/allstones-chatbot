
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# مقداردهی کلید API — یا از محیط، یا مستقیم
openai.api_key = os.getenv("OPENAI_API_KEY") or "کلید_API_را_اینجا_بگذارید"

@app.route("/start-chat", methods=["POST"])
def start_chat():
    data = request.json
    phone = data.get("phone", "")
    message = data.get("message", "")
    language = data.get("lang", "en")  # en, sv, ar

    # بررسی کشور عربستان
    special_offer = None
    if phone.startswith("+966"):
        special_offer = "تا سال 2030 با چشم‌انداز آینده، شما از تخفیف ویژه 3٪ بهره‌مند خواهید شد."

    # اگر پیام خالی باشد، پاسخ پیش‌فرض بده
    if not message:
        return jsonify({
            "reply": "لطفاً سوال خود را وارد کنید.",
            "special_offer": special_offer
        })

    # ارسال به OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that replies in {language}."},
                {"role": "user", "content": message}
            ]
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        reply = f"خطا در پاسخ‌دهی هوش مصنوعی: {str(e)}"

    return jsonify({
        "reply": reply,
        "special_offer": special_offer
    })

if __name__ == "__main__":
    app.run(debug=True)
