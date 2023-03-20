import os
from glob import glob
from urllib.parse import quote

import aiohttp_jinja2
from aiohttp import web

from libs.tpdf import TPdf


class ResponseFile(web.Response):
    def __new__(cls, file_name, file_body):
        headers = {
            'Content-Type': 'application/pdf; charset="utf-8"',
            'Content-Disposition': "inline; filename*=UTF-8''{}".format(
                quote(file_name, encoding='utf-8'))
        }
        return web.Response(body=file_body, headers=headers)


@aiohttp_jinja2.template('positioning.html')
async def positioning(request):
    tpdf = TPdf()
    # дефолтные параметры
    in_data = {
        'pdf_name': 'ClearPage',
        'page_num': '1',
    }
    in_data.update(dict(request.query))
    fields = tpdf.load_fields_from_file(name=in_data['pdf_name'], to_front=True)
    fonts = [os.path.basename(filename)[:-4] for filename in glob(os.path.join(tpdf.FONTS, '*.ttf'))]
    in_data.update({'fields': fields, 'fonts': fonts})
    return in_data


async def save_form_fields(request):
    rq = await request.json()
    return TPdf.save_fields_to_file(rq['pos'])


mime = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'bmp': 'image/bmp',
    'gif': 'image/gif',
    'pdf': 'application/pdf',
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.ms-excel',
    'xlsm': 'application/vnd.ms-excel',
    'doc': 'application/msword',
    'docx': 'application/msword',
    'rtf': 'application/rtf',
    'ppt': 'application/powerpoint',
    'pptx': 'application/powerpoint',
}


async def get_file(request):
    pdf_name = request.query['pdf_name']
    tpdf = TPdf()
    file = tpdf.get_pdf(pdf_name, b64='False', fill_x=True)
    return ResponseFile(pdf_name, file)


async def servicedog(request):
    # набор данных для генерации комплекта документов
    data = {
        'sh_n': '1',
        'date': '12',
        'month': '03',
        'year': '23',
        'byer': 'Герасимов Евгений',
        'name': 'Проверка "Тайный покупатель"',
        'count': '1',
        'sht': 'шт',
        'price': '89031',
        'summ': '89031 руб',
        'Itog': '12300 руб',
        'NDS': '89031 руб',
        'Vsego': '89031 руб',
        'rub': '89031',
        'kol': '1',
        'propis': 'Восемьдесят девять тысяч тридцать один рубль',
    }

    # перечень документов в комплекте
    complete = [
        ('servicedog', 1),
        ('ClearPage', 1),
    ]

    # загружаем данные в основной класс и получаем комплект документов в pdf
    tpdf = TPdf(**data)
    # можно сгенерировать один файл или комплект документов
    # file = tpdf.get_pdf('ZayavlenieNaZagranpasport ', b64='False')
    file = tpdf.get_complete(complete, b64='False')

    return ResponseFile('servicedog.pdf', file)
