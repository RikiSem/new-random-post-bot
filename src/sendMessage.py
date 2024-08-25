import telebot
from sys import argv
from app.Confs.TgApiConf import TgApiConf

userId = argv[1]
message = argv[2]


bot = telebot.TeleBot(TgApiConf.token)

bot.send_message(userId, message)