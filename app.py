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
line_bot_api = LineBotApi('nVAkcHapCVZmdyGJktS8TlSUNXsj9KFfjeIsf04YfLBcdx30cNR1w76CsbuXW02/VYBGN8v40UsC7Eg3G7g5j3+vFu+jtlx4jZyYgdqjT1aeKzHBYSh/UIMpX95yGGTiGnmquHCQU6a3cJn3djCoMQdB04t89/1O/w1cDnyilFU=')
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
def handle_text_message(event):
    user_text = event.message.text
    if user_text == 'profile':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='Display name: ' + profile.display_name
                    ),
                    TextSendMessage(
                        text='Status message: ' + profile.status_message
                    )
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't use profile API without user ID"))
    elif user_text == 'pic':
        pic_url ='https://media.licdn.com/dms/image/C5103AQGFkQP0UXEFLA/profile-displayphoto-shrink_200_200/0?e=1529672400&v=beta&t=_tGqGLrPJ856JRyxZ-f9zhBGny5iWUSIQqxQ5N5hKsQ'
        image_message = ImageSendMessage(
            original_content_url= pic_url,
            preview_image_url= pic_url
            )
        line_bot_api.reply_message(event.reply_token,image_message)
                
    elif user_text == 'About me':
        buttons_template = ButtonsTemplate(
            thumbnail_image_url='https://via.placeholder.com/1024x1024',
            title='Yi-Han Chen', 
            text='Student from NTUST', 
            actions=[
                URITemplateAction(
                    label='My Linkedin', uri='https://www.linkedin.com/in/hannah-chen-326918101/'),
                MessageTemplateAction(label='Experience', text='experience'),
                MessageTemplateAction(label='Side Project', text='side project')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif user_text== 'experience':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='@Microsoft', title='MSP', actions=[
                MessageTemplateAction(label='Main Job',text='MSP main job'),
                URITemplateAction(
                    label='MSP event', uri='https://old.accupass.com/org/detail/r/1610281115031638932479/1/0')
                
            ]),
            CarouselColumn(text='@CTBC', title='IT Intern', actions=[
                    PostbackTemplateAction(label='Testing', data='Testing'),
                    PostbackTemplateAction(label='Spring', data='Spring')            
            ]),

        ])

        template_message = TemplateSendMessage(
            alt_text='experience', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif user_text == "MSP main job":
        msg_send = []
        firstM = TextSendMessage(text="MSP means Microsoft Student Partner")
        secondM = TextSendMessage(text="We have passion on technology !")
        pic_url = 'https://imgur.com/cCPeQe4.jpg'
        image_message = ImageSendMessage(
            original_content_url= pic_url,
            preview_image_url= pic_url
        )
        thirdM = TextSendMessage(text="this is the evnet I held at 4/18!")

        msg_send.append(firstM)
        msg_send.append(secondM)
        msg_send.append(image_message)
        msg_send.append(thirdM)

        line_bot_api.reply_message(event.reply_token , msg_send)
        
        
    elif user_text == 'side project':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='MSP 4/18 event', title='Voice Assistant', actions=[
                URITemplateAction(
                    label='Github', uri='https://github.com/tp6hannah/scraper_bing_speech_api'),
                MessageTemplateAction(label='Scraper', text='udn news'),
                MessageTemplateAction(label='people?', text='25')
            ]),
            CarouselColumn(text='by Django', title='Portfolio', actions=[
                URITemplateAction(
                    label='Links', uri='https://msp12.herokuapp.com/new/'),
                PostbackTemplateAction(label='Invest', data='Invest'),
                PostbackTemplateAction(label='Platform', data='Platform')            
            ]),
        ])

        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif user_text == 'Why':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://i2.wp.com/littleboyreports.com/wp-content/uploads/2016/03/Learn-to-code-1.jpg',
                                action= PostbackTemplateAction(label='Passion', data='Passion') ),
            ImageCarouselColumn(image_url='https://media1.tenor.com/images/b30733ad3df009f32a78ac237555f123/tenor.gif?itemid=4413385',
                                action= PostbackTemplateAction(label='Proactive', data='Proactive')),
            ImageCarouselColumn(image_url='https://spunout.ie/images/made/images/articles/ThinkstockPhotos-625736338_800_440_80_c1.jpg',
                                action= PostbackTemplateAction(label='Team-Player', data='Team-Player')),
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        
    elif user_text=='No':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="Click 'Click Here !' anytime you want"))
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=user_text))


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )
# greeting text and image
@handler.add(FollowEvent)
def handle_follow_message(event):
    reply_arr=[]
    firstM = TextSendMessage(text="Hi! I'm Yi-Han Chen")
    secondM = TextSendMessage(text="Yes, this is me!")
    pic_url ='https://media.licdn.com/dms/image/C5103AQGFkQP0UXEFLA/profile-displayphoto-shrink_200_200/0?e=1529672400&v=beta&t=_tGqGLrPJ856JRyxZ-f9zhBGny5iWUSIQqxQ5N5hKsQ'
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

    

if __name__ == "__main__":
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

