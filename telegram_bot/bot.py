#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import (ReplyKeyboardMarkup,ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, InlineQueryHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

INFO, CONVERSION, ASK= range(3)


def start(bot, update):
    reply_keyboard = [['Условия', 'Я готов сдавать!']]
    update.message.reply_text(
        'Привет! Я твой донор бот! Если хочешь немного узнать об сдаче крови - напиши условия.'
        'Если ты уже готов сдавать крвь - напиши да', 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return INFO

def info(bot, update):
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
    	return ConversationHandler.END #TODO
    elif ("условия" == user.lower()):
    	update.message.reply_text('Тут написаны условия сдачи крови.', reply_markup=ReplyKeyboardRemove())
    	update.message.reply_text('Ну что готов сдавать?', 
    		reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    	return ASK
    return ConversationHandler.END

def ask(bot, update):
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
    	return ConversationHandler.END #TODO
    elif ("нет, пока что нет." == user.lower()):
    	update.message.reply_text('Что же, надеюсь ты передумаешь.'
    		'Если хочешь со мной снова поговорить введите /start', reply_markup=ReplyKeyboardRemove())
    	return ConversationHandler.END


def conversation(bot, update):
    pass


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
    updater = Updater("337189866:AAHgeSgnTpGmC-t7aalEj5bI-oDnybX59Q4")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            INFO: [RegexHandler('^(Условия|Я готов сдавать!)$', info)],

            ASK: [RegexHandler('^(Hет, пока что нет.|Я готов сдавать!)$', ask)]
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