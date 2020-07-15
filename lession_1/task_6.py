"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.

Подсказки:
--- обратите внимание, что заполнять файл вы можете в любой кодировке
но отерыть нужно ИМЕННО в формате Unicode (utf-8)

например, with open('test_file.txt', encoding='utf-8') as t_f
невыполнение условия - минус балл
"""

from chardet.universaldetector import UniversalDetector


def to_bytes(strings):
    """all to bytes"""
    return bytes(strings, encoding="utf_8")


def detect():
    """encoding definition"""
    detector = UniversalDetector()
    with open('test_file.txt', 'rb') as file:
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result


def write_str(strings):
    """write to file"""
    file = open('test_file.txt', 'wb')
    for i in strings:
        file.write(to_bytes(i + '\n'))
    file.close()


def open_utf():
    """opening in UTF"""
    with open('test_file.txt', encoding='utf-8') as file:
        for string in file:
            print(string, end='')


STR = ["сетевое программирование", "сокет", "декоратор"]

write_str(STR)
print(detect())
open_utf()
