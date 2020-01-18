import logging

"""ban lam gu"""
import sqlite3

import os
my_file = 'dict.db'
if os.path.exists(my_file):
    os.remove(my_file)
else:
    print ('no such file')
conn = sqlite3.connect('dict.db') #('example.db')
c = conn.cursor()
c.execute('''CREATE TABLE hokk
             (p text, h text)''')
c.execute('''CREATE TABLE zhtc
             (p text, zh text)''')
def is_zh(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False
with open("dict.txt") as f:
    entries = f.readlines()
entries = [x.strip() for x in entries] 
for item in entries:
    splited = item.split(" ", 1)
    p = splited[0]
    if is_zh(splited[1]):
        zh = splited[1]
        c.execute("INSERT INTO zhtc VALUES ('" + p +"','" + zh + "')")
    else: 
        h = splited[1]
        c.execute("INSERT INTO hokk VALUES ('" + p +"','" + h + "')")
		

conn.commit()


c.execute('SELECT * FROM zhtc')
print(c.fetchone())
c.execute('SELECT * FROM hokk')
print(c.fetchone())
conn.close()



from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    txt = update.message.text
    print(txt)
    conn = sqlite3.connect('dict.db') #('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM zhtc WHERE lower(p)=lower('" + txt + "')")
    r = c.fetchall()
    print(r)
  
    if r:
        re = r[0][1]
    else:
        re = "Not found."
    update.message.reply_html(re + """
    debug: <code>""" + str(r) + "</code>")
    conn.close

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1020977276:"+"AAHG4z13InRSBhXvbhK"+"Iqainexn6Zvug_gk", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

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






