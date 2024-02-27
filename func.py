import json
from datetime import datetime
from dateutil.parser import parse


get_data_operations = "user_operations.json"
def load_data_operations():
    """
    функция выводит список словарей операций в формате:
    'state': 'EXECUTED', 'date': '2018-08-06T16:22:54.643491', 'operationAmount': {'amount': '82946.19', 'currency':
    {'name': 'руб.', 'code': 'RUB'}}, 'description': 'Открытие вклада', 'to': 'Счет 12189246980267075758'}
    :return:list
    """
    with open(get_data_operations, "rt", encoding="utf-8") as file:
        data_operations = json.load(file)
        return data_operations
        # print(data_operations)
# print(load_data_operations())


def sort_data_operations(data_operations):
    """
    функция сортирует операции и выводит список по наличию признака EXECUTED
    :param data_operations: список словарей [operations_data] из функции load_data_operations()
    :return: list
    """
    ex_operations = []
    for data_operation in data_operations:
        if data_operation.get('state') == 'EXECUTED':
            ex_operations.append(data_operation)
        else:
            continue

    sorted_operations = sorted(ex_operations, key=lambda operation: operation['date'], reverse=True)
    five_last_operations = sorted_operations[:5]
    return five_last_operations


def reformat_date(date_str):
    """
    функция преобразует дату "date: 2019-08-26T10:50:58.294041" в формат "4.10.2018"
    :param date_str: 2019-08-26T10:50:58.294041 str
    :return:4.10.2018 str
    """
    # date_of_operation = datetime.strptime(date_str, "%Y-%m-%d")
    date_of_operation = parse(date_str)
    return date_of_operation.strftime("%d.%m.%Y")

#
# def mask_card_number(operate_info):
#     """
#     функция выводит зашифрованные данные по номерам карт и
#     счету операции
#     "from": "Maestro 1596837868705199",
#     "to": "Счет 64686473678894779589"
#     в зашифрованном виде: Visa Platinum 7000 79** **** 6361
#     :param operate_info: str(from to)
#     """
#     card_number = operate_info.split()[-1]
#     bank_name = operate_info.split()[:-1]
#     if bank_name == "Счет":
#         card_number = "**" + card_number[-4:]
#     else:
#         card_number = card_number[:5] + " " + card_number[5:7] + "** ****" + card_number[-4:]
#     masked_creds = " ".join(bank_name, card_number)
#     return masked_creds
#
#
# def mask_adress(banc_info: dict):
#     """
#     функция выводит замаскированный счет
#     :param banc_info: dict (полная банковская операция в виде словаря)
#     :return: str (7000 79** **** 6361 -> Счет **9638)
#     """
#     from_card = banc_info.get("from", "default")
#     to_card = banc_info.get("to")
#     if from_card != "default":
#         from_card = mask_card_number("from")
#     else:
#         to_card = mask_card_number("to")
#     result_str = f"{from_card} -> {to_card}"
#     return result_str
#
#
# def mask_amount(banc_info: dict):
#     """
#     функция выводит сумму операции и валюту (82771.72 руб.)
#     :param banc_info: dict (полная банковская операция в виде словаря)
#     :return:str (82771.72 руб.)
#     """
#     amount_info = banc_info['operationAmount']
#     money_amount = amount_info['amount']
#     money_currency = amount_info['currency']['name']
#     result_str = f"{money_amount} {money_currency}"
#     return result_str
#
#
# def show_info(banc_info: dict):
#     """
#     функция формирования строки конечного результата
#     :param banc_info: dict (полная банковская операция в виде словаря)
#     :return: str (14.10.2018 Перевод организации
#                   Visa Platinum 7000 79** **** 6361 -> Счет **9638
#                   82771.72 руб.
#     """
#     date = reformat_date(banc_info['date'])
#     adr = mask_adress(banc_info)
#     amount = mask_amount(banc_info)
#     result_str = (f"{date} {banc_info['description']}\n{adr}\n{amount}")
#     return result_str

