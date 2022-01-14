"""
Задание 3.

Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- обязательно!!! усложните задачу, "отловив" и обработав исключение,
придумайте как это сделать
"""
word1, word2, word3, word4 = "attribute", "класс", "функция", "type"
list_of_bytes = [word1, word2, word3, word4]


for word in list_of_bytes:
    try:
        print(bytes(word, 'ASCII'))
    except Exception as e:
        print(f'{word}: {e}')