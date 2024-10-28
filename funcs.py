from datetime import datetime
from datetime import timedelta
import openai
from languages import lang_dict
from aiocryptopay import AioCryptoPay, Networks

# 101298:AAJZwArQifXWJyfPUZctjQUVyha4GsrOFUS
crypto_api = '101696:AA4nScwtRh2XLmqkY2CKuhMrmkwKIPy8uST'
crypto = AioCryptoPay(token=crypto_api, network=Networks.MAIN_NET)


def gpt_response(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=text,
        max_tokens=1500
    )
    return response


def set_context_length(id, context_data):
    while sum(context_data[str(id)]['tokens_list']) > 2500:
        context_data[str(id)]['context'].pop(0)
        context_data[str(id)]['tokens_list'].pop(0)
        context_data[str(id)]['total_tokens'] = sum(context_data[str(id)]['tokens_list'])
    return context_data


def get_premium_status(id, id_data):
    if id_data[str(id)]['premium']:
        return True
    else:
        return False


def set_access_time(id, id_data):
    tomorrow_date = datetime.now() + timedelta(days=1)
    access_list = id_data[str(id)]['access_time']
    if id_data[str(id)]['message_count'] == 0:
        id_data[str(id)]['access_time'] = [tomorrow_date.year, tomorrow_date.month, tomorrow_date.day,
                                           tomorrow_date.hour, tomorrow_date.minute]
    elif (datetime(access_list[0], access_list[1], access_list[2], access_list[3], access_list[4]) <=
          datetime.now()):
        id_data[str(id)]['message_count'] = 0
        id_data[str(id)]['access_time'] = [tomorrow_date.year, tomorrow_date.month, tomorrow_date.day,
                                           tomorrow_date.hour, tomorrow_date.minute]
    return id_data


def set_premium_access_time(id, id_data, days):
    if id_data[str(id)]['premium'] is False:
        date = datetime.now() + timedelta(days=days)
        id_data[str(id)]['premium_access_time'] = [date.year, date.month, date.day,
                                                   date.hour, date.minute]
        id_data[str(id)]['premium'] = True
    else:
        current_access_list = id_data[str(id)]['premium_access_time']
        premium_access_time = datetime(current_access_list[0], current_access_list[1], current_access_list[2],
                                       current_access_list[3], current_access_list[4]) + timedelta(days=days)
        id_data[str(id)]['premium_access_time'] = [premium_access_time.year, premium_access_time.month,
                                                   premium_access_time.day,
                                                   premium_access_time.hour, premium_access_time.minute]
    return id_data


def check_premium_access_time(id, id_data):
    access_list = id_data[str(id)]['premium_access_time']
    if datetime(access_list[0], access_list[1], access_list[2], access_list[3], access_list[4]) <= datetime.now():
        id_data[str(id)]['premium_access_time'] = None
        id_data[str(id)]['premium'] = False
    return id_data


def set_prompt_tokens(response, tokens_list):
    prompt_tokens = response['usage']['prompt_tokens']
    prompt_tokens -= sum(tokens_list)
    return prompt_tokens


def get_lang(id, id_data, comm):
    lang = id_data[str(id)]['language']
    return lang_dict[lang][comm]


def get_premium_time(id, id_data):
    date_list = id_data[str(id)]['premium_access_time']
    remaining_time = datetime(date_list[0], date_list[1], date_list[2], date_list[3], date_list[4]) - datetime.now()
    if remaining_time < timedelta(seconds=0):
        remaining_time = 0
    return remaining_time.days


async def create_invoice(asset, amount):
    invoice = await crypto.create_invoice(asset=asset, amount=amount)
    await crypto.close()
    return invoice


async def get_invoice(id):
    invoice = await crypto.get_invoices(invoice_ids=id)
    await crypto.close()
    return invoice
