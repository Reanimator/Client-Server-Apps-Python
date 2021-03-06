"""
3. Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b''.

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- Попробуйте усложнить задачу, "отлавливая" и обрабатывая исключение
"""

STR = ["attribute", "класс", "функция", "type"]

for i in STR:
    try:
        print(bytes(i, encoding='ascii'))
    except UnicodeEncodeError:
        print("Слово %s невозможно записать в виде байтовой строки" % i)
