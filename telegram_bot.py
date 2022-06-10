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

# есть игра Unity
# покупаешь завод кристалов 2шт, питаются 1 электростанцией (без нее не работают)
# нужно 50 энергии, одна ЭС выдает 100 энергии
# научный центр запускает дрон - выдет рандомные награды, работает 2-3 часа
# редкости заводов поккупаются
# нужно сделать магазин где покупается что то
# свапалка в игре, монетки с криптой
# данные кошелька крипты нужно выводить в игру

# 1 - заводы
# 2 - научный центр
# 3 - информация крипты в игре

# step 1 - create document
# step 2 - create tasks (1 week)
# step 3 - create TZ
# step 4 - price
# step 4 - start working



