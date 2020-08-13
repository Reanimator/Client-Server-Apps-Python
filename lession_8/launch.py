import subprocess


WINDOW = []
while True:
    ACT = input('s - запуск, q - выход, x - закрыть всё')
    if ACT == 'q':
        break
    elif ACT == 's':
        WINDOW.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(1):
            WINDOW.append(subprocess.Popen('python client.py -m send', creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(2):
            WINDOW.append(subprocess.Popen('python client.py -m listen', creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACT == 'x':
        while WINDOW:
            WINDOW.pop().kill()
