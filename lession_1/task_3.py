"""
3. Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b''.

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- Попробуйте усложнить задачу, "отлавливая" и обрабатывая исключение
"""


# def to_bytes(strings):
#     """all to bytes"""
#     return bytes(strings, encoding="utf_8")
#
#
STR = ["attribute", "класс", "функция", "type"]
#
# for i in STR:
#     print(to_bytes(i))
#     print(type(to_bytes(i)))
#     # print(b"%r" % i)  # Или так, но там кавычки лишние вылезают, что не айс

"""
C bytes все работает, но это ж неправильно, не по заданию )
C b'' и eval можно вс. И на обработку ошибок ему что-то пофиг (
"""

def to_bytes2(string):
    """all to bytes"""
    return eval(b"string")


for i in STR:
    print(to_bytes2(i))
    print(type(to_bytes2(i)))




