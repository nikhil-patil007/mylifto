from rest_framework import status
from django.core.exceptions import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from django.db.models import F, Sum
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers  import make_password,check_password
from time import gmtime, strftime
# from sms import send_sms
from datetime import *
import datetime
date = datetime.date.today()
start_week = date - datetime.timedelta(days=11)
end_week = start_week + datetime.timedelta(6)


import re
import requests
import json

def send_notification(registration_ids , message_title , message_desc):
    # FireBase Token Api
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


# Function to convert string to datetime
def convert(date_time):
    format = '%I:%M%p' # The format
    datetime_str = datetime.datetime.strptime(date_time, format)
    realtime = datetime_str.strftime('%H:%M')
    return realtime 

# Driver code
# Create your views here.

email_pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
mobile_pattern = '^[0-9]{10,20}$'

from random import randint
import re

def Average(l): 
    avg = sum(l) / len(l) 
    return avg

#  _ ____     ____   ________            _______   ____  
#   |    \   |    \     |      |       | |        |    \ 
#   |     |  |____/     |      |       | |____    |____/ 
#   |     |  |  \       |       \     /  |        |  \   
#  _|____/   |   \   ___|____    \___/   |______  |   \
      
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@api_view(['POST'])
def SignUpDriver(request):
    if request.method  == "POST":
        # showtime = strftime("%Y-%m-%d %H:%M:%S", )
        data = request.data
        name = data['name'].casefold()
        per_km_price = '00' #data['per_km_price']
        # raw = data['email_or_num'].casefold()
        email = data['email'].casefold()
        number = data['number']
        nks = data['token']
        DeviceId = data['DeviceId']
        Id_proofe1 = data['Id_proofe1']
        showtime = data['datetime']
        if Id_proofe1:
            ex = Id_proofe1.name
            if ex.endswith('.jpg'):
                Id_proofe1 = Id_proofe1
            elif ex.endswith('.png'):
                Id_proofe1 = Id_proofe1
            elif ex.endswith('.jpeg'):
                Id_proofe1 = Id_proofe1
            else:
                return Response({"status": 0, "msg" : "Image Only use .jpg, .png, .jpeg"})
        else:
            Id_proofe1 = ''
        # elif Id_proofe1 == '0':
        #     Id_proofe1 = ''
        # else:
        #     return Response({"status": 0, "msg" : "Image is Required"})        
        
        otp = ''
        for i in range (4):
            otp+=str(randint(1,9))
        
        if(not number):
            return Response({'status' : 0 , 'msg' : "Phone Number Is Required"})
            
        password = data['password']
        cpassword = data['cpassword']

        if(not name):
            return Response({'status' : 0 , 'msg' : "Full Name Is Required"})
        if(not per_km_price):
            return Response({'status' : 0 , 'msg' : "Price For Per Km Is Required"})
        if(not password):
            return Response({'status' : 0 , 'msg' : "Password Field Is Required"})
        if(not cpassword):
            return Response({'status' : 0 , 'msg' : "Confirm Password Field Is Required"})
        
        devi = user_all.objects.filter(DeviceId=DeviceId,status = 'Deactive')
        if len(devi) > 0:
            devis = user_all.objects.filter(DeviceId=DeviceId)
            for i in devis:
                i.status = 'Deactive'
                i.save()
            return Response({'status' : 0 , 'msg' : "This Device has Block By Admin"})
        else:
            if(re.search(mobile_pattern,number)):
                if number[0] == '0' or number[0] == 0:
                    number = number
                else:
                    number = f"0{number}"
                num = user_all.objects.filter(contact_no=number,as_user = 'Driver')
                if len(num) > 0:
                    getid = user_all.objects.get(id=num[0].id,as_user = 'Driver')
                    if getid.status == 'Deactivate':
                        return Response({'status' : 0 , 'msg' : "This Account has been Block"})
                    else:
                        if getid.active_ac_with_otp == "0":
                            if password != cpassword:
                                    return Response({'status' : 0 , 'msg' : "Password Doesn't Match.!"})
                            else:
                                getid.password = make_password(password)
                                getid.cpassword = cpassword
                                getid.as_user = 'Driver'
                                getid.otp = otp
                                getid.name = name
                                getid.image1 = Id_proofe1
                                # getid.image2 = Id_proofe1
                                getid.fare_per_km = per_km_price
                                getid.status = 'Active'
                                getid.create_at = showtime
                                getid.DeviceId = DeviceId
                                getid.update_at = showtime
                                getid.ntk = nks
                                getid.save()
                                # send_sms(
                                #         f'Hii {getid.name} \n Your Verification Code Is Here \n {getid.otp} ',
                                #         '+91634545811120',
                                #         [getid.contact_no,]
                                # )
                                return Response({'status' : 1,'msg':'Driver Register Succesfully',"Id":getid.id,'Type':"Mobile",'OTP':getid.otp})
                        else:
                            return Response({'status' : 0 , 'msg' : "Phone Num Is Alread Used"})  
                else:
                    number = number     
            else:
                return Response({'status' : 0 , 'msg' : "Phone Number Is Not Valid"})
            
            if email:            
                if(re.search(email_pattern, email)):
                    mail = user_all.objects.filter(email=email,as_user = 'Driver')
                    if len(mail) > 0:
                        getid = user_all.objects.get(id=mail[0].id,as_user = 'Driver')
                        if getid.status == 'Deactivate':
                            return Response({'status' : 0 , 'msg' : "This Account has been Block"})
                        else:
                            if getid.active_ac_with_otp == "0":
                                if password != cpassword:
                                        return Response({'status' : 0 , 'msg' : "Password Doesn't Match.!"})
                                else:
                                    getid.password = make_password(password)
                                    getid.cpassword = cpassword
                                    getid.as_user = 'Driver'
                                    getid.otp = otp
                                    getid.name = name
                                    getidimage1 = Id_proofe1
                                    # getidimage2 = Id_proofe1
                                    getid.fare_per_km = per_km_price
                                    getid.create_at = showtime
                                    getid.update_at = showtime
                                    getid.status = 'Active'
                                    getid.ntk = nks
                                    getid.DeviceId = DeviceId
                                    getid.save()
                                    mail_subject = 'Sign Up With Otp.'
                                    message = f'Hi {getid.name.title()},\n Mail Sent Properly \n Otp is:-\'{getid.otp}\'\n Thank You' 
                                    email_from = settings.EMAIL_HOST_USER
                                    to_email = [getid.email,]
                                    send_mail(mail_subject, message, email_from, to_email)
                                    return Response({'status' : 1,'msg':'Driver Register Succesfully',"Id":getid.id,'Type':'Email','OTP':getid.otp})
                            else:
                                return Response({'status' : 0 , 'msg' : "Email Is Alread Used"})
                    else:
                        email = email
                else:
                    return Response({'status' : 0 , 'msg' : "Email Is Not Valid"})
            else:
                email =email

            if password != cpassword:
                return Response({'status' : 0 , 'msg' : "Password Doesn't Match.!"})
            else:
                driver = user_all.objects.create(
                    as_user = 'Driver',
                    name = name,
                    fare_per_km = per_km_price,
                    email = email,
                    image1 = Id_proofe1,
                    # image2 = Id_proofe1,
                    contact_no = number,
                    DeviceId = DeviceId,
                    password = password,
                    cpassword = cpassword,
                    status = 'Active',
                    ntk = nks,
                    create_at = showtime,
                    update_at = showtime,
                )
                driver.password = make_password(driver.password)
                driver.cpassword = driver.cpassword
                driver.otp = otp
                driver.save()
                if driver.email:
                    types = 'Email'
                    mail_subject = 'Sign Up With Otp.'
                    message = f'Hi {driver.name.title()},\n Mail Sent Properly \n Otp is:-\'{driver.otp}\'\n Thank You' 
                    email_from = settings.EMAIL_HOST_USER
                    to_email = [driver.email,]
                    send_mail(mail_subject, message, email_from, to_email)
                if driver.contact_no:
                    types = 'Mobile'
                    # send_sms(
                    #         f'Hii {driver.name} \n Your Verification Code Is Here \n {driver.otp} ',
                    #         '+91634545811120',
                    #         [driver.contact_no,]
                    # )
            return Response({'status' : 1,'msg':'Driver Register Succesfully','Id' :driver.id,'Type':types,'OTP':driver.otp})

@api_view(["POST"])
def LoginDriver(request):
    data = request.data
    raw = data['email_or_num'].casefold()
    getpass = data['password']
    nks = data['token']
    DeviceId = data['DeviceId']
    showtime = data['datetime']
    if(not raw):
        return Response({"status" : 0 , "msg" : "Email Or Phone Number Is Required"})
    if(not getpass):
            return Response({"status" : 0 , "msg" : "Password Is Required"})
    
    devi = user_all.objects.filter(DeviceId=DeviceId,status = 'Deactive')
    if len(devi) > 0:
        devis = user_all.objects.filter(DeviceId=DeviceId)
        for i in devis:
            i.status = 'Deactive'
            i.save()
        return Response({'status' : 0 , 'msg' : "This Device has Block By Admin"})
    else:       
        if(re.search(mobile_pattern,raw)):
            if raw[0] == '0' or raw[0] == 0:
                raw = raw
            else:
                raw = f"0{raw}"
            driver = user_all.objects.filter(contact_no=raw,as_user = 'Driver')
            passenger = user_all.objects.filter(contact_no=raw,as_user = 'Passenger')
            if len(driver) > 0 and len(passenger) > 0:
                dri = user_all.objects.get(id=driver[0].id,as_user = 'Driver')
                pas = user_all.objects.get(id=passenger[0].id,as_user = 'Passenger')
                if dri.active_ac_with_otp == "0" and pas.active_ac_with_otp == "0":
                    return Response({"status" : 0 , "msg" : "Unknow User"})
                else:
                    if dri.status == 'Active' and pas.status == 'Active':
                        passwrd = check_password(getpass, dri.password)
                        passwrd1 = check_password(getpass, pas.password)
                        if passwrd and passwrd1:
                            dri.ntk = nks
                            dri.save()
                            
                            pas.ntk = nks
                            pas.save()
                            logi = User_login.objects.filter(as_user='Driver',user_id=dri,DeviceId=DeviceId)
                            if len(logi) > 0:
                                pass
                            else:
                                logi = User_login.objects.create(
                                    as_user = 'Driver',
                                    user_id = dri,
                                    DeviceId = DeviceId,
                                    ntk = nks,
                                    create_at = showtime
                                )
                                
                            logi1 = User_login.objects.filter(as_user='Passenger',user_id=dri,DeviceId=DeviceId)
                            if len(logi1) > 0:
                                pass
                            else:
                                logi = User_login.objects.create(
                                    as_user = 'Passenger',
                                    user_id = dri,
                                    DeviceId = DeviceId,
                                    ntk = nks,
                                    create_at = showtime
                                )
                            Driver_name = dri.name.title()
                            Passenger_name = pas.name.title()
                            return Response({"status" : 1 , "msg" : "Login Success","Driver_id":dri.id,'Driver_name':Driver_name,"Passenger_id":pas.id,"Passenger_name":Passenger_name})
                        else:
                            return Response({"status" : 0 , "msg" : "Password Is Wrong"})
                    else:
                        return Response({"status" : 0 , "msg" : "Account Is Blocked"})
            else:
                return Response({"status" : 0 , "msg" : "Invalid Number"})
        elif(re.search(email_pattern, raw)):
            mail = user_all.objects.filter(email=raw,as_user = 'Driver')
            
            driver = user_all.objects.filter(email=raw,as_user = 'Driver')
            passenger = user_all.objects.filter(email=raw,as_user = 'Passenger')
            if len(driver) > 0 and len(passenger) > 0:
                dri = user_all.objects.get(id=driver[0].id,as_user = 'Driver')
                pas = user_all.objects.get(id=passenger[0].id,as_user = 'Passenger')
                if dri.active_ac_with_otp == "0" and pas.active_ac_with_otp == "0":
                    return Response({"status" : 0 , "msg" : "Unknow User"})
                else:
                    if dri.status == 'Active' and pas.status == 'Active':
                        passwrd = check_password(getpass, dri.password)
                        passwrd1 = check_password(getpass, pas.password)
                        if passwrd and passwrd1:
                            dri.ntk = nks
                            dri.save()
                            
                            pas.ntk = nks
                            pas.save()
                            logi = User_login.objects.filter(as_user='Driver',user_id=dri,DeviceId=DeviceId)
                            if len(logi) > 0:
                                pass
                            else:
                                logi = User_login.objects.create(
                                    as_user = 'Driver',
                                    user_id = dri,
                                    DeviceId = DeviceId,
                                    ntk = nks,
                                    create_at = showtime
                                )
                                
                            logi1 = User_login.objects.filter(as_user='Passenger',user_id=dri,DeviceId=DeviceId)
                            if len(logi1) > 0:
                                pass
                            else:
                                logi = User_login.objects.create(
                                    as_user = 'Passenger',
                                    user_id = dri,
                                    DeviceId = DeviceId,
                                    ntk = nks,
                                    create_at = showtime
                                )
                            Driver_name = dri.name.title()
                            Passenger_name = pas.name.title()
                            return Response({"status" : 1 , "msg" : "Login Success","Driver_id":dri.id,'Driver_name':Driver_name,"Passenger_id":pas.id,"Passenger_name":Passenger_name})
                        else:
                            return Response({"status" : 0 , "msg" : "Password Is Wrong"})
                    else:
                        return Response({"status" : 0 , "msg" : "Account Is Blocked"})
            else:
                return Response({"status" : 0 , "msg" : "Invalid Email"})  
        else:
            return Response({"status" : 0 , "msg" : "Email Or Phone Number Is Not Valid"})

# @api_view(["POST"])
# def LoginDriver(request):
#     # showtime = strftime("%Y-%m-%d %H:%M:%S", )
#     data = request.data
#     raw = data['email_or_num'].casefold()
#     getpass = data['password']
#     nks = data['token']
#     DeviceId = data['DeviceId']
#     showtime = data['datetime']
#     if(not raw):
#         return Response({"status" : 0 , "msg" : "Email Or Phone Number Is Required"})
#     if(not getpass):
#             return Response({"status" : 0 , "msg" : "Password Is Required"})
    
