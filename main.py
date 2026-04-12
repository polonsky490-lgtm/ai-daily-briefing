import os
import google.generativeai as genai
import requests

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_briefing():
    try:
        genai.configure(api_key=GEMINI_KEY)
        
        # Пробуем самую стабильную модель
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = """
        Ты — ИИ-аналитик. Подготовь отчет для Григория. 
        1. ИИ-ИНСАЙДЫ (3 шт).
        2. ИИ-ПРОЕКТЫ (5 шт с описанием и ссылками).
        Используй эмодзи. Стиль лаконичный.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Если снова ошибка — мы хотим знать, какие модели нам ВООБЩЕ доступны
        try:
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            return f"Ошибка модели. Доступные варианты: {models}. Ошибка: {str(e)}"
        except:
            return f"Критическая ошибка API: {str(e)}"

def send_to_tg(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

if __name__ == "__main__":
    report = get_briefing()
    send_to_tg(report)
