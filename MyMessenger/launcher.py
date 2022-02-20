import subprocess
import time

PROCESS = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все процессы: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('gnome-terminal -- python3 server.py', shell=True))
        print('s')
        time.sleep(2)
        for i in range(3):
            PROCESS.append(
                subprocess.Popen(f'gnome-terminal -- python3 client.py -m reader -u NewUser{i + 1}', shell=True))
            print('r', i)
            time.sleep(2)
    elif ACTION == 'x':
        while PROCESS != []:
            PROCESS[len(PROCESS) - 1].kill()
            PROCESS.pop()