#     devi = user_all.objects.filter(DeviceId=DeviceId,status = 'Deactive')
#     if len(devi) > 0:
#         devis = user_all.objects.filter(DeviceId=DeviceId)
#         for i in devis:
#             i.status = 'Deactive'
#             i.save()
#         return Response({'status' : 0 , 'msg' : "This Device has Block By Admin"})
#     else:       
#         if(re.search(mobile_pattern,raw)):
#             if raw[0] == '0' or raw[0] == 0:
#                 raw = raw
#             else:
#                 raw = f"0{raw}"
#             num = user_all.objects.filter(contact_no=raw,as_user = 'Driver')
#             if len(num) > 0:
#                 dri = user_all.objects.get(id=num[0].id,as_user = 'Driver')
#                 if dri.active_ac_with_otp == "0":
#                     return Response({"status" : 0 , "msg" : "Unknow User"})
#                 else:
#                     if dri.status == 'Active':
#                         passwrd = check_password(getpass, dri.password)
#                         if passwrd:
#                             # if dri.DeviceId == None:
#                             #     dri.DeviceId = DeviceId
#                             #     dri.save()
#                             #     print("please add Driverid with num",DeviceId)
#                             dri = user_all.objects.get(id=dri.id,as_user = 'Driver')
#                             dri.ntk = nks
#                             dri.save()
#                             logi = User_login.objects.filter(as_user='Driver',user_id=dri,DeviceId=DeviceId)
#                             if len(logi) > 0:
#                                 pass
#                             else:
#                                 logi = User_login.objects.create(
#                                     as_user = 'Driver',
#                                     user_id = dri,
#                                     DeviceId = DeviceId,
#                                     ntk = nks,
#                                     create_at = showtime
#                                 )
#                             Driver_name = dri.name.title() #if dri.name else dri.email_or_num
#                             return Response({"status" : 1 , "msg" : "Login Success","id":dri.id,'Driver_name':Driver_name})
#                         else:
#                             return Response({"status" : 0 , "msg" : "Password Is Wrong"})
#                     else:
#                         return Response({"status" : 0 , "msg" : "Account Is Blocked"})
#             else:
#                 return Response({"status" : 0 , "msg" : "Invalid Number"})
#         elif(re.search(email_pattern, raw)):
#             mail = user_all.objects.filter(email=raw,as_user = 'Driver')
#             if len(mail) > 0:
#                 dri = user_all.objects.get(id=mail[0].id,as_user = 'Driver')
#                 if dri.active_ac_with_otp == "0":
#                     return Response({"status" : 0 , "msg" : "Account Is Not Created"})
#                 else:
#                     if dri.status == 'Active':
#                         passwrd = check_password(getpass, dri.password)
#                         if passwrd:
#                             # if dri.DeviceId == None:
#                             #     dri.DeviceId = DeviceId
#                             #     dri.save()
#                             #     print("please add Driverid",DeviceId)
#                             dri = user_all.objects.get(id=dri.id,as_user = 'Driver')
#                             dri.ntk = nks
#                             dri.save()
#                             logi = User_login.objects.filter(as_user='Driver',user_id=dri,DeviceId=dri.DeviceId)
#                             if len(logi) > 0:
#                                 pass
#                             else:
#                                 logi = User_login.objects.create(
#                                     as_user = 'Driver',
#                                     user_id = dri,
#                                     DeviceId = DeviceId,
#                                     ntk = nks,
#                                     create_at = showtime
#                                 )
#                             Driver_name = dri.name.title() #if dri.name else dri.email_or_num
#                             return Response({"status" : 1 , "msg" : "Login Success","id":dri.id,'Driver_name':Driver_name})
#                         else:
#                             return Response({"status" : 0 , "msg" : "Password Is Wrong"})
#                     else:
#                         return Response({"status" : 0 , "msg" : "Account Is Blocked"})
#             else:
#                 return Response({"status" : 0 , "msg" : "Invalid Email"})  
#         else:
#             return Response({"status" : 0 , "msg" : "Email Or Phone Number Is Not Valid"})

@api_view(["POST"])
def VerifyOtpDriver(request):
    # showtime = strftime("%Y-%m-%d %H:%M:%S", )
    data = request.data
    raw = data['email_or_num'].casefold()
    getotp = data['otp']
    showtime = data['datetime']
    otp = ''
    for i in range (4):
        otp+=str(randint(1,9))
    newotp = otp
    
    if(not raw):
        return Response({"status" : 0 , "msg" : "Email Or Phone Number Is Required"})
    if(not getotp):
            return Response({"status" : 0 , "msg" : "OTP Field Is Required"})
        
    if(re.search(mobile_pattern,raw)):
        if raw[0] == '0' or raw[0] == 0:
            raw = raw
        else:
            raw = f"0{raw}"
        num = user_all.objects.filter(contact_no=raw,as_user = 'Driver')
        if len(num) > 0:
            dri = user_all.objects.get(id=num[0].id,as_user = 'Driver')
            if dri.active_ac_with_otp == "1":
                return Response({"status" : 0 , "msg" : "Otp Already Verify"})
            else:
                if dri.otp == getotp:
                    dri.active_ac_with_otp = "1"
                    dri.otp = newotp
                    dri.save()
                    logi = User_login.objects.filter(as_user='Driver',user_id=dri,DeviceId=dri.DeviceId)
                    if len(logi) > 0:
                        pass
                    else:
                        logi = User_login.objects.create(
                            as_user = 'Driver',
                            user_id = dri,
                            DeviceId = dri.DeviceId,
                            ntk = dri.ntk,
                            create_at = showtime
                        )
                    return Response({"status" : 1 , "msg" : "Otp Verify Successfully",'id':dri.id})
                else:
                    return Response({"status" : 0 , "msg" : "Otp Is Not Match"})
        else:
            return Response({"status" : 0 , "msg" : "Unknow User"})
    elif(re.search(email_pattern, raw)):
        mail = user_all.objects.filter(email=raw,as_user = 'Driver')
        if len(mail) > 0:
            dri = user_all.objects.get(id=mail[0].id,as_user = 'Driver')
            if dri.active_ac_with_otp == "1":
                return Response({"status" : 0 , "msg" : "Otp Already Verify",'id':dri.id})
            else:
                if dri.otp == getotp:
                    dri.active_ac_with_otp = "1"
                    dri.otp = newotp
                    dri.save()
                    logi = User_login.objects.filter(as_user='Driver',user_id=dri,DeviceId=dri.DeviceId)
                    if len(logi) > 0:
                        pass
                    else:
                        logi = User_login.objects.create(
                            as_user = 'Driver',
                            user_id = dri,
                            DeviceId = dri.DeviceId,
                            ntk = dri.ntk,
                            create_at = showtime
                        )
                    return Response({"status" : 1 , "msg" : "Otp Verify Successfully",'id':dri.id})
                else:
                    return Response({"status" : 0 , "msg" : "Otp Is Not Match"})
        else:
            return Response({"status" : 0 , "msg" : "Unknow User"})  
    else:
        return Response({"status" : 0 , "msg" : "Email Or Phone Number Is Not Valid"})

@api_view(["POST"])
def ResendOtpDriver(request):
    data = request.data
    raw = data['email_or_num']
    otp = ''
    for i in range (4):
        otp+=str(randint(1,9))
    getotp = otp
    if(not raw):
        return Response({'status' : 0 , 'msg' : "Email Or Phone Number Is Required"})
    if(re.search(mobile_pattern,raw)):
        if raw[0] == '0' or raw[0] == 0:
            raw = raw
        else:
            raw = f"0{raw}"
        num = user_all.objects.filter(contact_no=raw,active_ac_with_otp='0',as_user = 'Driver')
        if len(num) > 0:
            driver = user_all.objects.get(id=num[0].id,as_user = 'Driver')
            if driver.status == 'Active':
                driver.otp = getotp
                driver.save()
                return Response({'status' : 1 , 'msg' : "Otp Send Successfully Via Text","otp":driver.otp,'Type':"Mobile","token":driver.ntk})
            else:
                return Response({'status' : 0 , 'msg' : "Account Is Blocked"})
        else:
            return Response({'status' : 0 , 'msg' : "Number Is Not Found.!"})
    elif(re.search(email_pattern, raw)):
        mail = user_all.objects.filter(email=raw,active_ac_with_otp='0',as_user = 'Driver')
        if len(mail) > 0:
            driver = user_all.objects.get(id=mail[0].id,as_user = 'Driver')
            if driver.status == 'Active':
                driver.otp = getotp
                driver.save()
                    
                mail_subject = 'Sign Up With Otp'
                message = f'Hi {driver.email},\n Mail Sent Properly \n Otp is:- \'{driver.otp}\' \n Thank You' 
                email_from = settings.EMAIL_HOST_USER
                to_email = [raw,]
                send_mail(mail_subject, message, email_from, to_email)
                return Response({'status' : 1 , 'msg' : "Otp Send Successfully Via Email","otp":driver.otp,'Type':"Email","token":driver.ntk})
            else:
                return Response({'status' : 0 , 'msg' : "Account Is Blocked"})
        else:
            return Response({'status' : 0 , 'msg' : "Email Is Not Found.!"})
    else:
            return Response({'status' : 0 , 'msg' : "Email Or Phone Number Is Not Valid"})
 
# @api_view(["POST"])
# def ForgotOtpSendDriver(request):
#     data = request.data
#     raw = data['email_or_num']
#     otp = ''
#     for i in range (4):
#         otp+=str(randint(1,9))
#     getotp = otp
#     if(not raw):
#         return Response({'status' : 0 , 'msg' : "Email Or Phone Number Is Required"})
    
#     if(re.search(mobile_pattern,raw)):
#         if raw[0] == '0' or raw[0] == 0:
#             raw = raw
#         else:
#             raw = f"0{raw}"
#         passenger_num = user_all.objects.filter(contact_no=raw,as_user = 'Passenger').exclude(active_ac_with_otp='0')
#         Driver_num = user_all.objects.filter(contact_no=raw,as_user = 'Driver').exclude(active_ac_with_otp='0')
#         if len(passenger_num) > 0 and len(Driver_num) > 0:
#             passanger = user_all.objects.get(id=passenger_num[0].id,as_user = 'Passenger')
#             driver = user_all.objects.get(id=Driver_num[0].id,as_user = 'Driver')
#             if passanger.status == 'Active' and driver.status == 'Active':
#                 passanger.otp = getotp
#                 passanger.active_ac_with_otp = "2"
#                 passanger.save()
                
#                 driver.otp = getotp
#                 driver.active_ac_with_otp = "2"
#                 driver.save()
#                 print('Message Is Not Send')
#                 return Response({'status' : 1 , 'msg' : "Otp Send Successfully Via Text","Driver_id":driver.id,"Passenger_id":passanger.id,'Type':"Mobile","OTP":passanger.otp,"token":passanger.ntk})
#             else:
#                 return Response({'status' : 0 , 'msg' : "Account is Blocked"})
#         else:
#             return Response({'status' : 0 , 'msg' : "Number Is Not Found.!"})
#     elif(re.search(email_pattern, raw)):
#         passenger_mail = user_all.objects.filter(email=raw,as_user = 'Passenger').exclude(active_ac_with_otp='0')
#         Driver_mail = user_all.objects.filter(email=raw,as_user = 'Driver').exclude(active_ac_with_otp='0')
#         if len(passenger_mail) > 0 and len(Driver_mail) > 0:
#             passanger = user_all.objects.get(id=passenger_mail[0].id,as_user = 'Passenger')
#             driver = user_all.objects.get(id=Driver_mail[0].id,as_user = 'Driver')
#             if passanger.status == 'Active' and driver.status == 'Active':
#                 passanger.otp = getotp
#                 passanger.active_ac_with_otp = "2"
#                 passanger.save()
                
#                 driver.otp = getotp
#                 driver.active_ac_with_otp = "2"
#                 driver.save()
                    
#                 mail_subject = 'Forgot Password Otp From MyLifto'
#                 message = f'Hi {passanger.name.title},\n Set New Password Help of This Otp. \n Your Otp is:- {passanger.otp} \n Thank You' 
#                 email_from = settings.EMAIL_HOST_USER
#                 to_email = [raw,]
#                 send_mail(mail_subject, message, email_from, to_email)
#                 return Response({'status' : 1 , 'msg' : "Otp Send Successfully Via Email","Driver_id":driver.id,"Passenger_id":passanger.id,'Type':"Email","OTP":passanger.otp,"token":passanger.ntk})
#             else:
#                 return Response({'status' : 0 , 'msg' : "Account is Blocked"})
#         else:
#             return Response({'status' : 0 , 'msg' : "Email Is Not Found.!"})
#     else:
#         return Response({'status' : 0 , 'msg' : "Email Or Number Not Found.!"})

@api_view(['POST'])
def ForgotSetPasswordDriver(request,dk,pk):
    try:
        data = request.data
        showtime = data['datetime']
        otp = ''
        for i in range (4):
            otp+=str(randint(1,9))
        otp = otp
        
        password = data['password']
        cpassword = data['cpassword']
        
        if(not password):
            return Response({'status' : 0 , 'msg' : "Password Field Is Required"})
        if(not cpassword):
            return Response({'status' : 0 , 'msg' : "Confirm Password Field Is Required"})
        
        if password != cpassword:
            return Response({'status' : 0 , 'msg' : "Password Doesn't Match.!"})
        else:
            dri = user_all.objects.get(id=dk,as_user = 'Driver')
            dri.password = make_password(password)
            dri.cpassword = cpassword
            dri.active_ac_with_otp = '1'
            dri.update = showtime
            dri.otp = otp
            dri.save()
            
            pas = user_all.objects.get(id=pk,as_user = 'Passenger')
            pas.password = make_password(password)
            pas.cpassword = cpassword
            pas.active_ac_with_otp = '1'
            pas.update = showtime
            pas.otp = otp
            pas.save()
            return Response({'status' : 1 , 'msg' : "Password Updated","Driver_id":dri.id,"Passenger_id":pas.id})
    except:
        return Response({'status' : 0 , 'msg' : "User Id Not Founded"})

