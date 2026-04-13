import os
import google.generativeai as genai
import requests

# Загрузка секретов
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_instruction():
    # Читаем промпт из внешнего текстового файла
    try:
        with open("instruction.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return "Подготовь краткий отчет об ИИ." # Запасной вариант

def get_briefing(instruction):
    try:
        genai.configure(api_key=GEMINI_KEY)
        # Твоя проверенная модель
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        response = model.generate_content(instruction)
        return response.text
    except Exception as e:
        return f"Ошибка при работе с Gemini: {str(e)}"

def send_to_tg(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    # Отправляем сообщение частями, если оно слишком длинное для Telegram
    if len(text) > 4000:
        for x in range(0, len(text), 4000):
            requests.post(url, json={"chat_id": CHAT_ID, "text": text[x:x+4000]})
    else:
        requests.post(url, json={"chat_id": CHAT_ID, "text": text})

if __name__ == "__main__":
    # 1. Получаем "мозги" из текстового файла
    current_instruction = get_instruction()
    # 2. Генерируем отчет
    report = get_briefing(current_instruction)
    # 3. Доставляем в Telegram
    send_to_tg(report)
