# authentication/utils.py
# from datetime import datetime
# import pytz

# def get_ist_datetime():
#     ist = pytz.timezone('Asia/Kolkata')
#     return datetime.now(ist)

#5601751259
    #'8192429063:AAHpp_RAyw3Bp7_jywPzmsdhCyuzvQCiOxY'
import requests

def notify_admin_telegram(message):
    bot_token = '8192429063:AAHpp_RAyw3Bp7_jywPzmsdhCyuzvQCiOxY'
    chat_id = '5601751259'
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    data = {
        'chat_id': chat_id,
        'text': message
    }
    
    response = requests.post(url, data=data)
    return response.json()