@api_view(['POST'])
def AddRideForCar(request,pk):
    try:
        # showtime = strftime("%Y-%m-%d %H:%M:%S", )
        data = request.data
        pick = data['pickUp'].casefold()
        pickUp_latitude = data['pickUp_latitude']
        pickUp_longitude = data['pickUp_longitude']
        drop = data['dropout'].casefold()
        dropout_latitude = data['dropout_latitude']
        dropout_longitude = data['dropout_longitude']
        date = data['date']
        ls = data['route'].casefold()
        time = data['time'].upper()
        dtime = data['dtime'].upper()
        capacity = data['capacity']
        seats = data['seats']
        km = data['fees']
        showtime = data['datetime']
        
        if(not ls):
            route = [pick,drop]
        else:
            route = []
            st = ""
            for i in ls:
                if i == '[':
                    route.append(pick)
                else:
                    st = st + f"{i.replace(',','').replace(']','')}"
                    if i == ',':
                        route.append(st)
                        st = ''
                    if i == ']':
                        route.append(st)
                        route.append(drop)       
        add_information = data['add_information']
        per_price = data['per_km_price']
        pickup_address1 = data['pickup_address1']
        pickup_address2 = data['pickup_address2']
        dropout_address1 = data['dropout_address1']
        dropout_address2 = data['dropout_address2']
        getdriver = user_all.objects.get(id=pk,as_user = 'Driver')
        
        if (not capacity):
            capacity = '0'
            
        if (not seats):
            seats = '0'

        if(not pick):
            return Response({"status":0,"msg":"pick Point is not Add"})
        if(not pickUp_latitude):
            return Response({'status':0,"msg":"pickUp_latitude is Not Add"})
        if(not pickUp_longitude):
            return Response({'status':0,"msg":"pickUp_longitude is Not Add"})
        if(not drop):
            return Response({"status":0,"msg":"drop Point is not Add"})
        if(not dropout_latitude):
            return Response({'status':0,"msg":"dropout_latitude is Not Add"})
        if(not dropout_longitude):
            return Response({'status':0,"msg":"dropout_longitude is Not Add"})
        if(not date):
            return Response({"status":0,"msg":"select Date for Ride"})
        if(not getdriver):
            return Response({"status":0,"msg":"User Doesn't Login"})
        if(not time):
            return Response({'status':0,'msg':'Pick Up Time is Not Add'})
        if(not dtime):
            return Response({'status':0,'msg':'Drop off Time is Not Add'})
        if(not per_price):
            per_price = 1
            # return Response({'status':0,'msg':'KM Is Required'})
        
        # fees = round(float(km)) * int(per_price)
        fees = per_price

        # getdriver.fare_per_km = per_price
        # getdriver.save()
        
        ca = data['carid']
        publ = "0"
        if ca == '0':
            return Response({'status':0,"msg": "Please Add Car"})
        else:
            cars = Vehicle.objects.get(id=ca)
            
        # getname = getdriver.name if getdriver.name else getdriver.email_or_num
        tims = re.sub(" ","",time)
        
        ride_time = f"{str(date)} {str(convert(tims))}"
        rideserach = Ride.objects.filter(getdriver = getdriver,date = date,car = cars,publish='1',trip_status="P",status__range=['0','1']).exclude(status='3')
        
        if len(rideserach) > 0 and ca != "0":
            if (rideserach[0].status == "0" or rideserach[0].status == "1") and (rideserach[0].trip_status == "P" or rideserach[0].trip_status == "O"):
                return Response({"status" : 0 , "msg" : f"This Car Is Already Book For This Date {date}"})
            
        addrsd = Ride.objects.filter(as_user = 'Driver',getdriver = getdriver,pickUp = pick,dropout = drop,date = date,car = cars,ride_type = "C",publish = "0").exclude(status='3')
        if len(addrsd) > 0:
            addrsd[0].pickUp_latitude = pickUp_latitude
            addrsd[0].pickUp_longitude = pickUp_longitude
            addrsd[0].car_latitude = pickUp_latitude
            addrsd[0].car_longitude = pickUp_longitude
            addrsd[0].dropout_latitude = dropout_latitude
            addrsd[0].dropout_longitude = dropout_longitude
            addrsd[0].seats = seats
            addrsd[0].Max_seats = seats
            addrsd[0].fees = fees
            addrsd[0].capacity = capacity
            addrsd[0].Max_parcel = capacity
            # addrsd[0].pfees = per_price
            addrsd[0].per_km = per_price
            # addrsd[0].per_km = getdriver.fare_per_km
            addrsd[0].route = route
            addrsd[0].pickup_address1 = pickup_address1
            addrsd[0].pickup_address2 = pickup_address2
            addrsd[0].dropout_address1 = dropout_address1
            addrsd[0].dropout_address2 = dropout_address2
            addrsd[0].add_information = add_information
            addrsd[0].ride_time = ride_time
            addrsd[0].create_at = showtime
            addrsd[0].update_at = showtime
            addrsd[0].save()
            
            adds = Ride.objects.filter(as_user="Passenger",pickUp = pick,dropout = drop,date = date,trip_status="P",ride_type = 'C').exclude(status='3')
            if len(adds) >0:
                for h in adds:
                    lista = firebase_notifications.objects.filter(userid = h.getpassenger,rideid = h)
                    if len(lista) > 0:
                        lista[0].create_at = showtime
                        lista[0].notification_text = f"{getdriver.name.title()} has requested a ride from {pick.capitalize()} to {drop.capitalize()}"
                        lista[0].save()
                    else:
                        notif = firebase_notifications.objects.create(
                            userid = h.getpassenger,
                            rideid = h,
                            cancel_by = getdriver.name.title(),
                            notification_text = f"{getdriver.name.title()} has requested a ride from {pick.capitalize()} to {drop.capitalize()}",
                            create_at = showtime,
                        )   
                    send_notification([h.getpassenger.ntk] , 'New RIDE Request' , f"{getdriver.name.title()} has requested a ride from {pick.capitalize()} to {drop.capitalize()}")
            
            
            return Response({
                "Ride_Id" : addrsd[0].id,
                "status":1,
                "msg":"Ride Added Successfully"
                })
        else:
            addrid = Ride.objects.create(
                as_user = 'Driver',
                getdriver = getdriver,
                pickUp_latitude = pickUp_latitude,
                pickUp_longitude = pickUp_longitude,
                car_latitude = pickUp_latitude,
                car_longitude = pickUp_longitude,
                dropout_latitude = dropout_latitude,
                dropout_longitude = dropout_longitude,
                pickUp = pick,
                dropout = drop,
                date = date,
                # per_km = getdriver.fare_per_km,
                per_km = per_price,
                car = cars,
                route = route,
                publish = publ,
                fullbooked = "0",
                time = time,
                dtime = dtime,
                ride_type = "C",
                seats = seats,
                Max_seats = seats,
                capacity = capacity,
                Max_parcel = capacity,
                fees = fees,
                # pfees = per_price,
                pickup_address1 = pickup_address1,
                pickup_address2 = pickup_address2,
                dropout_address1 = dropout_address1,
                dropout_address2 = dropout_address2,
                # pet_allowed = pet,
                # max_seat_in_back = seatinback,
                # smoke_allowed = smoke,
                ride_time = ride_time,
                add_information = add_information,
                create_at = showtime,
                update_at = showtime
            )
            
            adds = Ride.objects.filter(as_user="Passenger",pickUp = pick,dropout = drop,date = date,trip_status="P",ride_type = 'C').exclude(status='3')

            for h in adds:
                lista = firebase_notifications.objects.filter(userid = h.getpassenger,rideid = h)
                if len(lista) > 0:
                    lista[0].create_at = showtime
                    lista[0].notification_text = f"{getdriver.name.title()} has requested a ride from {pick.capitalize()} to {drop.capitalize()}"
                    lista[0].save()
                else:
                    notif = firebase_notifications.objects.create(
                        userid = h.getpassenger,
                        rideid = h,
                        cancel_by = getdriver.name.title(),
                        notification_text = f"{getdriver.name.title()} has requested a ride from {pick.capitalize()} to {drop.capitalize()}",
                        create_at = showtime,
                    )   
                send_notification([h.getpassenger.ntk] , 'New RIDE Request' , f"{getdriver.name.title()} has requested a ride from {pick.capitalize()} to {drop.capitalize()}")
                
            return Response({
                "Ride_Id" : addrid.id,
                "status":1,
                "msg":"Ride Added Successfully"
            })
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong Or Data Missing"})

@api_view(['POST'])
def AddRideForTruck(request,pk):
    try:
        # showtime = strftime("%Y-%m-%d %H:%M:%S", )
        data = request.data
        pick = data['pickUp'].casefold()
        pickUp_latitude = data['pickUp_latitude']
        pickUp_longitude = data['pickUp_longitude']
        drop = data['dropout'].casefold()
        dropout_latitude = data['dropout_latitude']
        dropout_longitude = data['dropout_longitude']
        date = data['date']
        time = data['time'].upper()
        dtime = data['dtime'].upper()
        pickup_address1 = data['pickup_address1']
        pickup_address2 = data['pickup_address2']
        dropout_address1 = data['dropout_address1']
        dropout_address2 = data['dropout_address2']
        capacity = data['capacity']
        fees = data['fees']
        ls = data['route']
        showtime = data['datetime']
        
        add_information = data['add_information']
        if(not ls):
            route = [pick,drop]
        else:
            route = []
            st = ""
            for i in ls:
                if i == '[':
                    route.append(pick)
                else:
                    st = st + f"{i.replace(',','').replace(']','')}"
                    if i == ',':
                        route.append(st)
                        st = ''
                    if i == ']':
                        route.append(st)
                        route.append(drop)  
        # totalfees =  fees # int(capacity) * float(fees)
        totalfees =  0 # int(capacity) * float(fees)
        getdriver = user_all.objects.get(id=pk,as_user = 'Driver')
        
        if(not pickUp_latitude):
            return Response({'status':0,"msg":"PickUp_latitude is Not Add"})
        if(not pickUp_longitude):
            return Response({'status':0,"msg":"DickUp_longitude is Not Add"})
        if(not dropout_latitude):
            return Response({'status':0,"msg":"Dropout_latitude is Not Add"})
        if(not dropout_longitude):
            return Response({'status':0,"msg":"dropout_longitude is Not Add"})
        if(not pick):
            return Response({"status":0,"msg":"Pick Point is not Add"})
        if(not drop):
            return Response({"status":0,"msg":"Drop Point is not Add"})
        if(not date):
            return Response({"status":0,"msg":"Select Date for Ride"})
        if(not time):
            return Response({"status":0,"msg":"Select Pick Up Time for Ride"})
        if(not dtime):
            return Response({"status":0,"msg":"Select Drop off Time for Ride"})
        if(not getdriver):
            return Response({"status":0,"msg":"User Doesn't Login"})
        # if(not capacity):
        #     return Response({'status':0,'msg':'Parcel Capacity is Not Add'})
        if(not fees):
            return Response({'status':0,'msg':'Fees is Not Add'})
        tims = re.sub(" ","",time)
        ride_time = f"{str(date)} {str(convert(tims))}"
        addrid = Ride.objects.create(
            as_user = 'Driver',
            getdriver = getdriver,
            pickUp_latitude = pickUp_latitude,
            pickUp_longitude = pickUp_longitude,
            dropout_latitude = dropout_latitude,
            dropout_longitude = dropout_longitude,
            car_latitude = pickUp_latitude,
            car_longitude = pickUp_longitude,
            pickUp = pick,
            fullbooked = "0",
            dropout = drop,
            date = date,
            time = time,
            dtime = dtime,
            ride_type = "T",
            seats = '0',
            route = route,
            capacity = capacity,
            Max_parcel = capacity,
            fees = fees,
            per_km = fees,
            # fees = fees,
            add_information = add_information,
            publish = '1',
            pickup_address1 = pickup_address1,
            pickup_address2 = pickup_address2,
            dropout_address1 = dropout_address1,
            dropout_address2 = dropout_address2,
            ride_time = ride_time,
            create_at = showtime,
            update_at = showtime
        )
        adds = Ride.objects.filter(as_user="Passenger",pickUp = pick,dropout = drop,date = date,trip_status="P",ride_type = 'T').exclude(status='3')
        for h in adds:
            lista = firebase_notifications.objects.filter(userid = h.getpassenger,rideid = h)
            if len(lista) > 0:
                lista[0].create_at = showtime
                lista[0].notification_text = f"{getdriver.name.title()} has requested a ride from {pick.capitalize()} to {drop.capitalize()}"
                lista[0].save()
            else:
                notif = firebase_notifications.objects.create(
                    userid = h.getpassenger,
                    rideid = h,
                    cancel_by = getdriver.name.title(),
                    notification_text = f"{getdriver.name.title()} has requested a ride from {pick.capitalize()} to {drop.capitalize()}",
                    create_at = showtime,
                )   
            send_notification([h.getpassenger.ntk] , 'New RIDE Request' , f"{getdriver.name.title()} has requested a ride from {pick.capitalize()} to {drop.capitalize()}")
        # pickUp = addrid.pickUp_latitude , addrid.pickUp_longitude
        # dropout = addrid.dropout_latitude , addrid.dropout_longitude
        return Response({
            "Ride_Id" : addrid.id,
            "status":1,
            "msg":"Ride Added Successfully"
            })
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['POST'])
def RidePublishedStop(request,pk):
    try:
        print("=====================================>stop")
        rde = Ride.objects.get(id=pk,publish='1')
        if rde.trip_status == "P":
            ridepin = Ride_pin.objects.filter(getride=pk)
            for i in ridepin:
                if i.status == '1':
                    i.staus = '3'
                i.status = '3'
                i.save()
                if i.passengerid:
                    if rde.getdriver:
                        username = rde.getdriver.name.title()
                    # if rde.getpassenger:
                    #     username = rde.getpassenger.name.title()
                    notif = firebase_notifications.objects.create(
                        userid = i.passengerid,
                        rideid = rde,
                        cancel_by = username,
                        notification_text = f"{username} has cancelled the ride",
                        create_at = strftime("%Y-%m-%d %H:%M:%S"),
                    )
                    send_notification([i.passengerid.ntk] , 'has cancelled the Ride' , f"{username} has cancelled the ride")
            rde.trip_status2 = '4'
            rde.status = '3'
            rde.save()
            return Response({"status" : 1,'msg': "Ride stop",'passenger_token':''})
        elif rde.trip_status == "E":
            ridepin = Ride_pin.objects.filter(getride=pk)
            for i in ridepin:
                if i.status == '1':
                    i.staus = '3'
                i.status = '3'
                i.save()
                if i.passengerid:
                    send_notification([i.passengerid.ntk] , 'has cancelled the Ride' , f"{rde.getdriver.name.title()} has cancelled the ride")
                # if i.getdriver:
                #     send_notification([i.getdriver.ntk] , 'Ride cancel' , f"{i.getdriver.name.title()} has cancelled the ride")
            rde.trip_status2 = '4'
            rde.status = '3'
            rde.save()
            return Response({"status" : 1,'msg': "Ride stop",'passenger_token':''})
        else:
            rde = Ride.objects.get(id=pk,publish='1')
            if rde.trip_status == "O":
                Trip = "On The Way"
            if rde.trip_status == "E":
                Trip = "End"
            return Response({"status" : 0,'msg': f"Ride Is {Trip}"})
    except ObjectDoesNotExist:
        return Response({"status" : 0,'msg': "Ride Not found"})

@api_view(['POST'])
def RidePublishedDelete(request,pk,rr):
    try:
        print("**********************************************>Delete")
        if rr == '1':
            rde = Ride.objects.get(id=pk)
            ridepin = Ride_pin.objects.filter(getride=pk)
            for i in ridepin:
                if i.status == '1':
                    i.staus = '3'
                i.status = '3'
                i.delete()
            rde.trip_status2 = '4'
            rde.status = '3'
            rde.delete()
            return Response({"status" : 1,'msg': "Ride Delete"})
        if rr == '2':
            rde = Ride_pin.objects.get(id=pk)
            if rde.getride:
                rides = Ride.objects.get(id=rde.getride.id)
                if rides.status == "1":
                    rides.status = "0"
                    rides.save()
            rde.delete()
            return Response({"status" : 1,'msg': "Ride Delete"})
    except ObjectDoesNotExist:
        return Response({"status" : 0,'msg': "Ride Not found"})

@api_view(['PUT'])
def AddInformationRide(request,pk):
    showtime = strftime("%Y-%m-%d %H:%M:%S", )
    try:
        data = request.data
        updateride = Ride.objects.get(id=pk,publish='1')
        updateride.driver = updateride.getdriver.name if updateride.getdriver.name else updateride.getdriver.email_or_num
        updateride.update = showtime
        getdrop = RideSerializer(updateride,data=data)
        if getdrop.is_valid():
            getdrop.save()
        updateride.save()
        return Response({"status" : "1",'msg': "Ride Publish","Ride_Id" : updateride.id})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['PUT'])
