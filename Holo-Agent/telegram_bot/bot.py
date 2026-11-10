import os
import threading

import requests
import telebot

from config import ADMIN_ID, TELEGRAM_TOKEN


class TgBot:
    def __init__(self, token=TELEGRAM_TOKEN, admin_id=ADMIN_ID):
        self.token = token
        self.admin_id = admin_id
        self.bot = telebot.TeleBot(token, parse_mode="HTML")
        self._register_handlers()

    def _register_handlers(self):
        @self.bot.message_handler(commands=["start"])
        def cmd_start(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("Старт", "Стоп")
            markup.row("Статус", "Кубки")
            self.bot.send_message(message.chat.id, "Бот запущен.", reply_markup=markup)

        @self.bot.message_handler(func=lambda m: True)
        def handle_text(message):
            text = message.text.strip()

            if text == "Старт":
                if os.path.exists("pause.flag"):
                    os.remove("pause.flag")
                self.bot.send_message(message.chat.id, "Бот активирован.")
                return

            if text == "Стоп":
                with open("pause.flag", "w", encoding="utf-8") as f:
                    f.write("paused")
                self.bot.send_message(message.chat.id, "Пауза активирована.")
                return

            if text == "Статус":
                self.bot.send_message(message.chat.id, "Бот активен")
                return

            if text == "Кубки":
                try:
                    response = requests.get("https://httpbin.org/get", timeout=5)
                    cups = 7 if response.status_code == 200 else 0
                    self.bot.send_message(message.chat.id, f"Кубки: {cups}")
                except Exception:
                    self.bot.send_message(message.chat.id, "Кубки: 0")

    def run(self):
        thread = threading.Thread(target=self.bot.infinity_polling, daemon=True)
        thread.start()
        return thread
