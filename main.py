from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage
from geopy.distance import geodesic

app = Flask(__name__)

# ตั้งค่า TOKEN และ SECRET ของคุณ
LINE_CHANNEL_ACCESS_TOKEN = 'd06gh77lEptxLd8M2i9njAgtXsL5fQ22FWg75YAw55+rWvxWfKHQGAw1uzjcdYg/DcVsVhaXLgGx7mS66/18de2yIaFO3FxEmCKnSt9KrYRFD56YaxpJzNj71OJsxSWIcGFZagjb92y/T+00BirmiwdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '84c05a361aa06d0d9b1db76d0cb33f04'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ข้อมูลห้องน้ำจำลอง
TOILETS = [
    {"name": "ห้องน้ำอาคารเรียนรวม 1 (ชาย)", "lat": 7.006100, "lng": 100.497800, "floor": "ชั้น 1", "note": "ใกล้ลิฟต์"},
    {"name": "ห้องน้ำอาคารเรียนรวม 1 (หญิง)", "lat": 7.006150, "lng": 100.497850, "floor": "ชั้น 1", "note": "ฝั่งตรงข้ามลิฟต์"},
    {"name": "ห้องน้ำหอสมุดวิทยาศาสตร์", "lat": 7.005500, "lng": 100.495000, "floor": "ชั้น 2", "note": "ด้านใน"},
    {"name": "ห้องน้ำโรงอาหารกลาง", "lat": 7.004900, "lng": 100.496200, "floor": "ชั้น 1", "note": "ด้านขวาติดกำแพง"},
    {"name": "ห้องน้ำหอพักพยาบาล (หญิง)", "lat": 7.007727, "lng": 100.498387, "floor": "ชั้น 3", "note": "เฉพาะนักศึกษาหญิง"},
]

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text.lower()
    if 'หาห้องน้ำ' in text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="กรุณาส่งตำแหน่งของคุณด้วยฟังก์ชันแชร์ตำแหน่ง (Location)")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="พิมพ์ 'หาห้องน้ำ' เพื่อค้นหาห้องน้ำใกล้คุณ")
        )

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    user_location = (event.message.latitude, event.message.longitude)
    nearest = min(TOILETS, key=lambda t: geodesic((t["lat"], t["lng"]), user_location).meters)
    distance = geodesic((nearest["lat"], nearest["lng"]), user_location).meters

    reply_text = (
        f"\U0001f6bb ห้องน้ำใกล้คุณที่สุดคือ:\n"
        f"{nearest['name']} ({nearest['floor']})\n"
        f"📍 {nearest['note']}\n"
        f"📏 ห่างจากคุณประมาณ {int(distance)} เมตร\n"
        f"🗺️ https://maps.google.com/?q={nearest['lat']},{nearest['lng']}"
    )

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