def UpdateDriver(request,pk):
    # showtime = strftime("%Y-%m-%d %H:%M:%S", )
    try:
        data = request.data
        showtime = data['datetime']
        getdr = user_all.objects.get(id=pk,as_user = 'Driver')
        getdr.name = data['username'] if data['username'] else getdr.name
        # getdr.fare_per_km = data['per_km_price'] if data['per_km_price'] else getdr.fare_per_km
        getdr.email_or_num = getdr.email if getdr.email else getdr.contact_no
        email = data['email']
        num = data['contact_no']
        if(email):
            if(re.search(email_pattern, email)):
                getmail = user_all.objects.filter(email=email,as_user = 'Driver')
                if len(getmail) > 0:
                    for i in getmail:
                        if getdr.email == i.email:
                            getdr.email =getdr.email
                        elif email == i.email and getdr.email != i.email:
                            return Response({"status" : "0",'msg': "Email Is Already Used"})
                        else:
                            getdr.email = email
                else:
                    getdr.email = email
            else:
                return Response({'status':0,"msg":"Please Enter Valid Email"})
        else:
            getdr.email = email
        
        if(re.search(mobile_pattern, num)):
            if num[0] == '0' or num[0] == 0:
                num = num
            else:
                num = f"0{num}"
            getnum = user_all.objects.filter(contact_no=num,as_user = 'Driver')
            if len(getnum) > 0:
                for i in getnum:
                    if getdr.contact_no == i.contact_no:
                        getdr.contact_no =getdr.contact_no
                    elif num == i.contact_no and getdr.contact_no != i.contact_no:
                        return Response({"status" : "0",'msg': "Mobile Num Is Already Used"})
                    else:
                        getdr.contact_no = num
            else:
                getdr.contact_no = num
        else:
            getdr.contact_no = getdr.contact_no
        
        getdr.gender = data['gender']
        getdr.city = data['city'] if data['city'].capitalize() else data['city']
        try:
            getdr1 = data['pro_image']# if data['pro_image'] else  getdr.pro_image
            ex = getdr1.name
            if ex.endswith('.jpg'):
                getdr.pro_image = getdr1
            elif ex.endswith('.png'):
                getdr.pro_image = getdr1
            elif ex.endswith('.gif'):
                getdr.pro_image = getdr1
            elif ex.endswith('.jpeg'):
                getdr.pro_image = getdr1
            else:
                return Response({"status": 0, "msg" : "File Formate use jpg,jpeg,png"})
        except:
            getdr.pro_image = getdr.pro_image
        getdr.update = showtime
        getdr.save()
        name = getdr.name
        return Response({"status" : "1",'msg': f"{name.title()} Is Updated","Driver_Id" : getdr.id})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['POST'])
def RequestForBooking(request,bid,did):
    try:
        data = request.data
        ofprice = data['bid_price']
        per_seat_fees = data['per_seats_price']
        ca = data['car']
        showtime = data['datetime']
        add_information = data['note']
        if ca == 'Truck':
            car = None
        else:
            car = Vehicle.objects.get(id=ca)
        bookingid = Ride.objects.get(id=bid,publish='1',trip_status='P')
        if bookingid.status == '0':    
            driverid = user_all.objects.get(id=did,as_user = 'Driver')
            passid = user_all.objects.get(id=bookingid.getpassenger.id,as_user = 'Passenger')
            booking = Ride.objects.filter(getdriver=did,pickUp=bookingid.pickUp,dropout=bookingid.dropout,date=bookingid.date,as_user='Driver',ride_type=bookingid.ride_type).exclude(status='3')
            print(booking)
            if len(booking) > 0:
                rids = booking[0].id
                rid = Ride.objects.get(id=rids)
            else:
                rid = bookingid
            getbo = Ride_pin.objects.filter(getride=bookingid,getdriver=driverid,status='0')
            if getbo:
                return Response({"status": 0, "msg" : f"Already Request Send"})
            else:    
                createReq = Ride_pin.objects.create(
                    as_user = 'Driver_bid',
                    getdriver = driverid,
                    getride = bookingid,
                    getride1 = rid,
                    passengerid = passid,
                    per_seat_fees = per_seat_fees,
                    car = car,
                    for_passenger = bookingid.seats,
                    for_parcel = bookingid.capacity,
                    add_information = add_information,
                    ride_type = bookingid.ride_type,
                    ride_date = bookingid.date,
                    ride_time = bookingid.dtime,
                    offer_price = ofprice,
                    pickUp = bookingid.pickUp,
                    dropout = bookingid.dropout,
                    fees = ofprice,
                    request_date = showtime,
                )
                return Response({"status": 1, "msg" : f"Request Send","Request_Book_Id" : createReq.id,"passenger_token":passid.ntk,"passenger_id":passid.id,"passenger_name":passid.name.title()})
        else:
            return Response({"status": 0, "msg" : "Driver Select For This Ride"})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})
    # except KeyError:
    #     return Response({"status": 0, "msg" : "Please Update"})

# from operator import itemgetter

@api_view(['GET'])
def GetOwnBookin_PinListing(request,pk,tt):
    try:
        # status__range=['0','1']
        getride = Ride.objects.filter(fullbooked="0",getdriver=pk,ride_type=tt,publish__range=['1','3'],as_user = 'Driver').order_by('-trip_status2')
        getreq = Ride_pin.objects.filter(getdriver=pk,as_user='Driver_bid')#.exclude(status='3')
        # sr = DriverBookingpinSerializer(getreq,many=True)
        lis = []
        for instance1 in getride:
            if instance1.ride_type == tt or instance1.ride_type == "M":
                representation1 = {}
                representation1["id"] = 0
                representation1["this_is"] = "Ride"
                representation1["rid"] = instance1.id
                representation1["trip_pas_status"] = instance1.trip_status
                representation1["trip_pas_status2"] = instance1.trip_status2
                # representation1["rat_report"] = "Yes"
                # representation1["rat_report"] = "No"
                representation1["Passenger_id"] = ''
                representation1["Passenger_name"] = ''
                representation1["Passenger_pro_image"] = ""
                representation1["pickUp"] = instance1.pickUp.capitalize()
                representation1["dropout"] = instance1.dropout.capitalize()
                representation1["ride_date"] = instance1.date
                representation1["time"] = instance1.time
                representation1["dtime"] = instance1.dtime
                representation1["map_time"] = instance1.map_date
                representation1["Passenger"] = instance1.seats
                representation1["Parcel"] = instance1.capacity
                representation1["offer_price"] = f"{instance1.fees}"
                representation1["req_date"] = instance1.ride_time#.strftime("%d-%m-%Y")
                representation1["status"] = instance1.status
                # getridbok = Ride_pin.objects.filter(getride=instance1.id,status='1')
                # if instance1.status != '0' or len(getridbok) > 0:
                getridea = Ride_pin.objects.filter(getride=instance1.id,status='1')
                if instance1.status == '1' or len(getridea)>0:
                    lis.append(representation1)
            
        for instance in getreq:
            if instance.ride_type == tt or instance.ride_type == "M":
                representation = {}
                representation["id"] = instance.id
                representation1["this_is"] = "Request"
                representation["rid"] = instance.getride.id
                representation["trip_pas_status"] = instance.getride.trip_status
                representation["trip_pas_status2"] = instance.getride.trip_status2
                if instance.status == '1':
                    representation["Passenger_id"] = instance.passengerid.id
                    representation["Passenger_name"] = instance.passengerid.name.title()
                    representation["Passenger_pro_image"] = instance.passengerid.pro_image.url
                else:
                    representation["Passenger_id"] = ''
                    representation["Passenger_name"] = ''
                    representation["Passenger_pro_image"] = ""
                representation["pickUp"] = instance.pickUp.capitalize()
                representation["dropout"] = instance.dropout.capitalize()
                representation["ride_date"] = instance.getride.date
                representation["time"] = instance.getride.time
                representation["dtime"] = instance.getride.dtime
                representation["map_time"] = instance.getride.map_date
                representation["Passenger"] = instance.for_passenger
                representation["Parcel"] = instance.for_parcel
                representation["offer_price"] = f"{instance.offer_price}"
                representation["req_date"] = instance.request_date#.strftime("%d-%m-%Y")
                representation["status"] = instance.status
                lis.append(representation)
        
        my_list = sorted(lis, key=lambda k: k['ride_date'])
        # my_list = sorted(lis , key=lambda elem: "%02d %s" % (elem['ride_date'], elem['trip_pas_status2']))
        
        # newlist = sorted(lis, key=itemgetter('-ride_date'))#.sorted('-trip_pas_status2')
        # newlist = lis.sort(lambda x,y : cmp(x['ride_date'], y['trip_pas_status2']))
        return Response({'status': 1, 'msg': 'success','data' : my_list})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})        

@api_view(['GET'])
def PassengerProfileViewByPassenger(request,pk):
    try:
        getdri = user_all.objects.get(id=pk,as_user = 'Passenger')
        if getdri.gender == '0':
            gender = ''
        else:
            gender = getdri.gender
            
        rat = Passenger_Rating.objects.filter(mine=pk)
        ls = []
        for i in rat:
            ls.append(int(i.rates))
        if ls == []:
            average = 0.0
        else:
            average = Average(ls) 
        return Response({"status" : 1,"msg" : "Success",
                         "Passenger_name" : getdri.name.title(),
                         "Passenger_rating" : average,
                         "pro_image" : getdri.pro_image.url,
                         "Email" : getdri.email,
                         "passenger_token" : getdri.ntk,
                         "Contact" : getdri.contact_no,
                         "Gender" : gender,
                         "dob" : getdri.dob,
                         "city" : getdri.city,
                         "bio" : getdri.bio,
                         })
    except ObjectDoesNotExist:
        return Response({"status" : 0,"msg" : "Id Not Found"})

@api_view(['GET'])
def RidesBookingFilter(request,pk):
    try:
        getr = Ride.objects.get(id=pk,publish__range=['1','3'])
        getreq = Ride_pin.objects.filter(getride=getr.id,status="1")
        sr = []
        for instance in getreq:
            ratw = Passenger_Rating.objects.filter(tri=instance.id,mine=instance.passengerid.id,driverid=instance.getdriver.id)
            repo = Passenger_Report.objects.filter(tri=instance.id,mine=instance.passengerid.id,driverid=instance.getdriver.id)
            representations = {}
            representations['bid'] = instance.id
            if len(ratw) > 0 or len(repo) > 0:
                representations['rat'] = "Yes"
                representations['report'] = "Yes"
            else:
                representations['rat'] = "No"
                representations['report'] = "No"
            representations['Passenger_id'] = instance.passengerid.id
            representations['passenger_name'] = instance.passengerid.name.title()
            representations['passenger_profile'] = instance.passengerid.pro_image.url
            representations['for_passenger'] = instance.for_passenger
            representations['for_parcel'] = instance.for_parcel
            representations['Trip_status'] = instance.pas_status
            representations["Driver_Token"] = instance.getdriver.ntk
            representations["Passenger_Token"] = instance.passengerid.ntk
            representations['Location'] = instance.pickUp
            representations['fees'] = f"{instance.fees}"
            representations['Location_latitude'] = instance.pickUp_latitude
            representations['Location_longitude'] = instance.pickUp_longitude
            representations['Destination'] = instance.dropout
            representations['Destination_latitude'] = instance.dropout_latitude
            representations['Destination_longitude'] = instance.dropout_longitude
            representations['request_date'] = instance.request_date.strftime("%Y-%m-%d")
            sr.append(representations)
        if getr.ride_type == "T" or getr.ride_type == "t":
            fees = f"{getr.per_km}"
        else:
            fees = f"{getr.fees}"
        return Response({'status':1, 'msg':"Success",
                        "id": getr.id,
                        "driver": getr.getdriver.name.title(),
                        "per_km_price" : f"{getr.getdriver.fare_per_km}",
                        "Profile": getr.getdriver.pro_image.url,
                        "pickUp": getr.pickUp,
                        "ride_type" : getr.ride_type,
                        "ride_status" : getr.trip_status,
                        "pickUp_latitude" : getr.pickUp_latitude,
                        "pickUp_longitude" : getr.pickUp_longitude,
                        "pickup_address1" : getr.pickup_address1,
                        "pickup_address2" : getr.pickup_address2,
                        "dropout": getr.dropout,
                        "dropout_latitude" : getr.dropout_latitude,
                        "dropout_longitude" : getr.dropout_longitude,
                        "dropout_address1" : getr.dropout_address1,
                        "dropout_address2" : getr.dropout_address2,
                        "time" : getr.time,
                        "dtime" : getr.dtime,
                        "total_seats": getr.Max_seats,
                        "seats": getr.seats,
                        "total_capacity": getr.Max_parcel,
                        "capacity": getr.capacity,
                        "date": getr.date,
                        "fees": fees,
                        "add_information": getr.add_information.title(),
                        "data":sr})      
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['GET'])
def RideListingOfFilter(request,pk):
    try:
        getreq = Ride_pin.objects.filter(getride=pk,status="0").exclude(as_user='Driver_bid')
        sr = MineRidepinSerializer(getreq,many=True)
        ride_st = Ride.objects.get(id=pk,publish='1')
        return Response({'status':1, 'msg':"Success",
                            "data":sr.data})      
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['GET'])
def DriverProfile(request,pk):
    try:
        driver = user_all.objects.get(id=pk,as_user = 'Driver')
        rea = Drivers_Rating.objects.filter(mine=pk)
        ls = []
        for i in rea:
            ls.append(int(i.rates))
        if ls == []:
            average = 0.0
        else:
            average = Average(ls)
        if driver.gender == '0':
            gender = ''
        else:
            gender = driver.gender
        getcar = Vehicle.objects.filter(driverid=pk)
        vehicles = []
        for i in getcar:
            res = {}
            res['id'] = i.id
            res['reg_num'] = i.reg_num
            if i.Car_Img:
                res['Car_img'] = i.Car_Img.url
            else:
                res['Car_img'] = ""
            res['vehical_variant'] = f"{i.vehical_variant.brand.brand} {i.vehical_variant.cars}"
            if i.vehical_variant.photo_of_vehicle:
                res['admin_image'] = i.vehical_variant.photo_of_vehicle.url
            else:
                res['admin_image'] = ""
            res['vehicle_type'] = i.vehicle_type
            res['vehicle_model_year'] = i.vehicle_model_year
            res['dimension'] = i.dimension
            res['length_in_feet'] = i.length_in_feet
            res['width_in_feet'] = i.width_in_feet
            res['AC'] = i.ac_non_ac
            res['vehicle_color'] = i.vehicle_color
            res['status_car'] = i.status
            vehicles.append(res)
        return Response({'status': 1, 'msg' : "Success",
                        'pro_image' : driver.pro_image.url,'username' : driver.name.title(),'Total_rating': average,
                        'email' : driver.email,'contact_no' : driver.contact_no,'driver_token': driver.ntk,"per_km_price" : f"{driver.fare_per_km}",
                        'gender' : gender,'dob' : driver.dob,'city' : driver.city,"Full_booking": driver.fullbooked,
                        'bio' : driver.bio,"vehicles":vehicles})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['POST'])
def RejectRequestForTripByDriver(request,pk):
    try:
        getbooking = Ride_pin.objects.get(id=pk)
        if getbooking.status == '0':
            getbooking.status = '2'
            getbooking.save()
            return Response({'status':1, 'msg': f"Request Rejected",'Passenger_id':getbooking.passengerid.id,"Passenger_token":getbooking.passengerid.ntk})
        else:
            return Response({'status':0,'msg':'Request is Accpeted'})
    except ObjectDoesNotExist:
        return Response({"status" : "0",'msg': "Wrong Id"})

