
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# دریافت کلید API از محیط یا مقدار پیش‌فرض
openai.api_key = os.getenv("OPENAI_API_KEY") or "کلید_API_خود_را_اینجا_قرار_دهید"

@app.route("/start-chat", methods=["POST"])
def start_chat():
    data = request.json
    phone = data.get("phone", "")
    message = data.get("message", "")
    language = data.get("lang", "en")  # پیش‌فرض انگلیسی: en, sv, ar

    # بررسی شماره تلفن مربوط به عربستان
    special_offer = None
    if phone.startswith("+966"):
        special_offer = "تا سال 2030 با چشم‌انداز آینده، شما از تخفیف ویژه 3٪ بهره‌مند خواهید شد."

    # بررسی خالی بودن پیام
    if not message:
        return jsonify({
            "reply": "لطفاً سوال خود را وارد کنید.",
            "special_offer": special_offer
        })

    # ارسال پیام به GPT-4
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant replying in {language}."},
                {"role": "user", "content": message}
            ]
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        reply = f"خطا در ارتباط با OpenAI: {str(e)}"

    return jsonify({
        "reply": reply,
        "special_offer": special_offer
    })

if __name__ == "__main__":
    app.run(debug=True)
