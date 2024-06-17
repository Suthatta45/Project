from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import *

channel_secret = "50262202ecae408b310333454e7d3293"
channel_access_token = "s0hByNP7ySM9UXVK+WfCB2grt+iOtAvnSWqD/CNQxAUsS1UUOAfNCwTKKqB+gl+uoVM5a2rPwqBerVK9F6E6j8Wa0J3vHhvHIPMeOLI0ZCPunRotedPHrplSIXyv1VtPFrok08s12iRczQAZlOCICgdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token) # หลังบ้าน --> หน้าบ้าน
handler = WebhookHandler(channel_secret)        # หน้าบ้าน --> หลังบ้าน

app = Flask(__name__) 

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
                                   TextSendMessage(text=text_out))

        
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

if __name__ == "__main__":  
    app.run()


    

