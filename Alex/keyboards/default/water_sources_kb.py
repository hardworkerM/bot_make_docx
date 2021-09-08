from aiogram.types import ReplyKeyboardMarkup


def source_type():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Индивидуальная скважина')
    markup.add('Общая скважина')
    markup.add('Городской водопровод')
    markup.add('Колодец')
    markup.add('Открытый водоем')
    markup.add('Водонапорная башня')
    markup.add('другое')

    return markup


def object_type_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Коттедж индивидуальный')
    markup.add('Производство')
    markup.add('Котельная')
    markup.add('другое')

    return markup

def water_manage_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Хозяйственно-питьевые нужды')
    markup.add('Производство пива')
    markup.add('Производство безалкогольных напитков')
    markup.add('Производство негазированной питьевой воды')
    markup.add('Хозяйственно-питьевые нужды')
    markup.add('Производство пива')
    markup.add('Производство ликероводочной продукции')
    markup.add('Отопительные системы')
    markup.add('другое')

    return markup


def water_usage_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Непрерывный')
    markup.add('Периодический')
    markup.add('Посменный')
    markup.add('другое')

    return markup


def sewage_system_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Выгребная яма')
    markup.add('Аэрационный септик')
    markup.add('Центральная')
    markup.add('другое')

    return markup

"(Непрерывный, периодический, посменный(количество смен в сутки)\n"
"Длительность смены\n в часах"