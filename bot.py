import telebot
import random
import os
from datetime import datetime

# ====== Получаем токен из переменной окружения ======
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# ====== Статистика и дата последнего сброса ======
stats = {}  # Счетчик добропожеланий
last_reset_date = datetime.now().date()

# ====== GIF списки ======
morning_gifs = [
    "https://cdn.oonimages.ru/posts/big/kartinka-dobroe-utro-s-kotikom-4690.gif",
    "https://otkritkiok.ru/posts/big/otkrytka-dobroe-utro-s-chudesnym-kotom-92947.gif",
    "https://otkritkiok.ru/posts/big/simpaticnaya-otkrytka-dobroe-utro-s-kotikom-141165.gif"
]

night_gifs = [
    "https://otkritkiok.ru/posts/big/otkrytka-spokoynoy-nochi-so-spyashchim-kотиком-84002.gif",
    "https://i.pinimg.com/originals/1b/71/eb/1b71ebc942ad2236e03221e835dd5b39.gif",
    "https://cdn.oonimages.ru/posts/big/kartinka-spokoynoy-nochi-s-kotikom-2920.gif"
]

badwords_gifs = [
    "https://99px.ru/sstorage/86/2016/02/image_861302160010511602429.gif",
    "https://media.tenor.com/TFpTD5Cj-ukAAAAM/cat-%D0%BA%D0%BE%D1%88%D0%BA%D0%B0.gif",
    "https://lh4.googleusercontent.com/proxy/DB3uJ0LyQsaxlrxEcg3kW7XgqoBaKIPxr5H1f1o26vXEZ8ezmTMY6FC6-Vuq_cC3QKewfRD_ZFhAS2AwNdMx5flPR1CdM_kNjEI"
]

# Ключевые слова
morning_keywords = ["доброе утро", "доброго утра", "утречко", "утро", "gm"]
night_keywords = ["спокойной ночи", "сладких снов", "споки ноки", "споки", "gn", "good night"]
bad_keywords = ["иди нахуй", "пошёл нахуй", "мне похуй"]

# ====== Функции ======
def check_keywords(text, keywords):
    t = text.lower()
    return any(k in t for k in keywords)

def get_username(user):
    if user.username:
        return user.username
    if user.first_name:
        return user.first_name
    return "друг"

# ====== /start ======
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user = get_username(message.from_user)

    welcome_gif = "https://cdn.oonimages.ru/posts/big/otkrytka-privet-s-kotom-8589.gif"

    if message.chat.type == "private":
        welcome_text = (
            f"Привет, {user}! 👋\n\n"
            "Я Доброе Утро Бот 🌞\n"
            "Я умею отправлять GIF с пожеланиями доброго утра и спокойной ночи.\n"
            "Веду статистику: кто сколько раз пожелал что-то доброго (сброс каждый день) 😎\n"
            "Создатель: @kirill9ka 🐾\n\n"
            "Просто напиши 'доброе утро' или 'спокойной ночи', и я пришлю GIF!"
        )
        bot.send_animation(chat_id, welcome_gif, caption=welcome_text)
    else:
        group_text = (
            "Привет всем в этой группе! 👋\n\n"
            "Я Доброе Утро Бот 🌞\n"
            "Я умею отправлять GIF с пожеланиями доброго утра и спокойной ночи.\n"
            "Веду статистику: кто сколько раз пожелал что-то доброго (сброс каждый день) 😎\n"
            "Создатель: @kirill9ka 🐾\n\n"
            "Пишите 'доброе утро' или 'спокойной ночи', и я пришлю GIF всем!"
        )
        bot.send_animation(chat_id, welcome_gif, caption=group_text)

# ====== /stats ======
@bot.message_handler(commands=['stats'])
def get_stats(message):
    chat_id = message.chat.id
    if chat_id not in stats or not stats[chat_id]:
        bot.send_message(chat_id, "Статистика пока пустая 🐾")
        return

    msg = "📊 *Статистика добропожеланий:*\n\n"
    for user, count in stats[chat_id].items():
        msg += f"• {user}: {count} добропожеланий\n"

    bot.send_message(chat_id, msg, parse_mode="Markdown")

# ====== Текстовые сообщения ======
@bot.message_handler(content_types=['text'])
def handle_text(message):
    global last_reset_date

    chat_id = message.chat.id
    user = get_username(message.from_user)
    text = message.text.lower()

    today = datetime.now().date()
    if today != last_reset_date:
        stats.clear()
        last_reset_date = today

    stats.setdefault(chat_id, {})

    if check_keywords(text, morning_keywords):
        stats[chat_id][user] = stats[chat_id].get(user, 0) + 1
        gif = random.choice(morning_gifs)
        bot.send_animation(chat_id, gif, caption=f"Доброе утро, @{user}! ☀️")
        return

    if check_keywords(text, night_keywords):
        stats[chat_id][user] = stats[chat_id].get(user, 0) + 1
        gif = random.choice(night_gifs)
        bot.send_animation(chat_id, gif, caption=f"Спокойной ночи, @{user}! 🌙")
        return

    if check_keywords(text, bad_keywords):
        stats[chat_id][user] = stats[chat_id].get(user, 0) + 1
        gif = random.choice(badwords_gifs)
        bot.send_animation(chat_id, gif, caption=f"Это было грубо!, @{user}! 😖")
        return

# ====== Запуск бота ======
bot.polling(none_stop=True)
