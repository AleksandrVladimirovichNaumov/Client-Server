import subprocess
import time

PROCESS = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('gnome-terminal -- python3 server.py', shell=True))
        print('s')
        time.sleep(2)
        for i in range(2):
            PROCESS.append(subprocess.Popen(f'gnome-terminal -- python3 client.py -m reader -u NewUser{i+1}', shell=True))
            print('r', i)
            time.sleep(2)
        for m in range(2):
            PROCESS.append(subprocess.Popen(f'gnome-terminal -- python3 client.py -m sender -u NewUser{m+1}', shell=True))
            time.sleep(1)
            print('s', m)
    elif ACTION == 'x':
        while PROCESS != []:
            PROCESS[len(PROCESS) - 1].kill()
            PROCESS.pop()
