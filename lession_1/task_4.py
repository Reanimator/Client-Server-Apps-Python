"""
4. Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""


def sandwich(string):
    """all to bytes und back"""
    byte_str = str.encode(string, encoding="utf-8")
    print(byte_str)
    print(type(byte_str))
    str_str = bytes.decode(byte_str, encoding="utf-8")
    print(str_str)
    print(type(str_str))


STR = ["разработка", "администрирование", "protocol", "standard"]

for i in STR:
    sandwich(i)
