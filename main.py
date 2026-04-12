import os
import google.generativeai as genai
import requests

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_briefing():
    try:
        genai.configure(api_key=GEMINI_KEY)
        
        # Используем самую актуальную модель из твоего списка
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        # Возвращаем наш детальный промпт
        prompt = """
        Ты — ИИ-аналитик. Подготовь ежедневный отчет для Григория. 
        Структура:
        1. 🧠 ИИ-ИНСАЙДЫ: Топ-3 тренда за 24 часа.
        2. 🚀 ИИ-ПРОЕКТЫ: Топ-5 новых прикладных сервисов (не просто LLM). 
           Для каждого: Название, эмодзи-логотип, краткая суть, ссылка.
        Стиль: Профессиональный, лаконичный.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Ошибка при работе с Gemini: {str(e)}"

def send_to_tg(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    # Отправляем как обычный текст, чтобы не было ошибок форматирования
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

if __name__ == "__main__":
    report = get_briefing()
    send_to_tg(report)
