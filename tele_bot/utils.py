from datetime import datetime, timedelta, timezone


def convert_to_utc(timestamp):
    """Перевод полученного времени в формат datetime"""
    current_datetime = datetime.now()
    date_str = timestamp["date"]
    month, day = map(int, date_str.split('.'))

    year = current_datetime.year
    time_str = timestamp["time"]
    hour, minute = map(int, time_str.split(':'))

    converted_datetime = datetime(year, day, month, hour, minute)
    utc_offset = timedelta(hours=0)
    utc_datetime = converted_datetime - utc_offset

    formatted_datetime = utc_datetime.strftime('%Y-%m-%d %H:%M:%S.%f %z')

    return formatted_datetime


def format_telegram_message(data):
    message = "Список записей на прием:\n\n"

    for item in data:
        date_time = datetime.fromisoformat(item['date'].replace('Z', '+00:00'))
        formatted_date = date_time.strftime("%Y-%m-%d %H:%M")

        message += f"Дата: {formatted_date}\n"
        message += f"Вид животного: {item['pet']}\n"
        message += "---------------------\n"

    return message