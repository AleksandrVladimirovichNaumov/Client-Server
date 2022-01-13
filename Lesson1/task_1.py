"""
Задание 1.

Каждое из слов «разработка», «сокет», «декоратор» представить
в буквенном формате и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать
в набор кодовых точек Unicode (НО НЕ В БАЙТЫ!!!)
и также проверить тип и содержимое переменных.

Подсказки:
--- 'разработка' - буквенный формат
--- '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430' - набор кодовых точек
--- используйте списки и циклы, не дублируйте функции
"""

word1, word2, word3 = "разработка", "сокет", "декоратор"
list_of_words = [word1, word2, word3]
u_word1 = "\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430"
u_word2 = "\u0441\u043e\u043a\u0435\u0442"
u_word3 = "\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440"
list_of_u_words = [u_word1, u_word2, u_word3]


def type_of(word_list):
    """
    get type of element from list
    :param word_list: list of words
    :return: string
    """
    for word in word_list:
        print(f"тип {word}: {type(word)}")


if __name__ == '__main__':
    type_of(list_of_words)
    print("*" * 10)
    type_of(list_of_u_words)
