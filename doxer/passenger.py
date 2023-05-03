from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from django.conf import settings
from django.core.exceptions import *
from django.core.mail import send_mail
from django.contrib.auth.hashers  import make_password,check_password
from time import strftime
from django.db.models import Max

from datetime import *
import datetime

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
# from django.template.loader import render_to_string

# Create your views here.
email_pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
mobile_pattern = '^[0-9]{10,20}$'

from random import randint

import re

def Average(l): 
    avg = sum(l) / len(l) 
    return avg

#   ____      ____    ______
#  |    \    /    \  |  
#  |____/   |______| |______    
#  |        |      |        |
#  |        |      |  ______|


@api_view(['POST'])
def SignUpPassanger(request):
    if request.method  == "POST":
        # showtime = strftime("%Y-%m-%d %H:%M:%S", )
        
        data = request.data
        name = data['name'].casefold()
        # raw = data['email_or_num'].casefold()
        email = data['email'].casefold()
        number = data['number']
        nks =data['token']
        password = data['password']
        cpassword = data['cpassword']
        DeviceId = data['DeviceId']
        showtime = data['datetime']
        Id_proofe1 = data['Id_proofe1']
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
                em = '' 
                num = user_all.objects.filter(contact_no=number,as_user = 'Passenger')
                if len(num) > 0:
                    getid = user_all.objects.get(id=num[0].id,as_user = 'Passenger')
                    if getid.status == 'Deactivate':
                        return Response({'status' : 0 , 'msg' : "Account Has been Block"})
                    else:
                        if getid.active_ac_with_otp == '0':
                            if password != cpassword:
                                    return Response({'status' : 0 , 'msg' : "Password Doesn't Match.!"})
                            else:
                                getid.password = make_password(password)
                                getid.cpassword = cpassword
                                getid.otp = otp
                                getid.as_user = 'Passenger'
                                getid.name = name
                                getid.image1 = Id_proofe1
                                # getid.image2 = Id_proofe1
                                getid.ntk = nks
                                getid.DeviceId = DeviceId
                                getid.create = showtime
                                getid.update_at = showtime
                                getid.save()
                                return Response({'status' : 1,'msg':'Passanger Register Succesfully','Id' :getid.id,'Type':"Mobile",'OTP':getid.otp})
                        else:
                            return Response({'status' : 0 , 'msg' : "Phone Num Is Alread Used"})
                else:
                    number = number     
            else:
                return Response({'status' : 0 , 'msg' : "Phone Number Is Not Valid"})
            
            if email:    
                if(re.search(email_pattern, email)):
                    mail = user_all.objects.filter(email=email,as_user = 'Passenger')
                    if len(mail) > 0:
                        getid = user_all.objects.get(id=mail[0].id,as_user = 'Passenger')
                        if getid.status == 'Deactivate':
                            return Response({'status' : 0 , 'msg' : "Account Has been Block"})
                        else:
                            if getid.active_ac_with_otp == '0':
                                if password != cpassword:
                                        return Response({'status' : 0 , 'msg' : "Password Doesn't Match.!"})
                                else:
                                    getid.password = make_password(password)
                                    getid.cpassword = cpassword
                                    getid.otp = otp
                                    getid.as_user = 'Passenger'
                                    getid.DeviceId = DeviceId
                                    getid.name = name
                                    getid.image1 = Id_proofe1
                                    # getid.image2 = Id_proofe1
                                    getid.ntk = nks
                                    getid.create = showtime
                                    getid.update_at = showtime
                                    getid.save()
                                    mail_subject = 'Otp Sent With API.'
                                    # message = render_to_string('doxer_admin/mail.html', {
                                    #     'name': getid.name.title(),
                                    #     'otp': getid.otp,
                                    # })
                                    message = f'Hi {getid.name.title()},\n Mail Sent Properly \n Otp is:-\'{getid.otp}\'\n Thank You' 
                                    email_from = settings.EMAIL_HOST_USER
                                    to_email = [getid.email,]
                                    send_mail(mail_subject, message, email_from, to_email)
                                    return Response({'status' : 1,'msg':'Passanger Register Succesfully','Id' :getid.id,'Type':"Email",'OTP':getid.otp})
                            else:
                                return Response({'status' : 0 , 'msg' : "Email Is Alread Used"})
                    else:
                        email = email  
                else:
                    return Response({'status' : 0 , 'msg' : "Email Or Phone Number Is Not Valid"})
            else:
                 email = email
        if password != cpassword:
            return Response({'status' : 0 , 'msg' : "Password Doesn't Match.!"})
        else:
            passanger = user_all.objects.create(
                email = email,
                name = name,
                as_user = 'Passenger',
                DeviceId = DeviceId,
                pro_image = "Users/passanger.png",
                ntk = nks,
                contact_no= number,
                image1 = Id_proofe1,
                # image2 = Id_proofe1,
                password = password,
                cpassword = cpassword,
                status = 'Active',
                create_at = showtime,
                update_at = showtime,
            )
            passanger.password = make_password(passanger.password)
            passanger.cpassword = passanger.cpassword
            passanger.otp = otp
            passanger.save()
            if passanger.email:
                types = 'Email'
                mail_subject = 'Otp Sent With API.'
                message = f'Hi {passanger.name.title()},\n Mail Sent Properly \n Otp is:-\'{passanger.otp}\'\n Thank You' 
                # message = render_to_string('doxer_admin/mail.html', {
                #                             'name': passanger.name.title(),
                #                             'otp': passanger.otp,
                # })
                email_from = settings.EMAIL_HOST_USER
                to_email = [passanger.email,]
                send_mail(mail_subject, message, email_from, to_email)
                
            if passanger.contact_no:
                types = 'Mobile'
                
            return Response({'status' : 1,'msg':'Passanger Register Succesfully','Id' :passanger.id,'Type':types,'OTP':passanger.otp})

# @api_view(['POST'])
# def LoginPassanger(request):
#     # showtime = strftime("%Y-%m-%d %H:%M:%S", )
#     data = request.data
#     raw = data['email_or_num'].casefold()
#     getpass = data['password']
#     nks = data['token']
#     showtime = data['datetime']
#     DeviceId = data['DeviceId']
#     if(not raw):
#         return Response({"status" : 0 , "msg" : "Email Or Phone Number Is Required"})
#     if(not getpass):
#             return Response({"status" : 0 , "msg" : "Password Field Is Required"})
    
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
#             num = user_all.objects.filter(contact_no=raw,as_user = 'Passenger')
#             if len(num) > 0:
#                 pas = user_all.objects.get(id=num[0].id,as_user = 'Passenger')
#                 if pas.active_ac_with_otp == "0":
#                     return Response({"status" : 0 , "msg" : "Account Is Not Created",})
#                 else:
#                     if pas.status == 'Active':
#                         passwrd = check_password(getpass, pas.password)
#                         if passwrd:
#                             dri = user_all.objects.get(id=pas.id,as_user = 'Passenger')
#                             dri.ntk = nks
#                             dri.save()
#                             logi = User_login.objects.filter(as_user='Passenger',user_id=dri,DeviceId=DeviceId)
#                             if len(logi) > 0:
#                                 pass
#                             else:
#                                 logi = User_login.objects.create(
#                                     as_user = 'Passenger',
#                                     user_id = dri,
#                                     ntk = nks,
#                                     DeviceId = DeviceId,
#                                     create_at = showtime
#                                 )
#                             Passenger_name = dri.name.title() #if dri.name else dri.email_or_num
#                             return Response({"status" : 1 , "msg" : "Login Success","id":dri.id,"Passenger_name":Passenger_name})
#                         else:
#                             return Response({"status" : 0 , "msg" : "Password Is Wrong"})
#                     else:
#                         return Response({"status" : 0 , "msg" : "Account Is Blocked",})
#             else:
#                 return Response({"status" : 0 , "msg" : "Invalid Number"})
#         elif(re.search(email_pattern, raw)):
#             mail = user_all.objects.filter(email=raw,as_user='Passenger')
#             if len(mail) > 0:
#                 pas = user_all.objects.get(id=mail[0].id,as_user = 'Passenger')
#                 if pas.active_ac_with_otp == "0":
#                     return Response({"status" : 0 , "msg" : "Account Is Not Created",})
#                 else:
#                     if pas.status == 'Active':
#                         passwrd = check_password(getpass, pas.password)
#                         if passwrd:
#                             dri = user_all.objects.get(id=pas.id,as_user = 'Passenger')
#                             dri.ntk = nks
#                             dri.save()
#                             logi = User_login.objects.filter(as_user='Passenger',user_id=dri,DeviceId=DeviceId)
#                             if len(logi) > 0:
#                                 pass
#                             else:
#                                 logi = User_login.objects.create(
#                                     as_user = 'Passenger',
#                                     user_id = dri,
#                                     DeviceId = DeviceId,
#                                     ntk = nks,
#                                     create_at = showtime
#                                 )
#                             Passenger_name = dri.name.title() #if dri.name else dri.email_or_num
#                             return Response({"status" : 1 , "msg" : "Login Success","id":dri.id,'Passenger_name':Passenger_name})
#                         else:
#                             return Response({"status" : 0 , "msg" : "Password Is Wrong"})
#                     else:
#                         return Response({"status" : 0 , "msg" : "Account Is Blocked",})
#             else:
#                 return Response({"status" : 0 , "msg" : "Invalid Email"})  
#         else:
#             return Response({"status" : 0 , "msg" : "Email Or Phone Number Is Not Valid"})

@api_view(["POST"])
def LoginPassanger(request):
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


