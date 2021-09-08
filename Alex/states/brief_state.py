from aiogram.dispatcher.filters.state import StatesGroup, State


class brief(StatesGroup):
    buyer = State()
    address = State()
    number = State()
    water_sources = State()
    water_sources_depth = State()
    object_type = State()
    water_manage = State()
    problems_from_customer = State()
    water_usage = State()
    water_usage_days = State()
    water_usage_hours = State()
    pump_efficiency = State()
    pressure = State()
    pressure_1 = State()
    water_use_max = State()
    water_use_normal = State()
    points = State()
    people = State()
    people_max = State()
    material = State()
    sewage_system = State()
    requirement = State()
    other = State()
    send_doc = State()


#Водоисточник: индивидуальная скважина, общая скважина (глубина: ), городской водопровод, колодец(глубина: ),
#открытый водоем, водонапорная башня,др. (нужное подчеркнуть)