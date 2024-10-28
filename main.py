import openai
import telebot
from telebot import types
import json
import funcs
import threading
import asyncio

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

apikey = 'apikey'
tg_token = 'apikey'

openai.api_key = apikey
bot = telebot.TeleBot(tg_token)

id_default_dict = {
    'message_count': 0,
    'premium': False,
    'access_time': None,
    'language': 'ru',
    'premium_access_time': None}

context_default_dict = {
    'context': [],
    'total_tokens': 0,
    'tokens_list': []}

thread_dict = {}
invoice_dict = {}
is_start_active = False


@bot.message_handler(commands=['start'])
def start(message):
    global is_start_active
    with open('users_id.json') as f:
        id_data = json.load(f)
    if str(message.chat.id) not in id_data:
        is_start_active = True
        id_data[message.chat.id] = id_default_dict
        with open('users_id.json', 'w') as f:
            json.dump(id_data, f, indent=4)
        with open('users_context.json') as f:
            context_data = json.load(f)
        context_data[message.chat.id] = context_default_dict
        with open('users_context.json', 'w') as f:
            json.dump(context_data, f, indent=4)
        is_start_active = False
        bot.send_message(message.chat.id, 'Привет, с помощью этого бота можно вести диалог с чатом GPT\n\n'
                                          'Hello, with this bot you can have a dialogue with the GPT chat')
    else:
        lang = funcs.get_lang(message.chat.id, id_data, 'start')
        bot.send_message(message.chat.id, lang['in_chat_mess'])


@bot.message_handler(commands=['help'])
def desc(message):
    if is_start_active:
        desc(message)
    with open('users_id.json') as f:
        id_data = json.load(f)
    lang = funcs.get_lang(message.chat.id, id_data, 'help')
    bot.send_message(message.chat.id, lang)


@bot.message_handler(commands=['premium'])
def premium(message):
    if is_start_active:
        premium(message)
    with open('users_id.json') as f:
        id_data = json.load(f)
    lang = funcs.get_lang(message.chat.id, id_data, 'premium')
    button = [[types.InlineKeyboardButton(lang['1m_button'], callback_data='buy1')],
              [types.InlineKeyboardButton(lang['2m_button'], callback_data='buy2')],
              [types.InlineKeyboardButton(lang['3m_button'], callback_data='buy3')]]
    markup = types.InlineKeyboardMarkup(button)
    bot.send_message(message.chat.id, lang['default_mess'], reply_markup=markup)


@bot.message_handler(commands=['account'])
def account(message):
    if is_start_active:
        account(message)
    with open('users_id.json') as f:
        id_data = json.load(f)
    lang = funcs.get_lang(message.chat.id, id_data, 'account')
    message_count = id_data[str(message.chat.id)]['message_count']
    if funcs.get_premium_status(message.chat.id, id_data) is False:
        prem = lang['prem_false']
        message_accessed = 30 - message_count
    else:
        prem = lang['prem_true']
        message_accessed = 100 - message_count
        if message_accessed < 0:
            message_accessed = 0
        remaining_time = funcs.get_premium_time(message.chat.id, id_data)
        if remaining_time < 0:
            remaining_time = 0
        bot.send_message(message.chat.id, f'{lang["subs_type"]}: {prem} \n \n'
                                          f'{lang["prem_time"]}: {remaining_time} {lang["days"]}\n'
                                          f'{lang["mess_sent"]}: {message_count} \n'
                                          f'{lang["mess_left"]}: {message_accessed}')
        return
    if message_accessed < 0:
        message_accessed = 0
    bot.send_message(message.chat.id, f'{lang["subs_type"]}: {prem} \n \n'
                                      f'{lang["mess_sent"]}: {message_count} \n'
                                      f'{lang["mess_left"]}: {message_accessed}')


@bot.message_handler(commands=['context'])
def context(message):
    if is_start_active:
        context(message)
    with open('users_context.json') as f:
        context_data = json.load(f)
    with open('users_id.json') as f:
        id_data = json.load(f)
    lang = funcs.get_lang(message.chat.id, id_data, 'context')
    context_data[str(message.chat.id)]['context'] = []
    context_data[str(message.chat.id)]['total_tokens'] = 0
    context_data[str(message.chat.id)]['tokens_list'] = []
    with open('users_context.json', 'w') as f:
        json.dump(context_data, f, indent=4)
    bot.send_message(message.chat.id, lang)


