

lang_dict = {'ru': {'start': {'hello_mess': 'Привет, с помощью этого бота можно вести диалог с чатом GPT',
                              'in_chat_mess': 'Можно начинать диалог прямо сейчас'},
                    'help': "Этот бот использует модель gpt-3.5-turbo \n \nДанный чат-бот умеет: \n \n"
                                      "-Создавать и редактировать код (лучше всего работает с Python) \n"
                                      "-Отвечать на вопросы \n"
                                      "-Помогать в написанни студенческих работ \n"
                                      "-Переводить текст на любой язык \n \n"
                                      "Вы можете общаться с ботом на абсолютно любые темы, но учитывайте,"
                                      "что база данных ограничена 2021 годом \n \n"
                                      "Без подписки в день можно делать не более 30 запросов, чтобы обойти "
                                      "это ограничение можно приобрести платную подписку за 5 долларов в месяц "
                                      "и увеличить дневной лимит до 100 запросов",
                    'premium': {'default_mess': 'В сутки можно делать не более 30 запросов боту\n \n'
                                      'Купите премиум подписку, и ваш дневной лимит вырастет до 100 запрсоов \n \n'
                                      'Цена подписки составляет 5 долларов в месяц, покупая подписку сразу на '
                                      'несколько месяцев вы получаете скидку',
                                '1m_button': 'Купить на месяц',
                                '2m_button': 'Купить на 2 месяца',
                                '3m_button': 'Купить на 3 месяца'},
                    'account': {'prem_false': 'Стандартная',
                                'prem_true': 'Премиум',
                                'subs_type': 'Тип подписки',
                                'mess_sent': 'Сообщений отправлено',
                                'mess_left': 'Сообщений осталось',
                                'prem_time': 'Оставшееся время подписки',
                                'days': 'дней'},
                    'context': 'Контекст успешно удален',
                    'language': {'choose_lang': 'Выберите язык',
                                 'succ_change': 'Язык успешно изменен'},
                    'thread_mess': {'overload_err': 'Сервера сейчас перегружены, повторите попытку позже',
                                    'req_err': 'Вы уже сделали запрос, пожалуйста дождитесь ответа'},
                    'text_mess': {'mess_len_err': 'Максимально допустимая длина сообщения - 1000 символов',
                                  'prem_false_err': 'Без премиум подписки можно отправлять не более 30 сообщений в день',
                                  'prem_true_err': 'С премиум подпиской можно делать не более 100 запросов в день',
                                  'in_process': 'Бот обрабатывает ваш запрос, пожалуйста подождите',
                                  'err': 'Ошибка, повторите попытку позже'},
                    'payment': {'desc': 'Вы покупаете премиум подписку, производите оплату только по последней '
                                        'ссылке\nОбязательно нажмите на кнопку после оплаты',
                                'payment_passed': 'Оплата прошла успешно',
                                'payment_failed': 'Оплата еще не прошла',
                                'check': 'Проверить оплату'}},

             'en': {'start': {'hello_mess': 'Hello, with this bot you can have a dialogue with the GPT chat',
                              'in_chat_mess': 'You can start a conversation right now'},
                    'help': "This bot uses the gpt-3.5-turbo model \n \nThis chatbot can: \n \n"
                                      "-Create and edit code (works best with Python) \n"
                                      "-Anwser the questions \n"
                                      "-Help in studies \n"
                                      "-Translate text into any language \n \n"
                                      "You can chat with the bot on absolutely any topic, but keep in mind that "
                                      "the database is limited to 2021 \n \n"
                                      "Without a subscription, you can make no more than 30 requests per day, "
                                      "to bypass this limitation, you can purchase a paid subscription for 5 dollars "
                                      "per month and increase your daily limit to 100 requests",
                    'premium': {'default_mess': 'You can make no more than 30 requests to the bot per day\n \n'
                                      'Buy a premium subscription and your daily limit will increase to 100 requests \n \n'
                                      'The subscription price is 5 dollars per month, buying a subscription for '
                                      'several months at once you get a discount',
                                '1m_button': 'Buy for a month',
                                '2m_button': 'Buy for 2 months',
                                '3m_button': 'Buy for 3 months',
                                'check': 'Check payment'},
                    'account': {'prem_false': 'Standard',
                                'prem_true': 'Premium',
                                'subs_type': 'Subscription type',
                                'mess_sent': 'Messages sent',
                                'mess_left': 'Remaining messages',
                                'prem_time': 'Remaining subscription time',
                                'days': 'days'},
                    'context': 'Context deleted successfully',
                    'language': {'choose_lang': 'Choose language',
                                 'succ_change': 'Language changed successfully'},
                    'thread_mess': {'overload_err': 'Servers are currently overloaded, please try again later',
                                    'req_err': 'You have already made a request, please wait for a response'},
                    'text_mess': {'mess_len_err': 'The maximum allowable message length is 1000 characters',
                                  'prem_false_err': 'Without a premium subscription, you can send no more than 30 '
                                                    'messages per day',
                                  'prem_true_err': 'With a premium subscription, you can make no more than 100 '
                                                   'requests per day',
                                  'in_process': 'The bot is processing your request, please wait',
                                  'err': 'Error, please try again later'},
                    'payment': {'desc': 'You buy a premium subscription, pay only for the last link'
                                        '\nBe sure to click on the button after payment',
                                'payment_passed': 'Payment successfully completed',
                                'payment_failed': 'Payment has not passed',
                                'check': 'Check payment'}}}
