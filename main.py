import re
import csv


def format_names(contacts_list):
    """Format names in phonebook"""

    for line in contacts_list:
        pattern_name = (
            r"^([А-Я][а-яё]+)\s?\,?([А-Я][а-яё]+)\,?\s?([А-Я][а-яё]+|)"
        )
        result_name = re.findall(pattern_name, ','.join(line))
        if len(result_name) > 0:
            line[0] = list(result_name[0])[0]  # Фамилия
            line[1] = list(result_name[0])[1]  # Имя
            line[2] = list(result_name[0])[2]  # Отчество
    print("ФИО отформатированы")


def format_phones(contacts_list):
    """Format phones in phonebook"""

    for line in contacts_list:
        pattern_phone = (
            r"(\+7|8)\s*\(?(\d{3})\)?\s?\-?(\d{3})\s?"
            r"\-?(\d{2})\s?\-?(\d{2})\s?\(?[доб. ]*(\d{4})?"
        )
        result_phone = re.findall(pattern_phone, ','.join(line))
        if len(result_phone) > 0 and list(result_phone[0])[5] == "":
            phone_number = (
                f'+7({list(result_phone[0])[1]}){list(result_phone[0])[2]}-'
                f'{list(result_phone[0])[3]}-{list(result_phone[0])[4]}'
            )
        elif len(result_phone) > 0 and list(result_phone[0])[5] != "":
            phone_number = (
                f'+7({list(result_phone[0])[1]}){list(result_phone[0])[2]}-'
                f'{list(result_phone[0])[3]}-{list(result_phone[0])[4]} '
                f'доб.{list(result_phone[0])[5]}'
            )
        else:
            phone_number = ""
        line[5] = phone_number  # Телефон
    print("Номера телефонов отформатированы")


def merge_dubl(unic, dubl):
    """Merge dublicates in phonebook"""

    for i in range(0, len(unic)):
        if unic[i] == "" and dubl[i] != "":
            unic[i] = dubl[i]


def delete_dublicates(contacts_list):
    """Delete dublicates by lastname/firstname and update info in phonebook"""

    contacts_list_copy = contacts_list.copy()
    for num, line in enumerate(contacts_list_copy, 1):
        bio = line[0] + line[1]  # Уникальный идентификатор записи
        if num != len(contacts_list_copy):
            # Проверяем вниз по списку:
            for i in range(num, len(contacts_list_copy)):
                # Совпадение уникальных идентификаторов
                if bio == contacts_list_copy[i][0] + contacts_list_copy[i][1]:
                    merge_dubl(line, contacts_list_copy[i])
                    contacts_list.remove(contacts_list_copy[i])
    print("Дубликаты удалены")


def main():
    """Main function"""

# Считываем справочник --------------------------------
    with open('phonebook_raw.csv') as file:
        rows = csv.reader(file, delimiter=',')
        contacts_list = list(rows)

# Обрабатываем справочник -----------------------------
    format_names(contacts_list)
    format_phones(contacts_list)
    delete_dublicates(contacts_list)

# Записываем итоговый справочник ----------------------
    with open("phonebook.csv", "w") as file:
        datawriter = csv.writer(file, delimiter=',')
        datawriter.writerows(contacts_list)
    print("Обновленный справочник записан в файл 'phonebook.csv'")


if __name__ == '__main__':
    main()
