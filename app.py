from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from check import check_update

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_BOT_KEY)
handler = WebhookHandler(HANDLER)


@app.route("/")
def home():
    return 'home OK'

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if (event.message.text == "進度"):
        update, name, href = check_update()
        mess = name+"\n"+href
        if (update):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mess))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="No updated"))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
    
    
