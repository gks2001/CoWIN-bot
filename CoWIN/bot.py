from fake_useragent import UserAgent
from datetime import date
from telegram import *
from telegram.ext import *
import requests
import datetime
import json
import time

user_agent = UserAgent()
browser_header = {'User-Agent': user_agent.random}

def getdata():
    res = []
    arr = []
    today = date.today()
    formatted_date = today.strftime("%d-%m-%Y")
    district = 571
    age = 20
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id={}&date={}".format(district, formatted_date)
    response = requests.get(URL, headers=browser_header)
    if response.ok:
        resp_json = response.json()
        for center in resp_json["centers"]:
            for session in center["sessions"]:
                if session["min_age_limit"] <= age and session["vaccine"] == "COVAXIN":
                    tem = []
                    t = abs(600096 - center["pincode"])
                    tem.append(t)
                    tem.append(center["name"])
                    tem.append(center["block_name"])
                    tem.append(center["fee_type"])
                    tem.append(session["available_capacity_dose1"])
                    if(session["vaccine"] != ''):
                        tem.append(session["vaccine"])
                    arr.append(tem)
        arr.sort(key = lambda x: int(x[0]))
        for i in range (0, len(arr)):
            arr[i] = arr[i][1:]
        for i in range (0, len(arr)):
            if arr[i][3] > 0:
                res.append(arr[i])
    else:
        print("Error!")
    return res

cowin_bot = Bot("1876736163:AAE69-BYwysokA7PyJM8KFGsvR7lr_KhIdA")
updater = Updater("1876736163:AAE69-BYwysokA7PyJM8KFGsvR7lr_KhIdA", use_context = True)
dispatcher = updater.dispatcher
def func(update:Update, context:CallbackContext):
    while True:
        array = getdata()
        for i in array:
            string = 'Name: ' + str(i[0]) + '\nArea: ' + str(i[1]) + '\nFee: ' + str(i[2]) + '\nDose 1 availability: ' + str(i[3]) + '\nVaccine: ' + str(i[4])
            cowin_bot.send_message(chat_id=update.effective_chat.id, text = string)
        time.sleep(10)
    
start_value = CommandHandler('covaxin', func)
dispatcher.add_handler(start_value)
updater.start_polling(5)

# array = getdata()
# print(array)