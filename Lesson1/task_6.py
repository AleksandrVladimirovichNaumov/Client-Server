"""
Задание 6.

Создать  НЕ программно (вручную) текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».

Принудительно программно открыть файл в формате Unicode и вывести его содержимое.
Что это значит? Это значит, что при чтении файла вы должны явно указать кодировку utf-8
и файл должен открыться у ЛЮБОГО!!! человека при запуске вашего скрипта.

При сдаче задания в папке должен лежать текстовый файл!

Это значит вы должны предусмотреть случай, что вы по дефолту записали файл в cp1251,
а прочитать пытаетесь в utf-8.

Преподаватель будет запускать ваш скрипт и ошибок НЕ ДОЛЖНО появиться!

Подсказки:
--- обратите внимание, что заполнять файл вы можете в любой кодировке
но открыть нужно ИМЕННО!!! в формате Unicode (utf-8)
--- обратите внимание на чтение файла в режиме rb
для последующей переконвертации в нужную кодировку

НАРУШЕНИЕ обозначенных условий - задание не выполнено!!!
"""
import chardet



#checking what is a real characters encoding and open with it
with open('test_file.txt', 'rb') as file:
    lines = file.read()
    detected_dict = chardet.detect(lines)
    print(f'кодировка: {detected_dict["encoding"]}')
    print(lines.decode(detected_dict["encoding"]).encode('UTF-8').decode('UTF-8'))
    print('*'*10)
with open('test_file.txt', 'w', encoding='utf-8') as file:
    file.write(lines.decode(detected_dict["encoding"]).encode('UTF-8').decode('UTF-8'))

# open with UTF-8 characters encoding by default
try:
    with open('test_file.txt', encoding='utf-8') as file:
        lines = file.read()
        print(lines)
except Exception as e:
    print(e)