
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
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,ImageSendMessage,
    URITemplateAction
)
# RichMenu, RichMenuBound, RichMenuArea,
app = Flask(__name__)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)


# parser = WebhookParser(channel_secret)
# Channel Access Token
line_bot_api = LineBotApi(channel_access_token)
# Channel Secret
handler = WebhookHandler(channel_secret)

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


# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     user_message = event.message.text

#     # create menu
#     if user_message == "cr":
#         rich_menu_to_create = RichMenu(
#                                 size=RichMenuBound(
#                                     width=2500,
#                                     height=1686
#                                 ),
#                                 selected= False,
#                                 name="nice richmenu",
#                                 chatBarText="touch me",
#                                 areas=[
#                                     RichMenuArea(
#                                         RichMenuBound(
#                                             x=0,
#                                             y=0,
#                                             width=2500,
#                                             height=1686
#                                         ),
#                                         URITemplateAction(
#                                             uri='line://nv/location'
#                                         )
#                                     )
#                                 ]
#                             )
#         rich_menu_id = line_bot_api.create_rich_menu(data=rich_menu_to_create)
#         line_bot_api.reply_message(event.reply_token, TextSendMessage(text=rich_menu_id)) 
#         print(rich_menu_id)

#     # echo user message 
#     else:
#         line_bot_api.reply_message(event.reply_token, TextSendMessage(text=user_message))    



    


# greeting text and image
@handler.add(FollowEvent)
def handle_follow_message(event):
    reply_arr=[]
    firstM = TextSendMessage(text="這是東伯的柚子園")
    # secondM = TextSendMessage(text="Yes, this is me!")
    # pic_url ='img/welcome_pic.img'
    # image_message = ImageSendMessage(
    #     original_content_url= pic_url,
    #     preview_image_url= pic_url
    # )

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