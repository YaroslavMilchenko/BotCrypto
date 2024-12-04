import telebot
import requests
import json
import socket
import schedule
import time
from threading import Thread

API_TOKEN = '6546950432:AAFICrqH1yYPr2IPgwXS1XLgkQ_-_howuRo'
SERVER_ADDRESS = ('127.0.0.1', 65433)
BINANCE_API_URL = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'

bot = telebot.TeleBot(API_TOKEN)

# Функція для відправлення запиту до сервера
def send_request_to_server(data):
    try:
        with socket.create_connection(SERVER_ADDRESS, timeout=5) as sock:
            sock.sendall(json.dumps(data).encode("utf-8"))
            response = sock.recv(1024).decode("utf-8")
            return json.loads(response)
    except Exception as e:
        print(f"Помилка з'єднання із сервером: {e}")
        return {"message": "Не вдалося підключитися до сервера."}

# Функція для отримання курсу BTC з Binance
def get_bitcoin_price():
    try:
        response = requests.get(BINANCE_API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("price", "Помилка отримання ціни")
    except requests.RequestException as e:
        print(f"Помилка запиту до Binance: {e}")
        return "Помилка отримання даних"

# Функція для розсилки курсу підписникам
def send_bitcoin_price_to_subscribers():
    print("Розсилка ціни розпочата...")
    price = get_bitcoin_price()
    response = send_request_to_server({"action": "get_subscribers"})
    subscribers = response.get("subscribers", [])
    if not isinstance(subscribers, list):
        print("Помилка: Список підписників некоректний")
        return
    print(f"Поточні підписники: {subscribers}")
    for user_id in subscribers:
        try:
            bot.send_message(user_id, f"Поточний курс BTC/USDT: {price}")
        except Exception as e:
            print(f"Помилка надсилання повідомлення для {user_id}: {e}")

# Підписка на розсилку
@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    user_id = message.chat.id
    service = "BTCUSDT"
    response = send_request_to_server({"action": "subscribe", "user_id": user_id, "service": service})
    bot.send_message(user_id, response.get("message", "Помилка підписки"))

# Відписка від розсилки
@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    user_id = message.chat.id
    service = "BTCUSDT"
    response = send_request_to_server({"action": "unsubscribe", "user_id": user_id, "service": service})
    bot.send_message(user_id, response.get("message", "Помилка відписки"))

# Планувальник для автоматичної розсилки
def start_scheduled_tasks():
    print("Планувальник розпочав роботу...")
    schedule.every(1).minute.do(send_bitcoin_price_to_subscribers)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Запуск планувальника
def start_scheduler():
    scheduler_thread = Thread(target=start_scheduled_tasks)
    scheduler_thread.daemon = True
    scheduler_thread.start()

if __name__ == "__main__":
    send_bitcoin_price_to_subscribers()  # Тестова розсилка
    start_scheduler()
    print("Бот працює...")
    bot.polling(none_stop=True)
