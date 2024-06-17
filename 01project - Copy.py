from flask import Flask, request, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage , ImageMessage, ImageSendMessage
import os
import tempfile
import cv2
import numpy as np
from yolo_predictions import YOLO_Pred

from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
#model = load_model("keras_Model.h5", compile=False)
model = load_model("MobileNetV2_SGD_NoAUG_lr0.01_Fold1.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()
# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

yolo = YOLO_Pred('ex20obj.onnx','ex20obj.yaml')

channel_secret = "50262202ecae408b310333454e7d3293"
channel_access_token = "s0hByNP7ySM9UXVK+WfCB2grt+iOtAvnSWqD/CNQxAUsS1UUOAfNCwTKKqB+gl+uoVM5a2rPwqBerVK9F6E6j8Wa0J3vHhvHIPMeOLI0ZCPunRotedPHrplSIXyv1VtPFrok08s12iRczQAZlOCICgdB04t89/1O/w1cDnyilFU="


line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

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

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp').replace("\\","/")
    print(static_tmp_path)
    
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='jpg' + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name
        
    dist_path = tempfile_path + '.jpg'  # เติมนามสกุลเข้าไปในชื่อไฟล์เป็น jpg-xxxxxx.jpg
    os.rename(tempfile_path, dist_path) # เปลี่ยนชื่อไฟล์ภาพเดิมที่ยังไม่มีนามสกุลให้เป็น jpg-xxxxxx.jpg

    filename_image = os.path.basename(dist_path) # ชื่อไฟล์ภาพ output (ชื่อเดียวกับ input)
    filename_fullpath = dist_path.replace("\\","/")   # เปลี่ยนเครื่องหมาย \ เป็น / ใน path เต็ม
    
    #img = cv2.imread(filename_fullpath)
    
    # Replace this with the path to your image
    image = Image.open(filename_fullpath).convert("RGB")

    # ใส่โค้ดประมวลผลภาพตรงส่วนนี้
    #-------------------------------------------------------------
    #pred_image, obj_box = yolo.predictions(img)

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction) #คือ lable ที่ได้ 0,1
    class_name = class_names[index] # เอาชื่อใน lableมา
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)
    #text_out = "มีโอกาศเป็น:" + str(class_name[2:]) + "ประมาณ:" + str(confidence_score*100) + "%"
    #print(text_out)

    url1 = request.url_root + '/static/Untitled-4.jpg'
    url2 = request.url_root + '/static/Untitled-2.jpg'
    url3 = request.url_root + '/static/Untitled-3.jpg'
    url4 = request.url_root + '/static/Untitled-5.jpg'
    
    #-------------------------------------------------------------
        
    #cv2.imwrite(filename_fullpath,pred_image)
    
    #dip_url = request.host_url + os.path.join('static', 'tmp', filename_image).replace("\\","/")
    #print(dip_url)
    #line_bot_api.reply_message(
    #    event.reply_token,[
    #        TextSendMessage(text='text_out'),
    #        ImageSendMessage(dip_url,dip_url)])

    if(confidence_score >= 0.70):
        
        if(index == 0):
            text_out = (f"มีโอกาศเป็นโรค ขอบใบแห้ง ประมาณ:" + "{:.2f}".format(confidence_score * 100) +"%")
            print(text_out)
            line_bot_api.reply_message(
                event.reply_token,[
                    TextSendMessage(text = text_out),
                    ImageSendMessage(url1,url1)])
        elif(index == 1):
            text_out = (f"มีโอกาศเป็นโรค โรคไหม้  ประมาณ:" + "{:.2f}".format(confidence_score * 100) +"%")
            print(text_out)
            line_bot_api.reply_message(
                event.reply_token,[
                    TextSendMessage(text = text_out),
                    ImageSendMessage(url2,url2)])
        elif(index == 2):
            text_out = (f"มีโอกาศเป็นโรค ใบจุดสีน้ำตาล ประมาณ:" + "{:.2f}".format(confidence_score * 100) +"%")
            print(text_out)
            line_bot_api.reply_message(
                event.reply_token,[
                    TextSendMessage(text = text_out),
                    ImageSendMessage(url3,url3)])
        elif(index == 3):
            text_out = (f"มีโอกาศเป็นโรค ใบสีส้ม ประมาณ:" + "{:.2f}".format(confidence_score * 100) +"%")
            print(text_out)
            line_bot_api.reply_message(
                event.reply_token,[
                    TextSendMessage(text = text_out),
                    ImageSendMessage(url4,url4)])
    else:
        line_bot_api.reply_message(
                event.reply_token,[
                    TextSendMessage(text = "ไม่สามารถทำนายได้ กรุณาถ่ายรูปใหม่")])
    
    
@app.route('/static/<path:path>')
def send_static_content(path):
    return send_from_directory('static', path)

if __name__ == "__main__":          
    app.run()

