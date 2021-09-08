from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,KeyboardButtonPollType

def get_loc():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    a = KeyboardButton('Контакт', request_contact=True)
    markup.add(a)

    return markup