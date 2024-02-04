import functools
from os.path import exists
from csv import DictReader, DictWriter


class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt


def getInfo():
    first_name = "Иван"
    last_name = "Иванов"

    is_valid_phone = False
    while not is_valid_phone:
        try:
            phone_number = int(input("Введите номер: "))
            if len(str(phone_number)) != 11:
                raise LenNumberError("Неверная длина номера.")
            else:
                is_valid_phone = True
        except ValueError:
            print("Не валидный номер.")
            continue
        except LenNumberError as err:
            print(err)
            continue

    return [first_name, last_name, phone_number]


def createFile(file_name):
    # with - Менеджер контекста
    with open(file_name, "w", encoding="utf-8") as data:
        f_writer = DictWriter(data, fieldnames=["Имя", "Фамилия", "Телефон"])
        f_writer.writeheader()


def readFile(file_name):
    with open(file_name, "r", encoding="utf-8") as data:
        f_reader = DictReader(data)
        return list(f_reader)


def writeFile(file_name, lst):
    res = readFile(file_name)
    for elem in res:
        if elem["Телефон"] == str(lst[2]):
            print("Такой телефон уже существует.")
            return
    obj = {"Имя": lst[0], "Фамилия": lst[1], "Телефон": lst[2]}
    res.append(obj)
    with open(file_name, "w", encoding="utf-8", newline="") as data:
        f_writer = DictWriter(data, fieldnames=["Имя", "Фамилия", "Телефон"])
        f_writer.writeheader()
        f_writer.writerows(res)


file_name = "phone.csv"


def main():
    while True:
        command = input("Введите команду: ")
        if command == "q":
            break
        elif command == "w":
            if not exists(file_name):
                createFile(file_name)
            writeFile(file_name, getInfo())
        elif command == "r":
            if not exists(file_name):
                print("Файл отсутствует, создайте его.")
                continue
            print(*readFile(file_name))
        elif command == "c":
            src_file = input("Введите имя исходного файла!: ")
            dest_file = input("Введите имя целевого файла!: ")
            line_num = int(input("Введите номер строки для копирования!: "))

            if not exists(src_file):
                print("Исходный файл не найден.")
                continue

            src_data = readFile(src_file)
            if line_num > len(src_data):
                print("Номер строки превышает количество строк в файле.")
                continue

            if not exists(dest_file):
                createFile(dest_file)

            dest_data = readFile(dest_file)
            dest_data.append(src_data[line_num])

            with open(dest_file, "w", encoding="utf-8", newline="") as data:
                f_writer = DictWriter(data, fieldnames=["Имя", "Фамилия", "Телефон"])
                f_writer.writeheader()
                f_writer.writerows(dest_data)

main()
