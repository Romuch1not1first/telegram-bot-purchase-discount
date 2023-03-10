import telebot
from sql import TelbotDatabase
import config
token = config.TOKENsELLER

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(True, True)
    markup.row(('Check Code'))
    bot.send_message(message.chat.id, 'Bot for the seller', reply_markup= markup)

def menu(message):
    # button
    markup = telebot.types.ReplyKeyboardMarkup(True, True)
    markup.row(('Check Code'))
    bot.send_message(message.chat.id, )

@bot.message_handler(content_types=['text'])
def write(message):
    if message.text == 'Check Code':
        markup = telebot.types.ReplyKeyboardMarkup(True, True)
        bot.send_message(message.chat.id, 'Enter a code:', reply_markup= markup)
        bot.register_next_step_handler(message, answer)


def answer(message):
    database = TelbotDatabase()

    select = f"""SELECT promocodecol, chatid FROM {config.log_in_mysql['database']}.promocode WHERE promocodecol = '{message.text}';"""
    answers = ''
    for colums in database.data_answer(select):
        answers = colums[1]

    # button
    markup = telebot.types.ReplyKeyboardMarkup(True, True)
    markup.row(('Check Code'))

    if answers != '':
        select = f"""DELETE FROM {config.log_in_mysql['database']}.promocode WHERE chatid = '{answers}';"""
        database.data_answer(select)

        # message to the seller
        bot.send_message(message.chat.id, 'Working promo code!', reply_markup= markup)

        #сообщение покупателю
        client_bot_buyer = telebot.TeleBot(config.TOKENbUYER)
        client_bot_buyer.send_message(answers, 'Thank you! Your code has been taken into account')
    else:
        # message to the seller
        bot.send_message(message.chat.id, 'Promo code not working!', reply_markup= markup)




# run
if __name__ == '__main__':
    bot.polling(non_stop=True)