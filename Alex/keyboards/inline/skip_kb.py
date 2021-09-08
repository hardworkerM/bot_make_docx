from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def skip_bt(message):
    markup = InlineKeyboardMarkup()
    skip = InlineKeyboardButton(text='Пропустить', callback_data='skip')
    markup.row(skip)
    await message.answer('Вы можете пропустить этот вопрос, если не знаете как ответить', reply_markup=markup)


def change_bt():
    markup = InlineKeyboardMarkup()
    change = InlineKeyboardButton('переписать', callback_data='change')
    markup.row(change)

    return markup