# @api_view(['GET'])
# def GetMyCarRide(request,pk):
#     try:
#         getdri = user_all.objects.get(id=pk,as_user = 'Driver')
#         getride = Ride.objects.filter(fullbooked="0",getdriver=getdri,ride_type='C',publish__range=['1','3'],as_user = 'Driver').exclude(status__range=['1','3']).order_by('-trip_status2')
#         if getride:
#             serial = CarRideFilterserializer(getride,many=True)
#             return Response({'status':1, 'msg':"Success","data":serial.data}) 
#         else:
#             return Response({'status':0,'msg':'No Ride Founded'})
#     except ObjectDoesNotExist:
#         return Response({"status": 0, "msg" : "Id IS wrong"})

# @api_view(['GET'])
# def GetMyTruckRide(request,pk):
#     try:
#         getdri = user_all.objects.get(id=pk,as_user = 'Driver')
#         getride = Ride.objects.filter(fullbooked="0",getdriver=getdri,ride_type='T',publish__range=['1','3'],as_user = 'Driver').exclude(status__range=['1','3']).order_by('-trip_status2')
#         if len(getride) > 0:
#             serial = TruckRideFilterserializer(getride,many=True)
#             return Response({'status':1, 'msg':"Success","data":serial.data}) 
#         else:
#             return Response({'status':0,'msg':'No Ride Founded'})
#     except ObjectDoesNotExist:
#         return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['GET'])
def GetMyRidelist(request,pk,tt):
    try:
        if tt == "car":
            rd = "C"
        elif tt == "truck":
            rd = "T"
        else:
            return Response({'status':0,'msg':'No Ride Founded'})
        getdri = user_all.objects.get(id=pk,as_user = 'Driver')
        getride = Ride.objects.filter(fullbooked="0",getdriver=getdri,ride_type=rd,publish__range=['1','3'],as_user = 'Driver').exclude(status__range=['1','3']).order_by('-trip_status2')
        if len(getride) > 0:
            data = []
            # serial = TruckRideFilterserializer(getride,many=True)
            for instance in getride:
                representation = {}
                representation["id"] = instance.id
                representation["driver"] = instance.getdriver.name.title()
                representation["Profile"] = instance.getdriver.pro_image.url
                representation["seat"] = instance.seats
                representation["capacity"] = instance.capacity
                representation["pickUp"] = instance.pickUp.capitalize()
                representation["time"] = instance.time
                representation["dtime"] = instance.dtime
                representation["map_time"] = instance.map_date
                representation["dropout"] = instance.dropout.capitalize()
                representation["date"] = instance.date.strftime("%d-%m-%Y")
                representation["fees"] = instance.fees
                if instance.publish == '1':
                    representation["EnableDisable"] = "1"
                else:
                    representation["EnableDisable"] = "0"
                representation["status"] = instance.status
                representation["trip_status"] = instance.trip_status
                representation["trip_pas_status"] = instance.trip_status
                representation["add_information"] = instance.add_information.title()
                # ridebok = Ride_pin.objects.filter(getride=instance.id,status="1")
                # if len(ridebok) > 0:
                #     pass
                # else:
                #     data.append(representation)
                data.append(representation)
            return Response({'status':1, 'msg':"Success","data":data}) 
        else:
            return Response({'status':0,'msg':'No Ride Founded'})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['POST'])
def DriverChangePassword(request,dk,pk):
    try:
        data = request.data
        getpassenger = user_all.objects.get(id=pk,as_user = 'Passenger')
        getdriver = user_all.objects.get(id=dk,as_user = 'Driver')
        curpass = data['curpass']
        showtime = data['datetime']
        npass = data['npass']
        ncpass = data['ncpass']
        dri = check_password(curpass, getdriver.password)
        pas = check_password(curpass, getpassenger.password)
        if dri and pas:
            if npass != ncpass:
                return Response({'status' : 0,'msg': 'New Password And Confirm Password Not Match..'})
            else:
                getdriver.password = make_password(npass)
                getdriver.cpassword = ncpass
                getdriver.update_at = showtime
                getdriver.save()
                
                getpassenger.password = make_password(npass)
                getpassenger.cpassword = ncpass
                getpassenger.update_at = showtime
                getpassenger.save()
                return Response({'status':1,'msg':'Password Is Changed..'})
        else:
            return Response({'status':0,'msg':'Wrong Current Password'})
    except ObjectDoesNotExist:
        return Response({'status':0 ,"msg":"Wrong Id"})

@api_view(['POST'])
def DriverAddCar(request,pk,mid):
    try:
        # showtime = strftime("%Y-%m-%d %H:%M:%S", )
        data = request.data
        getdri = user_all.objects.get(id=pk,as_user = 'Driver')
        model = Car_name.objects.get(id=mid)
        if getdri:
            if model:
                rnum = data['reg_num']
                vehicle_type = data['v_type']
                vehicle_model_year = data['v_year']
                ac_non_ac = data['ac'].title()
                showtime = data['datetime']
                color = data['vehicle_color']
                Car_Img = data['Car_Img']
                length_in_feet = data['length']
                width_in_feet = data['width']
                dimension = data['dimension']
                if Car_Img:
                    try:
                        ex = Car_Img.name
                        if ex.endswith('.jpg'):
                            Car_Img = Car_Img
                        elif ex.endswith('.png'):
                            Car_Img = Car_Img
                        elif ex.endswith('.jpeg'):
                            Car_Img = Car_Img
                        else:
                            return Response({"status": 0, "msg" : "Car Image Formate use jpg,jpeg,png"})
                    except:
                        Car_Img = Car_Img
                Car_Doc = data['Car_Doc']
                if Car_Doc:
                    try:
                        ex = Car_Doc.name
                        if ex.endswith('.jpg'):
                            Car_Doc = Car_Doc
                        elif ex.endswith('.png'):
                            Car_Doc = Car_Doc
                        elif ex.endswith('.jpeg'):
                            Car_Doc = Car_Doc
                        else:
                            return Response({"status": 0, "msg" : "Car Document Formate use jpg,jpeg,png"})
                    except:
                        Car_Doc = Car_Doc
                # ad = Vehicle.objects.filter(reg_num=rnum)
                # if len(ad) > 0:
                #     return Response({"status":0,"msg":"Register Number Is Already Used"})
                # else:
                addcar = Vehicle.objects.create(
                    driverid = getdri,
                    reg_num = rnum,
                    created = showtime,
                    Car_Img = Car_Img,
                    Car_Doc = Car_Doc,
                    vehical_variant = model,
                    vehicle_color = color,
                    vehicle_type = vehicle_type,
                    vehicle_model_year = vehicle_model_year,
                    ac_non_ac = ac_non_ac,
                    length_in_feet = length_in_feet,
                    width_in_feet = width_in_feet,
                    dimension = dimension,
                )
                return Response({"status":1,"msg":"Vehicle Add Successfully","Car_id":addcar.id})
            else:
                return Response({"status":0,"msg":"Wrong Car's Id"})
        else:
            return Response({"status":0,"msg":"Wrong Driver's Id"})
    except ObjectDoesNotExist:
        return Response({"status":0,"msg":"Wrong Id"})

@api_view(['POST'])
def SearchBookingFilter(request,dd):
    data = request.data
    pickup = data['pickUp'].casefold()
    dropout = data['dropout'].casefold()
    pick = pickup
    drop = dropout
    # pick = re.sub(" ","",pickup)
    # drop = re.sub(" ","",dropout)
    date = data['date']
    seats = data['seat_parcel']
    
    driver = data['driverid']
    if (not driver):
        driverid = '0'
    else:
        driverid = driver
        
    # All Data
    if pickup and dropout and date:
        filter = "Yes"
        book = Ride.objects.filter(ride_type=dd,pickUp__startswith=pick,dropout__startswith=drop,date=date,as_user="Passenger",publish='1',trip_status='P').exclude(status='3')
    
    # Only No Drop
    if pickup and (not dropout) and date:
        filter = "Yes"
        book = Ride.objects.filter(ride_type=dd,pickUp__startswith=pick,date=date,as_user="Passenger",publish='1',trip_status='P').exclude(status='3')
    
    # Only Pick
    if pickup and (not dropout) and (not date):
        filter = "Yes"
        book = Ride.objects.filter(ride_type=dd,pickUp__startswith=pick,as_user="Passenger",publish='1',trip_status='P').exclude(status='3') 
    
    # Only No Date
    if pickup and dropout and (not date):
        filter = "Yes"
        book = Ride.objects.filter(ride_type=dd,pickUp__startswith=pick,dropout__startswith=drop,as_user="Passenger",publish='1',trip_status='P').exclude(status='3')
    
    # Only No Pick
    if (not pickup) and dropout and date:
        filter = "Yes"
        book = Ride.objects.filter(ride_type=dd,dropout__startswith=drop,date=date,as_user="Passenger",publish='1',trip_status='P').exclude(status='3')
    
    # Only Date
    if (not pickup) and (not dropout) and date:
        filter = "Yes"
        book = Ride.objects.filter(ride_type=dd,date=date,as_user="Passenger",publish='1',trip_status='P').exclude(status='3')
    
    # Only Drop
    if (not pickup) and dropout and (not date):
        filter = "Yes"
        book = Ride.objects.filter(ride_type=dd,dropout__startswith=drop,as_user="Passenger",publish='1',trip_status='P').exclude(status='3')
    
    # All Blank
    if (not pickup) and (not dropout) and (not date):
        filter = "No"
        book = Ride.objects.filter(ride_type=dd,as_user="Passenger",publish='1',trip_status='P').exclude(status='3')
        
    if len(book) > 0:
        lis = []
        for i in book:
            current_date =datetime.datetime.now()
            if i.status == "0" or i.status == "1":
                if str(i.date) >= current_date.strftime('%Y-%m-%d'):
                    res = {}
                    #     if str(i.date) == current_date.strftime('%Y-%m-%d'):
                    #         res['rideshow'] = "Yes"
                    #     else:
                    #         res['rideshow'] = "Yes"
                    # else:
                    #     res['rideshow'] = "No"
                        
                        
                    if driverid == '0':
                        res['bid_status'] = "No"
                    else:
                        booki = Ride_pin.objects.filter(getride=i.id,getdriver=driverid).exclude(status='3')
                        if booki:
                            res['bid_status'] = "Yes"
                        else:
                            res['bid_status'] = "No"
                    res['id'] = i.id
                    res['Passanger_Id'] = i.getpassenger.id
                    rat = Passenger_Rating.objects.filter(mine=i.getpassenger.id)
                    ls = []
                    for iij in rat:
                        ls.append(int(iij.rates))
                        
                    if ls == []:
                        res['Passenger_rating'] = 0.0
                    else:
                        res['Passenger_rating'] = Average(ls) 
                        
                    res['Passenger_name'] = i.getpassenger.name.title()
                    res['Passenger_number'] = i.getpassenger.contact_no if i.getpassenger.contact_no else ''
                    res['Passenger_token'] = i.getpassenger.ntk
                    res['pro_image'] = i.getpassenger.pro_image.url
                    res['pickUp'] = i.pickUp.capitalize()
                    res['dropout'] = i.dropout.capitalize()
                    res['date'] = i.date.strftime("%d-%m-%Y")
                    res['time'] = i.time
                    res['dtime'] = i.dtime
                    res['ride_status'] = i.status
                    res['note'] = i.add_information.title()
                    res['Passengers'] = i.seats
                    res['Parcels'] = i.capacity
                    res['filter'] = filter
                    if seats == "" or seats == "0":
                        lis.append(res)
                    elif seats == "F" or seats == "f":
                        if i.seats == "F" or i.seats == "f": 
                            lis.append(res)
                    else:
                        if i.seats == "F" or i.seats == "f":
                            pass
                        else:
                            res['filter'] = "Yes"
                            if i.ride_type == "T":
                                if int(i.capacity) >= int(seats):
                                    lis.append(res)
                            if i.ride_type == "C":
                                if int(i.seats) >= int(seats):
                                    lis.append(res)
                
        return Response({"status" : 1,"msg" : "success","data" :lis})
    else:
        return Response({'status': 0, 'msg':"Record Not Found"})

@api_view(['POST'])
def DriverGiveRating(request,Rid):
    try:
        # showtime = strftime("%Y-%m-%d")
        data = request.data
        ra = float(data["rate"])
        rat = round(ra)
        review = data["review"]
        showtime = data['datetime']
        getride = Ride_pin.objects.get(id=Rid)
        getpas = user_all.objects.get(id=getride.passengerid.id,as_user = 'Passenger')
        getdri = user_all.objects.get(id=getride.getdriver.id,as_user = 'Driver')    
        rate = Passenger_Rating.objects.filter(
            mine = getpas,
            tri = getride,
            driverid = getdri,
        )
        if len(rate) > 0:
            return Response({'status':0,'msg' : 'Rating has been Given'})
        else:
            rat = Passenger_Rating.objects.create(
                mine = getpas,
                tri = getride,
                driverid = getdri,
                rates = rat,
                review = review,
                create = showtime,
            )
            return Response({'status':1,'msg' : 'Rating Add Successfully'})
    except ObjectDoesNotExist:
        return Response({'status':0,'msg' : 'Ride Is Not Found'})
        
@api_view(['GET'])
def DriverGetRating(request,pk):
    try:
        getdri = user_all.objects.get(id=pk,as_user = 'Driver')
        getride = Drivers_Rating.objects.filter(mine=getdri).order_by('-create')
        if getride:
            serial = DriverGetRatingSeializer(getride,many=True)
            return Response({'status':1, 'msg':"Success","data":serial.data}) 
        else:
            return Response({'status':0,'msg':'No Rating List Founded'})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})
        
@api_view(['GET'])
def DriverDrivenRatingList(request,pk):
    try:
        getdri = user_all.objects.get(id=pk,as_user = 'Driver')
        getride = Passenger_Rating.objects.filter(driverid=getdri).order_by('-create')
        if getride:
            serial = DriverDrivenRatingSeializer(getride,many=True)
            return Response({'status':1, 'msg':"Success","data":serial.data}) 
        else:
            return Response({'status':0,'msg':'No Rating List Founded'})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['GET'])
def CarsListing(request,pk):
    try:
        # cas = Vehicle.objects.filter(driverid=pk,status='1')
        cas = Vehicle.objects.filter(driverid=pk)
        serial = CarListingSerializer(cas,many=True)
        return Response({"status":1,"msg":"Success",'data':serial.data})
    except ObjectDoesNotExist:
        return Response({'status':0 ,"msg":"Wrong Id"})

