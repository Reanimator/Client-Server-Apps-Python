"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet
"""

import subprocess
import chardet


SITES = ["yandex.ru", "youtube.com"]
for sites in SITES:
    PING = subprocess.Popen(['ping', sites], stdout=subprocess.PIPE)
    for line in PING.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))
