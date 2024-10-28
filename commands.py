from main import bot
import telebot

bot.set_my_commands([telebot.types.BotCommand('start', 'Start texting'),
                     telebot.types.BotCommand('help', 'Description'),
                     telebot.types.BotCommand('premium', 'Buy premium'),
                     telebot.types.BotCommand('account', 'My account'),
                     telebot.types.BotCommand('context', 'Delete context'),
                     telebot.types.BotCommand('language', 'Choose language')])
