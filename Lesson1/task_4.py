"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

word1, word2, word3, word4 = "разработка", "администрирование", "protocol", "standard"
list_of_words = [word1, word2, word3, word4]


def converter(list_obj, method):
    """
    encode or decode to UTF-8
    :param list_obj: list to decode/encode
    :param method: decode/encode
    :return: list of decode/encode obj
    """
    list_of_bytes = []
    for word in list_obj:
        if method == 'encode':
            list_of_bytes.append(word.encode('UTF-8'))
        elif method == 'decode':
            list_of_bytes.append(word.decode('UTF-8'))
    return list_of_bytes


list_of_bytes = converter(list_of_words, 'encode')
print(list_of_bytes)
print(converter(list_of_bytes, 'decode'))