@api_view(['POST'])
def AcceptRequestForTripByDriver(request,pk):
    try:
        getbooking = Ride_pin.objects.get(id=pk)
        getbok = Ride.objects.get(id=getbooking.getride.id,publish='1')
        if getbok.ride_type == "C":
            if getbok.status == '0' :
                if getbooking.status == '0':
                    if int(getbooking.for_passenger):
                        if int(getbok.Max_seats) >= int(getbooking.for_passenger):
                            pas = int(getbok.Max_seats) - int(getbooking.for_passenger)
                            if pas == 0:
                                getbok.status = "1"
                                getbok.Max_seats = pas
                            else:
                                getbok.Max_seats = pas
                            getbok.save()
                            getbooking.status = "1"
                            getbooking.save()
                            return Response({'status':1, 'msg': f"Request Accept",'Passenger_id':getbooking.passengerid.id,"Passenger_token":getbooking.passengerid.ntk})
                        else :
                            return Response({'status':0, 'msg': "You Have Limited Seats"})
                    if int(getbooking.for_parcel):
                        if int(getbok.Max_parcel) >= int(getbooking.for_parcel):
                            pas = int(getbok.Max_parcel) - int(getbooking.for_parcel)
                            if pas == 0:
                                getbok.status = "1"
                                getbok.Max_parcel = pas
                            else:
                                getbok.Max_parcel = pas
                            getbok.save()
                            getbooking.status = "1"
                            getbooking.save()
                            return Response({'status':1, 'msg': f"Request Accept",'Passenger_id':getbooking.passengerid.id,"Passenger_token":getbooking.passengerid.ntk})
                        else :
                            return Response({'status':0, 'msg': "You Have Limited Capecity"})
                else :
                    return Response({'status':0, 'msg': "Passenger Request Accepted"})
            else :
                return Response({'status':0, 'msg': "Seats & Space Full"})

        if getbok.ride_type == "T":
            if getbok.status == '0' :
                if getbooking.status == '0':
                    if int(getbooking.for_parcel):
                        if int(getbok.Max_parcel) >= int(getbooking.for_parcel):
                            pas = int(getbok.Max_parcel) - int(getbooking.for_parcel)
                            if pas == 0:
                                getbok.status = "1"
                                getbok.Max_parcel = pas
                            else:
                                getbok.Max_parcel = pas
                            getbok.save()
                            getbooking.status = "1"
                            getbooking.save()
                            return Response({'status':1, 'msg': f"Request Accept",'Passenger_id':getbooking.passengerid.id,"Passenger_token":getbooking.passengerid.ntk})
                        else :
                            return Response({'status':0, 'msg': "You Have Limited Capecity"})
                else :
                    return Response({'status':0, 'msg': "Passenger Request Accepted"})
            else :
                return Response({'status':0, 'msg': "Space Full"})
        # else:
        #     if getbok.status == '0' :
        #         getbooking.status = "1"
        #         getbooking.save()
        #         return Response({'status':1, 'msg': f"Request Accept",'Driver_token':getbooking.getdriver.ntk,"Passenger_token":getbooking.passengerid.ntk})
        #     else :
        #         return Response({'status':0, 'msg': "Seats Full"})
            
        #     return Response({'status':0, 'msg': "this Is Truck Ride"})
            
    except ObjectDoesNotExist:
        return Response({"status" : "0",'msg': "Wrong Id"})

@api_view(['POST'])
def SendIDProofe(request,dk,pk):
    try:
        getdriver = user_all.objects.get(id=dk,as_user = 'Driver')
        getpassenger = user_all.objects.get(id=pk,as_user = 'Passenger')
        data = request.data
        showtime = data['datetime']
        if (getpassenger.img_status == "P" and getdriver.img_status == "P") or (getdriver.img_status == "R" and getpassenger.img_status == "R") :
            try:
                image1 = data['image1']
                ex = image1.name
                if ex.endswith('.jpg'):
                    getdriver.image1 = image1
                    getpassenger.image1 = image1
                elif ex.endswith('.png'):
                    getdriver.image1 = image1
                    getpassenger.image1 = image1
                elif ex.endswith('.jpeg'):
                    getdriver.image1 = image1
                    getpassenger.image1 = image1
                else:
                    getdriver.image1 = getdriver.image1
                    getpassenger.image1 = getpassenger.image1
                    return Response({"status": 0, "msg" : "File Formate use jpg,jpeg,png"})
            except:
                getdriver.image1 = getdriver.image1
            try:
                image2 = data['image2']
                ex = image2.name
                if ex.endswith('.jpg'):
                    getdriver.image2 = image2
                    getpassenger.image2 = image2
                elif ex.endswith('.png'):
                    getdriver.image2 = image2
                    getpassenger.image2 = image2
                elif ex.endswith('.jpeg'):
                    getdriver.image2 = image2
                    getpassenger.image2 = image2
                else:
                    getdriver.image2 = getdriver.image2
                    getpassenger.image2 = getpassenger.image2
                    return Response({"status": 0, "msg" : "File Formate use jpg,jpeg,png"})
            except:
                getdriver.image2 = getdriver.image2
            getdriver.img_status == "P"
            getpassenger.img_status == "P"
            getdriver.save()
            getpassenger.save()
            return Response({"status": 1,"msg" : "Success","Driver_id" : getdriver.id,"Passenger_id":getpassenger.id})
        else:
            return Response({"status": 0,"msg" : "Document Updated"})
    except ObjectDoesNotExist:
        return Response({"status": 0,"msg" : "Wrong Id"})

@api_view(['GET'])
def MyIdProofe(request,pk):
    ids = Id_proofe.objects.filter(driverid=pk)
    prof = Id_proofeSerializerForDriver(ids,many=True)
    return Response({"status": 1,"msg" : "Success","Proofe_id" : prof.data})

@api_view(['POST'])
def CancelRideRequest(request,pk):
    try:
        getbooking = Ride_pin.objects.get(id=pk)
        dird = Ride.objects.get(id=getbooking.getride.id)
        if dird.trip_status == 'P':
            if getbooking.status == '0' or getbooking.status == "1":
                getbooking.status = '3'
                getbooking.save()
                dird.status = '0'
                dird.save()
                getbooking.save()
                return Response({'status':1 ,"msg":"Cancel Booking"})    
            else:
                return Response({'status':0 ,"msg":"Booking Already Reject Or Cancel"})
        else:
            return Response({'status': 0 ,"msg":"Booking Not Cancel"})    
    except ObjectDoesNotExist:
        return Response({'status':0 ,"msg":"Ride Booking Id Not Found"})

@api_view(['POST'])
def ReportPassengerBehavior(request,Rid):
    try:
        # showtime = strftime("%Y-%m-%d")
        data = request.data
        report_text = data["report_text"]
        showtime = data['datetime']
        getride = Ride_pin.objects.get(id=Rid)
        getpas = user_all.objects.get(id=getride.passengerid.id,as_user = 'Passenger')
        getdri = user_all.objects.get(id=getride.getdriver.id,as_user = 'Driver')    
        ratw = Passenger_Report.objects.filter(
            mine = getpas,
            tri = getride,
            driverid = getdri
        )
        if len(ratw) > 0:
            return Response({'status':0,'msg' : 'Report has been Given'})
        else:
            rat = Passenger_Report.objects.create(
                mine = getpas,
                tri = getride,
                driverid = getdri,
                report_text = report_text,
                create = showtime,  
            )
            getride.pas_status = 'E'
            getride.save()
            return Response({'status':1,'msg' : 'Report Add Successfully'})
    except ObjectDoesNotExist:
        return Response({'status':0,'msg' : 'Ride Is Not Found'})

@api_view(['POST'])
def AddHistory(request,pk):
    try:
        data = request.data
        # showtime = strftime("%Y-%m-%d", )
        pick = data['pick']
        drop = data['drop']
        pick_lat = data['pick_lat']
        pick_lng = data['pick_lng']
        drop_lat = data['drop_lat']
        drop_lng = data['drop_lng']
        date = data['date']
        location = data['location']
        showtime = data['datetime']
        getdri = user_all.objects.get(id=pk,as_user = 'Driver')
        adda = Search_History.objects.filter(driverid = getdri,pick = pick,drop = drop,pick_lat = pick_lat,pick_lng = pick_lng,drop_lat = drop_lat,drop_lng = drop_lng,date = date,location = location,create = showtime,)
        if len(adda) > 0:
            for i in adda:
                i.delete()
            add = Search_History.objects.create(
                driverid = getdri,
                pick = pick,
                drop = drop,
                pick_lat = pick_lat,
                pick_lng = pick_lng,
                drop_lat = drop_lat,
                drop_lng = drop_lng,
                date = date,
                location = location,
                create = showtime,
            )
        else:
            add = Search_History.objects.create(
                driverid = getdri,
                pick = pick,
                drop = drop,
                pick_lat = pick_lat,
                pick_lng = pick_lng,
                drop_lat = drop_lat,
                drop_lng = drop_lng,
                date = date,
                location = location,
                create = showtime,
            )
        return Response({'status' : 1,'msg' : 'History Added'})
    except ObjectDoesNotExist:
        return Response({'status' : 0,'msg' : 'Driver Id Wrong'})

@api_view(['GET'])
def HistoryView(request,pk,ll):
    try:
        his = Search_History.objects.filter(driverid=pk,location=ll)[:4]
        if len(his)> 0:
            serial = HistoryViewForDriver(his,many=True)
            return Response({'status':1 ,"msg": "Success", 'data' : serial.data})
        else:
            return Response({'status':0 ,"msg": "No Record"})
    except ObjectDoesNotExist:
        return Response({'status':0 ,"msg": "Fail"})

@api_view(['POST'])
def tripsetting(request,pk):
    try:
        data = request.data
        date = datetime.date.today()
        showtime1 = data['date']
        hour = data['hour']
        mins = data['minute']
        # showtime1 = strftime("%Y-%m-%d", )
        # hour = strftime("%H")
        # mins = strftime("%M")
        ride = Ride.objects.get(id=pk,publish='1')
        rr = Ride_pin.objects.filter(getride=pk)
        hh = ride.ride_time.strftime("%H")
        mi = ride.ride_time.strftime("%M")
        mm = ride.ride_time.strftime("%I:%M %p")
        if ride.trip_status == 'P':
            if str(ride.date) == str(showtime1):
                if int(hh) <= int(hour):
                    if (int(mi) <= int(mins)) or (int(hh) < int(hour) and int(mi) >= int(mins)):
                        ride.trip_status = 'O'
                        ride.trip_status2 = '1'
                        for j in rr:
                            if j.status == '0':
                                j.status = '2'
                                j.save()
                        ride.save()
                        return Response({'status':1 ,"msg": f"Trip Started"})
                    else:
                        return Response({'status':0 ,"msg": f"Wait For Few Minutes"})
                else:
                    return Response({'status':0 ,"msg": f"Ride Can't start Beacuse Ride Time is {mm}","ride_date" : f"{mm}"})
            else:
                ride = Ride.objects.get(id=pk,publish='1')
                value = True
                i = 0
                while (value):
                    yesterday = date - datetime.timedelta(days=i)
                    tomorrow = date + datetime.timedelta(days=i)
                    i = i + 1
                    dates = ride.date.strftime("%d-%m-%Y")
                    if str(ride.date) == str(yesterday):
                        value = False
                        i = i - 1
                        ride.status = '3'
                        for kk in rr:
                            kk.status = '3'
                            kk.save()
                        ride.save()
                        return Response({'status':0 ,"msg": f"This Ride Date Has A Previous Date {dates} which is Gone before {i} days Ago", "ride_date" : dates,"days" : i})
                    if str(ride.date) == str(tomorrow):
                        value = False
                        i = i - 1
                        return Response({'status':0 ,"msg": f"Ride couldn't be able to start as it is on {dates} Please Come Again After {i} days", "ride_date" : dates,"days" : i})
                        
        if ride.trip_status == 'O':
            for i in rr:
                if i.status == '1':
                    i.pas_status = "E"
                    i.today = showtime1
                    i.save()
                if i.status == '2':
                    i.delete()    
            ride.trip_status = 'E'
            ride.trip_status2 = '3'
            ride.save()
            return Response({'status':1 ,"msg": f"Trip Complete"})
        
        if ride.trip_status == 'E':
            return Response({'status':1 ,"msg": f"Trip Complete"})
            
    except ObjectDoesNotExist:
        return Response({'status':0 ,"msg": "Something Wrong"})

@api_view(['GET'])
def MyCars(request,pk):
    try:
        # cars = Vehicle.objects.filter(driverid=pk,status='1')
        cars = Vehicle.objects.filter(driverid=pk)
        if cars:
            lius = [{'Cid':'0','type':'','car':"Select Car",}]
            for instance in cars:
                res = {}
                res['Cid'] = instance.id
                if instance.vehicle_type == "A":
                    res['type'] = "Auto"
                if instance.vehicle_type == "B":
                    res['type'] = "Bike"
                if instance.vehicle_type == "C":
                    res['type'] = "Car"
                if instance.vehicle_type == "T":
                    res['type'] = "Truck"
                res['car'] = f"{instance.vehical_variant.brand} {instance.vehical_variant}"
                # res['car'] = f"{instance.vehical_variant}"
                lius.append(res)
            return Response({'status':1 ,"msg": f"Success","Per_km_price" : f"{instance.driverid.fare_per_km}",'data' : lius})
        else:
            return Response({'status':0 ,"msg": 'No Cars'})            
    except ObjectDoesNotExist:
        return Response({'status':0 ,"msg": 'ID Found'})

@api_view(['GET'])
def BlockStatusForDriver(request,pk):
    try:
        getd = user_all.objects.get(id=pk)
        if getd.status == 'Active':
            return Response({'status':0,'msg':'Unblock'})
        else:
            return Response({'status':1,'msg':'Block'})
    except:
        return Response({'status':1,'msg':'User Deleted'})

@api_view(['POST'])
def ContactUsDriver(request):
    data = request.data
    name = data['name']
    email = data['email'].casefold()
    message = data['messages']
    if (not name):
        return Response({"status":0,"msg":'Name Is Required..!'})
    if (not email):
        return Response({"status":0,"msg":'Email Is Required..!'})
    if (not message):
        return Response({"status":0,"msg":'Message Is Required..!'})
    
    if(re.search(email_pattern, email)):
        mail_subject = f'Contact By {name} Regarding MyLifto App'
        message = f'{name}\n{email}\n{message}' 
        email_from = settings.EMAIL_HOST_USER
        to_email = [email_from,]
        send_mail(mail_subject, message, f'{name}', to_email)
        return Response({'status' : 1,'msg':'Mail Sent Successfully'})
    else:
        return Response({'status' : 0 , 'msg' : "Email Is Not Proper"})
    
@api_view(['POST','PUT'])
def CurrentLoc(request,pk):
    try:
        data = request.data
        ar = Ride.objects.filter(getdriver=pk,publish='1').exclude(status='3')
        if len(ar) > 0:    
            for i in ar:
                if i.trip_status == 'O':
                    i.car_latitude = float(data['car_latitude']) if float(data['car_latitude']) else i.car_latitude
                    i.car_longitude = float(data['car_longitude']) if float(data['car_longitude']) else i.car_longitude
                    i.save()
            return Response({'status':1 ,"msg": "success"})
        else:
            return Response({'status':0 ,"msg": "No Ride Founded"})
    except ObjectDoesNotExist:
        return Response({'status':3 ,"msg": "Fail"})

@api_view(['GET'])
def RatingDetailsPageForRecieve(request,pk):
    rat = Drivers_Rating.objects.get(id=pk)
    context = {
        'status' : 1,
        'msg' : 'success',
        "Passenger_name" : rat.passengerid.name.title(),
        "Passenger_pro_image" : rat.passengerid.pro_image.url,
        "ride_id" : rat.tri.id,
        "pickup" : rat.tri.pickUp.capitalize(),
        "dropout" : rat.tri.dropout.capitalize(),
        "ride_date" : rat.tri.date,
        "create" : rat.create,
        "rate" : float(rat.rates),
        "review" : rat.review,
    }
    return Response(context)
    
