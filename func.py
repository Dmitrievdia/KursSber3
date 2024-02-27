import json
import os
# from datetime import datetime, date, time
from dateutil.parser import parse

if os.path.isfile("user_operations.json"):
    get_data_operations = "user_operations.json"
else:
    print('Файл базы данных user_operations.json отсутствует!')
    exit(0)


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
    date_of_operation = parse(date_str.split("T")[0])
    return date_of_operation.strftime("%d.%m.%Y")


# reformat_date("2019-08-26T10:50:58.294041")


def mask_card_number(operate_info):
    """
    функция выводит зашифрованные данные по номерам карт и
    счету операции
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589"
    в зашифрованном виде: Visa Platinum 7000 79** **** 6361
    :param operate_info: str(from to)
    """
    card_number = operate_info.split()[-1]
    bank_name = " ".join(operate_info.split()[:-1])
    if bank_name == "Счет":
        card_number = "**" + card_number[-4:]
    else:
        card_number = card_number[:5] + " " + card_number[5:7] + "** ****" + card_number[-4:]
    masked_creds = " ".join([bank_name, card_number])
    return masked_creds
    # print(masked_creds)


# mask_card_number("Счет 64686473678894779589")
# mask_card_number("Maestro Card 1596837868705199")


def mask_adress(banc_info: dict):
    """
    функция выводит замаскированный счет
    :param banc_info: dict (полная банковская операция в виде словаря)
    :return: str (7000 79** **** 6361 -> Счет **9638)
    """
    from_card = banc_info.get('from', "default")
    to_card = banc_info.get('to', "default")
    if from_card != "default":
        from_card = mask_card_number(from_card)
    if to_card != "default":
        to_card = mask_card_number(to_card)
    result_str = f"{from_card} -> {to_card}"
    return result_str
    # print(result_str)


# mask_adress(
#   {
#     "id": 441945886,
#     "state": "EXECUTED",
#     "date": "2019-08-26T10:50:58.294041",
#     "operationAmount": {
#       "amount": "31957.58",
#       "currency": {
#         "name": "руб.",
#         "code": "RUB"
#       }
#     },
#     "description": "Перевод организации",
#     "from": "Maestro 1596837868705199",
#     "to": "Счет 64686473678894779589"
#   })

def mask_amount(banc_info: dict):
    """
    функция выводит сумму операции и валюту (82771.72 руб.)
    :param banc_info: dict (полная банковская операция в виде словаря)
    :return:str (82771.72 руб.)
    """
    amount_info = banc_info['operationAmount']
    money_amount = amount_info['amount']
    money_currency = amount_info['currency']['name']
    result_str = f"{money_amount} {money_currency}"
    # amount = banc_info['operationAmount']['amount']
    # currency = banc_info['operationAmount']['currency']['name']
    # result_str = f"{amount} {currency}"
    return result_str

    # print(result_str)


# mask_amount({
#     "id": 441945886,
#     "state": "EXECUTED",
#     "date": "2019-08-26T10:50:58.294041",
#     "operationAmount": {
#       "amount": "31957.58",
#       "currency": {
#         "name": "руб.",
#         "code": "RUB"
#       }
#     },
#     "description": "Перевод организации",
#     "from": "Maestro 1596837868705199",
#     "to": "Счет 64686473678894779589"
#   })

def show_info(banc_info: dict):
    """
    функция формирования строки конечного результата
    :param banc_info: dict (полная банковская операция в виде словаря)
    :return: str (14.10.2018 Перевод организации
                  Visa Platinum 7000 79** **** 6361 -> Счет **9638
                  82771.72 руб.
    """

    date = reformat_date(banc_info['date'])
    # date_of_operation = reformat_date(date_str)
    adr = mask_adress(banc_info)
    amount = mask_amount(banc_info)
    result_str = f"\n{date} {banc_info['description']}\n{adr}\n{amount}"
    return result_str
    # print(result_str)

# show_info({
#     "id": 51314762,
#     "state": "EXECUTED",
#     "date": "2018-08-25T02:58:18.764678",
#     "operationAmount": {
#       "amount": "52245.30",
#       "currency": {
#         "name": "USD",
#         "code": "USD"
#       }
#     },
#     "description": "Перевод с карты на карту",
#     "from": "Visa Classic 4040551273087672",
#     "to": "Visa Platinum 7825450883088021"
#   }
# )
# ,
#   {
#     "id": 464419177,
#     "state": "CANCELED",
#     "date": "2018-07-15T18:44:13.346362",
#     "operationAmount": {
#       "amount": "71024.64",
#       "currency": {
#         "name": "руб.",
#         "code": "RUB"
#       }
#     },
#     "description": "Перевод с карты на счет",
#     "from": "Visa Gold 9657499677062945",
#     "to": "Счет 19213886662094884261"
#   },
#   {
#     "id": 560813069,
#     "state": "CANCELED",
#     "date": "2019-12-03T04:27:03.427014",
#     "operationAmount": {
#       "amount": "17628.50",
#       "currency": {
#         "name": "USD",
#         "code": "USD"
#       }
#     },
#     "description": "Перевод с карты на карту",
#     "from": "MasterCard 1796816785869527",
#     "to": "Visa Classic 7699855375169288"
#   },
#   {
#     "id": 894961746,
#     "state": "EXECUTED",
#     "date": "2019-08-04T20:17:25.443322",
#     "operationAmount": {
#       "amount": "2523.44",
#       "currency": {
#         "name": "руб.",
#         "code": "RUB"
#       }
#     },
#     "description": "Перевод со счета на счет",
#     "from": "Счет 33721541831646393763",
#     "to": "Счет 68774571780974952778"
#   },
#   {
#     "id": 360577236,
#     "state": "EXECUTED",
#     "date": "2019-09-07T07:20:13.889610",
#     "operationAmount": {
#       "amount": "18536.73",
#       "currency": {
#         "name": "руб.",
#         "code": "RUB"
#       }
#     },
#     "description": "Перевод с карты на карту",
#     "from": "Maestro 4284341727554246",
#     "to": "МИР 1582474475547301"
#   },
#   {
#     "id": 285353808,
#     "state": "EXECUTED",
#     "date": "2018-08-06T16:22:54.643491",
#     "operationAmount": {
#       "amount": "82946.19",
#       "currency": {
#         "name": "руб.",
#         "code": "RUB"
#       }
#     },
#     "description": "Открытие вклада",
#     "to": "Счет 12189246980267075758"
#   })
