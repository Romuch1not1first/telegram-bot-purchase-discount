import telebot
import secrets
import string
from sql import TelbotDatabase
import config
token = config.TOKENbUYER

bot = telebot.TeleBot(token)

count_request_promocode = 0

@bot.message_handler(commands=['start'])
def request_handler(message):
    bot.send_message(message.chat.id,'welcome message')


@bot.message_handler(content_types=['text'])
def menu(message):
    global count_request_promocode

    if message.text == 'Discount':

        if check_sub_channel(bot.get_chat_member(chat_id='-1001150329100', user_id=message.from_user.id)):

            # promocode
            if count_request_promocode == 0:
                
                database = TelbotDatabase()
                count_request_promocode += 1
                
                # generate promo code
                answer_count = 0
                while answer_count >= 0:
                    promocode = generate_promo_code()

                    select = f"""SELECT promocodecol, chatid FROM {config.log_in_mysql['database']}.promocode WHERE promocodecol = '{promocode}';"""
                    for _ in database.data_answer(select):
                        answer_count +=1
                    answer_count -=1

                #save to sql promo code and id chat
                select = f"""INSERT promocode (promocodecol, chatid) VALUES('{promocode}',{message.chat.id});"""
                database.data_answer(select)

                # message
                bot.send_message(message.chat.id,f'Here is your promo code for x% off: {promocode}')

        else:
            button = telebot.types.InlineKeyboardMarkup()
            url_btn = telebot.types.InlineKeyboardButton(text='SUBSCRIBE', url='https://t.me/romuchYT')
            markup = button.add(url_btn)
            bot.send_message(message.chat.id, 'You are not subscribed to the channel! Subscribe.', reply_markup = markup)


def generate_promo_code():
    letters_and_digits = string.ascii_letters + string.digits
    crypt_rand_string = ''.join(secrets.choice(
        letters_and_digits) for _ in range(5))
    return crypt_rand_string.upper()

def check_sub_channel(chat_member):
    if chat_member.status != 'left':
        return True

    return False


# run
if __name__ == '__main__':
    bot.polling(non_stop=True)