@api_view(['GET'])
def GivenRatingDetailsPageFor(request,pk):
    rat = Passenger_Rating.objects.get(id=pk)
    context = {
        'status' : 1,
        'msg' : 'success',
        "Passenger_name" : rat.mine.name.title(),
        "Passenger_pro_image" : rat.mine.pro_image.url,
        "ride_id" : rat.tri.getride.id,
        "pickup" : rat.tri.getride.pickUp.capitalize(),
        "dropout" : rat.tri.getride.dropout.capitalize(),
        "ride_date" : rat.tri.getride.date,
        "create" : rat.create,
        "rate" : float(rat.rates),
        "review" : rat.review,
    }
    
    return Response(context)

@api_view(['GET'])
def BidDetalis(request,pk,dd):
    try:
        ri = Ride.objects.get(id=pk,publish__range=['1','3'])
        print(ri.as_user)
        if ri.as_user == 'Passenger':
            di = Ride_pin.objects.filter(getride=ri.id,getdriver=dd).exclude(status='2')            
            if di[0].status == '1':
                ratw = Passenger_Rating.objects.filter(tri=di[0].id,mine=ri.getpassenger.id,driverid=dd)
                repo = Passenger_Report.objects.filter(tri=di[0].id,mine=ri.getpassenger.id,driverid=dd)
                if len(ratw) > 0 or len(repo) > 0:
                    rat = "Yes"
                    repo = "Yes"
                else:
                    rat = "No"
                    repo = "No"
                context = {
                    'status':1,
                    'msg':'success',
                    'id':ri.id,
                    'booking_id':di[0].id,
                    'pickup' : ri.pickUp.capitalize(),
                    'pickup_address1' : ri.pickup_address1.capitalize(),
                    'pickup_address2' : ri.pickup_address2.capitalize(),
                    'dropout' : ri.dropout.capitalize(),
                    'dropout_address1' : ri.dropout_address1.capitalize(),
                    'dropout_address2' : ri.dropout_address2.capitalize(),
                    'ride_type' : ri.ride_type,
                    'trip_pas_status' : ri.trip_status,
                    'seat' : ri.seats,
                    'time' : ri.time,
                    'rat' : rat,
                    'repo' : repo,
                    'dtime' : ri.dtime,
                    'capacity' : ri.capacity,
                    'Passenger_id' : f"{ri.getpassenger.id}",
                    'Passenger_name' : ri.getpassenger.name.title(),
                    'Passenger_image' : ri.getpassenger.pro_image.url,
                    'fees' : f"{di[0].fees}",
                    "request_date" : f"{di[0].request_date.strftime('%Y-%m-%d')}",
                    }
                return Response(context)
            else:
                context = {
                    'status':1,
                    'msg':'success',
                    'id':ri.id,
                    'rat':"Yes",
                    'repo':"Yes",
                    'pickup' : ri.pickUp.capitalize(),
                    'pickup_address1' : ri.pickup_address1.capitalize(),
                    'pickup_address2' : ri.pickup_address2.capitalize(),
                    'dropout' : ri.dropout.capitalize(),
                    'dropout_address1' : ri.dropout_address1.capitalize(),
                    'dropout_address2' : ri.dropout_address2.capitalize(),
                    'ride_type' : ri.ride_type,
                    'time' : ri.time,
                    'dtime' : ri.dtime,
                    'trip_pas_status' : ri.ride_type,
                    'seat' : ri.seats,
                    'capacity' : ri.capacity,
                    'Passenger_id' : "",
                    'Passenger_name' : "",
                    'Passenger_image' : "",
                    'fees' : f"{di[0].fees}",
                    "request_date" : f"{di[0].request_date.strftime('%Y-%m-%d')}",
                    }
                return Response(context)
        else:
            return Response({"status":0,'msg':'No Record'})
    except:
        return Response({"status":0,'msg':'Wrong Id'})

@api_view(['GET'])
def Check_My_Car(request,pk):
    try:
        user = user_all.objects.get(id=pk,as_user='Driver')
        car = Vehicle.objects.filter(driverid=user.id,status='0')
        if len(car) > 0:
            return Response({"status":1,'msg':'Previous added car is still in pending mode. Do you still want to add new car?'})
        else:
            return Response({"status":0,'msg':'Add New Car'})
    except:
        return Response({"status":2,'msg':'Something Wrong'})

@api_view(['POST'])
def FullBookedDriver(request,pk):
    # try:
    data = request.data
    getcar = data['carid']
    fullbook = data['fullbooked']
    current_date = data['current_date']
    showtime = data['datetime']
    current_location = data['current_location']
    if(not showtime):
        return Response({"status":0,'msg':'DateTime Required.!'})
    lis = []
    st = ""
    for i in getcar:
        if i == '[':
            pass
        else:
            st = st + f"{i.replace(',','').replace(']','')}"
            if i == ',' or i == ']':
                lis.append(st.replace(" ",''))
                st = ''
    getdriver = user_all.objects.get(id=pk,as_user='Driver')
    if fullbook == "0" or fullbook == 0: 
        ride = Ride.objects.filter(as_user='Driver',getdriver=getdriver,publish = '1')
        if len(ride) > 0 :
            for i in ride:
                if i.fullbooked == '1' or i.fullbooked == '2':
                    i.delete()
            return Response({"status":2,'msg':'Driver Has Remove Full Book'})
        else:
            return Response({"status":2,'msg':'Driver Has Remove Full Book'})
    if fullbook == 1 or fullbook == "1":
        addrid = Ride.objects.create(
            as_user = 'Driver',
            getdriver = getdriver,
            date = current_date,
            fullbooked = "1",
            publish = '1',
            current_location = current_location,
            current_date = current_date,
            create_at = showtime,
            update_at = showtime
        )
        for j in lis:
            car = Vehicle.objects.get(id=j)
            #     addrid.ride_type = car.vehicle_type
            # else:
            #     addrid.ride_type = "M"
            addrid.ride_type = "M"
            addrid.manycar.add(car)
            addrid.save()
            
            addnewbooking = Ride.objects.create(
                as_user = 'Driver',
                car = car,
                getdriver = getdriver,
                date = current_date,
                ride_type = car.vehicle_type,
                fullbooked = "2",
                publish = '1',
                current_location = current_location,
                current_date = current_date,
                create_at = showtime,
                update_at = showtime
            )
        return Response({"status":1,'msg':'Driver Has Full Book For Today'})
    # except:
    #     return Response({"status":0,'msg':'Something Wrong'})

@api_view(['POST'])        
def EnableToDisableRide(request,pk):
    try:
        data = request.data
        sta = data['EnableAndDisable']
        rd = Ride.objects.get(id=pk)
        if sta == '0':
            rd.publish = '3'
            status = 0
            msg = "Ride Is Disable"
        elif sta == '1':
            rd.publish = '1'
            status = 1
            msg = "Ride Is Enable"
        else:
            return Response({"status" : 0 ,'msg': "Not Defined Value"})
            
        rd.save()
        return Response({"status" : status ,'msg': msg})
    except:
        return Response({"status" : 0 ,'msg': "Something Wrong"})
        
@api_view(['GET'])
def CheckFullBooked(request,driverid,current_date):
    ride = Ride.objects.filter(as_user='Driver',getdriver=driverid,date = current_date,fullbooked = '1',publish = '1',current_date = current_date)
    if len(ride) > 0:
        if ride[0].current_location:
            current_location = ride[0].current_location.title()
        else:
            current_location = ""
        return Response({"status":1,"current_location":current_location})
    else:
        return Response({"status":0,"current_location":''})

@api_view(["POST"])
def ForgotOtpSendDriver(request):
    data = request.data
    raw = data['email_or_num']
    otp = ''
    for i in range (4):
        otp+=str(randint(1,9))
    getotp = otp
    if(not raw):
        return Response({'status' : 0 , 'msg' : "Email Or Phone Number Is Required"})
    
    # if(re.search(mobile_pattern,raw)):
        
    if(re.search(email_pattern, raw)):
        passenger_mail = user_all.objects.filter(email=raw,as_user = 'Passenger').exclude(active_ac_with_otp='0')
        Driver_mail = user_all.objects.filter(email=raw,as_user = 'Driver').exclude(active_ac_with_otp='0')
        if len(passenger_mail) > 0 and len(Driver_mail) > 0:
            passanger = user_all.objects.get(id=passenger_mail[0].id,as_user = 'Passenger')
            driver = user_all.objects.get(id=Driver_mail[0].id,as_user = 'Driver')
            if passanger.status == 'Active' and driver.status == 'Active':
                passanger.otp = getotp
                passanger.active_ac_with_otp = "2"
                passanger.save()
                
                driver.otp = getotp
                driver.active_ac_with_otp = "2"
                driver.save()
                    
                mail_subject = 'Forgot Password Otp From MyLifto'
                message = f'Hi {passanger.name.title},\n Set New Password Help of This Otp. \n Your Otp is:- {passanger.otp} \n Thank You' 
                email_from = settings.EMAIL_HOST_USER
                to_email = [raw,]
                send_mail(mail_subject, message, email_from, to_email)
                return Response({'status' : 1 , 'msg' : "Otp Send Successfully Via Email","Driver_id":driver.id,"Passenger_id":passanger.id,'Type':"Email","OTP":passanger.otp,"token":passanger.ntk})
            else:
                return Response({'status' : 0 , 'msg' : "Account is Blocked"})
        else:
            return Response({'status' : 0 , 'msg' : "Email Is Not Found.!"})
    else:
        # if raw[0] == '0' or raw[0] == 0:
        #     raw = raw
        # else:
        #     raw = f"0{raw}"
        passenger_num = user_all.objects.filter(contact_no=raw,as_user = 'Passenger').exclude(active_ac_with_otp='0')
        Driver_num = user_all.objects.filter(contact_no=raw,as_user = 'Driver').exclude(active_ac_with_otp='0')
        if len(passenger_num) > 0 and len(Driver_num) > 0:
            passanger = user_all.objects.get(id=passenger_num[0].id,as_user = 'Passenger')
            driver = user_all.objects.get(id=Driver_num[0].id,as_user = 'Driver')
            if passanger.status == 'Active' and driver.status == 'Active':
                passanger.otp = getotp
                passanger.active_ac_with_otp = "2"
                passanger.save()
                
                driver.otp = getotp
                driver.active_ac_with_otp = "2"
                driver.save()
                return Response({'status' : 1 , 'msg' : "Otp Send Successfully Via Text","Driver_id":driver.id,"Passenger_id":passanger.id,'Type':"Mobile","OTP":passanger.otp,"token":passanger.ntk})
            else:
                return Response({'status' : 0 , 'msg' : "Account is Blocked"})
        else:
            return Response({'status' : 0 , 'msg' : "Number Is Not Found.!"})
@api_view(["POST"])
def AddInCityRide(request,pk):
    try:
        data = request.data
        pick = data['pickUp'].casefold()
        pickUp_latitude = data['pickUp_latitude']
        pickUp_longitude = data['pickUp_longitude']
        drop = data['dropout'].casefold()
        dropout_latitude = data['dropout_latitude']
        dropout_longitude = data['dropout_longitude']
        date = data['date']
        time = data['time'].upper()
        dtime = data['dtime'].upper()
        capacity = data['capacity']
        seats = data['seats']
        fees = data['fees']
        showtime = data['datetime']
        add_information = data['add_information'].casefold()
        pickup_address1 = data['pickup_address1'].casefold()
        pickup_address2 = data['pickup_address2'].casefold()
        dropout_address1 = data['dropout_address1'].casefold()
        dropout_address2 = data['dropout_address2'].casefold()
        vehicle = data['vehicle'].casefold()
        getdriver = user_all.objects.get(id=pk,as_user = 'Driver')
        
        if (not capacity):
            capacity = '0'
            
        if (not seats):
            seats = '0'
    
        if(not pick):
            return Response({"status":0,"msg":"pick Point is not Add"})
        if(not pickUp_latitude):
            return Response({'status':0,"msg":"pickUp_latitude is Not Add"})
        if(not pickUp_longitude):
            return Response({'status':0,"msg":"pickUp_longitude is Not Add"})
        if(not drop):
            return Response({"status":0,"msg":"drop Point is not Add"})
        if(not dropout_latitude):
            return Response({'status':0,"msg":"dropout_latitude is Not Add"})
        if(not dropout_longitude):
            return Response({'status':0,"msg":"dropout_longitude is Not Add"})
        if(not date):
            return Response({"status":0,"msg":"select Date for Ride"})
        if(not getdriver):
            return Response({"status":0,"msg":"User Doesn't Login"})
        if(not time):
            return Response({'status':0,'msg':'Pick Up Time is Not Add'})
        if(not dtime):
            return Response({'status':0,'msg':'Drop off Time is Not Add'})
        publ = "1"
        tims = re.sub(" ","",time)
        ride_time = f"{str(date)} {str(convert(tims))}"
        # rideserach = InRide.objects.filter(getdriver = getdriver,date = date,vehicle = vehicle,publish='1',trip_status="P",status__range=['0','1']).exclude(status='3')
        
        # if len(rideserach) > 0:
        #     return Response({"status" : 0 , "msg" : f"This Car Is Already Book For This Date {date}"})
        # else:
        addrsd = InRide.objects.filter(as_user = 'Driver',getdriver = getdriver,pickUp = pick,dropout = drop,date = date,vehicle = vehicle).exclude(status='3')
        if len(addrsd) > 0:
            addrsd[0].pickUp_latitude = pickUp_latitude
            addrsd[0].pickUp_longitude = pickUp_longitude
            addrsd[0].driver_latitude = pickUp_latitude
            addrsd[0].driver_longitude = pickUp_longitude
            addrsd[0].dropout_latitude = dropout_latitude
            addrsd[0].dropout_longitude = dropout_longitude
            addrsd[0].seats = seats
            addrsd[0].Max_seats = seats
            addrsd[0].fees = fees
            addrsd[0].capacity = capacity
            addrsd[0].Max_parcel = capacity
            addrsd[0].per_km = getdriver.fare_per_km
            addrsd[0].pickup_address1 = pickup_address1
            addrsd[0].pickup_address2 = pickup_address2
            addrsd[0].dropout_address1 = dropout_address1
            addrsd[0].dropout_address2 = dropout_address2
            addrsd[0].add_information = add_information
            addrsd[0].ride_time = ride_time
            addrsd[0].create_at = showtime
            addrsd[0].update_at = showtime
            addrsd[0].save()
            return Response({
                "Ride_Id" : addrsd[0].id,
                "status":1,
                "msg":"Ride Added Successfully"
                })
        else:
            addrid = InRide.objects.create(
                as_user = 'Driver',
                getdriver = getdriver,
                pickUp_latitude = pickUp_latitude,
                pickUp_longitude = pickUp_longitude,
                driver_latitude = pickUp_latitude,
                driver_longitude = pickUp_longitude,
                dropout_latitude = dropout_latitude,
                dropout_longitude = dropout_longitude,
                pickUp = pick,
                dropout = drop,
                date = date,
                per_km = getdriver.fare_per_km,
                publish = publ,
                time = time,
                vehicle = vehicle,
                dtime = dtime,
                seats = seats,
                Max_seats = seats,
                capacity = capacity,
                Max_parcel = capacity,
                fees = fees,
                pickup_address1 = pickup_address1,
                pickup_address2 = pickup_address2,
                dropout_address1 = dropout_address1,
                dropout_address2 = dropout_address2,
                ride_time = ride_time,
                add_information = add_information,
                create_at = showtime,
                update_at = showtime
            )
            return Response({
                "Ride_Id" : addrid.id,
                "status":1,
                "msg":"Ride Added Successfully"
            })
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong Or Data Missing"})
    
