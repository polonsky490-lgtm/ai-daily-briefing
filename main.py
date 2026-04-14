import os
import google.generativeai as genai
import requests
from datetime import datetime

# Загрузка секретов
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_instruction():
    try:
        with open("instruction.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return "Подготовь краткий отчет об ИИ."

def get_briefing(instruction):
    try:
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        # Получаем реальную дату сервера
        current_date = datetime.now().strftime("%d.%m.%Y")
        
        # Вставляем реальную дату в начало инструкции
        full_prompt = f"СЕГОДНЯШНЯЯ ДАТА: {current_date}\n\n{instruction}"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Ошибка при работе с Gemini: {str(e)}"

def send_to_tg(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    if len(text) > 4000:
        for x in range(0, len(text), 4000):
            requests.post(url, json={"chat_id": CHAT_ID, "text": text[x:x+4000]})
    else:
        requests.post(url, json={"chat_id": CHAT_ID, "text": text})

if __name__ == "__main__":
    current_instruction = get_instruction()
    report = get_briefing(current_instruction)
    send_to_tg(report)
