import telebot

# todo:                                         .. :: Telegram Bot :: ..


bot = telebot.TeleBot("5399648161:AAGO3-jdK6yEG9hJFy5_vhz5AvdDAfz4PN4", parse_mode=None)


state = {
    'write_sms': False,
    "code": 0,
}


@bot.message_handler()
def send_welcome(message):
    if not state['write_sms']:
        msg = "I don't understand."
        bot.send_message(message.chat.id, msg)
    else:
        msg = "Yes, it is."
        bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = f"{message.from_user.first_name} starting"
    bot.send_message(message.chat.id, msg)
    from kaban_parse import start_driver
    start_driver()


@bot.message_handler(commands=['stop'])
def send_welcome(message):
    msg = f"{message.from_user.first_name} stop"
    bot.send_message(message.chat.id, msg)
    from kaban_parse import stop_driver
    stop_driver()


@bot.message_handler(commands=['enter_code'])
def send_welcome(message):
    state['write_sms'] = True
    msg = "Enter the code"
    bot.send_message(message.chat.id, msg)


bot.infinity_polling()

