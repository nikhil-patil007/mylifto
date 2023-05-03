from django.conf import settings
import requests
from doxer.models import *
from datetime import *
import datetime
import json

def send_notification(registration_ids , message_title , message_desc):
    # fcm_api = settings.FireBase_API_KEY
    fcm_api = "AAAArz4KUBo:APA91bGVbwnMSAY90DLP5-4R1n7jBPZaVtqGj6ttqAaOvAJgLDB0cNGLesf4rT06n445NVeM08QNyHqU74nF_OjcRCv0g6PNy_F87qAVbIQPhV1WufUXcggiwvDO-qlc1_D7xkbkSRQ3"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key='+fcm_api}

    payload = {
        "registration_ids" :registration_ids,
        "priority" : "high",
        "notification" : {
            "body" : message_desc,
            "title" : message_title,
            "icon": "https://softskillers.ca/mylifto/static/images/doxerlogopush.png",
            # "image" : "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
            
        }
    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers )

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "",' \
         '        authDomain: "",' \
         '        databaseURL: "",' \
         '        projectId: "",' \
         '        storageBucket: "",' \
         '        messagingSenderId: "",' \
         '        appId: "",' \
         '        measurementId: ""' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")

from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 #20 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'project.my_cron_job'    # a unique code

    def do(self):
        print("Crone Job Run")
        current_datetime = datetime.datetime.now()
        dat1 = current_datetime.strftime("%Y-%m-%d %H:%M")
        
        # Go Back 1 Day To Current Date
        current_date = (current_datetime - datetime.timedelta(days=1))
        
        # ridedek = Ride.objects.filter(publish='1',date=current_date,trip_status="P",trip_status2="2")
        # for k in ridedek:
        #     k.trip_status2 = "4"
        #     k.save()
            
        # Date Show Formate
        lastdats = current_date.strftime("%Y-%m-%d")
        
        # Full Book Delete Function 
        user = user_all.objects.filter(current_date=lastdats,as_user='Driver')
        ride = Ride.objects.filter(current_date = lastdats)
        for jj in ride:
            if jj.fullbooked == '1' or jj.fullbooked == '2':
                jj.delete()

        # Ride Delete Function
        # ride = Ride.objects.all() #(date=lastdats,trip_status="P")
        # for n in ride:
        #     # print("date",n.date.strftime("%Y-%m-%d"),"lastdats",lastdats,f"Ride No:- {n.id} For Delete:-{n.date.strftime('%Y-%m-%d') == lastdats and n.trip_status == 'P'}")
        #     if n.date.strftime("%Y-%m-%d") == lastdats and n.trip_status == "P":
        #         # n.delete()
                
        # Get Time Before 30 Minutes
        # Send Notification Before 30 min Function
        dat = (current_datetime + datetime.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")+":00"
        rides = Ride.objects.filter(publish='1',ride_time=dat)
        for i in rides:
            if i.getdriver:
                notif = firebase_notifications.objects.create(
                    userid = i.getdriver,
                    rideid = i,
                    notification_text = f"{i.getdriver.name.title()} your ride from {i.pickUp.capitalize()} to {i.dropout.capitalize()} will start at {i.ride_time.strftime('%I:%M %p')}",
                    create_at = current_date.strftime("%Y-%m-%d %H:%M"),
                )
                send_notification([i.getdriver.ntk] , 'MyLifto Ride Alert..' , f"{i.getdriver.name.title()} your ride from {i.pickUp.capitalize()} to {i.dropout.capitalize()} will start at {i.ride_time.strftime('%I:%M %p')}")
