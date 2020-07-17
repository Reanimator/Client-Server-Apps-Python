"""
2. Задание на закрепление знаний по модулю json. Есть файл orders
в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий
его заполнение данными.

Для этого:
Создать функцию write_order_to_json(), в которую передается
5 параметров — товар (item), количество (quantity), цена (price),
покупатель (buyer), дата (date). Функция должна предусматривать запись
данных в виде словаря в файл orders.json. При записи данных указать
величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.

ПРОШУ ВАС НЕ УДАЛЯТЬ ИСХОДНЫЙ JSON-ФАЙЛ
ПРИМЕР ТОГО, ЧТО ДОЛЖНО ПОЛУЧИТЬСЯ

{
    "orders": [
        {
            "item": "printer",
            "quantity": "10",
            "price": "6700",
            "buyer": "Ivanov I.I.",
            "date": "24.09.2017"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        }
    ]
}

вам нужно подгрузить JSON-объект
и достучаться до списка, который и нужно пополнять
а потом сохранять все в файл
"""

import json


def write_order_to_json(item, quantity, price, buyer, date):
    with open('mein_orders.json') as file:
        OBJ = json.load(file)
        OBJ['orders'].append({"item": item, "quantity": quantity, "price": price, "buyer": buyer, "date": date})
    with open('mein_orders.json', 'w') as file:
        json.dump(OBJ, file, indent=4)


ORDER = ["printer", "20", "6700", "Petrov P.P.", "24.09.2017"]
"""Тут может быть ваша реклама, шутка, тут может быть ввод с клавиатуры или любой другой способ как ввести информацию"""

write_order_to_json(ORDER[0], ORDER[1], ORDER[2], ORDER[3], ORDER[4])
