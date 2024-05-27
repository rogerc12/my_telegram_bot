import requests
from bs4 import BeautifulSoup
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import time
import schedule
import threading
import os

# Bot token'ınızı ve chat ID'nizi buraya ekleyin
bot_token = '6647970505:AAED6eAD0MVlc7Aro1k_chNIoP9oDssOQ4k'
chat_id = 'whatadmin34'

# Bot token'ını ve chat ID'sini ortam değişkenlerinden almak için aşağıdaki kodu kullanabilirsiniz
# bot_token = os.getenv('TELEGRAM_TOKEN')
# chat_id = os.getenv('CHAT_ID')

# Bot token'ı geçerli olup olmadığını kontrol edin
if not bot_token:
    raise ValueError("TELEGRAM_TOKEN environment variable not set")
if not chat_id:
    raise ValueError("CHAT_ID environment variable not set")

bot = telegram.Bot(token=bot_token)

# URL ve kontrol edilecek sekme
url = 'https://www.klasgame.com/mmorpg-oyunlar/knight-unity/knight-unity-goldbar'
tab_to_check = 'BİZE SAT'

# Başlangıçta bildirimler kapalı
notifications_enabled = False

def check_tab():
    global notifications_enabled
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP hatalarını kontrol et
        soup = BeautifulSoup(response.content, 'html.parser')

        # Sekmeyi kontrol et
        tab = soup.find('a', text=tab_to_check)
        if tab and 'active' in tab.get('class', []):
            if notifications_enabled:
                bot.send_message(chat_id=chat_id, text=f"'{tab_to_check}' sekmesi açık!")
        else:
            print(f"'{tab_to_check}' sekmesi kapalı.")
    except Exception as e:
        print(f"Hata: {e}")

def enable_notifications(update: Update, context: CallbackContext):
    global notifications_enabled
    notifications_enabled = True
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bildirimler açıldı.")

def disable_notifications(update: Update, context: CallbackContext):
    global notifications_enabled
    notifications_enabled = False
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bildirimler kapatıldı.")

# Uygulamayı başlatın
application = Application.builder().token(bot_token).build()

# Komutları ekleyin
application.add_handler(CommandHandler('acik', enable_notifications))
application.add_handler(CommandHandler('kapali', disable_notifications))

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(600)

# Her saat başında kontrol et
schedule.every().hour.at(":00").do(check_tab)

if __name__ == "__main__":
    # Scheduler'ı ayrı bir thread'de çalıştır
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # Botu başlat
    application.run_polling()
