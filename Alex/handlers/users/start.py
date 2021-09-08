import os
from aiogram.types import CallbackQuery
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db, bot
from states.brief_state import brief
from states.special_state import msg
from aiogram.dispatcher import FSMContext
from keyboards.default.water_sources_kb import source_type, \
    object_type_kb, water_manage_kb, water_usage_kb, sewage_system_kb
from keyboards.default.get_info_kb import get_loc
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline.skip_kb import skip_bt, change_bt
from DataBase.make_file_2 import make_file
import datetime, time
import json

months = {'01': 'января',
          '02': 'февраля',
          '03': 'марта',
          '04': 'апреля',
          '05': 'мая',
          '06': 'июня',
          '07': 'июля',
          '08': 'августа',
          '09': 'сентября',
          '10': 'октября',
          '11': 'ноября',
          '12': 'декабря'}


@dp.message_handler(commands='start')
async def start_cmnd(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,
                         photo=open(r"C:\Users\Григорий\PycharmProjects\Alex_bot\Alex\start_pic.png", 'rb'),
                         caption='ПОДБОР ВОДООЧИСТНОГО ОБОРУДОВАНИЯ\n\n'
                                 'Вы ответите на <b>вопросы</b>, а в конце мы пришлём заполненный документ - заявку\n\n'
                                 'Давайте начнём!\n')
    await message.answer('<b>Напишите ваше ФИО или юр.лицо</b>\n\n'
                         , reply_markup=ReplyKeyboardRemove())
    await brief.buyer.set()

    # 565843474


@dp.message_handler(state=brief.buyer)
async def buyer_name(message: types.Message, state: FSMContext):
    date = str(message.date)
    date = date.split(' ')[0].split('-')
    year = date[0]
    month = months[date[1]]
    day = date[2]
    async with state.proxy() as data:
        data['month'] = month
        data['day'] = day
        data['year'] = year
        data['buyer'] = message.text
    await message.answer('<b>Укажите адрес объекта</b>')
    await brief.address.set()


@dp.message_handler(state=brief.address)
async def buyer_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text

    await message.answer("<b>Напишите ваш телефон </b>\n\n"
                         "Пожалуйста, запишите в формате\n"
                         , reply_markup=get_loc()
                         # "<i>Так мы сможем с вами связаться</i>")
                         )
    await brief.number.set()