@bot.message_handler(commands=['language'])
def language(message):
    if is_start_active:
        language(message)
    with open('users_id.json') as f:
        id_data = json.load(f)
    lang = funcs.get_lang(message.chat.id, id_data, 'language')
    buttons = [[types.InlineKeyboardButton('Russian', callback_data='ru')],
               [types.InlineKeyboardButton('English', callback_data='en')]]
    markup = types.InlineKeyboardMarkup(buttons)
    bot.send_message(message.chat.id, lang['choose_lang'], reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    if is_start_active:
        call_handler(call)
    if call.data == 'ru' or call.data == 'en':
        with open('users_id.json') as f:
            id_data = json.load(f)
        id_data[str(call.from_user.id)]['language'] = call.data
        lang = funcs.get_lang(call.from_user.id, id_data, 'language')
        with open('users_id.json', 'w') as f:
            json.dump(id_data, f, indent=4)
        bot.send_message(call.from_user.id, lang['succ_change'])
    elif call.data == 'buy1' or call.data == 'buy2' or call.data == 'buy3':
        with open('users_id.json') as f:
            id_data = json.load(f)
        lang = funcs.get_lang(call.from_user.id, id_data, 'payment')
        buttons = [[types.InlineKeyboardButton(lang['check'], callback_data='check')]]
        markup = types.InlineKeyboardMarkup(buttons)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        if call.data == 'buy1':
            invoice = loop.run_until_complete(funcs.create_invoice('USDT', 5))
            loop.close()
            invoice_dict[call.from_user.id] = {'invoice_id': invoice.invoice_id, 'days': 30}
            bot.send_message(call.from_user.id, f'{lang["desc"]}\n{invoice.pay_url}', reply_markup=markup)
        elif call.data == 'buy2':
            invoice = loop.run_until_complete(funcs.create_invoice('USDT', 8))
            loop.close()
            invoice_dict[call.from_user.id] = {'invoice_id': invoice.invoice_id, 'days': 60}
            bot.send_message(call.from_user.id, f'{lang["desc"]}\n{invoice.pay_url}', reply_markup=markup)
        elif call.data == 'buy3':
            invoice = loop.run_until_complete(funcs.create_invoice('USDT', 10))
            loop.close()
            invoice_dict[call.from_user.id] = {'invoice_id': invoice.invoice_id, 'days': 90}
            bot.send_message(call.from_user.id, f'{lang["desc"]}\n{invoice.pay_url}', reply_markup=markup)

    elif call.data == 'check':
        with open('users_id.json') as f:
            id_data = json.load(f)
        lang = funcs.get_lang(call.from_user.id, id_data, 'payment')
        if call.from_user.id not in invoice_dict:
            bot.send_message(call.from_user.id, lang['payment_failed'])
        else:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            current_invoice = loop.run_until_complete(funcs.get_invoice(invoice_dict[call.from_user.id]['invoice_id']))
            loop.close()
            if current_invoice.status == 'active':
                bot.send_message(call.from_user.id, lang['payment_failed'])
            elif current_invoice.status == 'paid':
                bot.send_message(call.from_user.id, lang['payment_passed'])
                changed_id_data = funcs.set_premium_access_time(call.from_user.id, id_data,
                                                                invoice_dict[call.from_user.id]['days'])
                with open('users_id.json', 'w') as f:
                    json.dump(changed_id_data, f, indent=4)
                invoice_dict.pop(call.from_user.id)


@bot.message_handler(content_types=['text'])
def thread(message):
    if is_start_active:
        thread(message)
    with open('users_id.json') as f:
        id_data = json.load(f)
    lang = funcs.get_lang(message.chat.id, id_data, 'thread_mess')
    if threading.active_count() > 5000:
        bot.send_message(message.chat.id, lang['overload_err'])
        return
    if message.chat.id not in thread_dict:
        user_thread = threading.Thread()
        user_thread.name = 'thread' + str(message.chat.id)
        thread_dict[message.chat.id] = user_thread
        user_thread.target = {gpt_message(message)}
    elif thread_dict[message.chat.id].is_alive:
        bot.send_message(message.chat.id, lang['req_err'])


def gpt_message(message):
    with open('users_id.json') as f:
        id_data = json.load(f)
    lang = funcs.get_lang(message.chat.id, id_data, 'text_mess')
    if len(message.text) > 1000:
        bot.send_message(message.chat.id, lang['mess_len_err'])
        thread_dict.pop(message.chat.id)
        return

    changed_id_data = funcs.set_access_time(message.chat.id, id_data)
    message_count = changed_id_data[str(message.chat.id)]['message_count']
    premium_status = funcs.get_premium_status(message.chat.id, changed_id_data)

    if premium_status is True:
        changed_id_data = funcs.check_premium_access_time(message.chat.id, changed_id_data)
        premium_status = changed_id_data[str(message.chat.id)]['premium']

    if message_count >= 30 and premium_status is False:
        bot.send_message(message.chat.id, lang['prem_false_err'])
        thread_dict.pop(message.chat.id)
        return
    if message_count >= 100 and premium_status is True:
        bot.send_message(message.chat.id, lang['prem_true_err'])
        thread_dict.pop(message.chat.id)
        return
    mess = bot.send_message(message.chat.id, lang['in_process'])

    user_dict = {'role': 'user', 'content': message.text}
    with open('users_context.json') as f:
        context_data = json.load(f)
    changed_context_data = funcs.set_context_length(message.chat.id, context_data)[str(message.chat.id)]['context']
    changed_context_data.append(user_dict)

    try:
        response = funcs.gpt_response(changed_context_data)
    except:
        bot.delete_message(message.chat.id, mess.message_id)
        bot.send_message(message.chat.id, lang['err'])
        thread_dict.pop(message.chat.id)
        return

    changed_id_data[str(message.chat.id)]['message_count'] += 1
    with open('users_id.json', 'w') as f:
        json.dump(changed_id_data, f, indent=4)
    response_text = response.choices[0].message['content']
    tokens_list = context_data[str(message.chat.id)]['tokens_list']
    assistant_dict = {'role': 'assistant', 'content': response_text}
    changed_context_data.append(assistant_dict)
    context_data[str(message.chat.id)]['context'] = changed_context_data
    context_data[str(message.chat.id)]['tokens_list'].append(funcs.set_prompt_tokens(response, tokens_list))
    context_data[str(message.chat.id)]['tokens_list'].append(response['usage']['completion_tokens'])
    context_data[str(message.chat.id)]['total_tokens'] = response['usage']['total_tokens']
    with open('users_context.json', 'w') as f:
        json.dump(context_data, f, indent=4)
    bot.delete_message(message.chat.id, mess.message_id)
    bot.send_message(message.chat.id, response_text)
    thread_dict.pop(message.chat.id)


bot.infinity_polling()
