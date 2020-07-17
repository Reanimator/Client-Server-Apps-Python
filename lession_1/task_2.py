"""
2. Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""


def to_bytes(string):
    """all to bytes"""
    return bytes(string, encoding="utf_8")


STR_1 = ["class", "function", "method"]

for i in STR_1:
    print(to_bytes(i))
    print(type(to_bytes(i)))
    print(len(to_bytes(i)))

"""
Тут не было в задании что нужно использовать b'', только совет, и bytes тоже вроде не запрещали
Сделал с b' '
"""

STR_2 = [b"class", b"function", b"method"]

for i in STR_2:
    print(i)
    print(type(i))
    print(len(i))
