"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений или другого инструмента извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""
import csv
import os


# get all *.txt from current directory
doc_list = list(filter(lambda x: x.endswith(".txt"), os.listdir()))


def get_data(list_of_files, *args):
    """
    :param list_of_files:  список файлов для обработки
    :param args: какие заголовки надо искать в файлах
    :return: список словарей для каждого из файла
    """
    list_of_dict = []
    for file in list_of_files:
        # создаем словарь сразу с нужным порядком ключей (как задано в args), чтобы его потом не сортировать
        working_dict = {}
        for key in args:
            working_dict[key]=''
        #построчно считываем файл для нахождения необходимых значений
        with open(file) as doc:
            for line in doc:
                # определение загаловка
                name = line[:line.find(':')]
                # проверяем, есть ли заголовок в наших аргументах
                if name in args:
                    working_dict[name] = line[line.find(':') + 1:].strip()
            list_of_dict.append(working_dict)
    return list_of_dict


def write_to_csv(list_of_dict):
    """
    запись словарей в *.CSV файл
    :param list_of_dict: список словарей для записи в файл
    :return: -
    """
    with open('data_report.csv', 'w') as csv_file:
        F_N_WRITER = csv.DictWriter(csv_file, fieldnames=list(list_of_dict[0].keys()), quoting=csv.QUOTE_NONE)
        F_N_WRITER.writeheader()
        for d in list_of_dict:
            F_N_WRITER.writerow(d)


write_to_csv(get_data(doc_list, 'Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы'))

with open('data_report.csv') as f_n:
    print(f_n.read())
