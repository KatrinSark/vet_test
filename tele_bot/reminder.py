import schedule
import time
import datetime
import requests


class Reminder:
    def __init__(self, api, bot):
        self.user_id = None
        self.api = api
        self.bot = bot

    def send_reminder(self):
        appointments = requests.get(f"http://{self.api}:8000/appointment/")
        if appointments.ok:
            for appointment in appointments.json():
                json_date = appointment["date"]
                user_id = appointment["owner"]

                today = datetime.datetime.now().date()
                json_datetime = datetime.datetime.strptime(json_date, '%Y-%m-%dT%H:%M:%S%z').date()
                difference = json_datetime - today
                if difference.days == 1:
                    self.bot.send_message(user_id, f"У вас завтра запланирована запись на прием.")

    def schedule_reminders(self):
        schedule.every().day.at("09:00").do(self.send_reminder)
        while True:
            time.sleep(1)
            schedule.run_pending()
