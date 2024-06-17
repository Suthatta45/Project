from flask import Flask, request, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage,TextSendMessage, LocationSendMessage,ImageSendMessage
from linebot.models import *
from wit import Wit

wit_access_token = "XJ6PA6FIAJS3C2GCKHSL4MVCDZBFZO7J"
client = Wit(wit_access_token)

channel_secret = "50262202ecae408b310333454e7d3293"
channel_access_token = "s0hByNP7ySM9UXVK+WfCB2grt+iOtAvnSWqD/CNQxAUsS1UUOAfNCwTKKqB+gl+uoVM5a2rPwqBerVK9F6E6j8Wa0J3vHhvHIPMeOLI0ZCPunRotedPHrplSIXyv1VtPFrok08s12iRczQAZlOCICgdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token) # หลังบ้าน --> หน้าบ้าน
handler = WebhookHandler(channel_secret)        # หน้าบ้าน --> หลังบ้าน

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    print(text)
    if (text=="ความรู้ทั่วไป"):
        text_out = "ความรู้เรื่องข้าว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

    elif (text=="ความรู้เกี่ยวกับโรคข้าว"): #ต้องเป็นโปสเตอร์
        text_out = "โรคข้าวมี22โรค"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))
        
    elif (text=="วิธีใช้"):
        text_out = "วิธีใช้ไลน์บอท"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))
    elif (text=="ติดต่อเจ้าหน้าที่"):
        text_out = "ติดต่อเจ้าหน้าที่"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))
    '''    
    elif (text=="ภาพถ่ายการเรียนการสอน"):
        url1 = request.url_root + '/static/image01.jpg'
        url2 = request.url_root + '/static/image02.jpg'
        url3 = request.url_root + '/static/image03.jpg'
        line_bot_api.reply_message(event.reply_token,
                                   [ImageSendMessage(url1,url1),
                                    ImageSendMessage(url2,url2),
                                    ImageSendMessage(url3,url3)])
                
    elif (text=="สถานที่ตั้ง"):
        title = "สาขาวิชาเทคโนโลยีสารสนเทศ"
        address = "คณะวิทยาศาสตร์ มหาวิทยาลัยราชภัฏบุรีรัมย์"
        lati = 14.990461
        longi = 103.101045
        line_bot_api.reply_message(event.reply_token,
                                   LocationSendMessage(
                                       title=title,
                                       address=address,
                                       latitude=lati,
                                       longitude=longi))
    '''
    if (text != ""):
        ret = client.message(text)  #ดูกลุ่มคำจากwit.aiว่าตรงกับintentsไหนถ้าตรงมากกว่า0.8ก็เป็นintentsนั้นแล้วตอบกลับไป
        if len(ret["intents"]) > 0:
            confidence = ret["intents"][0]['confidence']
            if (confidence > 0.8):
                intents_name = ret["intents"][0]['name']        
                print("intent = ",intents_name)
                if(intents_name == "ask_hello"):
                    text_out = "ยินดีที่ได้รู้จัก"
                    line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=text_out))
                if(intents_name == "ask_name"):
                    text_out = "ชื่อใบข้าว"
                    line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=text_out))                
                if(intents_name == "ask_rice"):
                    text_out = "มีอะไรให้เราช่วยเหลือเกี่ยวกับโรคข้าวพิมพ์มาได้เลย"
                    line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=text_out))
            else:
                print("intent = unknow")
                text_out = "ไม่เข้าใจค่ะ กรุณาพิมพ์ใหม่"
                line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=text_out))
        else:
            print("intent = unknow")
            text_out = "ไม่เข้าใจค่ะ กรุณาพิมพ์ใหม่"
            line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=text_out))
'''
    ask_hello = ["สวัสดี","ดี","ดีจ้า","ดีครับ","ดีคับ","สวีดัส","สวัสดีค่ะ","สวัสดีครับ","สวัสดีคับ"] #กลุ่มคำ
    ask_name = ["ชื่อไร","ชื่ออะไร","ชื่อไรคะ","ชื่อไรครับ","ชื่ออะไรคะ","ชื่ออะไรครับ"]
    ask_rice = ["โรคข้าว","ความรู้โรคข้าว","ปัญหาโรคข้าว","ปัญหา","ช่วยอะไรหน่อยได้ไหม","สอบถาม","สอบถามโรคข้าว"]
   
    if(text in ask_hello): #ตอบคำถามจากกลุ่มคำ
        text_out = "ยินดีที่ได้รู้จัก"
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=text_out))
    if(text in ask_name):
        text_out = "ชื่อใบข้าว"
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=text_out))
    if(text in ask_rice):
        text_out = "มีอะไรให้เราช่วยเหลือเกี่ยวกับโรคข้าวพิมพ์มาได้เลย"
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=text_out)
'''
 
'''
    if(text == "สวัสดี"):  #ถ้าข้อความที่ผู้ใช้ส่งมาเท่ากับสวัสดี
        text_out = "ยินดีที่ได้รู้จัก"   #ก็จะส่งกลับไปว่ายินดีที่ได้รู้จัก
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=text_out))
    if(text == "ชื่ออะไร"):
        text_out = "น้องใบข้าว"
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=text_out))
'''
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event): 
    text_out = "คุณส่งสติ๊กเกอร์เข้ามา"
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))
    
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event): #ส่วนที่ไว้ประมวลผลภาพ
    text_out = "คุณส่งรูปภาพเข้ามา"
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))
    
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    text_out = "คุณส่งตำแหน่งที่ตั้งเข้ามา"
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

@app.route('/static/<path:path>')
def send_static_content(path):
    return send_from_directory('static', path)

if __name__ == "__main__":  
    app.run()


    

