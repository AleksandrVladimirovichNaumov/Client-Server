"""
Задание 2.

Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя!!! методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""

import task_1

word1, word2, word3 = b"class", b"function", b"method"
list_of_bytes = [word1, word2, word3]

for bytes in list_of_bytes:
    print(f'длина {bytes}: {bytes.__len__()}')

print('*'*10)

task_1.type_of(list_of_bytes)