@api_view(['POST'])
def VerifyOtpPassanger(request):
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
        print("this is Num")
        num = user_all.objects.filter(contact_no=raw,as_user = 'Passenger')
        if len(num) > 0:
            dri = user_all.objects.get(id=num[0].id,as_user = 'Passenger')
            if dri.active_ac_with_otp == "1":
                return Response({"status" : 0 , "msg" : "Otp Already Verify",'id':dri.id})
            else:
                if dri.otp == getotp:
                    dri.active_ac_with_otp = "1"
                    dri.otp = newotp
                    dri.save()
                    logi = User_login.objects.filter(as_user='Passenger',user_id=dri,DeviceId=dri.DeviceId)
                    if len(logi) > 0:
                        pass
                    else:
                        logi = User_login.objects.create(
                            as_user = 'Passenger',
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
        mail = user_all.objects.filter(email=raw,as_user = 'Passenger')
        if len(mail) > 0:
            dri = user_all.objects.get(id=mail[0].id,as_user = 'Passenger')
            if dri.active_ac_with_otp == "1":
                return Response({"status" : 1 , "msg" : "Otp Already Verify",'id':dri.id})
            else:
                if dri.otp == getotp:
                    dri.active_ac_with_otp = "1"
                    dri.otp = newotp
                    dri.save()
                    logi = User_login.objects.filter(as_user='Passenger',user_id=dri,DeviceId=dri.DeviceId)
                    if len(logi) > 0:
                        pass
                    else:
                        logi = User_login.objects.create(
                            as_user = 'Passenger',
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
def ResendOtpPassanger(request):
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
        num = user_all.objects.filter(contact_no=raw,active_ac_with_otp="0",as_user = 'Passenger')
        if len(num) > 0:
            passanger = user_all.objects.get(id=num[0].id,as_user = 'Passenger')
            if passanger.status == 'Active':
                passanger.otp = getotp
                passanger.save()
                return Response({'status' : 1 , 'msg' : "Otp Send Successfully Via Text",'Type':"Mobile","OTP":passanger.otp,'token' : passanger.ntk})
            else:
                return Response({'status' : 0 , 'msg' : "Account Is Not Created"})
        else:
            return Response({'status' : 0 , 'msg' : "Number Is Not Found.!"})
    elif(re.search(email_pattern, raw)):
        mail = user_all.objects.filter(email=raw,active_ac_with_otp='0',as_user = 'Passenger')
        if len(mail) > 0:
            passanger = user_all.objects.get(id=mail[0].id,as_user = 'Passenger')
            if passanger.status == 'Active':
                passanger.otp = getotp
                passanger.save()
                mail_subject = 'Otp Sent With API.'
                message = f'Hi {passanger.email},\n Mail Sent Properly \n Otp is:- \'{passanger.otp}\' \n Thank You' 
                email_from = settings.EMAIL_HOST_USER
                to_email = [raw,]
                send_mail(mail_subject, message, email_from, to_email)
                return Response({'status' : 1 , 'msg' : "Otp Send Successfully Via Email",'Type':"Email","OTP":passanger.otp})
            else:
                return Response({'status' : 0 , 'msg' : "Account Is Not Created"})
        else:
            return Response({'status' : 0 , 'msg' : "Email Is Not Found.!"})
    else:
            return Response({'status' : 0 , 'msg' : "Email Or Phone Number Is Not Valid"})

# @api_view(["POST"])
# def ForgotOtpSendPassanger(request):
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
def ForgotSetNewPasswordPassenger(request,dk,pk):
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

@api_view(['PUT'])
def UpdatePassenger(request,pk):
    try:
        getpas = user_all.objects.get(id=pk,as_user = 'Passenger')
        # if request.data:
        data = request.data
        # showtime = strftime("%Y-%m-%d %H:%M:%S", )
        showtime = data['datetime']
        getpas.name = data['username'] if data['username'] else getpas.name
        try:
            getdr1 = data['pro_image']# if data['pro_image'] else  getdr.pro_image
            ex = getdr1.name
            if ex.endswith('.jpg'):
                getpas.pro_image = getdr1
            elif ex.endswith('.png'):
                getpas.pro_image = getdr1
            elif ex.endswith('.gif'):
                getpas.pro_image = getdr1
            elif ex.endswith('.jpeg'):
                getpas.pro_image = getdr1
            else:
                return Response({"status": 0, "msg" : "File Formate use jpg,jpeg,png"})
        except:
            getpas.pro_image = getpas.pro_image
        email = data['email']
        num = data['contact_no']   
        if(email):
            if(re.search(email_pattern, email)):
                getmail = user_all.objects.filter(email=email,as_user = 'Passenger')
                if len(getmail) > 0:
                    for i in getmail:
                        if getpas.email == i.email:
                            getpas.email =getpas.email
                        elif email == i.email and getpas.email != i.email:
                            return Response({"status" : "0",'msg': "Email Is Already Used"})
                        else:
                            print('Email Not Use')
                            getpas.email = email
                else:
                    getpas.email = email
            else:
                return Response({'status':0,"msg":"Please Enter Valid Email"})
        else:
            getpas.email = email
        
        if(re.search(mobile_pattern, num)):
            print('-------------num--------',num)
            if num[0] == '0' or num[0] == 0:
                num = num
            else:
                num = f"0{num}"
            getnum = user_all.objects.filter(contact_no=num,as_user = 'Passenger')
            if len(getnum) > 0:
                for i in getnum:
                    if getpas.contact_no == i.contact_no:
                        getpas.contact_no =getpas.contact_no
                    elif num == i.contact_no and getpas.contact_no != i.contact_no:
                        return Response({"status" : "0",'msg': "Mobile Num Is Already Used"})
                    else:
                        print('Number Not Use')
                        getpas.contact_no = num
            else:
                getpas.contact_no = num
        else:
            getpas.contact_no = getpas.contact_no
        getpas.gender = data['gender']
        getpas.city = data['city'] if data['city'].capitalize() else data['city']
        getpas.update_at = showtime
        getpas.save()
        name = getpas.name # if getpas.name else getpas.email_or_num
        return Response({"status" : "1",'msg': f"'{name.title()}' Passenger Is Updated","Driver Id" : getpas.id})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['POST'])
def RequestForRide(request,pid,rid):
    try:
        # showtime = strftime("%Y-%m-%d %H:%M:%S", )
        ridegid = Ride.objects.get(id=rid,publish='1')
        data = request.data
        showtime = data['datetime']
        pickUp = data['pickup']
        pickUp_latitude = data['pickUp_latitude']
        pickUp_longitude = data['pickUp_longitude']
        dropout = data['dropout']
        km = data['km']
        dropout_latitude = data['dropout_latitude']
        dropout_longitude = data['dropout_longitude']
        pas = data['passenger']
        par = data['parcel']
        price = data['price']
        note = data['note']
        per_seat_fees = data['per_seats_price']
        if ridegid.ride_type == "C":
            if pas == '' or pas == 0 or pas =='0':
                return Response({"status": 0, "msg" : f"Please Add Passenger"})
                
            if pas and par:
                pas = pas
                par = par
        #         cost = (float(km) * int(pas)) / float(ridegid.per_km)
        #         pasw = ridegid.fees * int(pas)
        #         parw = ridegid.fees * int(par)
        #         muls = pasw + parw
            
            if(not par):
                par = 0
                pas = pas
                # muls = (float(km) * int(pas)) / float(ridegid.per_km)
                    
            if(not pas):
                pas = 0
                par = par
                # if pas == '':
                #     return Response({"status": 0, "msg" : f"Parcel Add"})
        #         else:
        #             muls = ridegid.fees * int(par)
                
        
        if ridegid.ride_type == "T":
            if par == '' or par == 0 or par =='0':
                return Response({"status": 0, "msg" : f"Please Add Parcel"})
            
            if par:
                pas = 0
                par = par
        #         muls = float(ridegid.per_km) * int(par)
            
        pasid = user_all.objects.get(id=pid,as_user = 'Passenger')
        driid = ridegid.getdriver
        getdr = user_all.objects.get(id=driid.id,as_user = 'Driver')
        getbo = Ride_pin.objects.filter(getride=ridegid,passengerid=pasid,status='0',pickUp = pickUp ,dropout = dropout).exclude(status='2').order_by('-id')
        if len(getbo) > 0:
            if getbo[0].ride_type == 'C':
                getbo[0].for_passenger = int(getbo[0].for_passenger) + int(pas)
                getbo[0].fees = int(getbo[0].fees) + int(price)
                getbo[0].for_parcel = int(getbo[0].for_parcel) + int(price)
                getbo[0].request_date = showtime
                getbo[0].add_information = note
                getbo[0].per_seat_fees = per_seat_fees
                getbo[0].save()
                return Response({"status": 1, "msg" : f"Request Send","Request_Book_Id" : getbo[0].id,"Driver_name" : getdr.name.title(),"Driver_token":getdr.ntk,"Passenger_token":pasid.ntk})
            if getbo[0].ride_type == 'T':
                return Response({"status": 0, "msg" : f"Request Already Send"})
        else:      
            createReq = Ride_pin.objects.create(
                pickUp = pickUp ,
                pickUp_latitude = pickUp_latitude ,
                pickUp_longitude = pickUp_longitude ,
                dropout = dropout ,
                dropout_latitude = dropout_latitude ,
                dropout_longitude = dropout_longitude ,
                as_user = 'Passenger_bid',
                getdriver = getdr,
                getride = ridegid,
                add_information = note,
                ride_type = ridegid.ride_type,
                ride_date = ridegid.date,
                ride_time = ridegid.time,
                for_passenger = pas,
                fees = price,
                per_seat_fees = per_seat_fees,
                for_parcel = par,
                car = ridegid.car,
                passengerid = pasid,
                request_date = showtime,
            )
            return Response({"status": 1, "msg" : f"Request Send","Request_Book_Id" : createReq.id,"Driver_name" : getdr.name.title(),"Driver_token":getdr.ntk,"Passenger_token":pasid.ntk})
        # else:
        #     return Response({"status": 0, "msg" : "This Ride Full"})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"}) 

@api_view(['POST'])
def AcceptRequestForTripByPassenger(request,pk):
    try:
        getbooking = Ride_pin.objects.get(id=pk)
        getbok = Ride.objects.get(id=getbooking.getride1.id,publish='1')
        if getbooking.status == '0':
            getbooking.status = "1"
            getbok.car = getbooking.car
            getbok.getdriver = getbooking.getdriver
            getbok.fees = getbooking.fees
            getbok.status = "1"
            getbooking.save()
            getbok.save()
            return Response({'status':1, 'msg': f"Req Accept","Driver_id":getbooking.getdriver.id,"Driver_token":getbooking.getdriver.ntk})
        else:
            return Response({'status':0, 'msg': "Something Wrong"})
    except ObjectDoesNotExist:
        return Response({"status" : "0",'msg': "Wrong Id"})

@api_view(['POST'])
def RejectRequestForTripByPassenger(request,pk):
    try:
        getbooking = Ride_pin.objects.get(id=pk)
        if getbooking.status == '0':
            getbooking.status = '3'
            getbooking.save()
            return Response({'status':1, 'msg': f"Request Rejected","Driver_id":getbooking.getdriver.id,"Driver_token":getbooking.getdriver.ntk})
        else:
            return Response({'status':0,'msg':'Request is Accpeted'})
    except ObjectDoesNotExist:
        return Response({"status" : "0",'msg': "Wrong Id"})

@api_view(['GET'])
def ViewPassengerRide(request,pk):
    try:
        getpas = Ride.objects.get(id=pk,publish='1')
        print(getpas)
        getreq = Ride_pin.objects.filter(getride=getpas.id,status='0',as_user='Driver_bid')
        print(getreq)
        sr = BookingpinSerializer(getreq,many=True)
        return Response({'status': 1, 'msg': 'success',
                        'data' : sr.data})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})        

