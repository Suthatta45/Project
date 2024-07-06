from flask import Flask, request, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from linebot import LineBotApi, WebhookHandler
from linebot.models import *
import requests
import os
import tempfile
import cv2
import numpy as np
from yolo_predictions import YOLO_Pred
from keras.models import load_model
from PIL import Image, ImageOps

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model(
    "MobileNetV2_BEAM_SGD_NoAUG_lr0.001_Fold3.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# Create the array of the right shape to feed into the keras model
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

yolo = YOLO_Pred('ex20obj.onnx', 'ex20obj.yaml')

channel_secret = "50262202ecae408b310333454e7d3293"
channel_access_token = "s0hByNP7ySM9UXVK+WfCB2grt+iOtAvnSWqD/CNQxAUsS1UUOAfNCwTKKqB+gl+uoVM5a2rPwqBerVK9F6E6j8Wa0J3vHhvHIPMeOLI0ZCPunRotedPHrplSIXyv1VtPFrok08s12iRczQAZlOCICgdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)


def start_loading_animation(user_id):
    url = "https://api.line.me/v2/bot/chat/loading/start"
    headers = {
        'Authorization': f'Bearer {channel_access_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "chatId": user_id,
        "loadingSeconds": 5
    }
    response = requests.post(url, headers=headers, json=payload)
    return response


@app.route("/", methods=["GET", "POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except Exception as e:
        print(f"Error: {e}")
    return "Hello Line Chatbot"


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    user_id = event.source.user_id

    if text.lower() == "วิธีใช้":
        start_loading_animation(user_id)  # Start the loading animation
        quick_reply_items = [
            QuickReplyButton(action=CameraRollAction(label="ส่งรูปภาพ")),
            QuickReplyButton(action=CameraAction(label="เปิดกล้อง"))
        ]
        quick_reply = QuickReply(items=quick_reply_items)
        text_message = TextSendMessage(
            text="โปรดเลือกการดำเนินการ:",
            quick_reply=quick_reply
        )
        line_bot_api.reply_message(event.reply_token, text_message)

    if text.lower() == "ติดต่อเจ้าหน้าที่":
        start_loading_animation(user_id)  # Start the loading animation
        quick_reply_items = [
            QuickReplyButton(action=MessageAction(
                label="เว็บไซต์", text="เว็บไซต์")),
            QuickReplyButton(action=MessageAction(
                label="ข้อมูลติดต่อ ที่อยู่", text="ข้อมูลติดต่อ ที่อยู่"))
        ]
        quick_reply = QuickReply(items=quick_reply_items)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="ส่วนติดต่อเจ้าหน้าที่",
                quick_reply=quick_reply
            )
        )
    if text == "เว็บไซต์":
        start_loading_animation(user_id)  # Start the loading animation
        text_out = "https://www.opsmoac.go.th/about-moac_province?fbclid=IwAR1g5HZbzSaIogR-Xr-K7ql5q9jmUyaUcsZIl-blyWXz0rpfwkcx_rICEEA_aem_AT1cLPZjfNHI7eHoqDyw4pQySw7TkZwQ0wJdTV-y6GvRaT2eODqSEnxH8g9rqldde4M"
        line_bot_api.reply_message(
            event.reply_token, [TextSendMessage(text=text_out)])
    if text == "ข้อมูลติดต่อ ที่อยู่":
        start_loading_animation(user_id)  # Start the loading animation
        text_out = "https://www.nfc.or.th/contactusp"
        line_bot_api.reply_message(
            event.reply_token, [TextSendMessage(text=text_out)])

    if text.lower() == "ความรู้เกี่ยวกับโรคข้าว":
        start_loading_animation(user_id)  # Start the loading animation
        bubble_json = {
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://itbru.com/rice_recognition/640112418084/Screenshot_2.png",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "ความรู้ทั่วไปเกี่ยวกับโรคข้าว",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#0B19B7FF",
                                "align": "center",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคไหม้",
                                    "text": "โรคไหม้"
                                },
                                "color": "#00D3F1FF",
                                "style": "secondary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคใบจุดสีน้ำตาล",
                                    "text": "โรคใบจุดสีน้ำตาล"
                                },
                                "color": "#00D3F1FF",
                                "style": "secondary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคขอบใบแห้ง",
                                    "text": "โรคขอบใบแห้ง"
                                },
                                "color": "#00D3F1FF",
                                "style": "secondary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคใบสีส้ม",
                                    "text": "โรคใบสีส้ม"
                                },
                                "color": "#00D3F1FF",
                                "style": "secondary"
                            }
                        ]
                    }
                },
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://itbru.com/rice_recognition/640112418084/Screenshot_3.png",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "ความรู้ทั่วไปเกี่ยวกับโรคข้าว",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#846500FF",
                                "align": "center",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคใบขีดสีน้ำตาล",
                                    "text": "โรคใบขีดสีน้ำตาล"
                                },
                                "color": "#F4EA39FF",
                                "style": "secondary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคใบวงสีน้ำตาล",
                                    "text": "โรคใบวงสีน้ำตาล"
                                },
                                "color": "#F4EA39FF",
                                "style": "secondary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคกาบใบแห้ง",
                                    "text": "โรคกาบใบแห้ง"
                                },
                                "color": "#F4EA39FF",
                                "style": "secondary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคกาบใบเน่า",
                                    "text": "โรคกาบใบเน่า"
                                },
                                "color": "#F4EA39FF",
                                "style": "secondary"
                            }
                        ]
                    }
                },
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://itbru.com/rice_recognition/640112418084/Screenshot_4.png",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "ความรู้ทั่วไปเกี่ยวกับโรคข้าว",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#A40083FF",
                                "align": "center",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคเมล็ดด่าง",
                                    "text": "โรคเมล็ดด่าง"
                                },
                                "color": "#FF00CDFF",
                                "style": "primary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคถอดฝักดาบ",
                                    "text": "โรคถอดฝักดาบ"
                                },
                                "color": "#FF00CDFF",
                                "style": "primary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคกล้าเน่า",
                                    "text": "โรคกล้าเน่า"
                                },
                                "color": "#FF00CDFF",
                                "style": "primary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคลำต้นเน่า",
                                    "text": "โรคลำต้นเน่า"
                                },
                                "color": "#FF00CDFF",
                                "style": "primary"
                            }
                        ]
                    }
                },
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://itbru.com/rice_recognition/640112418084/Screenshot_1.png",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "ความรู้ทั่วไปเกี่ยวกับโรคข้าว",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#B96000FF",
                                "align": "center",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคดอกกระถิน",
                                    "text": "โรคดอกกระถิน"
                                },
                                "color": "#FFA010FF",
                                "style": "primary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคใบขีดโปร่งแสง",
                                    "text": "โรคใบขีดโปร่งแสง"
                                },
                                "color": "#FFA010FF",
                                "style": "primary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคใบหงิก",
                                    "text": "โรคใบหงิก"
                                },
                                "color": "#FFA010FF",
                                "style": "primary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคเขียวเตี้ย",
                                    "text": "โรคเขียวเตี้ย"
                                },
                                "color": "#FFA010FF",
                                "style": "primary"
                            }
                        ]
                    }
                },
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://itbru.com/rice_recognition/640112418084/Screenshot_5.png",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "ความรู้ทั่วไปเกี่ยวกับโรคข้าว",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#000D5DFF",
                                "align": "center",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคหูด",
                                    "text": "โรคหูด"
                                },
                                "color": "#2868FFFF",
                                "style": "primary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคใบสีแสด",
                                    "text": "โรคใบสีแสด"
                                },
                                "color": "#2868FFFF",
                                "style": "primary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคเหลืองเตี้ย",
                                    "text": "โรคเหลืองเตี้ย"
                                },
                                "color": "#2868FFFF",
                                "style": "primary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรครากปม",
                                    "text": "โรครากปม"
                                },
                                "color": "#2868FFFF",
                                "style": "primary"
                            }
                        ]
                    }
                },
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://itbru.com/rice_recognition/640112418084/Screenshot_6.png",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "ความรู้ทั่วไปเกี่ยวกับโรคข้าว",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#62007AFF",
                                "align": "center",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคใบแถบแดง",
                                    "text": "โรคใบแถบแดง"
                                },
                                "color": "#D62EFFFF",
                                "style": "primary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "โรคเมาตอซัง",
                                    "text": "โรคเมาตอซัง"
                                },
                                "color": "#D62EFFFF",
                                "style": "primary"
                            }
                        ]
                    }
                }
            ]
        }

        # สร้าง Flex Message จาก JSON
        flex_message = FlexSendMessage(
            alt_text="Flex Message", contents=bubble_json)

        # ส่ง Flex Message กลับไปยังผู้ใช้งาน
        line_bot_api.reply_message(event.reply_token, flex_message)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    static_tmp_path = os.path.join(os.path.dirname(
        __file__), 'static', 'tmp').replace("\\", "/")
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='jpg' + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.jpg'
    os.rename(tempfile_path, dist_path)
    filename_image = os.path.basename(dist_path)
    filename_fullpath = dist_path.replace("\\", "/")

    image = Image.open(filename_fullpath).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    url1 = request.url_root + '/static/1.jpg'
    url2 = request.url_root + '/static/2.jpg'
    url3 = request.url_root + '/static/3.jpg'
    url4 = request.url_root + '/static/4.jpg'

    user_id = event.source.user_id

    if confidence_score >= 0.70:
        if index == 0:
            start_loading_animation(user_id)  # Start the loading animation
            text_out = f"มีโอกาศเป็นโรค ขอบใบแห้ง ประมาณ: {confidence_score * 100:.2f}%"
            line_bot_api.reply_message(event.reply_token, [
                TextSendMessage(text=text_out),
                ImageSendMessage(url1, url1)
            ])
        elif index == 1:
            start_loading_animation(user_id)  # Start the loading animation
            text_out = f"มีโอกาศเป็นโรค โรคไหม้ ประมาณ: {confidence_score * 100:.2f}%"
            line_bot_api.reply_message(event.reply_token, [
                TextSendMessage(text=text_out),
                ImageSendMessage(url2, url2)
            ])
        elif index == 2:
            start_loading_animation(user_id)  # Start the loading animation
            text_out = f"มีโอกาศเป็นโรค ใบจุดสีน้ำตาล ประมาณ: {confidence_score * 100:.2f}%"
            line_bot_api.reply_message(event.reply_token, [
                TextSendMessage(text=text_out),
                ImageSendMessage(url3, url3)
            ])
        elif index == 3:
            start_loading_animation(user_id)  # Start the loading animation
            text_out = f"มีโอกาศเป็นโรค ใบสีส้ม ประมาณ: {confidence_score * 100:.2f}%"
            line_bot_api.reply_message(event.reply_token, [
                TextSendMessage(text=text_out),
                ImageSendMessage(url4, url4)
            ])
    else:
        start_loading_animation(user_id)  # Start the loading animation
        line_bot_api.reply_message(event.reply_token, [
            TextSendMessage(text="ไม่สามารถทำนายได้ กรุณาถ่ายรูปใหม่")
        ])


@app.route('/static/<path:path>')
def send_static_content(path):
    return send_from_directory('static', path)


if __name__ == "__main__":
    app.run()
