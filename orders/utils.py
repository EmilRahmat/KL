import requests
from decouple import config

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID')

def notify_telegram(order):
    text = f"🛒 Новый заказ #{order.pk}\nПользователь: {order.user.phone_number}\nСостав:\n"
    for item in order.items.all():
        text += f"- {item.variation.sku} {item.product.name} ({item.variation.size}) x {item.quantity}\n"
    text += f"\nСтатус: {order.get_status_display()}"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
    requests.post(url, data=data)
