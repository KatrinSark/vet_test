from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard(dict_data):
    """Обраотчик клавиатуры"""
    buttons = [
        InlineKeyboardButton(
            text=button_data.get("text"), callback_data=button_data.get("callback_data")
        )
        for button_data in dict_data
    ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    for button in buttons:
        keyboard.add(button)
    return keyboard


def get_date_buttons() -> InlineKeyboardMarkup:
    """ Кнопки с датами """
    main_button_data = [
        {"text": "17.05", "callback_data": "date_17.05"},
        {"text": "18.05", "callback_data": "date_18.05"},
        {"text": "19.05", "callback_data": "date_19.05"},
        {"text": "20.05", "callback_data": "date_20.05"},
        {"text": "21.05", "callback_data": "date_21.05"},
        {"text": "22.05", "callback_data": "date_22.05"},
    ]
    return get_keyboard(main_button_data)


def get_time_buttons() -> InlineKeyboardMarkup:
    """ Кнопки со временем """
    main_button_data = [
        {"text": "10:00", "callback_data": "time_10:00"},
        {"text": "11:00", "callback_data": "time_11:00"},
        {"text": "12:00", "callback_data": "time_12:00"},
        {"text": "13:00", "callback_data": "time_13:00"},
        {"text": "14:00", "callback_data": "time_14:00"},
        {"text": "15:00", "callback_data": "time_15:00"},
    ]
    return get_keyboard(main_button_data)


def get_main_menu_buttons() -> InlineKeyboardMarkup:
    """Кнопки главного меню авторизированного пользователя. """

    main_button_data = [
        {"text": "Записаться на прием", "callback_data": "create_appointment"},
        {"text": "Просмотреть свои записи", "callback_data": "check_appointment"},
    ]
    return get_keyboard(main_button_data)