@api_view(['GET'])
def PassengerProfile(request,pk):
    try:
        pas = user_all.objects.get(id=pk,as_user = 'Passenger')
        rat = Passenger_Rating.objects.filter(mine=pk)
        ls = []
        for i in rat:
            ls.append(int(i.rates))
        if ls == []:
            average = 0.0
        else:
            average = Average(ls) 
        if pas.gender == '0':
            gender = ''
        else:
            gender = pas.gender
        serializer = {
            'status' : 1,
            'msg' : "success",
            "username" : pas.name.title(),
            "email" : pas.email,
            "pro_image" : pas.pro_image.url,
            "contact_no" : pas.contact_no,
            "gender" : gender,
            "dob" : pas.dob,
            "city" : pas.city,
            "review" : average,
            "bio" : pas.bio,
        }
        return Response(serializer)
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['POST'])
def SearchForRide(request,dd):
    data = request.data
    num = 9999999999999
    pickup1 = data["pickUp"].casefold().replace(" ", "")
    dropout1 = data["dropout"].casefold().replace(" ", "")
    date = data["date"]
    fullbook = data["fullbook"]
    current_date = data["current_date"]
    space_seat = data["space_seat"]
    current_location = data["current_location"]

    # For All Get
    if pickup1 and dropout1 and date and (not fullbook) and (not current_date) and space_seat and (not current_location):
        filter = "Yes"
        if dd == 'T' or dd == 't':
            pps = Ride.objects.filter(date=date,publish='1',trip_status='P',Max_parcel__range = [int(space_seat),num],as_user = 'Driver',fullbooked='0').exclude(status='3')
        else:
            pps = Ride.objects.filter(date=date,publish='1',trip_status='P',Max_seats__range = [int(space_seat),num],as_user = 'Driver',fullbooked='0').exclude(status='3')
        ls = []
        for i in pps:
            va1 = i.route
            st = ""
            route = []
            for ps in va1:
                if ps == '[' or ps == "'":
                    pass
                else:
                    st = st + f"{ps.replace(',','').replace(']','')}"
                    if ps == ',':
                        route.append(st.replace(' ',''))
                        st = ''
                    if ps == ']':
                        route.append(st.replace(' ',''))

            if (pickup1 in route) and (dropout1 in route):
                gpi = i.id
                pi = route.index(pickup1)
                dr = route.index(dropout1)
                if pi < dr:
                    ls.append(gpi)
        pp = Ride.objects.filter(id__in=ls).exclude(status='3')
        
    if pickup1 and dropout1 and date and (not fullbook) and (not current_date) and (not space_seat) and (not current_location):
        filter = "Yes"
        pps = Ride.objects.filter(date=date,publish='1',trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
        ls = []
        for i in pps:
            va1 = i.route
            st = ""
            route = []
            for ps in va1:
                if ps == '[' or ps == "'":
                    pass
                else:
                    st = st + f"{ps.replace(',','').replace(']','')}"
                    if ps == ',':
                        route.append(st.replace(' ',''))
                        st = ''
                    if ps == ']':
                        route.append(st.replace(' ',''))

            if (pickup1 in route) and (dropout1 in route):
                gpi = i.id
                pi = route.index(pickup1)
                dr = route.index(dropout1)
                if pi < dr:
                    ls.append(gpi)
        pp = Ride.objects.filter(id__in=ls).exclude(status='3')

    # Pick And Drop
    if pickup1 and dropout1 and (not date) and (not fullbook) and (not current_date) and (not space_seat) and (not current_location):
        filter = "Yes"
        pps = Ride.objects.filter(publish='1',trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
        ls = []
        for i in pps:
            va1 = i.route
            st = ""
            route = []
            for ps in va1:
                if ps == '[' or ps == "'":
                    pass
                else:
                    st = st + f"{ps.replace(',','').replace(']','')}"
                    if ps == ',':
                        route.append(st.replace(' ',''))
                        st = ''
                    if ps == ']':
                        route.append(st.replace(' ',''))

            if (pickup1 in route) and (dropout1 in route):
                gpi = i.id
                pi = route.index(pickup1)
                dr = route.index(dropout1)
                if pi < dr:
                    ls.append(gpi)
        pp = Ride.objects.filter(id__in=ls).exclude(status='3')
        
    if pickup1 and dropout1 and (not date) and (not fullbook) and (not current_date) and space_seat and (not current_location):
        filter = "Yes"
        if dd == "t" or dd == "T":
            pps = Ride.objects.filter(publish='1',Max_parcel__range = [int(space_seat),num],trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
        else:
            pps = Ride.objects.filter(publish='1',Max_seats__range = [int(space_seat),num],trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
        ls = []
        for i in pps:
            va1 = i.route
            st = ""
            route = []
            for ps in va1:
                if ps == '[' or ps == "'":
                    pass
                else:
                    st = st + f"{ps.replace(',','').replace(']','')}"
                    if ps == ',':
                        route.append(st.replace(' ',''))
                        st = ''
                    if ps == ']':
                        route.append(st.replace(' ',''))

            if (pickup1 in route) and (dropout1 in route):
                gpi = i.id
                pi = route.index(pickup1)
                dr = route.index(dropout1)
                if pi < dr:
                    ls.append(gpi)
        pp = Ride.objects.filter(id__in=ls).exclude(status='3')
        
    # Only PickUp
    if pickup1 and (not dropout1) and (not date) and (not fullbook) and (not current_date) and (not space_seat) and (not current_location):
        filter = "Yes1"
        pps = Ride.objects.filter(publish='1',trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
        ls = []
        for i in pps:
            va1 = i.route
            st = ""
            route = []
            for ps in va1:
                if ps == '[' or ps == "'":
                    pass
                else:
                    st = st + f"{ps.replace(',','').replace(']','')}"
                    if ps == ',':
                        route.append(st.replace(' ',''))
                        st = ''
                    if ps == ']':
                        route.append(st.replace(' ',''))
            print('---------------------------------',route)
            if (pickup1 in route):
                gpi = i.id
                pi = route.index(pickup1)
                if pi == (len(route)-1):
                    pass
                else:
                    ls.append(gpi)
                    
        pp = Ride.objects.filter(id__in=ls).exclude(status='3')  
        
    if pickup1 and (not dropout1) and (not date) and (not fullbook) and (not current_date) and space_seat and (not current_location):
        filter = "Yes"
        if dd == 'T' or dd == "t":
            pps = Ride.objects.filter(publish='1',trip_status='P',as_user = 'Driver',fullbooked='0',Max_parcel__range = [int(space_seat),num]).exclude(status='3')
        else:
            pps = Ride.objects.filter(publish='1',trip_status='P',as_user = 'Driver',fullbooked='0',Max_seats__range = [int(space_seat),num]).exclude(status='3')
        ls = []
        for i in pps:
            va1 = i.route
            st = ""
            route = []
            for ps in va1:
                if ps == '[' or ps == "'":
                    pass
                else:
                    st = st + f"{ps.replace(',','').replace(']','')}"
                    if ps == ',':
                        route.append(st.replace(' ',''))
                        st = ''
                    if ps == ']':
                        route.append(st.replace(' ',''))

            if (pickup1 in route):
                gpi = i.id
                pi = route.index(pickup1)
                if pi == (len(route)-1):
                    pass
                else:
                    ls.append(gpi)
                    
        pp = Ride.objects.filter(id__in=ls).exclude(status='3')  

    # PickUp With Date
    if pickup1 and (not dropout1) and date and (not fullbook) and (not current_date) and (not space_seat) and (not current_location):
        filter = "Yes"
        pps = Ride.objects.filter(date=date,publish='1',trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
        ls = []
        for i in pps:
            va1 = i.route
            st = ""
            route = []
            for ps in va1:
                if ps == '[' or ps == "'":
                    pass
                else:
                    st = st + f"{ps.replace(',','').replace(']','')}"
                    if ps == ',':
                        route.append(st.replace(' ',''))
                        st = ''
                    if ps == ']':
                        route.append(st.replace(' ',''))

            if (pickup1 in route):
                gpi = i.id
                pi = route.index(pickup1)
                if pi == (len(route)-1):
                    pass
                else:
                    ls.append(gpi)
                    
        pp = Ride.objects.filter(id__in=ls).exclude(status='3')
    
    if pickup1 and (not dropout1) and date and (not fullbook) and (not current_date) and space_seat and (not current_location):
        filter = "Yes"
        if dd == "T" or dd == "t":
            pps = Ride.objects.filter(Max_parcel__range = [int(space_seat),num],date=date,publish='1',trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
        else:
            pps = Ride.objects.filter(Max_seats__range = [int(space_seat),num],date=date,publish='1',trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
        ls = []
        for i in pps:
            va1 = i.route
            st = ""
            route = []
            for ps in va1:
                if ps == '[' or ps == "'":
                    pass
                else:
                    st = st + f"{ps.replace(',','').replace(']','')}"
                    if ps == ',':
                        route.append(st.replace(' ',''))
                        st = ''
                    if ps == ']':
                        route.append(st.replace(' ',''))

            if (pickup1 in route):
                gpi = i.id
                pi = route.index(pickup1)
                if pi == (len(route)-1):
                    pass
                else:
                    ls.append(gpi)
                    
        pp = Ride.objects.filter(id__in=ls).exclude(status='3')

    # Only Drop
    if (not pickup1) and dropout1 and (not date) and (not fullbook) and (not current_date) and (not space_seat) and (not current_location):
        filter = "Yes"
        pps = Ride.objects.filter(publish='1',trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
        ls = []
        for i in pps:
            va1 = i.route
            st = ""
            route = []
            for ps in va1:
                if ps == '[' or ps == "'":
                    pass
                else:
                    st = st + f"{ps.replace(',','').replace(']','')}"
                    if ps == ',':
                        route.append(st.replace(' ',''))
                        st = ''
                    if ps == ']':
                        route.append(st.replace(' ',''))

            if (dropout1 in route):
                gpi = i.id
                pi = route.index(dropout1)
                if pi == 0:
                    pass
                else:
                    ls.append(gpi)
                    
        pp = Ride.objects.filter(id__in=ls).exclude(status='3')
        
    if (not pickup1) and dropout1 and (not date) and (not fullbook) and (not current_date) and space_seat and (not current_location):
        filter = "Yes"
        if dd == "T" or dd == "t":
            pps = Ride.objects.filter(Max_parcel__range = [int(space_seat),num],publish='1',trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
        else:
            pps = Ride.objects.filter(Max_seats__range = [int(space_seat),num],publish='1',trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
        ls = []
        for i in pps:
            va1 = i.route
            st = ""
            route = []
            for ps in va1:
                if ps == '[' or ps == "'":
                    pass
                else:
                    st = st + f"{ps.replace(',','').replace(']','')}"
                    if ps == ',':
                        route.append(st.replace(' ',''))
                        st = ''
                    if ps == ']':
                        route.append(st.replace(' ',''))

            if (dropout1 in route):
                gpi = i.id
                pi = route.index(dropout1)
                if pi == 0:
                    pass
                else:
                    ls.append(gpi)
                    
        pp = Ride.objects.filter(id__in=ls).exclude(status='3')

    # Drop With Date
    if (not pickup1) and dropout1 and date and (not fullbook) and (not current_date) and space_seat and (not current_location):
        filter = "Yes"
        if dd == "T" or dd =="t":
            pps = Ride.objects.filter(Max_parcel__range = [int(space_seat),num],date=date,publish='1',trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
        else:
            pps = Ride.objects.filter(Max_seats__range = [int(space_seat),num],date=date,publish='1',trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
        ls = []
        for i in pps:
            va1 = i.route
            st = ""
            route = []
            for ps in va1:
                if ps == '[' or ps == "'":
                    pass
                else:
                    st = st + f"{ps.replace(',','').replace(']','')}"
                    if ps == ',':
                        route.append(st.replace(' ',''))
                        st = ''
                    if ps == ']':
                        route.append(st.replace(' ',''))

            if (dropout1 in route):
                gpi = i.id
                pi = route.index(dropout1)
                if pi == 0:
                    pass
                else:
                    ls.append(gpi)
                    
        pp = Ride.objects.filter(id__in=ls).exclude(status='3')     
    
    if (not pickup1) and dropout1 and date and (not fullbook) and (not current_date) and (not space_seat) and (not current_location):
        filter = "Yes"
        pps = Ride.objects.filter(date=date,publish='1',trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
        ls = []
        for i in pps:
            va1 = i.route
            st = ""
            route = []
            for ps in va1:
                if ps == '[' or ps == "'":
                    pass
                else:
                    st = st + f"{ps.replace(',','').replace(']','')}"
                    if ps == ',':
                        route.append(st.replace(' ',''))
                        st = ''
                    if ps == ']':
                        route.append(st.replace(' ',''))

            if (dropout1 in route):
                gpi = i.id
                pi = route.index(dropout1)
                if pi == 0:
                    pass
                else:
                    ls.append(gpi)
                    
        pp = Ride.objects.filter(id__in=ls).exclude(status='3')     

    # Only Date
    if (not pickup1) and (not dropout1) and date and (not fullbook) and (not current_date) and space_seat and (not current_location):
        filter = "Yes"
        if dd == "T" or dd == "t":
            pp = Ride.objects.filter(Max_parcel__range = [int(space_seat),num],date=date,publish='1',trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
        else:
            pp = Ride.objects.filter(Max_seats__range = [int(space_seat),num],date=date,publish='1',trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')
    
    if (not pickup1) and (not dropout1) and date and (not fullbook) and (not current_date) and (not space_seat) and (not current_location):
        filter = "Yes"
        pp = Ride.objects.filter(date=date,publish='1',trip_status='P',as_user = 'Driver',fullbooked='0').exclude(status='3')

    # Full booked Only
    if (not pickup1) and (not dropout1) and (not date) and fullbook and current_date and (not current_location):
        filter = "Yes"
        pp = Ride.objects.filter(publish='1',trip_status='P',as_user = 'Driver',fullbooked='2',current_date=current_date).exclude(status='3')
        
    if (not pickup1) and (not dropout1) and (not date) and fullbook and current_date and current_location:
        filter = "Yes"
        pp = Ride.objects.filter(publish='1',current_location = current_location,trip_status='P',as_user = 'Driver',fullbooked='2',current_date=current_date).exclude(status='3')
        
    # For Not Data
    if (not pickup1) and (not dropout1) and (not date) and (not fullbook) and (not current_date) and (not space_seat) and (not current_location):
        pp = Ride.objects.filter(publish='1',trip_status='P',as_user = 'Driver').exclude(status='3')
        filter = "No"
        
    if (not pickup1) and (not dropout1) and (not date) and (not fullbook) and (not current_date) and space_seat and (not current_location):
        filter = "Yes"
        if dd == "T" or dd == "t":
            pp = Ride.objects.filter(Max_parcel__range = [int(space_seat),num],publish='1',trip_status='P',as_user = 'Driver').exclude(status='3')
        else:
            pp = Ride.objects.filter(Max_seats__range = [int(space_seat),num],publish='1',trip_status='P',as_user = 'Driver').exclude(status='3')
    
    if (not current_date) and fullbook:
        return Response({"status":0,"msg":"Date is Required.!"})
        
    if len(pp) > 0:
        ls = []
        for instance in pp:
            current_date =datetime.datetime.now()
            representation = {}
            if str(instance.date) >= current_date.strftime('%Y-%m-%d'):
            #     representation["ridecheck"] = f"Presenr Future {instance.date}"
                representation["ride_id"] = instance.id
                rea = Drivers_Rating.objects.filter(mine=instance.getdriver.id)
                lis = []
                for i in rea:
                    lis.append(float(i.rates))
                if lis == []:
                    average = 0.0
                else:
                    average = Average(lis)
                if instance.fullbooked == "0":
                    if instance.ride_type == dd.upper():
                        representation["driver_Rating"] = average
                        representation["driver_id"] = instance.getdriver.id
                        representation["driver"] = instance.getdriver.name.title()
                        representation["drivers_number"] = instance.getdriver.contact_no if instance.getdriver.contact_no else ''
                        representation["driver_token"] = instance.getdriver.ntk
                        representation["filter"] = filter
                        if instance.getdriver.pro_image:
                            representation["pro_image"] = instance.getdriver.pro_image.url
                        else:
                            representation["pro_image"] = ""
                        representation["pickUp"] = instance.pickUp.capitalize()
                        representation["dropout"] = instance.dropout.capitalize()
                        representation["time"] = instance.time
                        representation["dtime"] = instance.dtime
                        representation["map_time"] = instance.map_date
                        representation["date"] = instance.date.strftime("%d-%m-%Y")
                        representation["FullBooked"] = instance.fullbooked
                        representation["current_location"] = instance.current_location
                        representation["current_date"] = instance.current_date#.strftime("%d-%m-%Y")
                        representation["vehicle_type"] = instance.ride_type
                        if instance.car:
                            representation["Car_name"] = f"{instance.car.vehical_variant.brand.brand} {instance.car.vehical_variant.cars}"
                            representation["car_color"] = instance.car.vehicle_color
                            # representation["many_car_list"] = ""
                        else:
                            representation["Car_name"] = ""
                            representation["car_color"] = ""
                            # representation["many_car_list"] = ""
                        if dd == 'T' or dd == 't':
                            representation["fees"] = f"{instance.per_km}"
                        else:
                            representation["fees"] = f"{instance.fees}"
                            
                        representation["capacity"] = f"{instance.Max_parcel}"
                        representation["Available_space"] = f"{instance.capacity}"
                        representation["seats"] = f"{instance.Max_seats}"
                        representation["Available_seats"] = f"{instance.Max_seats}"
                            
                        representation["add_information"] = instance.add_information.title()
                        ls.append(representation)
                else:
                    if instance.ride_type == dd.upper() or (dd.upper() == "C" and (instance.ride_type == "A" or instance.ride_type == "B" or instance.ride_type == "C")):
                        representation["driver_Rating"] = average
                        representation["driver_id"] = instance.getdriver.id
                        representation["driver"] = instance.getdriver.name.title()
                        representation["drivers_number"] = instance.getdriver.contact_no if instance.getdriver.contact_no else ''
                        representation["driver_token"] = instance.getdriver.ntk
                        representation["filter"] = filter
                        representation["vehicle_type"] = instance.ride_type
                        if instance.car:
                            representation["Car_name"] = f"{instance.car.vehical_variant.brand.brand} {instance.car.vehical_variant.cars}"
                            representation["car_color"] = instance.car.vehicle_color
                            # representation["many_car_list"] = ""
                        else:
                            representation["Car_name"] = ""
                            representation["car_color"] = ""
                            # if instance.ride_type == "M":
                            #     Vehicles = instance.manycar.all() #filter(id=instance.id)
                            #     Car_list = []
                            #     for i in Vehicles:
                            #         Car_dict = {}
                            #         if i.vehicle_type == "A":
                            #             vehicle_type = "Auto"
                            #         if i.vehicle_type == "B":
                            #             vehicle_type = "Bike"
                            #         if i.vehicle_type == "C":
                            #             vehicle_type = "Car"
                            #         if i.vehicle_type == "T":
                            #             vehicle_type = "Truck"
                            #         Car_dict['Car_name'] = f"{i.vehical_variant.brand.brand} {i.vehical_variant.cars}"
                            #         Car_dict['car_color'] = i.vehicle_color
                            #         Car_dict['car_type'] = vehicle_type
                            #         Car_list.append(Car_dict)
                            #         # Car_name_list.append(f"{i.vehical_variant.brand.brand} {i.vehical_variant.cars} {vehicle_type}")
                            #         # car_color_list.append(i.vehicle_color)
                            #     representation["many_car_list"] = Car_list
                            # else:
                            #     representation["many_car_list"] = ""
                        if instance.getdriver.pro_image:
                            representation["pro_image"] = instance.getdriver.pro_image.url
                        else:
                            representation["pro_image"] = ""
                        representation["capacity"] = instance.capacity
                        representation["FullBooked"] = instance.fullbooked
                        representation["current_location"] = instance.current_location
                        representation["current_date"] = instance.current_date.strftime("%d-%m-%Y")
                        ls.append(representation)
            # else:
            #     representation["ridecheck"] = f"Past {instance.date}"
        return Response({'status':1 ,"msg":"Success", 'data':ls})    
    else:
        return Response({'status':0 ,"msg":"No Ride Founded"})     

@api_view(['GET'])
def FilterRideType(request,pk):
    try:
        pp = Ride.objects.filter(ride_type=pk,status='0',publish='1').exclude(status='3')
        if len(pp) > 0:
            serial = Filterserializer(pp,many=True)
            return Response({"status": 1,"msg": "success","data": serial.data})
        else:
            return Response({'status':0 ,"msg":"Record Not Founded"})
    except ObjectDoesNotExist:
        return Response({'status':0 ,"msg":"Wrong Id"})

@api_view(['GET'])
def ViewRideDetails(request,pk,pp):
    try:
        pa = user_all.objects.get(id=pp,as_user = 'Passenger')
        getr = Ride.objects.get(id=pk,publish__range=['1','3'])
        if getr.status == '0' or getr.status == '1' or getr.status == '3' :
            myride = Ride_pin.objects.filter(getride=pk,status__range=['0','1'],passengerid=pp)
            if len(myride) > 0 :
                myride = "Yes"
            else:
                myride = "No"
            getq = Ride_pin.objects.filter(getride=pk,status='1').exclude(passengerid=pp)
            sera = RidepinSerializer(getq,many=True)
            if getr.ride_type == 'C':
                return Response({'status':1, 'msg':"Success","ride_booked":myride,"ride_type" : getr.ride_type,"time" : getr.time,"dtime" : getr.dtime,"map_time" : getr.map_date,"driver_id": getr.getdriver.id,"driver": getr.getdriver.name.title(),"Profile": getr.getdriver.pro_image.url,"car_name": f"{getr.car.vehical_variant.brand.brand} {getr.car.vehical_variant.cars}","car_color": getr.car.vehicle_color,"pickUp": getr.pickUp,"pick_lat":getr.pickUp_latitude,"pick_long":getr.pickUp_longitude,"drop_lat":getr.dropout_latitude,"drop_long":getr.dropout_longitude,"dropout": getr.dropout,"Available_seats": getr.seats,"seats": f"{getr.Max_seats}","Available_space": getr.capacity,"capacity": f"{getr.Max_parcel}","date": getr.date.strftime('%d-%m-%Y'),"adda" : getr.status,"fees": f"{getr.fees}","add_information": getr.add_information.title(),'data' : sera.data})
            if getr.ride_type == 'T':
                return Response({'status':1, 'msg':"Success","ride_booked":myride,"ride_type" : getr.ride_type,"time" : getr.time,"dtime" : getr.dtime,"map_time" : getr.map_date,"driver_id": getr.getdriver.id,"driver": getr.getdriver.name.title(),"Profile": getr.getdriver.pro_image.url,"pickUp": getr.pickUp,"pick_lat":getr.pickUp_latitude,"pick_long":getr.pickUp_longitude,"drop_lat":getr.dropout_latitude,"drop_long":getr.dropout_longitude,"dropout": getr.dropout,"Available_seats": getr.seats,"seats": f"{getr.Max_seats}","Available_space": getr.capacity,"capacity": f"{getr.Max_parcel}","date": getr.date.strftime('%d-%m-%Y'),"adda" : getr.status,"fees": f"{getr.per_km}","add_information": getr.add_information.title(),'data' : sera.data})
        else:
            return Response({'status' : 0,'msg':'No Ride'})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['POST'])
def PassengerChangePassword(request,dk,pk):
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

from datetime import datetime, timedelta   
import datetime

def convert(date_time):
    format = '%I:%M %p' # The format
    datetime_str = datetime.datetime.strptime(date_time, format)
    realtime = datetime_str.strftime('%H:%M')
    return realtime 

@api_view(['POST'])
def PassengerAddBooking(request,pk):
    try:
        data = request.data
        pickUp = data["pickUp"].casefold()
        dropout = data["dropout"].casefold()
        pickUp_lat = data["pickUp_lat"]
        dropout_lat = data["dropout_lat"]
        pickUp_lan = data["pickUp_lan"]
        dropout_lan = data["dropout_lan"]
        date = data["date"]
        time = data["time"].upper()
        add_information = data["note"]
        passenger = data["passenger"]
        parcel = data["parcel"]
        fees = data["fees"]
        pickup_address1 = data['pickup_address1']
        pickup_address2 = data['pickup_address2']
        dropout_address1 = data['dropout_address1']
        dropout_address2 = data['dropout_address2']
        showtime = data['datetime']
        getpas = user_all.objects.get(id=pk,as_user = 'Passenger')
        
        if(not pickUp):
            return Response({'status':0,'msg': 'PickUp Is Not Added..'})
        if(not dropout):
            return Response({'status':0,'msg': 'Dropout Is Not Added..'})
        if(not date):
            return Response({'status':0,'msg': 'Please Select Date For Ride'})
        if(not passenger):
            return Response({'status':0,'msg': 'Please Add Seats'})
        if (not parcel):
            return Response({'status':0,'msg': 'Please Add Parcel'})
            
        if (not parcel):
            parcel = '0'
        if (not passenger):
            passenger = '0'
            
        if parcel != '0' and passenger != '0':
            typ = 'C'
        elif passenger != '0':
            typ = 'C'
        elif parcel != '0':
            typ = 'T'  
        else:
            typ = 'C'  
        fees = None
        publish = "0"
            
        addbookings = Ride.objects.filter(
            as_user = 'Passenger',
            getpassenger = getpas,
            ride_type = typ,
            pickUp = pickUp,
            dropout = dropout,
            date = date,
            publish = '0'
        ).exclude(status='3')
        
        ride_time = f"{str(date)} {str(convert(time))}"
        if len(addbookings) > 0:
            addbookings[0].ride_time = ride_time
            addbookings[0].capacity = parcel
            addbookings[0].seats = passenger
            addbookings[0].fees = fees
            addbookings[0].pickUp_latitude = pickUp_lat
            addbookings[0].pickUp_longitude = pickUp_lan
            addbookings[0].car_latitude = pickUp_lat
            addbookings[0].car_longitude = pickUp_lan
            addbookings[0].dropout_latitude = dropout_lat
            addbookings[0].dropout_longitude = dropout_lan
            addbookings[0].pickup_address1 = pickup_address1
            addbookings[0].pickup_address2 = pickup_address2
            addbookings[0].dropout_address1 = dropout_address1
            addbookings[0].dropout_address2 = dropout_address2
            addbookings[0].add_information = add_information
            addbookings[0].create_at = showtime
            addbookings[0].time = time
            addbookings[0].update_at = showtime
            addbookings[0].save()
            
            adds = Ride.objects.filter(as_user="Driver",pickUp = pickUp,dropout = dropout,date = date,trip_status="P",ride_type = typ).exclude(status='3')

            for h in adds:
                lista = firebase_notifications.objects.filter(userid = h.getdriver,rideid = h)
                if len(lista) > 0:
                    lista[0].create_at = showtime
                    lista[0].notification_text = f"{getpas.name.title()} has requested a ride from {pickUp.capitalize()} to {dropout.capitalize()}"
                    lista[0].save()
                else:
                    notif = firebase_notifications.objects.create(
                        userid = h.getdriver,
                        rideid = h,
                        cancel_by = getpas.name.title(),
                        notification_text = f"{getpas.name.title()} has requested a ride from {pickUp.capitalize()} to {dropout.capitalize()}",
                        create_at = showtime,
                    )
                send_notification([h.getdriver.ntk] , 'New RIDE Request' , f"{getpas.name.title()} has requested a ride from {pickUp.capitalize()} to {dropout.capitalize()}")
                
            return Response({
                    "Booking_Id" : addbookings[0].id,
                    "status":1,
                    "msg":"Booking Added Successfully"
                    })
        else:
            addbooking = Ride.objects.create(
                as_user = 'Passenger',
                getpassenger = getpas,
                capacity = parcel,
                seats = passenger,
                ride_type = typ,
                publish = publish,
                pickUp_latitude = pickUp_lat,
                pickUp_longitude = pickUp_lan,
                car_latitude = pickUp_lat,
                car_longitude = pickUp_lan,
                dropout_latitude = dropout_lat,
                dropout_longitude = dropout_lan,
                pickup_address1 = pickup_address1,
                pickup_address2 = pickup_address2,
                dropout_address1 = dropout_address1,
                dropout_address2 = dropout_address2,
                pickUp = pickUp,
                dropout = dropout,
                date = date,
                fees = fees,
                add_information = add_information,
                ride_time = ride_time,
                time = time,
                create_at = showtime,
                update_at = showtime
            )
            
            adds = Ride.objects.filter(as_user="Driver",pickUp = pickUp,dropout = dropout,date = date,trip_status="P",ride_type = typ).exclude(status='3')
            if len(adds)>0:
                for h in adds:
                    lista = firebase_notifications.objects.filter(userid = h.getdriver,rideid = h)
                    if len(lista) > 0:
                        lista[0].create_at = showtime
                        lista[0].notification_text = f"{getpas.name.title()} has requested a ride from {pickUp.capitalize()} to {dropout.capitalize()}"
                        lista[0].save()
                    else:
                        notif = firebase_notifications.objects.create(
                            userid = h.getdriver,
                            rideid = h,
                            cancel_by = getpas.name.title(),
                            notification_text = f"{getpas.name.title()} has requested a ride from {pickUp.capitalize()} to {dropout.capitalize()}",
                            create_at = showtime,
                        )
                    send_notification([h.getdriver.ntk] , 'New RIDE Request' , f"{getpas.name.title()} has requested a ride from {pickUp.capitalize()} to {dropout.capitalize()}")

            return Response({
                    "Booking_Id" : addbooking.id,
                    "status":1,
                    "msg":"Booking Added Successfully"
                    })
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['POST'])
def BookingPublishedStop(request,pk):
    try:
        rde = Ride.objects.get(id=pk,publish='1',as_user='Passenger')
        bookingpin = Ride_pin.objects.filter(getride=pk)
        if rde.trip_status == 'P':
            for i in bookingpin:
                if i.status == '1':
                    i.staus = '3'
                i.status = '3'
                i.save()
            rde.trip_status2 = '4'
            rde.status = '3'
            rde.save()
            return Response({"status" : 1,'msg': "Ride Request stop"})
        else:
            return Response({"status" : 0,'msg': "Ride Is Not Stop"})
    except ObjectDoesNotExist:
        return Response({"status" : 0,'msg': "Ride Request Not found"})

@api_view(['GET'])
def PassengerRideList(request,pk,tt):
    try:
        getpas = user_all.objects.get(id=pk,as_user = 'Passenger')
        bb = Ride.objects.filter(getpassenger=pk,publish='1',ride_type=tt).exclude(status__range=['1','3']).order_by('-trip_status2')
        lis = []
        for i in bb:
            if i.status == '0' or i.status == '1':
                bb2 = Ride_pin.objects.filter(getride1=i.id,status='1')
                representation = {}
                representation["id"] = i.id
                representation["Passanger_Id"] = i.getpassenger.id
                representation["Passenger_name"] = i.getpassenger.name.title()
                representation["pickUp"] = i.pickUp.capitalize()
                representation["dropout"] = i.dropout.capitalize()
                representation["date"] = i.date.strftime('%d-%m-%Y')
                representation["time"] = i.time
                representation["dtime"] = i.dtime
                representation["map_time"] = i.map_date
                representation["ride_status"] = i.status
                representation["trip_pas_status"] = i.trip_status
                if i.status == '1':
                    for bb2 in bb2:
                        representation["Driver_name"] = bb2.getdriver.name.title()
                        representation["Driver_Image"] = bb2.getdriver.pro_image.url
                        representation["offer_price"] = bb2.offer_price
                        # if bb2.pas_status == "W":
                        #     representation["trip_pas_status"] = "P"
                        # else:
                        #     representation["trip_pas_status"] = bb2.pas_status
                representation["Passengers"] = i.seats
                representation["Parcels"] = i.capacity
                lis.append(representation)
                
        return Response({"status": 1,"msg": "success","data": lis})
    except ObjectDoesNotExist:
        return Response({'status':0 ,"msg":"Wrong Id"})

@api_view(['GET'])
def PassengerBookingLists(request,pk,tt):
    try:
        bts = Ride.objects.filter(getpassenger=pk,publish='1',ride_type=tt,status="1").order_by('-trip_status2')
        bb = Ride_pin.objects.filter(passengerid=pk,ride_type=tt).order_by('-pas_status')
        # bb = Ride_pin.objects.filter(passengerid=pk,ride_type=tt).order_by('-pas_status')
        lis = []
        # for instance1 in bts:
        #     representations1 = {}
        #     representations1['ride_id'] = instance1.id
        #     representations1['booking_id'] = 0
        #     representations1['ride_status'] = instance1.status
        #     representations1['Driver_id'] = instance1.getdriver.id
        #     rea = Drivers_Rating.objects.filter(mine=instance1.getdriver.id)
        #     ls = []
        #     for i in rea:
        #         ls.append(int(i.rates))
        #     if ls == []:
        #         representations1['Driver_Rating'] = 0.0
        #     else:
        #         representations1['Driver_Rating'] = Average(ls)
        #     representations1['Driver'] = instance1.getdriver.name.title() if instance1.getdriver.name.title() else instance1.getdriver.email_or_num
        #     representations1['ride_type'] = instance1.ride_type
        #     representations1['trip_pas_status'] = instance1.trip_status
        #     representations1['fees'] = f"{instance1.fees}"
        #     representations1['for_passenger'] = instance1.seats
        #     representations1['for_parcel'] = instance1.capacity
        #     representations1['request_date'] = f"{instance1.date.strftime('%d-%m-%Y')}"
        #     representations1['ride_time'] = instance1.time
        #     representations1['ride_dtime'] = instance1.dtime
        #     representations1['Location'] = instance1.pickUp.capitalize()
        #     representations1['Destination'] = instance1.dropout.capitalize()
        #     lis.append(representations1)
            
        for instance in bb:
            representations = {}
            representations['ride_id'] = instance.id
            representations['booking_id'] = instance.getride.id
            representations['Driver_id'] = instance.getdriver.id
            representations['Driver_token'] = instance.getdriver.ntk
            rea = Drivers_Rating.objects.filter(mine=instance.getdriver.id)
            rid = Drivers_Rating.objects.filter(tri=instance.getride.id,mine=instance.getdriver.id,passengerid=pk)
            repo = Driver_Report.objects.filter(tri=instance.getride.id,mine=instance.getdriver.id,passengerid=pk)
            if len(rid) > 0 or len(repo) > 0:
                representations['rat_report'] = "Yes"
            else:
                representations['rat_report'] = "No"
                
            ls = []
            for i in rea:
                ls.append(int(i.rates))
            if ls == []:
                representations['Driver_Rating'] = 0.0
            else:
                representations['Driver_Rating'] = Average(ls)
            representations['Driver'] = instance.getdriver.name.title() if instance.getdriver.name.title() else instance.getdriver.email_or_num
            representations['ride_type'] = instance.ride_type
            if instance.pas_status == 'W':
                representations['trip_pas_status'] = "P"
            else:
                representations['trip_pas_status'] = instance.pas_status
            representations['fees'] = f"{instance.fees}"
            representations['for_passenger'] = instance.for_passenger
            representations['for_parcel'] = instance.for_parcel
            representations['request_date'] = f"{instance.ride_date.strftime('%d-%m-%Y')}"
            representations['ride_time'] = instance.getride.time
            representations['ride_status'] = instance.status
            # if instance.status == '2':
            #     representations['ride_status'] = "Reject"
            # elif instance.status == '1':
            #     representations['ride_status'] = "Accept"
            # elif instance.status == '3':
            #     representations['ride_status'] = "Cancel"
            # else:
            #     representations['ride_status'] = "Pending"
                
            representations['ride_dtime'] = instance.getride.dtime
            representations['Location'] = instance.pickUp.capitalize()
            representations['Destination'] = instance.dropout.capitalize()
            if (instance.status == '0' and instance.as_user == "Passenger_bid") or (instance.status == "1"):
                lis.append(representations)
        serial = GetRidepinSerializer(bb,many=True)
        return Response({"status": 1,"msg": "success","data": lis})
    except ObjectDoesNotExist:
        return Response({'status':0 ,"msg":"Wrong Id"})
    
# @api_view(['GET'])
# def PassengerBookingList(request,pk):
#     try:
#         bb = Ride_pin.objects.filter(passengerid=pk,ride_type="C",status__range=['0','1']).order_by('-pas_status')
#         serial = GetRidepinSerializer(bb,many=True)
#         return Response({"status": 1,"msg": "success","data": serial.data})
#     except ObjectDoesNotExist:
#         return Response({'status':0 ,"msg":"Wrong Id"})
    
# @api_view(['GET'])
# def PassengerBookingListByT(request,pk):
#     try:
#         bb = Ride_pin.objects.filter(passengerid=pk,ride_type="T",status__range=['0','1']).order_by('-pas_status')
#         serial = GetRidepinSerializer(bb,many=True)
#         return Response({"status": 1,"msg": "success","data": serial.data})
#     except ObjectDoesNotExist:
#         return Response({'status':0 ,"msg":"Wrong Id"})

@api_view(['GET'])
def OwnBookingFilterDetails(request,pk,pp):
    try:
        pa = user_all.objects.get(id=pp,as_user = 'Passenger')
        getq = Ride_pin.objects.get(id=pk)
        rid = Drivers_Rating.objects.filter(tri=getq.getride,mine=getq.getride.getdriver,passengerid=pp)
        repo = Driver_Report.objects.filter(tri=getq.getride,mine=getq.getride.getdriver,passengerid=pp)
        if len(rid) > 0 or len(repo) > 0:
            rid = 'Yes'
            repo = 'Yes'
        else:
            repo = 'No'
            rid = 'No'
        
        getpin = Ride_pin.objects.filter(getride=getq.getride,status='1')
        ls = []
        for instance in getpin:
            if getq.id != instance.id:
                representations = {}
                representations['rid_status'] = instance.status
                representations['pin_id'] = instance.id
                representations['ride_type'] = instance.ride_type
                representations['Passenger_id'] = instance.passengerid.id
                representations['passenger_name'] = instance.passengerid.name.title()
                representations['passenger_profile'] = instance.passengerid.pro_image.url
                representations['for_passenger'] = instance.for_passenger
                representations['for_parcel'] = instance.for_parcel
                representations['request_date'] = instance.request_date
                representations['fees'] = instance.fees
                representations['Location'] = instance.pickUp.capitalize()
                representations['Destination'] = instance.dropout.capitalize()
                ls.append(representations)
        print(ls)
        if getq.getride.ride_type == "T":
            return Response({'status':1, 'msg':"Success",
                "ride_type": getq.getride.ride_type,
                "RID": getq.getride.id,
                "rate": rid,
                "report": repo,
                "ride_status" : getq.status,
                "driver_id" : getq.getride.getdriver.id,
                "driver": getq.getride.getdriver.name.title(),
                "Profile": getq.getride.getdriver.pro_image.url,
                "pickUp": getq.getride.pickUp.capitalize(),
                "pickup_address1": getq.getride.pickup_address1,
                "pickup_address2": getq.getride.pickup_address2,
                "pickUp_latitude": getq.getride.pickUp_latitude,
                "pickUp_longitude": getq.getride.pickUp_longitude,
                "dropout": getq.getride.dropout.capitalize(),
                "dropout_address1": getq.getride.dropout_address1,
                "dropout_address2": getq.getride.dropout_address2,
                "dropout_latitude": getq.getride.dropout_latitude,
                "dropout_longitude": getq.getride.dropout_longitude,
                "time": getq.getride.time,
                "dtime": getq.getride.dtime,
                "map_time": getq.getride.map_date,
                "trip_status": getq.getride.trip_status,
                "capacity": f"{getq.for_parcel}",
                "date": getq.getride.date.strftime('%d-%m-%Y'),
                "fees": f"{getq.fees}",
                "add_information": getq.getride.add_information.title(),
                'data' : ls
            })
        if getq.getride.ride_type == "C":
            return Response({'status':1, 'msg':"Success",
                "ride_type": getq.getride.ride_type,
                "RID": getq.getride.id,
                "rate": rid,
                "report": repo,
                "ride_status" : getq.status,
                "driver_id" : getq.getride.getdriver.id,
                "driver": getq.getride.getdriver.name.title(),
                "Profile": getq.getride.getdriver.pro_image.url,
                "pickUp": getq.getride.pickUp.capitalize(),
                "pickup_address1": getq.getride.pickup_address1,
                "pickup_address2": getq.getride.pickup_address2,
                "pickUp_latitude": getq.getride.pickUp_latitude,
                "pickUp_longitude": getq.getride.pickUp_longitude,
                "dropout": getq.getride.dropout.capitalize(),
                "dropout_address1": getq.getride.dropout_address1,
                "dropout_address2": getq.getride.dropout_address2,
                "dropout_latitude": getq.getride.dropout_latitude,
                "dropout_longitude": getq.getride.dropout_longitude,
                "time": getq.getride.time,
                "dtime": getq.getride.dtime,
                "map_time": getq.getride.map_date,
                "trip_status": getq.getride.trip_status,
                "seats": f"{getq.for_passenger}",
                "date": getq.getride.date.strftime('%d-%m-%Y'),
                "fees": f"{getq.fees}",
                "add_information": getq.getride.add_information.title(),
                'data' : ls
            })
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['POST'])
def PassengerGiveRating(request,Rid,pp):
    # try:
    # showtime = strftime("%Y-%m-%d")
    data = request.data
    ra = float(data["rate"])
    rat = round(ra)
    showtime = data['datetime']
    review = data["review"]
    getride = Ride.objects.get(id=Rid,publish='1')
    getpas = user_all.objects.get(id=pp,as_user = 'Passenger')
    getdri = user_all.objects.get(id=getride.getdriver.id,as_user = 'Driver')  
    rate = Drivers_Rating.objects.filter(
        mine = getdri,
        tri = getride,
        passengerid = getpas,
    )
    if len(rate) > 0:
        return Response({'status':0,'msg' : 'Rating has been Given'})
    else:
        rat = Drivers_Rating.objects.create(
            mine = getdri,
            tri = getride,
            passengerid = getpas,
            rates = rat,
            review = review,
            create = showtime,
        )
        return Response({'status':1,'msg' : 'Rating Add Successfully'})
    # except ObjectDoesNotExist:
    #         return Response({'status':0,'msg' : 'Trip Id Is Not Found'})

@api_view(['GET'])
def PassengerGetRating(request,pk):
    try:
        getpas = user_all.objects.get(id=pk,as_user = 'Passenger')
        getride = Passenger_Rating.objects.filter(mine=getpas).order_by('-create')
        if getride:
            serial = PassengerGetRatingSeializer(getride,many=True)
            return Response({'status':1, 'msg':"Success","data":serial.data}) 
        else:
            return Response({'status':0,'msg':'No Rating List Founded'})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['GET'])
def PassengerDrivenRating(request,pk):
    try:
        getpas = user_all.objects.get(id=pk,as_user = 'Passenger')
        getride = Drivers_Rating.objects.filter(passengerid=getpas).order_by('-create')
        if getride:
            serial = PassengerDrivenRatingSeializer(getride,many=True)
            return Response({'status':1, 'msg':"Success","data":serial.data}) 
        else:
            return Response({'status':0,'msg':'No Rating List Founded'})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['GET'])
def DriverProfileViewByPassenger(request,pk):
    try:
        getdri = user_all.objects.get(id=pk,as_user = 'Driver')
        if getdri.gender == '0':
            gender = ''
        else:
            gender = getdri.gender
        rea = Drivers_Rating.objects.filter(mine=pk)
        lis = []
        for i in rea:
            lis.append(float(i.rates))
        if lis == []:
            average = 0.0
        else:
            average = Average(lis)
        return Response({"status" : 1,"msg" : "Success",
                         "Driver_name" : getdri.name.title(),
                         "Driver_Rating" : average,
                         "pro_image" : getdri.pro_image.url,
                         "Email" : getdri.email,
                         "driver_token" : getdri.ntk,
                         "Contact" : getdri.contact_no,
                         "Gender" : gender,
                         "dob" : getdri.dob,
                         "city" : getdri.city.capitalize(),
                         "bio" : getdri.bio.capitalize(),
                         })
    except ObjectDoesNotExist:
        return Response({"status" : 0,"msg" : "Id Not Found"})

# @api_view(['POST'])
# def MultiRideFilterByPassenger(request):
#     data = request.data
#     pick = data["pickUp"]
#     drop = data["dropout"]
#     date = data["date"]
#     seat =  data["seat"]
#     parcel = data["parcel"]
#     price = data["price"]
#     animal = data["pet_allowed"]
#     backseat = data["max_seat_in_back"]
#     cigarate = data["smoke_allowed"]
#     govid = data["Gov_id"]
#     tyme = data["tyme"]
#     tyme1 = data["tyme1"]
#     max_seat = Ride.objects.filter(ride_type='C',publish='1',pickUp=pick,dropout=drop,date=date,trip_status='P').exclude(status='3')#.aggregate(Max('seats'))
#     maxs = 0
#     maxs1 = 0

#     for i in max_seat:
#         print(i.seats,'seats in the id',i.id)
#         print(i.capacity,'parcel in the id',i.id)
        
#         if maxs > int(i.seats):
#             pass
#         else:
#             maxs = int(i.seats)
            
#         if maxs1 > int(i.capacity):
#             pass
#         else:
#             maxs1 = int(i.capacity)
    
#     if pick and drop:
#         # All
#         if animal == "True" and backseat == "True" and cigarate == "True" and govid == "True":
#             print('all')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True,max_seat_in_back=True,smoke_allowed=True,gov_id=True).exclude(status='3')
            
#         # With Lowest Price
#         elif animal == "True" and backseat == "True" and cigarate == "True" and govid == "True" and price == "True":
#             print('all,price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True,max_seat_in_back=True,smoke_allowed=True,gov_id=True).exclude(status='3').order_by("fees")
        
#         # Animal With Other Two
#         elif animal == "True" and backseat == "True" and cigarate == "True":
#             print('animal,backseat,cigarate')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True,max_seat_in_back=True,smoke_allowed=True).exclude(status='3')
#         elif animal == "True" and backseat == "True" and govid == "True":
#             print('animal,backseat,govid')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True,max_seat_in_back=True,gov_id=True).exclude(status='3')
#         elif animal == "True" and govid == "True" and cigarate == "True":
#             print('animal,govid,cigarate')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True,gov_id=True,smoke_allowed=True).exclude(status='3')
#         elif backseat == "True" and govid == "True" and cigarate == "True":
#             print('backseat,govid,cigarate')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],max_seat_in_back=True,gov_id=True,smoke_allowed=True).exclude(status='3')
            
#         # With Price Lowest
#         elif animal == "True" and backseat == "True" and cigarate == "True" and price == "True":
#             print('animal,backseat,cigarate,Price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True,max_seat_in_back=True,smoke_allowed=True).exclude(status='3').order_by("fees")
#         elif animal == "True" and backseat == "True" and govid == "True" and price == "True":
#             print('animal,backseat,govid,Price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True,max_seat_in_back=True,gov_id=True).exclude(status='3').order_by("fees")
#         elif animal == "True" and govid == "True" and cigarate == "True" and price == "True":
#             print('animal,govid,cigarate,Price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True,gov_id=True,smoke_allowed=True).exclude(status='3').order_by("fees")
#         elif backseat == "True" and govid == "True" and cigarate == "True" and price == "True":
#             print('backseat,govid,cigarate,Price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],max_seat_in_back=True,gov_id=True,smoke_allowed=True).exclude(status='3').order_by("fees")
        
#         # With Animal
#         elif animal == "True" and cigarate == "True":
#             print('animal,cigarate')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True,smoke_allowed=True).exclude(status='3')
#         elif animal == "True" and govid == "True":
#             print('animal,govid')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True,gov_id=True).exclude(status='3')
#         elif animal == "True" and backseat == "True":
#             print('animal,backseat')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True,max_seat_in_back=True).exclude(status='3')
            
#         # With Lowest Price
#         elif animal == "True" and cigarate == "True" and price == "True" :
#             print('animal,cigarate,price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True,smoke_allowed=True).exclude(status='3').order_by("fees")
#         elif animal == "True" and govid == "True" and price == "True" :
#             print('animal,govid,price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True,gov_id=True).exclude(status='3').order_by("fees")
#         elif animal == "True" and backseat == "True" and price == "True" :
#             print('animal,backseat,price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True,max_seat_in_back=True).exclude(status='3').order_by("fees")
            
#         # With Cigarate
#         elif cigarate == "True" and govid == "True":
#             print('cigarate,govid')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],smoke_allowed=True,gov_id=True).exclude(status='3')
#         elif cigarate == "True" and backseat == "True":
#             print('backseat,cigaret')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],smoke_allowed=True,max_seat_in_back=True).exclude(status='3')
            
#         # With Lowest Price
#         elif cigarate == "True" and govid == "True" and price == "True":
#             print('cigarate,govid,Price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],smoke_allowed=True,gov_id=True).exclude(status='3').order_by("fees")
#         elif cigarate == "True" and backseat == "True" and price == "True":
#             print('backseat,cigaret,Price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],smoke_allowed=True,max_seat_in_back=True).exclude(status='3').order_by("fees")
            
#         # Back Seats
#         elif backseat == "True" and govid == "True":
#             print('backseat,govid')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],max_seat_in_back=True,gov_id=True).exclude(status='3')
        
#         # With Lowest Price
#         elif backseat == "True" and govid == "True" and price == "True":
#             print('backseat,govid,price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],max_seat_in_back=True,gov_id=True).exclude(status='3').order_by("fees")
            
#         # With Price
#         elif animal == "True" and price == "True":
#             print('animal,price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True).exclude(status='3').order_by("fees")
#         elif backseat == "True" and price == "True":
#             print('back Seat,price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],max_seat_in_back=True).exclude(status='3').order_by("fees")
#         elif cigarate == "True" and price == "True":
#             print('cigarate,price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],smoke_allowed=True).exclude(status='3').order_by("fees")
#         elif govid == "True" and price == "True":
#             print('govid,price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],gov_id=True).exclude(status='3').order_by("fees")
#         elif tyme == "True" and price == "True":
#             time1 = '12:00'
#             time2 = '13:00'
#             print('Time,price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],time__range=[time1,time2]).exclude(status='3').order_by("fees")
#         elif tyme1 == "True" and price == "True":
#             time3 = '18:00'
#             time4 = '23:59'
#             print('Time1,price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],time__range=[time3,time4]).exclude(status='3').order_by("fees")
        
#         # Single Filter
#         elif animal == "True":
#             print('animal')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],pet_allowed=True).exclude(status='3').order_by('-id')
#         elif backseat == "True":
#             print('back Seat')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],max_seat_in_back=True).exclude(status='3').order_by('-id')
#         elif cigarate == "True":
#             print('cigarate')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],smoke_allowed=True).exclude(status='3').order_by('-id')
#         elif govid == "True":
#             print('govid')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],gov_id=True).exclude(status='3').order_by('-id')
#         elif tyme == "True":
#             time1 = '12:00'
#             time2 = '13:00'
#             print('Time')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],time__range=[time1,time2]).exclude(status='3').order_by('-id')
#         elif tyme1 == "True":
#             time3 = '18:00'
#             time4 = '23:59'
#             print('Time1')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1],time__range=[time3,time4]).exclude(status='3').order_by('-id')
#         elif price == "True":
#             print('Price')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs],capacity__range=[parcel,maxs1]).exclude(status='3').order_by('fees')
#         else:
#             print('None')
#             pp = Ride.objects.filter(status='0',ride_type='C',pickUp=pick,dropout=drop,date=date,trip_status='P',seats__range=[seat,maxs]).exclude(status='3').order_by('-id')

#         if len(pp) > 0:
#             serial = MultiFilterserializer(pp,many=True)
#             return Response({'status':1 ,"msg":"Success", 'data':serial.data})    
#         else:
#             return Response({'status':0 ,"msg":"No Record Founded"})
#     else:
#         return Response({'status':0 ,"msg":"No Record Founded"})

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
    try:
        ids = user_all.objects.get(id=pk,as_user = 'Passenger')
        return Response({"status": 1,"msg" : "Success","Proofe_id" : [{"image1" : ids.image1.url,"image2" : ids.image2.url}]})
    except:
        return Response({"status": 0,"msg" : "Not Founded"})

@api_view(['POST'])
def CancelBooking(request,pk):
    try:
        getbooking = Ride_pin.objects.get(id=pk)
        if getbooking.status == '0' or getbooking.status == "1":
            getbooking.status = '3'
            if getbooking.for_passenger != '0' or getbooking.for_passenger != 0:
                if getbooking.status == "1":
                    getride = Ride.objects.get(id=getbooking.getride.id)
                    if getride.status == '1':
                        getride.status = '0'
                    getride.Max_seats = int(getride.Max_seats) + int(getbooking.for_passenger)
                    getride.save()
                
            if getbooking.for_parcel != '0' or getbooking.for_parcel != 0:
                if getbooking.status == "1":
                    getride = Ride.objects.get(id=getbooking.getride.id)
                    if getride.status == '1':
                        getride.status = '0'
                    getride.Max_parcel = int(getride.Max_parcel) + int(getbooking.for_parcel)
                    getride.save()
                
            getbooking.save()
            if getbooking.getride.getdriver:
                if getbooking.getdriver:
                    username = getbooking.getdriver.name.title()
                if getbooking.passengerid:
                    username = getbooking.passengerid.name.title()
                driver_token = getbooking.getride.getdriver.ntk
                notif = firebase_notifications.objects.create(
                    userid = getbooking.getride.getdriver,
                    rideid = getbooking.getride,
                    cancel_by = username,
                    notification_text = f"{username} has cancelled the ride",
                    create_at = strftime("%Y-%m-%d %H:%M:%S"),
                )
                send_notification([driver_token] , 'Ride cancel' , f"{username} has cancelled the ride")
            else:
                driver_token = ""
            return Response({'status':1 ,"msg":"Cancel Booking",'driver_token':driver_token})    
        else:
            return Response({'status':0 ,"msg":"Booking Already Reject Or Cancel"})
    except ObjectDoesNotExist:
        return Response({'status':0 ,"msg":"Ride Booking Id Not Found"})

@api_view(['POST'])
def DeleteBooking(request,pk,rr):
    try:
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
            getbooking = Ride_pin.objects.get(id=pk)
            if getbooking.getride:
                getride = Ride.objects.get(id=getbooking.getride.id)
                if getride.status == '1':
                    getride.status = '0'
                    getride.Max_seats = int(getride.Max_seats) + int(getbooking.for_passenger)
                    getride.Max_parcel = int(getride.Max_parcel) + int(getbooking.for_parcel)
                getride.save()
            getbooking.delete()
            return Response({"status" : 1,'msg': "Ride Delete"})
    except ObjectDoesNotExist:
        return Response({'status':0 ,"msg":"Ride Booking Id Not Found"})
    
@api_view(['POST'])
def ReportDriverBehavior(request,Rid,pk):
    try:
        # showtime = strftime("%Y-%m-%d")
        data = request.data
        report_text = data["report_text"]
        showtime = data['datetime']
        getride = Ride.objects.get(id=Rid,publish='1')
        ridepin = Ride_pin.objects.get(getride=Rid,passengerid=pk,status__range=['0','1'])
        getpas = user_all.objects.get(id=pk,as_user = 'Passenger')
        getdri = user_all.objects.get(id=getride.getdriver.id,as_user = 'Driver')    
        rate = Driver_Report.objects.filter(
            mine = getdri,
            tri = getride,
            passengerid = getpas,
        )
        if len(rate) > 0:
            return Response({'status':0,'msg' : 'Report has been Given'})
        else:
            rat = Driver_Report.objects.create(
                mine = getdri,
                tri = getride,
                passengerid = getpas,
                report_text = report_text,
                create = showtime,
            )
            ridepin.pas_status = "E"
            ridepin.save()
            return Response({'status':1,'msg' : 'Report Successfully'})
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
        getpass = user_all.objects.get(id=pk,as_user = 'Passenger')
        adda = Search_History.objects.filter(passengerid = getpass,pick = pick,drop = drop,pick_lat = pick_lat,pick_lng = pick_lng,drop_lat = drop_lat,drop_lng = drop_lng,date = date,location = location,create = showtime,)
        if len(adda) > 0:
            for i in adda:
                i.delete()
            add = Search_History.objects.create(
                passengerid = getpass,
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
                passengerid = getpass,
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
        his = Search_History.objects.filter(passengerid=pk,location=ll).order_by('-id')[:4]
        if len(his)> 0:
            serial = HistoryViewForPassenger(his,many=True)
            return Response({'status':1 ,"msg": "Success", 'data' : serial.data})
        else:
            return Response({'status':0 ,"msg": "No Record"})
    except ObjectDoesNotExist:
        return Response({'status':0 ,"msg": "Fail"})

@api_view(['POST'])
def tripsetting(request,pk):
    ride = Ride_pin.objects.get(id=pk)
    if ride.getride.trip_status == 'O':
        if ride.status == '1' or ride.status == '0':
            if ride.pas_status == 'W':
                ride.pas_status = 'O'
                ride.save()
                return Response({'status':1 ,"msg": "Trip Started"})
            
            if ride.pas_status == 'O':
                ride.pas_status = 'E'
                ride.save()
                return Response({'status':1 ,"msg": "Trip Complete"})
            
            if ride.pas_status == 'E':
                return Response({'status':1 ,"msg": "Trip Complete"})
        else:
            return Response({'status':0 ,"msg": "Your Doesn't Accept"})
    elif ride.getride.trip_status == 'E':
        return Response({'status':0 ,"msg": "Driver End Trip"})
    else:
        return Response({'status':0 ,"msg": "Driver Not Start Trip"})

@api_view(['POST'])
def ContactUsPassenger(request):
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
        email_from =  email
        to_email = [settings.EMAIL_HOST_USER,]
        send_mail(mail_subject, message,f'{name}', to_email)
        return Response({'status' : 1,'msg':'Mail Sent Successfully'})
    else:
        return Response({'status' : 0 , 'msg' : "Email Is Not Proper"})

@api_view(['GET'])
def BlockStatusForPassenger(request,pk):
    try:
        getd = user_all.objects.get(id=pk)
        if getd.status == 'Active':
            return Response({'status':0,'msg':'Unblock'})
        else:
            # send_notification([getd.ntk] , 'Account Security alert!' , f'Your {getd.as_user} account has been Blocked.')
            return Response({'status':1,'msg':'Block'})
    except:
        return Response({'status':1,'msg':'User Deleted'})

@api_view(['GET'])
def BidDetalis(request,pk):
    try:
        ri = Ride.objects.get(id=pk,publish__range=['1','3'])
        if ri.as_user == 'Passenger':
            # rate = "No"
            # repo = "No"
            di = Ride_pin.objects.filter(getride=ri.id,status='1',as_user='Driver_bid')
            if len(di)>0:
                context = {
                    'status':1,
                    'msg':'success',
                    'id':ri.id,
                    # 'rate':rate,
                    # 'report':repo,
                    'pickup' : ri.pickUp.capitalize(),
                    'pickup_address1' : ri.pickup_address1.capitalize(),
                    'pickup_address2' : ri.pickup_address2.capitalize(),
                    'dropout' : ri.dropout.capitalize(),
                    'dropout_address1' : ri.dropout_address1.capitalize(),
                    'dropout_address2' : ri.dropout_address2.capitalize(),
                    'ride_type' : ri.ride_type,
                    'trip_pas_status' : ri.trip_status,
                    'date' : ri.date.strftime('%Y-%m-%d'),
                    'time' : ri.time,
                    'dtime' : ri.dtime,
                    'seat' : ri.seats,
                    'capacity' : ri.capacity,
                    'add_information' : ri.add_information.title(),
                    'Driver_id' : di[0].getdriver.id,
                    'Driver_name' : di[0].getdriver.name.title(),
                    'Driver_image' : di[0].getdriver.pro_image.url,
                    'fees' : f"{di[0].fees}",
                    "request_date" : f"{di[0].request_date.strftime('%Y-%m-%d')}",
                    }
                return Response(context)
            else:
                context = {
                    'status':1,
                    'msg':'success',
                    'id':ri.id,
                    'pickup' : ri.pickUp.capitalize(),
                    'pickup_address1' : ri.pickup_address1.capitalize(),
                    'pickup_address2' : ri.pickup_address2.capitalize(),
                    'dropout' : ri.dropout.capitalize(),
                    'dropout_address1' : ri.dropout_address1.capitalize(),
                    'dropout_address2' : ri.dropout_address2.capitalize(),
                    'ride_type' : ri.ride_type,
                    'trip_pas_status' : ri.trip_status,
                    'seat' : ri.seats,
                    'date' : ri.date.strftime('%Y-%m-%d'),
                    'time' : ri.time,
                    'dtime' : ri.dtime,
                    'capacity' : ri.capacity,
                    'add_information' : ri.add_information.title(),
                    'Driver_id' : 0,
                    'Driver_name' : '',
                    'Driver_image' : '',
                    'fees' : '',
                    "request_date" : "",
                    }
                return Response(context)
        else:
            return Response({"status":0,'msg':'No Record'})
    except:
        return Response({"status":0,'msg':'Wrong Id'})

@api_view(['GET'])
def RatingDetailsPageForRecieve(request,pk):
    rat = Drivers_Rating.objects.get(id=pk)
    context = {
        'status' : 1,
        'msg' : 'success',
        "Driver_name" : rat.mine.name.title(),
        "Driver_pro_image" : rat.mine.pro_image.url,
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
        "Driver_name" : rat.driverid.name.title(),
        "Driver_pro_image" : rat.driverid.pro_image.url,
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
def cronejov(request,pk):
    user = user_all.objects.get(id=pk)
    send_notification([user.ntk] , 'You get Notify By Cronjob' , f"{user.name.title()} Cron Job Done.!")
    return Response({'status' : 1, "msg" : "Send notification" })
 
@api_view(['POST'])
def FullBookingList(request):
    data = request.data
    current_date = data['current_date']
    current_location = data['current_location']
    if current_location:
        user = user_all.objects.filter(fullbooked='1',current_date=current_date,current_location=current_location,as_user='Driver')
    else:
        user = user_all.objects.filter(fullbooked='1',current_date=current_date,as_user='Driver')
    ls = []
    for instance in user:
        representation = {}
        representation["driver_id"] = instance.id
        representation["driver_name"] = instance.name.title()
        representation["drivers_number"] = instance.contact_no if instance.contact_no else ''
        representation["pro_image"] = instance.pro_image.url
        rea = Drivers_Rating.objects.filter(mine=instance.id)
        lis = []
        for i in rea:
            lis.append(float(i.rates))
        if lis == []:
            average = 0.0
        else:
            average = Average(lis)
        representation["driver_Rating"] = average
        representation["driver_location"] = instance.current_location.title()
        representation["current_date"] = instance.current_date.strftime("%d-%m-%Y")
        
        representation["car"] = f"{instance.car_booked.vehical_variant.brand.brand} {instance.car_booked.vehical_variant.cars}"
        representation["car_color"] = instance.car_booked.vehicle_color
        ls.append(representation)
    return Response({'status':1,"msg":'success',"data":ls})

@api_view(["POST"])
def ForgotOtpSendPassanger(request):
    data = request.data
    raw = data['email_or_num']
    otp = ''
    for i in range (4):
        otp+=str(randint(1,9))
    getotp = otp
    if(not raw):
        return Response({'status' : 0 , 'msg' : "Email Or Phone Number Is Required"})
        
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
                print('Message Is Not Send')
                return Response({'status' : 1 , 'msg' : "Otp Send Successfully Via Text","Driver_id":driver.id,"Passenger_id":passanger.id,'Type':"Mobile","OTP":passanger.otp,"token":passanger.ntk})
            else:
                return Response({'status' : 0 , 'msg' : "Account is Blocked"})
        else:
            return Response({'status' : 0 , 'msg' : "Number Is Not Found.!"})

@api_view(['POST'])
def AddInCityRide(request,pk):
    data = request.data
    pickUp = data["pickUp"].casefold()
    dropout = data["dropout"].casefold()
    pickUp_lat = data["pickUp_lat"]
    dropout_lat = data["dropout_lat"]
    pickUp_lan = data["pickUp_lan"]
    dropout_lan = data["dropout_lan"]
    date = data["date"]
    time = data["time"].upper()
    add_information = data["note"].casefold()
    passenger = data["passenger"]
    parcel = data["parcel"]
    fees = data["fees"]
    vehicle = data['vehicle'].casefold()
    pickup_address1 = data['pickup_address1'].casefold()
    pickup_address2 = data['pickup_address2'].casefold()
    dropout_address1 = data['dropout_address1'].casefold()
    dropout_address2 = data['dropout_address2'].casefold()
    showtime = data['datetime']
    getpas = user_all.objects.get(id=pk,as_user = 'Passenger')
    
    if(not pickUp):
        return Response({'status':0,'msg': 'PickUp Is Not Added..'})
    if(not date):
        return Response({'status':0,'msg': 'Please Select Date For Ride'})
    if(not dropout):
        return Response({'status':0,'msg': 'Dropout Is Not Added..'})
        
    addbookings = InRide.objects.filter(as_user = 'Passenger',vehicle=vehicle,getpassenger = getpas,date = date,pickup_address1 = pickup_address1,dropout_address1 = dropout_address1).exclude(status='3')
    getalldriver = user_all.objects.filter(as_user = 'Driver',fullbooked="0",status="Active").exclude(active_ac_with_otp="0")
    lsi = []
    for ge in getalldriver:
        res = {}
        res['id'] = ge.id
        if ge.name:  
            res['name'] = ge.name.title()
        else:
            res['name'] = ""
        res['latitude'] = ge.latitude
        res['longitude'] = ge.longitude
        if ge.pro_image:
            res['pro_image'] = ge.pro_image.url
        else:
            res['pro_image'] = ""
        res['contact_no'] = ge.contact_no
        res['token'] = ge.ntk
        lsi.append(res)
    
    ride_time = f"{str(date)} {str(convert(time))}"
    if len(addbookings) > 0:
        addbookings[0].ride_time = ride_time
        addbookings[0].capacity = parcel
        addbookings[0].seats = passenger
        addbookings[0].fees = fees
        addbookings[0].pickUp_latitude = pickUp_lat
        addbookings[0].pickUp_longitude = pickUp_lan
        addbookings[0].passenger_latitude = pickUp_lat
        addbookings[0].passenger_longitude = pickUp_lan
        addbookings[0].dropout_latitude = dropout_lat
        addbookings[0].dropout_longitude = dropout_lan
        addbookings[0].pickup_address1 = pickup_address1
        addbookings[0].pickup_address2 = pickup_address2
        addbookings[0].dropout_address1 = dropout_address1
        addbookings[0].dropout_address2 = dropout_address2
        addbookings[0].add_information = add_information
        addbookings[0].create_at = showtime
        addbookings[0].time = time
        addbookings[0].update_at = showtime
        addbookings[0].save()
        return Response({"Booking_Id" : addbookings[0].id,"status":1,"msg":"Booking Added Successfully","driver_list":lsi})
    else:
        addbooking = InRide.objects.create(
            as_user = 'Passenger',
            getpassenger = getpas,
            capacity = parcel,
            seats = passenger,
            pickUp_latitude = pickUp_lat,
            pickUp_longitude = pickUp_lan,
            passenger_latitude = pickUp_lat,
            passenger_longitude = pickUp_lan,
            dropout_latitude = dropout_lat,
            dropout_longitude = dropout_lan,
            pickup_address1 = pickup_address1,
            pickup_address2 = pickup_address2,
            dropout_address1 = dropout_address1,
            dropout_address2 = dropout_address2,
            pickUp = pickUp,
            vehicle = vehicle,
            dropout = dropout,
            date = date,
            fees = fees,
            add_information = add_information,
            ride_time = ride_time,
            time = time,
            create_at = showtime,
            update_at = showtime
        )
        return Response({"Booking_Id" : addbooking.id,"status":1,"msg":"Booking Added Successfully","driver_list":lsi})

@api_view(['POST'])
def RideInCitySearch(request):
    data = request.data
    date = data['date']
    pickUp = data['pickUp'].casefold()
    dropout = data['dropout'].casefold()
    fees = data['fees']
    vehicle = data['vehicle'].casefold()
    ls = []
    if(not date):
        return Response({"status":0,"msg":"Date Is Not Founded"})
    if pickUp and dropout and fees and vehicle:
        pp = InRide.objects.filter(vehicle=vehicle,pickup_address1=pickUp,dropout_address1=dropout,publish='1',trip_status='P',as_user = 'Driver',date=date,status="0").exclude(status='3')
    else:
        pp = InRide.objects.filter(publish='1',trip_status='P',as_user = 'Driver',date=date,status="0").exclude(status='3')
    
    if len(pp)>0:
        for instance in pp:
            representation = {}
            representation["ride_id"] = instance.id
            rea = Drivers_Rating.objects.filter(mine=instance.getdriver.id)
            lis = []
            for i in rea:
                lis.append(float(i.rates))
            if lis == []:
                average = 0.0
            else:
                average = Average(lis)
            representation["driver_Rating"] = average
            representation["driver"] = instance.getdriver.name.title()
            representation["drivers_number"] = instance.getdriver.contact_no if instance.getdriver.contact_no else ''
            representation["pro_image"] = instance.getdriver.pro_image.url
            representation["pickUp"] = instance.pickup_address1.title()
            representation["dropout"] = instance.dropout_address1.title()
            representation["pickUp_city"] = instance.pickUp.capitalize()
            representation["dropout_city"] = instance.dropout.capitalize()
            representation["time"] = instance.time
            representation["dtime"] = instance.dtime
            representation["pickUp_latitude"] = instance.pickUp_latitude
            representation["pickUp_longitude"] = instance.pickUp_longitude
            representation["dropout_latitude"] = instance.dropout_latitude
            representation["dropout_longitude"] = instance.dropout_longitude
            if instance.vehicle:
                representation["vehicle"] = instance.vehicle.capitalize() 
            else:
                representation["vehicle"] = "" 
            representation["map_time"] = instance.map_date
            representation["date"] = instance.date.strftime("%d-%m-%Y")
            representation["fees"] = f"{instance.fees}"
                
            representation["capacity"] = f"{instance.Max_parcel}"
            representation["Available_space"] = f"{instance.capacity}"
            representation["seats"] = f"{instance.Max_seats}"
            representation["Available_seats"] = f"{instance.Max_seats}"
                
            representation["add_information"] = instance.add_information.title()
            if fees:
                if float(fees) >= float(instance.fees):
                    ls.append(representation)
            else:
                ls.append(representation)
        return Response({'status':1,"msg":"success",'data':ls})
    else:
        return Response({'status': 0, 'msg':"Record Not Found"})
  
# @api_view(['POST'])
# def RequestForInRide(request,pid,rid):
#     try:
#         ridegid = InRide.objects.get(id=rid,publish='1')
#         data = request.data
#         showtime = data['datetime']
        
#         pasid = user_all.objects.get(id=pid,as_user = 'Passenger')
#         var = ridegid.getmultipassenger.filter(id=pasid.id)
#         if len(var)>0:
#             return Response({"status": 1, "msg" : f"Request Send"})
#         else:
#             ridegid.getmultipassenger.add(pasid)
#             ridegid.save()
        
#         driid = ridegid.getdriver
#         getdr = user_all.objects.get(id=driid.id,as_user = 'Driver')
#         # getbo = InRide_pin.objects.filter(getride=ridegid,ride_type=ridegid.vehicle,passengerid=pasid,status='0',pickup_address1 = pickup_address1 ,dropout_address1 = dropout_address1).exclude(status='2').order_by('-id')
#         getbo = InRide_pin.objects.filter(getride=ridegid,ride_type=ridegid.vehicle,passengerid=pasid,status='0').exclude(status='2').order_by('-id')
#         if len(getbo) > 0:
#             getbo[0].request_date = showtime
#             getbo[0].save()
#             return Response({"status": 1, "msg" : f"Request Send","Request_Book_Id" : getbo[0].id,"Driver_name" : getdr.name.title(),"Driver_token":getdr.ntk,"Passenger_token":pasid.ntk})
#         else:      
#             createReq = InRide_pin.objects.create(
#                 pickUp = ridegid.pickUp ,
#                 pickup_address1 = ridegid.pickup_address1,
#                 dropout_address1 = ridegid.dropout_address1,
#                 pickUp_latitude = ridegid.pickUp_latitude ,
#                 pickUp_longitude = ridegid.pickUp_longitude ,
#                 dropout = ridegid.dropout ,
#                 dropout_latitude = ridegid.dropout_latitude ,
#                 dropout_longitude = ridegid.dropout_longitude ,
#                 as_user = 'Passenger_bid',
#                 getdriver = getdr,
#                 getride = ridegid,
#                 add_information = ridegid.add_information,
#                 ride_type = ridegid.vehicle,
#                 ride_date = ridegid.date,
#                 ride_time = ridegid.time,
#                 for_passenger = ridegid.seats,
#                 fees = ridegid.fees,
#                 for_parcel = ridegid.capacity,
#                 passengerid = pasid,
#                 request_date = showtime,
#             )
#             return Response({"status": 1, "msg" : f"Request Send","Request_Book_Id" : createReq.id,"Driver_name" : getdr.name.title(),"Driver_token":getdr.ntk,"Passenger_token":pasid.ntk})
#     except ObjectDoesNotExist:
#         return Response({"status": 0, "msg" : "Id IS wrong"})

@api_view(['POST'])
def RequestForInRide(request,pid,rid):
    try:
        data = request.data
        showtime = data['datetime']
        ridegid = InRide.objects.get(id=rid,publish='1')
        getdr = user_all.objects.get(id=pid,as_user = 'Driver')
        pasid = user_all.objects.get(id=ridegid.getpassenger.id,as_user = 'Passenger')
        filterreq = InRide_pin.objects.filter(
            pickup_address1 = ridegid.pickup_address1,
            dropout_address1 = ridegid.dropout_address1,
            as_user = 'Passenger_Req',
            getdriver = getdr,
            getride = ridegid,
            ride_date = ridegid.date,
            ride_time = ridegid.time,
            passengerid = pasid,
            ).order_by('id')
        if len(filterreq)>0:
            return Response({"status": 1, "msg" : f"Request Send","Request_Book_Id" : filterreq[0].id,"Driver_name" : getdr.name.title(),"Driver_token":getdr.ntk,"Passenger_token":pasid.ntk})
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
                as_user = 'Passenger_Req',
                getdriver = getdr,
                getride = ridegid,
                add_information = ridegid.add_information,
                ride_type = ridegid.vehicle,
                ride_date = ridegid.date,
                ride_time = ridegid.time,
                # for_passenger = ridegid.seats,
                fees = ridegid.fees,
                # for_parcel = ridegid.capacity,
                passengerid = pasid,
                request_date = showtime,
            )
            return Response({"status": 1, "msg" : f"Request Send","Request_Book_Id" : createReq.id,"Driver_name" : getdr.name.title(),"Driver_token":getdr.ntk,"Passenger_token":pasid.ntk})
    except ObjectDoesNotExist:
        return Response({"status": 0, "msg" : "Id IS wrong"})
    
@api_view(['GET'])
def ListInRide(request,pid):
    getbo = InRide.objects.filter(publish='1').exclude(status='2').order_by('-id')
    lis = []
    for i in getbo:
        res = {}
        var = i.getmultipassenger.filter(id=pid)
        if i.getpassenger:
            getpasss = str(i.getpassenger.id)
        else:
            getpasss = "0"
        if len(var) > 0 or getpasss == str(pid):
            res['id'] = i.id
            if i.as_user == "Passenger" and i.status == "0":
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
        if getbo.as_user == "Driver":
            getbo.getpassenger = None
            getbo.status = '0'
            getbo.trip_status = 'P'
            getbo.save()
        
        if getbo.as_user == "Passenger":
            getbo.delete()
        return Response({"status":1,'msg':'Ride Cancel SuccessFully'})
    except:
        return Response({"status":0,'msg':'Something Wrong'})
    
@api_view(['GET'])
def ReqListInRide(request,rid):
    try:
        ridegid = InRide.objects.get(as_user='Passenger',id=rid,publish='1')
        getbo = InRide_pin.objects.filter(getride=ridegid.id).exclude(status='2')
        ls = []
        for i in getbo:
            res = {}
            if i.status == "-1" or i.status == "0":
                res['id'] = i.id
                res['ride_id'] = ridegid.id
                if i.getdriver:
                    res['driver_id'] = i.getdriver.id
                    res['driver_name'] = i.getdriver.name.title()
                    res['driver_num'] = i.getdriver.contact_no
                    res['driver_token'] = i.getdriver.ntk
                    res['driver_image'] = i.getdriver.pro_image.url
                else:
                    res['driver_id'] = ""
                    res['driver_name'] = ""
                    res['driver_num'] = ""
                    res['driver_token'] = ""
                    res['driver_image'] = ""
                if i.status == "-1":
                    res['accept'] = "Yes"
                else:
                    res['accept'] = "No"
                res['fees'] = i.fees
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
                passengername = filterreq.passengerid.name.title()
                passengertoken = filterreq.passengerid.ntk
            else:
                passengername = ""
                passengertoken = ""
            if filterreq.getdriver:
                driverid = filterreq.getdriver.id
                drivername = filterreq.getdriver.name.title()
                drivertoken = filterreq.getdriver.ntk
            else:
                driverid = ""
                drivername = ""
                drivertoken = ""
            return Response({"status": 1, "msg" : f"Request Accepted","Request_Book_Id" : filterreq.id,"Driver_id":driverid,"Driver_name" : drivername,"Driver_token": drivertoken,"Passenger_name":passengername,"Passenger_token":passengertoken})
        else:
            return Response({'status': 0,"msg":'Ride Is Accepted By Other'})
    except:
        return Response({'status':0,"msg":"Id Wrong"})

@api_view(['POST'])
def RejectInRide(request,did,rid):
    try:
        ridegid = InRide.objects.get(as_user='Passenger',id=rid,publish='1')
        driid = user_all.objects.get(id=did,as_user = 'Driver')
        ridegid.getmultidriver.remove(driid)
        getbo = InRide_pin.objects.filter(getride=ridegid.id,ride_type=ridegid.vehicle,getdriver=driid.id,status='0').exclude(status='2')
        if len(getbo) > 0:
            getbo[0].delete()
        ridegid.save()
        return Response({'status':1,"msg":"success"})
    except:
        return Response({'status':0,"msg":"Id Wrong"})

@api_view(['POST'])
def getlocationincity(request,pid):
    try:
        data = request.data
        lat = data['lat']
        lon = data['lon']
        getbo = InRide.objects.filter(getpassenger=pid,publish='1').exclude(status='2')
        for u in getbo:
            u.passenger_latitude = lat
            u.passenger_longitude = lon
            u.save()
        pasid = user_all.objects.get(id=did)
        pasid.latitude = lat
        pasid.longitude = lon
        pasid.save()
        return Response({"status":1,"msg":"success"})
    except:
        return Response({"status":0,"msg":"Something Is Wrong"})
    