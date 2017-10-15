from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,InlineQueryResultArticle)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, InlineQueryHandler)

import logging
from data import data_test
import config
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

INFO, CONVERSION, ASK, DISTRICT, HOSPITAL, DESCRIPTION, ASK2, ASK3 = range(8)

data = data_test.SqlBase()

choose_hospital = list() # Hello kostyl
count_hospital = -1
num_district = -1

def start(bot, update):
    global data
    data.fetchall_hospital()
    reply_keyboard = [['Условия', 'Я готов сдавать!']]
    update.message.reply_text(
        'Привет! Я твой донор бот! Если хочешь немного узнать об сдаче крови - напиши условия.'
        'Если ты уже готов сдавать крвь - напиши да', 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return INFO

def info(bot, update):
    global data
    user = update.message.text
    reply_keyboard = [['Я готов сдавать!', 'Нет, пока что нет.']]
    """while not ("да" in user.lower() or "условия" == user.lower()): 
        update.message.reply_text('Так "да" или "условия"?')
        return INFO
    if ("да" in user.lower()):
        update.message.reply_text('Верное решение!')
        return ConversationHandler.END #TODO
    elif ("условия" == user.lower()):
        update.message.reply_text('Окей.')
        update.message.reply_text('Тут написаны условия сдачи крови.')
        update.message.reply_text('Ну что готов сдавать?')
        return ASK"""
    if ("я готов сдавать!" == user.lower()):
        update.message.reply_text('Верное решение!', reply_markup=ReplyKeyboardRemove())
        data.fetchall_district()
        list0 = data.list_of_name_districts()
        str_temp = ''
        for i in range(0,len(list0)):
            str_temp = str_temp + '\n' + str(i) +'. ' + list0[i]
        update.message.reply_text(str_temp)
        return DISTRICT
    elif ("условия" == user.lower()):
        update.message.reply_text('Тут написаны условия сдачи крови.', reply_markup=ReplyKeyboardRemove())
        update.message.reply_text('Ну что готов сдавать?', 
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ASK
    return ConversationHandler.END

def ask(bot, update):
    global data
    user = update.message.text
    """while not ("да " in user.lower() or "нет" in user.lower()): 
        update.message.reply_text('Так да или нет?')
        return ASK
    if ("да" in user.lower()):
        update.message.reply_text('Верное решение!')
        return ConversationHandler.END #TODO
    elif ("нет" in user.lower()):
        update.message.reply_text('Что же, надеюсь ты передумаешь.'
            'Если хочешь со мной снова поговорить введите /start')
        return ConversationHandler.END
    return ConversationHandler.END"""
    if ("я готов сдавать!" == user.lower()):
        update.message.reply_text('Верное решение!', reply_markup=ReplyKeyboardRemove())
        data.fetchall_district()
        list0 = data.list_of_name_districts()
        str_temp = ''
        for i in range(0,len(list0)):
            str_temp = str_temp + '\n' + str(i) +'. ' + list0[i]
        update.message.reply_text(str_temp)
        return DISTRICT
    elif ("нет, пока что нет." == user.lower()):
        update.message.reply_text('Что же, надеюсь ты передумаешь.'
            'Если хочешь со мной снова поговорить введите /start', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

def ask_circle(bot, update):
    global num_district
    user = update.message.text
    if ("районы" == user.lower()):
        data.fetchall_district()
        list0 = data.list_of_name_districts()
        str_temp = ''
        for i in range(0,len(list0)):
            str_temp = str_temp + '\n' + str(i) +'. ' + list0[i]
        update.message.reply_text(str_temp,
                              reply_markup=ReplyKeyboardRemove())
        return DISTRICT
    elif ("больницы" == user.lower()):
        num = num_district
        print('ask',num)
        list_names = data.list_of_name_hospital2(num)
        str_names = 'Выбирете больницу:\n'
        for i in range(0, len(list_names)):
            str_names = str_names + '\n' + str(i) + '. ' + str(list_names[i][1])
        update.message.reply_text(str_names,
                              reply_markup=ReplyKeyboardRemove())
        count_hospital = len(list_names)
        choose_hospital.clear()
        for i in range(0,count_hospital):
            choose_hospital.append((list_names[i][0]))
            print(choose_hospital[i])
        return DESCRIPTION
    elif ("я закончил(а)" == user.lower()):
        update.message.reply_text('Пока!',
                              reply_markup=ReplyKeyboardRemove())
        #return ConversationHandler.END

def district(bot, update):
    global data, choose_hospital, count_hospital, num_district
    user = update.message.text
    try:
        num = int(user)
        num_district = num
        print('num ', num, 'get_num ', data.get_num_of_districts())
        if (num < data.get_num_of_districts() and num >= 0): #TODO Нужно исправить на проверку районов 
            list_names = data.list_of_name_hospital2(num)
            str_names = 'Выбирете больницу:\n'
            for i in range(0, len(list_names)):
                str_names = str_names + '\n' + str(i) + '. ' + str(list_names[i][1])
            update.message.reply_text(str_names)
            count_hospital = len(list_names)
            choose_hospital.clear()
            for i in range(0,count_hospital):
                choose_hospital.append((list_names[i][0]))
                print(choose_hospital[i])
            return DESCRIPTION
        else:
            update.message.reply_text('Пожалуйста, введите корректное значение.1')

    except ValueError:
        update.message.reply_text('Пожалуйста, введите корректное значение.2')
        #TODO

def description(bot, update):
    global data, choose_hospital
    reply_keyboard = [['районы', 'больницы', 'я закончил(а)']]
    user = update.message.text
    try:
        num = int(user)
        print('num ', num, 'get_num ', data.get_num_of_hospital())
        if (num < count_hospital and num >= 0): #TODO Нужно исправить на проверку районов 
            list_names = data.list_of_name_hospital1()
            str_names = ''
            for i in range(0, len(list_names)):
                if (list_names[i][0] == choose_hospital[num]):
                    str_names = str_names + '\n' + str(list_names[i][1]) + '\n' + str(list_names[i][2])
            update.message.reply_text(str_names,
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ASK2
        else:
            update.message.reply_text('Пожалуйста, введите корректное значение.1')
    except ValueError:
        update.message.reply_text('Пожалуйста, введите корректное значение.2')
        #TODO

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            INFO: [RegexHandler('^(Условия|Я готов сдавать!)$', info)],

            ASK: [RegexHandler('^(Я готов сдавать!|Hет, пока что нет.)$', ask)],

            ASK2: [RegexHandler('^(районы|больницы|я закончил(а))$', ask_circle)],

            DISTRICT: [MessageHandler(Filters.text, district)],

            DESCRIPTION: [MessageHandler(Filters.text, description)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
