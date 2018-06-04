from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Hp3OkKuleQ22NU05uRmtGz+BD3WV90ZeFKpMJ6LK1pzWpPHMmNL4sUCYu4RyUzuDVYBGN8v40UsC7Eg3G7g5j3+vFu+jtlx4jZyYgdqjT1ah3Bl3ssEuZzhHyV8/mwo9l9cUGKabHQgppHFTBOGPYgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('253c905f2976cb943bfb3f6776c24f8a')

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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)