@dp.message_handler(state=brief.number, content_types=types.ContentTypes.CONTACT)
async def take_contact(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number

    async with state.proxy() as data:
        data['number'] = "+" + phone
    await message.answer('<b>Укажите свой источник воды</b>\n\n'
                         '<i>Ответ на этот вопрос поможет нам подобрать правильные методики'
                         ' и наборы показателей для анализа вашей воды</i>',
                         reply_markup=source_type())
    await brief.water_sources.set()


@dp.message_handler(state=brief.number)
async def buyer_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text
    await message.answer('<b>Укажите свой источник воды</b>\n\n'
                         '<i>Ответ на этот вопрос поможет нам подобрать правильные методики'
                         ' и наборы показателей для анализа вашей воды</i>',
                         reply_markup=source_type())
    await brief.water_sources.set()


# ВОДОИСТОЧНИК
@dp.message_handler(text='другое', state=brief.water_sources)
async def buyer_water_sources(message: types.Message, state: FSMContext):
    await message.answer('Укажите водоисточник\n\n'
                         '<i>Ответ на этот вопрос поможет нам подобрать правильные методики'
                         ' и наборы показателей для анализа вашей воды</i>',
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text='Общая скважина', state=brief.water_sources)
@dp.message_handler(text='Колодец', state=brief.water_sources)
async def buyer_water_sources(message: types.Message, state: FSMContext):
    await message.answer(f'<b>Пожалуйста, укажите глубину"{message.text}"\n\n</b>'
                         f'<i>Считается, что глубокие скважины чище, но это не всегда так.\n'
                         f' Чем глубже - тем больше вероятность обнаружения тяжелых металлов и радионуклидов.</i>',
                         reply_markup=ReplyKeyboardRemove())

    async with state.proxy() as data:
        data['water_sources'] = message.text
    await brief.water_sources_depth.set()


@dp.message_handler(state=brief.water_sources_depth)
async def buyer_water_sources_depth(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['water_sources_depth'] = message.text
    await message.answer('<b>Выберите объект установки</b>\n',
                         reply_markup=object_type_kb()
                         )
    await brief.object_type.set()


@dp.message_handler(state=brief.water_sources)
async def buyer_water_sources_orig(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['water_sources'] = message.text
    await message.answer('<b>Выберите объект установки</b>\n',
                         reply_markup=object_type_kb()
                         )
    await brief.object_type.set()


# ОБЪЕКТ УСТАНОВКИ
@dp.message_handler(text='другое', state=brief.object_type)
async def buyer_object_type_other(message: types.Message, state: FSMContext):
    await message.answer('<b>Напишите какой у вас объект установки</b>\n', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=brief.object_type)
async def buyer_object_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['object_type'] = message.text
    await message.answer('<b>Укажите Назначение воды</b>\n\n'
                         '<i>Выбор нормативных документов для оценки качества воды основывается на её применении.</i>',
                         reply_markup=water_manage_kb()
                         )
    await brief.water_manage.set()


# НАЗНАЧЕНИЕ ВОДЫ
@dp.message_handler(text='другое', state=brief.water_manage)
async def buyer_water_manage_other(message: types.Message, state: FSMContext):
    await message.answer("<b>Как Вы используете / планируете использовать воду?</b>\n\n"
                         "<i>Выбор нормативных документов для оценки качества воды основывается на её применении.</i>",
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=brief.water_manage)
async def buyer_water_manage(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['water_manage'] = message.text
    await message.answer("<b>Есть ли у вас жалобы на качество воды?</b>\n"
                         , reply_markup=ReplyKeyboardRemove())
    await brief.problems_from_customer.set()
    # await skip_bt(message)


# ЖАЛОБЫ
@dp.message_handler(state=brief.problems_from_customer)
async def buyer_problems_from_customer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['problems_from_customer'] = message.text
    await message.answer("<b>Укажите ваш режим водопотребления:</b>\n",
                         reply_markup=water_usage_kb()
                         )
    await brief.water_usage.set()


# Режим водопотребления
@dp.message_handler(text='другое', state=brief.water_usage)
async def buyer_water_usage_other(message: types.Message, state: FSMContext):
    await message.answer("Укажите ваш режим водопотребления", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text='Посменный', state=brief.water_usage)
async def buyer_water_usage_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['water_usage'] = message.text
    await message.answer("<b>Укажите количество смен в сутки</b>", reply_markup=ReplyKeyboardRemove())
    await brief.water_usage_days.set()


@dp.message_handler(state=brief.water_usage_days)
async def count_work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["water_usage_1"] = message.text
    await message.answer('<b>Укажите длительность смены в часах</b>', reply_markup=ReplyKeyboardRemove())
    await brief.water_usage_hours.set()


@dp.message_handler(state=brief.water_usage_hours)
async def count_work_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["water_usage_2"] = message.text
    data_full = await state.get_data()
    water1 = data_full.get('water_usage')
    water2 = data_full.get('water_usage_1')
    water3 = data_full.get('water_usage_2')
    water_usage = water1 + '. Количество смен:' + water2 + ', часов в смене ' + water3
    async with state.proxy() as data:
        data["water_usage"] = water_usage
    await message.answer("<b>Напишите производительность и марку подающего насоса</b>\n\n"
                         "<i>Единица измерения: м3/час</i>",
                         reply_markup=ReplyKeyboardRemove())
    # await skip_bt(message)
    await brief.pump_efficiency.set()
    current_state = await state.get_state()


@dp.message_handler(state=brief.water_usage)
async def buyer_water_usage(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['water_usage'] = message.text
    await message.answer("<b>Напишите производительность и марку подающего насоса</b>\n\n"
                         "<i>Единица измерения: м3/час</i>",
                         reply_markup=ReplyKeyboardRemove())
    # await skip_bt(message)
    await brief.pump_efficiency.set()


# Мощность
@dp.message_handler(state=brief.pump_efficiency)
async def buyer_pump_efficiency(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pump_efficiency'] = message.text
    await message.answer("<b>Укажите <u>номинальное</u> давление в системе водоснабжения</b>\n\n"
                         "<i>Единицы измерения: АТМ (атмосферы)</i>",
                         reply_markup=ReplyKeyboardRemove())
    # await skip_bt(message)
    await brief.pressure_1.set()


# Номинальное/пиковое
@dp.message_handler(state=brief.pressure_1)
async def buyer_pressure_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pressure_1'] = message.text
    await message.answer("<b>Укажите <u>пиковое</u> давление в системе водоснабжения</b>\n\n"
                         "<i>Единицы измерения: АТМ (атмосферы)</i>")
    # await skip_bt(message)
    await brief.pressure.set()


@dp.message_handler(state=brief.pressure)
async def buyer_object_type(message: types.Message, state: FSMContext):
    pressure_max = message.text
    data_full = await state.get_data()
    pressure_min = data_full.get('pressure_1')
    async with state.proxy() as data:
        data['pressure'] = pressure_min + '/' + pressure_max
    await message.answer("<b>Укажите пиковое водопотребление</b>\n\n"
                         "<i>Единицы измерения: м3/час </i>")
    # await skip_bt(message)
    await brief.water_use_max.set()


@dp.message_handler(state=brief.water_use_max)
async def buyer_object_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['water_use_max'] = message.text

    await message.answer("<b>Какое у вас среднее водопотребление в сутки</b>\n\n"
                         "<i>Единицы измерения: м3/сут </i>")
    # await skip_bt(message)
    await brief.water_use_normal.set()


@dp.message_handler(state=brief.water_use_normal)
async def buyer_object_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['water_use_normal'] = message.text
    data = await state.get_data()
    house_type = data.get('object_type')

    if house_type != 'Коттедж индивидуальный':
        await buyer_material(message, state, check=1)
        async with state.proxy() as data:
            data['points'] = ''
            data['people'] = ''

    else:
        await message.answer("<b>Характеристики объекта</b>\n\n"
                             "Укажите число точек водоразбора")
        await brief.points.set()


@dp.message_handler(state=brief.points)
async def buyer_object_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['points'] = message.text
    await message.answer("<b>Характеристики объекта</b>\n\n"
                         "Какое у вас <u>постоянное</u> число проживающих человек ?")

    await brief.people_max.set()


# количество проживающих
@dp.message_handler(state=brief.people_max)
async def buyer_object_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['people_min'] = message.text
    await message.answer("<b>Характеристики объекта</b>\n\n"
                         "Какое у вас <u>максимальное</u> число проживающих человек , чел ?")

    await brief.people.set()


@dp.message_handler(state=brief.people)
async def buyer_material(message: types.Message, state: FSMContext, check=None):
    if check is None:
        data_full = await state.get_data()
        people_norm = data_full.get('people_min')
        people_max = message.text
        async with state.proxy() as data:
            data['people'] = people_norm + ' / ' + people_max
    await message.answer("<b>Укажите материал и диаметр водопроводных труб</b>\n")
    await brief.material.set()
    current_state = await state.get_state()


# Тип канализации
@dp.message_handler(state=brief.material)
async def buyer_object_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['material'] = message.text
    await message.answer("<b>Укажите ваш тип канализации</b>\n",
                         reply_markup=sewage_system_kb()
                         )
    await brief.sewage_system.set()


@dp.message_handler(text='другое', state=brief.sewage_system)
async def buyer_object_type(message: types.Message, state: FSMContext):
    await message.answer("<b>Напишите ваш тип канализации</b>", reply_markup=ReplyKeyboardRemove())
    await brief.requirement.set()


@dp.message_handler(state=brief.sewage_system)
async def buyer_object_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sewage_system'] = message.text
    await message.answer("<b>У вас есть требования к качеству очищенной воды?</b>\n\n"
                         "<i>Напишите на что нам необходимо обратить внимание</i>", reply_markup=ReplyKeyboardRemove())
    await brief.requirement.set()


@dp.message_handler(state=brief.requirement)
async def buyer_object_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['requirement'] = message.text

    data_full = await state.get_data()
    buyer = data_full.get('buyer')
    address = data_full.get('address')
    number = data_full.get('number')
    water_sources = data_full.get('water_sources')
    water_sources_depth = data_full.get('water_sources_depth')
    object_type = data_full.get('object_type')
    water_manage = data_full.get('water_manage')
    problems_from_customer = data_full.get('problems_from_customer')
    water_usage = data_full.get('water_usage')
    pump_efficiency = data_full.get('pump_efficiency')
    pressure = data_full.get('pressure')
    water_use_max = data_full.get('water_use_max')
    water_use_normal = data_full.get('water_use_normal')
    points = data_full.get('points')
    people = data_full.get('people')
    material = data_full.get('material')
    sewage_system = data_full.get('sewage_system')
    requirement = data_full.get('requirement')
    day = data_full.get('day')
    month = data_full.get('month')
    year = data_full.get('year')
    doc = make_file(buyer,
                  address,
                  number,
                  water_sources,
                  buyer,
                  object_type,
                  water_manage,
                  problems_from_customer,
                  water_usage,
                  pump_efficiency,
                  pressure,
                  water_use_max,
                  water_use_normal,
                  points,
                  people,
                  material,
                  sewage_system,
                  requirement,
                  day,
                  month,
                  year,
                  depth=water_sources_depth)

    await bot.send_document(1865742665, open(doc, 'rb'), caption='Когда кто-то будет отвечать\n'
                                                                 'Именно тебе будет приходить сообщение с текстом:\n'
                                                                 '<b>Новая заявка!</b>')
    await bot.send_document(565843474, open(doc, 'rb'), caption='Новая заявка!')
    await bot.send_document(message.chat.id, open(doc, 'rb'))
    file_name = buyer + '.docx'
    os.remove(r"C:\Users\Григорий\PycharmProjects\Alex_bot\Alex" + f'\{file_name}')
    await message.answer(f"<b>Ваша заполненная заявка</b>\n\n"
                         f"<b>Заказчик: </b> \n"
                         f"<b>{buyer}</b>\n\n"
                         f"Проверьте введённые данные!\n"
                         f"<i>Если какие-то данные указаны неверно\n"
                         f"нажмите кнопку 'переписать'</i>",
                         reply_markup=change_bt()
                         )
    await state.finish()


@dp.callback_query_handler(text='change')
async def change_all(call: CallbackQuery):
    await start_cmnd(call.message)


# Вызываем фунцкию как в примере - для этого переименовать всё!
# Записываем пустоту или "Заказчик данные не указал - чтобы не было "None"
