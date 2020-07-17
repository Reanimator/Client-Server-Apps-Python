"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.


default_flow_style и так по умолчанию False насколько я понимаю и красивая стилизация и так работает.
Или может я не понял и наоборот надо было сделать. Только зачем.
И после дампа он расположил их в другом порядке. Я так понимаю это так надо и исправлять тут ничего не надо. )
Короче если что, переделаю )
"""

import yaml

ITEMS_LIST = ['computer', 'printer', 'keyboard', 'mouse']
NUMBERS_LIST = 4
PRICE_LIST = {
    'computer': "200-500\u20AC",
    'printer': "100-200\u20A1",
    'keyboard': "50-100\u20A9",
    'mouse': "10-50\u20BF"}
DATA_TO_YAML = {
    'items': ITEMS_LIST,
    'items_quantity': NUMBERS_LIST,
    'items_price': PRICE_LIST}

with open('my_file.yaml', 'w', encoding='utf8') as file:
    yaml.dump(DATA_TO_YAML, file, allow_unicode=True, default_flow_style=False)

with open('my_file.yaml', encoding='utf8') as file:
    FILE_CONTENT = yaml.load(file, Loader=yaml.FullLoader)
print(FILE_CONTENT)

print(DATA_TO_YAML)
