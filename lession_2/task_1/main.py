"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""

from chardet.universaldetector import UniversalDetector
import re


def write_to_csv():
    pass


def get_data():
    main_data = [[
        "",
        "Изготовитель системы:",
        "Название ОС:",
        "Код продукта:",
        "Тип системы:"]]
    os_list = []
    for files in FILE_LIST:
        for data_number in range(1, 5):
            with open(files, encoding=detect(files)) as file:
                for string in file:
                    match = search_match(data_number, string, main_data)
                    if match is not None:
                        os_list.append(match)
        main_data.append(os_list)
        os_list = []
    return main_data


def detect(files):
    """encoding definition"""
    detector = UniversalDetector()
    with open(files, 'rb') as file:
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']


def search_match(text_number, string, main_data):
    match = re.search(main_data[0][text_number] + r'\s+', string)
    if match is not None:
        return string[match.end():-1]


FILE_LIST = [
    "info_1.txt",
    "info_2.txt",
    "info_3.txt"]

print(get_data())



