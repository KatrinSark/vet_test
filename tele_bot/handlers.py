import os
import requests
import threading

from dotenv import load_dotenv
from telebot import TeleBot
from telebot.types import BotCommand, CallbackQuery

import buttons
from reminder import Reminder
from utils import convert_to_utc, format_telegram_message

load_dotenv()

TOKEN = os.getenv("TOKEN")
API_HOST = os.getenv("API_HOST")

bot = TeleBot(TOKEN)
bot.set_my_description("Запись на прием в ветклинику 'VET'.")
bot.set_my_commands([
    BotCommand("start", "Начни работу с ботом записи"),
])


class VetHandler:
    def __init__(self):
        self.states = {
            "waiting_for_name": 0,
            "waiting_for_surname": 1,
            "waiting_for_phone": 2
        }
        self.user_data = {}
        self.keyboard = buttons.get_main_menu_buttons()
        self.date_keyboard = buttons.get_date_buttons()
        self.time_keyboard = buttons.get_time_buttons()
        self.appointment_data = {}
        self.user_id = None

    def start(self):
        @bot.message_handler(commands=["start"])
        def start(message):
            self.user_id = message.from_user.id
            user = requests.get(f"http://{API_HOST}:8000/client/{message.from_user.id}")
            if user.ok:
                user_name = user.json()["name"]
                bot.send_message(message.chat.id, f"Здравствуйте, {user_name}!")
                bot.send_message(message.chat.id, "Выберете опцию:", reply_markup=self.keyboard)
            elif user.status_code == 404:
                self.user_data[message.chat.id] = {"telegram_id": message.from_user.id}
                bot.send_message(message.chat.id, f"Здравствуйте!")
                bot.send_message(message.chat.id, "Для совершения записи на прием "
                                                  "нужно авторизироваться.\n"
                                                  "Пожалуйста, введите свое имя:")
                self.set_state(message.chat.id, self.states["waiting_for_name"])
            else:
                bot.send_message(message.chat.id, f"Ошибка бота, попробуйте еще раз.")


        @bot.message_handler(func=lambda message: self.get_state(message.chat.id)
                             == self.states["waiting_for_name"])
        def get_name(message):
            self.user_data[message.chat.id]["name"] = message.text
            bot.send_message(message.chat.id, "Введите вашу фамилию:")
            self.set_state(message.chat.id, self.states["waiting_for_surname"])

        @bot.message_handler(func=lambda message: self.get_state(message.chat.id)
                             == self.states["waiting_for_surname"])
        def get_surname(message):
            self.user_data[message.chat.id]["surname"] = message.text
            bot.send_message(message.chat.id, "Введите ваш телефон:")
            self.set_state(message.chat.id, self.states["waiting_for_phone"])

        @bot.message_handler(func=lambda message: self.get_state(message.chat.id)
                             == self.states["waiting_for_phone"])
        def get_phone(message):
            self.user_data[message.chat.id]["phone"] = message.text
            bot.send_message(message.chat.id, "Спасибо за предоставленные данные!")
            bot.send_message(message.chat.id, "Выберете опцию:", reply_markup=self.keyboard)
            requests.post(f"http://{API_HOST}:8000/client/", data=self.user_data[message.chat.id])
            self.clear_all(message.chat.id)

        @bot.callback_query_handler(func=lambda callback: True)
        def appointment_callback(callback: CallbackQuery) -> None:
            message = callback.message
            if callback.data == "create_appointment":
                self.appointment_data[message.chat.id] = {"owner": self.user_id}
                bot.send_message(callback.message.chat.id, "Выберете дату:",
                                 reply_markup=self.date_keyboard)

            elif callback.data == "check_appointment":
                data = requests.get(
                    f"http://{API_HOST}:8000/appointment/user_list/?user_id={self.user_id}")
                appointments = format_telegram_message(data.json())
                bot.send_message(callback.message.chat.id, appointments)

            elif callback.data.startswith('date_'):
                date = callback.data.split("_")
                self.appointment_data[message.chat.id]["date"] = date[1]
                bot.send_message(callback.message.chat.id, "Выберете время:",
                                 reply_markup=self.time_keyboard)

            elif callback.data.startswith('time_'):
                time = callback.data.split("_")
                self.appointment_data[message.chat.id]["time"] = time[1]
                bot.send_message(callback.message.chat.id, "Введите вид животного:")

        @bot.message_handler(func=lambda message: True)
        def get_pet_name(message):
            self.appointment_data[message.chat.id]["pet"] = message.text
            date = convert_to_utc(self.appointment_data[message.chat.id])
            self.appointment_data[message.chat.id]["date"] = date
            del self.appointment_data[message.chat.id]["time"]

            requests.post(f"http://{API_HOST}:8000/appointment/",
                          data=self.appointment_data[message.chat.id])

            bot.send_message(message.chat.id, "Вы успешно записаны на прием!")

    def clear_all(self, user_id):
        if user_id in self.user_data:
            del self.user_data[user_id]

    def set_state(self, user_id, state):
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        self.user_data[user_id]["state"] = state

    def get_state(self, user_id):
        return self.user_data.get(user_id, {}).get("state")


if __name__ == "__main__":
    thread = threading.Thread(target=Reminder(API_HOST, bot).schedule_reminders)
    thread.start()
    VetHandler().start()

    polling_thread = threading.Thread(target=bot.polling, args=(True,))
    polling_thread.start()