@api_view(['POST'])
def RidesearchInCity(request):
    data = request.data
    date = data['date']
    pickUp = data['pickUp'].casefold()
    dropout = data['dropout'].casefold()
    fees = data['fees']
    vehicle = data['vehicle'].casefold()
    if(not date):
        return Response({"status":0,"msg":"Date Is Not Founded"})
    if pickUp and dropout and fees and vehicle:
        book = InRide.objects.filter(vehicle=vehicle,pickup_address1=pickUp,dropout_address1=dropout,publish='1',trip_status='P',as_user = 'Passenger',date=date,status="0").exclude(status='3')
    else:
        book = InRide.objects.filter(as_user="Passenger",publish='1',date=date,trip_status='P',status="0").exclude(status='3')
        
    if len(book) > 0:
        lis = []
        for i in book:
            res = {}
            res['id'] = i.id
            res['Passanger_Id'] = i.getpassenger.id
            res['Passenger_name'] = i.getpassenger.name.title()
            res['Passenger_number'] = i.getpassenger.contact_no if i.getpassenger.contact_no else ''
            res['pro_image'] = i.getpassenger.pro_image.url
            res['pickUp'] = i.pickup_address1.title()
            res['dropout'] = i.dropout_address1.title()
            res['pickUp_city'] = i.pickUp.capitalize()
            res['dropout_city'] = i.dropout.capitalize()
            res['date'] = i.date.strftime("%d-%m-%Y")
            res['time'] = i.time
            res['pickUp_latitude'] = i.pickUp_latitude
            res['pickUp_longitude'] = i.pickUp_longitude
            res['dropout_latitude'] = i.dropout_latitude
            res['dropout_longitude'] = i.dropout_longitude
            res['dtime'] = i.dtime
            res['fees'] = i.fees
            if i.vehicle:
                res['vehicle'] = i.vehicle.capitalize()
            else:
                res['vehicle'] = ''
            res['ride_status'] = i.status
            res['Passengers'] = i.seats
            res['Parcels'] = i.capacity
            if fees:
                if float(fees) >= float(i.fees):
                    lis.append(res)
            else:
                lis.append(res)
        return Response({"status" : 1,"msg" : "success","data" :lis})
    else:
        return Response({'status': 0, 'msg':"Record Not Found"})
        
@api_view(['POST'])
def RequestForInRide(request,rid,did):
    try:
        ridegid = InRide.objects.get(id=rid,publish='1')
        data = request.data
        showtime = data['datetime']
        fees = data['fees']
        
        pas = ridegid.getpassenger
        pasid = user_all.objects.get(id=pas.id,as_user = 'Passenger')
        getdr = user_all.objects.get(id=did,as_user = 'Driver')
        var = ridegid.getmultidriver.filter(id=getdr.id)
        if len(var)>0:
            return Response({"status": 1, "msg" : f"Request Send"})
        else:
            ridegid.getmultidriver.add(getdr)
            ridegid.save()
        
        getbo = InRide_pin.objects.filter(getride=ridegid,ride_type=ridegid.vehicle,getdriver=getdr,status='0').exclude(status='2').order_by('-id')
        if len(getbo) > 0:
            getbo[0].request_date = showtime
            getbo[0].fees = fees
            getbo[0].save()
            return Response({"status": 1, "msg" : f"Request Send","Request_Book_Id" : getbo[0].id,"Driver_name" : getdr.name.title(),"Driver_token":getdr.ntk,"Passenger_token":pasid.ntk})
        else:      
            createReq = InRide_pin.objects.create(
                pickUp = ridegid.pickUp ,
                pickup_address1 = ridegid.pickup_address1,
                dropout_address1 = ridegid.dropout_address1,
                pickUp_latitude = ridegid.pickUp_latitude ,
                pickUp_longitude = ridegid.pickUp_longitude ,
                dropout = ridegid.dropout ,
                dropout_latitude = ridegid.dropout_latitude ,
                dropout_longitude = ridegid.dropout_longitude ,
                as_user = 'Driver_bid',
                getdriver = getdr,
                getride = ridegid,
                add_information = ridegid.add_information,
                ride_type = ridegid.vehicle,
                ride_date = ridegid.date,
                ride_time = ridegid.time,
                for_passenger = ridegid.seats,
                fees = fees,
                for_parcel = ridegid.capacity,
                passengerid = pasid,
                request_date = showtime,
            )
            return Response({"status": 1, "msg" : f"Request Send","Request_Book_Id" : createReq.id,"Driver_name" : getdr.name.title(),"Driver_token":getdr.ntk,"Passenger_token":pasid.ntk})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})
        
@api_view(['GET'])
def ListInRide(request,did):
    getbo = InRide.objects.filter(publish='1').exclude(status='2').order_by('-id')
    lis = []
    for i in getbo:
        var = i.getmultidriver.filter(id=did)
        res = {}
        if i.getdriver:
            getdri = str(i.getdriver.id)
        else:
            getdri = "0"
        if  len(var)>0 or getdri == str(did):
            res['id'] = i.id
            
            if i.as_user == "Driver" and i.status == "0":
                res['Req_ride'] = "No"
            elif i.status == "1":
                res['Req_ride'] = "Naa"
            else:
                res['Req_ride'] = "Yes"
                
            res['pickup'] = i.pickup_address1.title()
            res['dropout'] = i.dropout_address1.title()
            res['date'] = i.date.strftime("%d-%m-%Y")
            res['fees'] = f"{i.fees}"
            res['pickUp_city'] = i.pickUp.title()
            res['dropout_city'] = i.dropout.title()
            res['time'] = i.time
            res['dtime'] = i.dtime
            res['driver_latitude'] = i.driver_latitude
            res['driver_longitude'] = i.driver_longitude
            res['passenger_latitude'] = i.passenger_latitude
            res['passenger_longitude'] = i.passenger_longitude
            if i.vehicle:
                res['vehicle'] = i.vehicle.title()
            else:
                res['vehicle'] = ''
            res['ride_status'] = i.status
            res['Passengers'] = i.seats
            res['Parcels'] = i.capacity
            lis.append(res)
    return Response({"status":1,'msg':'success','data':lis})

@api_view(['POST'])
def DeleteInRide(request):
    try:
        data = request.data
        rideid = data['rideid']
        getbo = InRide.objects.get(id=rideid,publish='1')
        if getbo.as_user == "Passenger":
            getbo.getdriver = None
            getbo.status = '0'
            getbo.trip_status = 'P'
            getbo.save()
        
        if getbo.as_user == "Driver":
            getbo.delete()
        return Response({"status":1,'msg':'Ride Cancel SuccessFully'})
    except:
        return Response({"status":0,'msg':'Something Wrong'})

@api_view(['GET'])
def ReqListInRide(request,rid):
    try:
        ridegid = InRide.objects.get(as_user='Driver',id=rid,publish='1')
        var = ridegid.getmultipassenger.all().order_by().reverse()
        ls = []
        for i in var:
            res = {}
            res['ride_id'] = ridegid.id
            res['pas_id'] = i.id
            res['pas_name'] = i.name.title()
            if i.pro_image:
                res['pas_pro_image'] = i.pro_image.url
            else:
                res['pas_pro_image'] = ""
            res['pas_contact_no'] = i.contact_no
            res['pas_token'] = i.ntk
            ls.append(res)
        return Response({'status':1,"msg":"success","data":ls})
    except:
        return Response({'status':0,"msg":"Id Wrong"})

@api_view(['POST'])
def AcceptInRide(request,rid):
    try:
        filterreq = InRide_pin.objects.get(id=rid,as_user = 'Passenger_Req')
        if filterreq.getride.status == "0":
            filterreq.status = "1"
            filterreq.save()
            rideid = filterreq.getride.id
            insde = InRide.objects.get(id=rideid)
            insde.getdriver = filterreq.getdriver
            insde.status = "1"
            insde.trip_status = "O"
            insde.save()
            if filterreq.passengerid:
                passengerid = filterreq.passengerid.id
                passengername = filterreq.passengerid.name.title()
                passengertoken = filterreq.passengerid.ntk
            else:
                passengerid = ""
                passengername = ""
                passengertoken = ""
            if filterreq.getdriver:
                drivername = filterreq.getdriver.name.title()
                drivertoken = filterreq.getdriver.ntk
            else:
                drivername = ""
                drivertoken = ""
            return Response({"status": 1, "msg" : f"Request Accepted","Request_Book_Id" : filterreq.id,"Driver_name" : drivername,"Driver_token": drivertoken,"Passenger_id":passengerid,"Passenger_name":passengername,"Passenger_token":passengertoken})
        else:
            return Response({'status': 0,"msg":'Ride Is Accepted By Other'})
    except:
        return Response({'status':0,"msg":"Id Wrong"})

@api_view(['POST'])
def RejectInRide(request,pid,rid):
    try:
        ridegid = InRide.objects.get(as_user='Driver',id=rid,publish='1')
        pasid = user_all.objects.get(id=pid,as_user = 'Passenger')
        ridegid.getmultipassenger.remove(pasid)
        ridegid.save()
        return Response({'status':1,"msg":"success"})
    except:
        return Response({'status':0,"msg":"Id Wrong"})

@api_view(['GET'])
def passengerList(request,did,date):
    filterreq = InRide_pin.objects.filter(as_user = 'Passenger_Req',getdriver=did,ride_date=date,status="0").exclude(status="2")
    li = []
    for y in filterreq:
        res = {}
        res['id'] = y.id
        res['ride_id'] = y.getride.id
        if y.passengerid:
            res['Passanger_Id'] = y.passengerid.id
            res['Passenger_name'] = y.passengerid.name.title()
            res['Passenger_number'] = y.passengerid.contact_no
            res['pro_image'] = y.passengerid.pro_image.url
        else:
            res['Passanger_Id'] = ""
            res['Passenger_name'] = ""
            res['Passenger_number'] = ""
            res['pro_image'] = ""
        res['pickUp'] = y.pickup_address1.title()
        res['dropout'] = y.dropout_address1.title()
        res['pickUp_city'] = y.pickUp.capitalize()
        res['dropout_city'] = y.dropout.capitalize()
        res['date'] = y.ride_date.strftime("%d-%m-%Y")
        res['time'] = y.ride_time
        res['pickUp_latitude'] = y.pickUp_latitude
        res['pickUp_longitude'] = y.pickUp_longitude
        res['dropout_latitude'] = y.dropout_latitude
        res['dropout_longitude'] = y.dropout_longitude
        res['fees'] = y.getride.fees
        li.append(res)
    return Response({"status": 1, "msg" : "success","data":li})

@api_view(['POST'])
def NegoPrice(request,pk):
    data = request.data
    filterreq = InRide_pin.objects.get(id=pk,as_user = 'Passenger_Req',status="0")
    filterreq.fees = data['fees']
    filterreq.status = '-1'
    filterreq.save()
    if filterreq.passengerid:
        passengerid = filterreq.passengerid.id
        passengername = filterreq.passengerid.name.title()
        passengertoken = filterreq.passengerid.ntk
    else:
        passengerid = ""
        passengername = ""
        passengertoken = ""
    if filterreq.getdriver:
        drivername = filterreq.getdriver.name.title()
        drivertoken = filterreq.getdriver.ntk
    else:
        drivername = ""
        drivertoken = ""
    return Response({"status": 1, "msg" : f"Request Send","Request_Book_Id" : filterreq.id,"Driver_name" : drivername,"Driver_token": drivertoken,"Passenger_id":passengerid,"Passenger_name":passengername,"Passenger_token":passengertoken})
    
@api_view(['POST'])
def getlocationincity(request,did):
    try:
        data = request.data
        lat = data['lat']
        lon = data['lon']
        getbo = InRide.objects.filter(getdriver=did,publish='1').exclude(status='2')
        for u in getbo:
            u.driver_latitude = lat
            u.driver_longitude = lon
            u.save()
        pasid = user_all.objects.get(id=did)
        pasid.latitude = lat
        pasid.longitude = lon
        pasid.save()
        return Response({"status":1,"msg":"success"})
    except:
        return Response({"status":0,"msg":"Something Is Wrong"})
        
@api_view(['GET'])
def getbookinglisting(request,rid):
    try:
        rr = Ride.objects.get(id=rid)
        if rr.getpassenger:
            passenger = rr.getpassenger.id
            passenger_name = rr.getpassenger.name
            passenger_img = rr.getpassenger.pro_image.url
            passenger_token = rr.getpassenger.ntk
        else:
            passenger = 0
            passenger_name = ""
            passenger_img = ""
            passenger_token = ""
        
        if rr.getdriver:
            driver = rr.getdriver.id
            driver_name = rr.getdriver.name
            driver_img = rr.getdriver.pro_image.url
            driver_token = rr.getdriver.ntk
        else:
            driver = 0
            driver_name = ""
            driver_img = ""
            driver_token = ""
            
        if rr.pickUp:
            pickUp = rr.pickUp.title()
        else:
            pickUp = ""
        if rr.dropout:
            dropout = rr.dropout.title()
        else:
            dropout = ""
        if rr.pickup_address1:
            pickup_address1 = rr.pickup_address1.title()
        else:
            pickup_address1 = ""
        if rr.pickup_address2:
            pickup_address2 = rr.pickup_address2.title()
        else:
            pickup_address2 = ""
        if rr.dropout_address1:
            dropout_address1 = rr.dropout_address1.title()
        else:
            dropout_address1 = ""
        if rr.dropout_address2:
            dropout_address2 = rr.dropout_address2.title()
        else:
            dropout_address2 = ""
        if rr.fees:
            fees = format(rr.fees, '.2f')
        else:
            fees = ""
        return Response({"status":1,"msg":"Success",
            "id" : rr.id,
            "passenger" : passenger,
            "passenger_name" : passenger_name,
            "passenger_img" : passenger_img,
            "passenger_token" : passenger_token,
            "driver" : driver,
            "driver_name" : driver_name,
            "driver_img" : driver_img,
            "driver_token" : driver_token,
            "ride_type" : rr.ride_type,
            "pickUp" : pickUp,
            "pickUp_latitude" : rr.pickUp_latitude,
            "pickUp_longitude" : rr.pickUp_longitude,
            "dropout" : dropout,
            "dropout_latitude" : rr.dropout_latitude,
            "dropout_longitude" : rr.dropout_longitude,
            "pickup_address1" : pickup_address1,
            "pickup_address2" : pickup_address2,
            "dropout_address1" : dropout_address1,
            "dropout_address2" : dropout_address2,
            "seats" : rr.seats,
            "fees" : fees,
            "capacity" : rr.capacity,
            "date" : rr.date,
            "note" : rr.add_information,
            "ride_status" : rr.status,
        })
    except:
        return Response({"status":0,"msg":"Ride Not Found"})




