import subprocess

WINDOW = []
while True:
    ACT = input('s - запуск, q - выход, x - закрыть всё')
    if ACT == 'q':
        break
    elif ACT == 's':
        QUAN_CLIENT = int(input('Введите колическтво клиентов'))
        WINDOW.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
        # WINDOW.append(subprocess.Popen('python client.py -n test1',
        #                                creationflags=subprocess.CREATE_NEW_CONSOLE))
        # WINDOW.append(subprocess.Popen('python client.py -n test2',
        #                                creationflags=subprocess.CREATE_NEW_CONSOLE))
        # WINDOW.append(subprocess.Popen('python client.py -n test3',
        #                                creationflags=subprocess.CREATE_NEW_CONSOLE))

        for i in range(QUAN_CLIENT):
            WINDOW.append(subprocess.Popen(f'python client.py -n user{i+1}',
                                           creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACT == 'x':
        while WINDOW:
            WINDOW.pop().kill()
