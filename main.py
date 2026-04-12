import os
import google.generativeai as genai
import requests

# Загрузка секретов
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_briefing():
    try:
        genai.configure(api_key=GEMINI_KEY)
        # Используем обновленную модель
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        Ты — ИИ-аналитик. Подготовь краткий отчет для Григория. 
        1. ИИ-ИНСАЙДЫ (3 шт).
        2. ИИ-ПРОЕКТЫ (5 шт с описанием и ссылками).
        Используй только базовый текст, без сложных символов.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Ошибка при работе с Gemini: {str(e)}"

def send_to_tg(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    # Убираем parse_mode="Markdown", чтобы исключить ошибки форматирования на первом этапе
    payload = {"chat_id": CHAT_ID, "text": text}
    res = requests.post(url, json=payload)
    if res.status_code != 200:
        print(f"Ошибка Telegram: {res.text}")

if __name__ == "__main__":
    report = get_briefing()
    send_to_tg(report)
