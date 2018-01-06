#!/usr/bin/env python

# Simple Bot to reply to Telegram messages and store info in SQLite database

"""
This Bot uses the Updater class to handle the bot.
First, the database is created (if it isn't) and a few callback functions are defined. Then, 
The bot checks for past records and loads them. Finally, the callback functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.

KNOWN ISSUE: '' user inputs appear as None. Unable to satisfactorily apply conditionals.
"""

#### SQLITE BRANCH ####
import sys
import sqlite3

def loadDB():
    # Creates SQLite database to store info.
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    cur.executescript('''CREATE TABLE IF NOT EXISTS userdata
    (
    id INTEGER NOT NULL PRIMARY KEY UNIQUE, 
    firstname TEXT, 
    Name TEXT,
    Age TEXT,
    Address TEXT,
    Amount TEXT);'''
    )
    conn.commit()
    conn.close()

def checkUser(update, user_data):
    # Checks if user has visited the bot before
    # If yes, load data of user
    # If no, then create a new entry in database
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    if len(cur.execute('''SELECT id FROM userdata WHERE id = ?        
            ''', (update.message.from_user.id,)).fetchall())>0:
        c=cur.execute('''SELECT Name FROM userdata WHERE id = ?''', (update.message.from_user.id,)).fetchone()
        user_data['Name']=c[0]
        c=cur.execute('''SELECT Age FROM userdata WHERE id = ?''', (update.message.from_user.id,)).fetchone()
        user_data['Age']=c[0]
        c=cur.execute('''SELECT Address FROM userdata WHERE id = ?''', (update.message.from_user.id,)).fetchone()
        user_data['Address']=c[0]
        c=cur.execute('''SELECT Amount FROM userdata WHERE id = ?''', (update.message.from_user.id,)).fetchone()
        user_data['Amount']=c[0]
        print('Past user')
    else:
        cur.execute('''INSERT OR IGNORE INTO userdata (id, firstname) VALUES (?, ?)''', \
        (update.message.from_user.id, update.message.from_user.first_name,))
        print('New user')
    conn.commit()
    conn.close()

def updateUser(category, text, update):
    # Updates user info as inputted.
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    # Update SQLite database as needed.
    cur.execute('''UPDATE OR IGNORE userdata SET {} = ? WHERE id = ?'''.format(category), \
        (text, update.message.from_user.id,))
    conn.commit()
    conn.close()
        
#### Python Telegram Bot Branch ####

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Name', 'Age'],
                  ['Address', 'Amount'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update, user_data):
    update.message.reply_text(
        "I am Mr Meeseeks look at me!. "
        "Why don't you tell me something about yourself?",
        reply_markup=markup)
    checkUser(update, user_data)
    return CHOOSING

def regular_choice(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    update.message.reply_text(
        'Your {}? Yes, I would love to hear about that!'.format(text.lower()))
    return TYPING_REPLY

def received_information(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    updateUser(category, text, update)
    del user_data['choice']

    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "{}"
                              "You can tell me more, or change your opinion on something.".format(
                                  facts_to_str(user_data)), reply_markup=markup)
    return CHOOSING

def done(bot, update, user_data):
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("TOKEN:token")
    print("Connection to Telegram established; starting bot.")
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_user_data=True)],
        
        states={
            CHOOSING: [RegexHandler('^(Name|Age|Address|Amount)$',
                                    regular_choice,
                                    pass_user_data=True),
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice,
                                           pass_user_data=True),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
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
    ### load SQLite databasse ###
    loadDB()
    main()