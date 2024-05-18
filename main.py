import telebot



TOKEN = '6906216735:AAEKPG6sjIXD9g-PHwM_VsV6AlbG4ciFeKQ'

bot = telebot.Telebot(TOKEN)


@bot.message_handler()
def echo_test(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'hello')


bot.polling()