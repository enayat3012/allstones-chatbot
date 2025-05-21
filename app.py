
from flask import Flask, request, render_template

app = Flask(__name__)

def detect_country(phone):
    if phone.startswith("+966"):
        return "Saudi Arabia"
    elif phone.startswith("+46"):
        return "Sweden"
    return "Other"

def show_offer(country):
    if country == "Saudi Arabia":
    if language == "en":
        return "As part of Vision 2030, you get a 3% special discount!"
    elif language == "ar":
        return "ضمن رؤية 2030، ستحصل على خصم خاص بنسبة 3٪!"
    else:
        return ""  # برای سوئدی یا سایر زبان‌ها، پیام خالی بده


@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    offer = ""
    if request.method == "POST":
        contact = request.form["contact"]
        lang = request.form["language"]
        country = detect_country(contact)
        offer = show_offer(country)

        greetings = {
            "en": "Hello! How can I help you today?",
            "sv": "Hej! Hur kan jag hjälpa dig idag?",
            "ar": "مرحباً! كيف يمكنني مساعدتك اليوم؟"
        }
        response = greetings.get(lang, greetings["en"])

    return render_template("index.html", response=response, offer=offer)

if __name__ == "__main__":
    app.run(debug=True)
