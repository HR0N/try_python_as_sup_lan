import telebot

# todo:                                         .. :: Telegram Bot :: ..


bot = telebot.TeleBot("5399648161:AAGO3-jdK6yEG9hJFy5_vhz5AvdDAfz4PN4", parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = f"{message.from_user.first_name} start skynet"
    bot.send_message(message.chat.id, msg)
    from kaban_parse import start_driver
    start_driver()


@bot.message_handler(commands=['stop'])
def send_welcome(message):
    msg = f"{message.from_user.first_name} shut down skynet"
    bot.send_message(message.chat.id, msg)
    from kaban_parse import stop_driver
    stop_driver()


bot.infinity_polling()

