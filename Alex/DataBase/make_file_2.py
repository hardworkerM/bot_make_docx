from docxtpl import DocxTemplate


def make_file(customer, address, number, water_sources, name, object_type,
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
                         depth=None):
    doc = DocxTemplate(r"C:\Users\Григорий\PycharmProjects\Alex_bot\Alex\DataBase\tamplate_word.docx")
    if depth is None:
        water_sources = water_sources

    else:
        water_sources = f'{water_sources}, глубина: {depth}'

    context = {'customer': f"{customer}",
               'address': f'{address}',
               'phone': f'{number}',
               'water_sources': f'{water_sources}',
               'object_type': f"{object_type}",
               'water_manage': f'{water_manage}',
               'problems_from_customer': f'{problems_from_customer}',
               'water_usage': f'{water_usage}',
               'pump_efficiency': f"{pump_efficiency}",
               'pressure': f'{pressure}',
               'water_use_max': f'{water_use_max}',
               'water_use_normal': f'{water_use_normal}',
               'points': f"{points}",
               'people': f'{people}',
               'material': f'{material}',
               'sewage_system': f'{sewage_system}',
               'requirement': f"{requirement}",
               'day': f'{day}',
               'month': f'{month}',
               'year': f'{year}',


               }

    doc.render(context)

    file_name = name + '.docx'
    try:
        doc.save(file_name)
    except PermissionError:
        file_name = '1' + file_name
        doc.save(file_name)
    final = r"C:\Users\Григорий\PycharmProjects\Alex_bot\Alex"+f'\{file_name}'
    return final

