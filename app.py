
from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
from argparse import ArgumentParser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,ImageSendMessage
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


# greeting text and image
@handler.add(FollowEvent)
def handle_follow_message(event):
    reply_arr=[]
    firstM = TextSendMessage(text="這是東伯的柚子園")
    secondM = TextSendMessage(text="Yes, this is me!")
    pic_url ='img/welcome_pic.img'
    image_message = ImageSendMessage(
        original_content_url= pic_url,
        preview_image_url= pic_url
    )

    confirm_template = ConfirmTemplate(text='Want to know more about me?', actions=[
            MessageTemplateAction(label='Yes!', text='About me'),
            MessageTemplateAction(label='No!', text='No'),
    ])
    template_message = TemplateSendMessage(
        alt_text='Confirm', template=confirm_template)

    reply_arr.append(firstM)
    reply_arr.append(image_message)
    reply_arr.append(secondM)
    reply_arr.append(template_message)    

    line_bot_api.reply_message(event.reply_token , reply_arr)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)