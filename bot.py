# -*- coding: utf-8 -*-
import telegram
import os
from flask import Flask, request

app = Flask(__name__)

global bot
bot = telegram.Bot(token=[TELEGRAM_TOKEN])

TOKEN = [TELEGRAM_TOKEN]
PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(TOKEN)

# add handlers
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
                      

@app.route('/HOOK', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        # retrieve the message in JSON and then transform it to Telegram object
        update = telegram.Update.de_json(request.get_json(force=True))

        chat_id = update.message.chat.id

        # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update.message.text.encode('utf-8')

        # repeat the same message back (echo)
        bot.sendMessage(chat_id=chat_id, text=text)

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('https://dashproject.herokuapp.com/HOOK')
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(debug=True)