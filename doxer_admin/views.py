from django.shortcuts import render,redirect
from django.core.exceptions import *
from django.contrib.auth.hashers import make_password,check_password
from time import strftime
from doxer.models import *
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from .models import *
from datetime import datetime
from time import gmtime, strftime
from django.db.models import F, Sum
from django.core.paginator import Paginator,EmptyPage
from time import strftime
from django.views.decorators.csrf import csrf_exempt
from .mixins import Directions
from django.contrib import messages
import re
import requests
import json

# Create your views here.
car_per_page = 10
driver_per_page = 10
passenger_per_page = 10
rides_per_page = 10


def send_notification(registration_ids , message_title , message_desc):
    fcm_api = "AAAArz4KUBo:APA91bGVbwnMSAY90DLP5-4R1n7jBPZaVtqGj6ttqAaOvAJgLDB0cNGLesf4rT06n445NVeM08QNyHqU74nF_OjcRCv0g6PNy_F87qAVbIQPhV1WufUXcggiwvDO-qlc1_D7xkbkSRQ3"
    # fcm_api = settings.FireBase_API_KEY
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

@csrf_exempt
def LoginAdmin(request):
    try:
        if request.method == "POST":
            uname = request.POST['Username']
            pswd = request.POST['password']
                
            # user = admin_credentials.objects.create(
            #     username = uname,
            #     password = pswd
            # )
            # user.password = make_password(user.password)
            # user.save()
            # messages.success(request, f"Register Successfully")
            # return redirect("doxer_admin:loginpage")
            user = admin_credentials.objects.filter(username=uname)
            # user = User.objects.filter(username=uname)
            if len(user) > 0:
                pas = check_password(pswd, user[0].password)
                if pas:
                    request.session['id'] = user[0].id
                    return redirect("doxer_admin:indexpage")
                else:
                    messages.error(request, f"Password is Incorrect..!")
                    request.session['uname'] = uname
                    return redirect("doxer_admin:loginpage")
            else:
                messages.error(request, f"{uname} User Not Founded")
                request.session['uname'] = uname
                request.session['pswd'] = pswd
                return redirect("doxer_admin:loginpage")
        else:
            messages.error(request, f"Something Wrong.!")
            return redirect("doxer_admin:loginpage")
    except:
        return redirect('doxer_admin:loginpage')

@csrf_exempt
def home(request):
    if 'id' in request.session:
        if 'uname' in request.session:
            del request.session['uname']
        if 'pswd' in request.session:
            del request.session['pswd']
        showtime = strftime("%Y-%m-%d")
        dri = user_all.objects.filter(as_user='Driver').exclude(active_ac_with_otp='0')
        dri1 = user_all.objects.filter(as_user='Driver',status="Deactive")
        pas = user_all.objects.filter(as_user='Passenger').exclude(active_ac_with_otp='0')
        pas1 = user_all.objects.filter(as_user='Passenger',status="Deactive")
        rid = Ride_pin.objects.filter(pas_status='E',status='1').exclude(status='2')#.aggregate(total=Sum(F('fees')))
        
        thevalue = 0
        for j in rid:
            if j.getride.trip_status == 'E':
                thevalue = thevalue + float(j.fees)

        rid1 = Ride_pin.objects.filter(pas_status='E',status='1',today=showtime).exclude(status='2')#.aggregate(total=Sum(F('fees')))
        
        todayvalue = 0
        for i in rid1:
            if i.getride.trip_status == 'E':
                todayvalue = todayvalue + float(i.fees)
        
        if request.method == 'POST':
            if thevalue == 0:
                income = "00.00"
            else:
                income = format(thevalue, '.2f')
            if todayvalue == 0:
                dayas = "00.00"
            else:
                dayas = format(todayvalue, '.2f')
                
            if 'id' in request.session:
                sess = "1"
            else:
                sess = "0"
            contax = {
                "sess" : sess,
                'dri' : dri.count(),
                'pas' : pas.count(),
                'dri1' : dri1.count(),
                'pas1' : pas1.count(),
                'income' : f"{income}",
                'today' : f"{dayas}",
                }
            return JsonResponse(contax)
        contax = {
            't1' : '1',
            'dri' : dri.count(),
            'pas' : pas.count(),
            'title' : "Home Page"
        }
        # return render(request,'Direction/Direction.html')
        return render(request,'doxer_admin/index.html',contax)
    else:
        return redirect("doxer_admin:loginpage")

@csrf_exempt
def LoginPage(request):
    if 'id' in request.session:
        return redirect('doxer_admin:indexpage')
    else:
        contax = {
            'title' : "Login Page",
        }
        return render(request,'doxer_admin/login.html',contax)

@csrf_exempt
def All_Drivers(request):
    if 'id' in request.session:
        allu = user_all.objects.filter(as_user='Driver').exclude(active_ac_with_otp='0').order_by('-id')
        per_page = driver_per_page
        # Paginator in a view function to paginate a queryset
        # show 4 news per page
        obj_paginator = Paginator(allu, per_page)
        # list of objects on first page
        first_page = obj_paginator.page(1).object_list
        
        page_range =  obj_paginator.page_range
        pages_range = page_range[-1]
        pages = pages_range
        context = {
        'obj_paginator':obj_paginator,
        'first_page':first_page,
        'page_range':page_range,
        'pages' : pages,
        'pages1' : pages-1,
        'a' : 1,
        'b' : 1 * per_page,
        't' : allu.count(),
        't1' : '3',
        'title': "All Drivers Page"
        }
        try:
            if request.method == 'POST':
                #getting page number
                page_no = request.POST.get('page_no', None) 
                starting_number= (int(page_no)-1)*per_page
                ending_number= int(page_no)*per_page
                res = user_all.objects.filter(as_user='Driver').exclude(active_ac_with_otp='0').order_by('-id')[starting_number:ending_number]
                results = []
                for i in res:
                    resa = {}
                    resa['id'] = i.id
                    resa['pro_image'] = i.pro_image.url
                    resa['username'] = i.name.title()
                    resa['email'] = i.email
                    resa['contact_no'] = i.contact_no
                    if i.gender == "M":
                        gender = 'Male'
                    elif i.gender == "F":
                        gender = 'Female'
                    elif i.gender == "O":
                        gender = 'Other'
                    else:
                        gender = ''
                    resa['gender'] = gender
                    resa['id_status'] = i.img_status
                    resa['city'] = i.city.capitalize()
                    resa['fare_per_km'] = format(i.fare_per_km, '.2f')
                    if i.image2 and i.image1:
                        resa['id_proofe'] = f"<a class='documentview' data-target='#IdProofemodel' data-toggle='modal' data='{i.id}'><div class='face-pile__images-container'><img class='artdeco-entity-image artdeco-entity-image--circle-1 face-pile__image face-pile__image--1 lazy-loaded' alt='IdProofe2' src='{i.image2.url}'><img class='artdeco-entity-image artdeco-entity-image--circle-1 face-pile__image face-pile__image--1 lazy-loaded' alt='IdProofe1' src='{i.image1.url}'></div></a>"
                    if (not i.image2) and i.image1:
                        resa['id_proofe'] = f"<a class='documentview' data-target='#IdProofemodel' data-toggle='modal' data='{i.id}'><div class='face-pile__images-container'><img class='artdeco-entity-image artdeco-entity-image--circle-1 face-pile__image face-pile__image--1 lazy-loaded' alt='IdProofe1' src='{i.image1.url}'></div></a>"
                    if (not i.image1) and i.image2:
                        resa['id_proofe'] = f"<a class='documentview' data-target='#IdProofemodel' data-toggle='modal' data='{i.id}'><div class='face-pile__images-container'><img class='artdeco-entity-image artdeco-entity-image--circle-1 face-pile__image face-pile__image--1 lazy-loaded' alt='IdProofe2' src='{i.image2.url}'></div></a>"
                    if (not i.image2) and (not i.image1):
                        resa['id_proofe'] = f"No ID Upload Here"
                    resa['status'] = i.status
                    resa['create_at'] = i.create_at.strftime("%d-%b-%Y ", ) + "<br><br>" + i.create_at.strftime("%I:%M %p", )
                    results.append(resa)

                    if ending_number >= allu.count():
                        b = allu.count()
                    else:
                        b = ending_number
                return JsonResponse({"results":results,'a' : starting_number + 1,'b' : b,'t' : allu.count()})
        except:
            return JsonResponse({"results":[''],'a' : 0,'b' : 0,'t' : allu.count()})
        return render(request,'doxer_admin/all_drivers.html',context)
    else:
        return redirect("doxer_admin:loginpage")

@csrf_exempt  
def All_Passengers(request):
    if 'id' in request.session:
        allu = user_all.objects.filter(as_user='Passenger').exclude(active_ac_with_otp='0').order_by('-id')
        per_page = passenger_per_page
        # Paginator in a view function to paginate a queryset
        # show 4 news per page
        obj_paginator = Paginator(allu, per_page)
        # list of objects on first page
        first_page = obj_paginator.page(1).object_list
        
        page_range =  obj_paginator.page_range
        pages_range = page_range[-1]
        pages = pages_range

        context = {
        'obj_paginator':obj_paginator,
        'first_page':first_page,
        'page_range':page_range,
        'pages' : pages,
        'pages1' : pages-1,
        't1' : '4',
        'title': "All Passengers Page"
        }
        try:            
            if request.method == 'POST':
                #getting page number
                page_no = request.POST.get('page_no', None)
                starting_number= (int(page_no)-1)*per_page
                ending_number= int(page_no)*per_page
                res = user_all.objects.filter(as_user='Passenger').exclude(active_ac_with_otp='0').order_by('-id')[starting_number:ending_number]
                results = []
                for i in res:
                    resa = {}
                    resa['id'] = i.id
                    resa['pro_image'] = i.pro_image.url
                    resa['username'] = i.name.title()
                    resa['email'] = i.email
                    resa['contact_no'] = i.contact_no
                    if i.gender == "M":
                        gender = 'Male'
                    elif i.gender == "F":
                        gender = 'Female'
                    elif i.gender == "O":
                        gender = 'Other'
                    else:
                        gender = ''
                    resa['gender'] = gender
                    resa['status'] = i.status
                    resa['id_status'] = i.img_status
                    # if i.image2:
                    #     resa['id_proofe'] = f"<a class='documentview' data-target='#IdProofemodel' data-toggle='modal' data='{i.id}'><div class='face-pile__images-container'><img class='artdeco-entity-image artdeco-entity-image--circle-1 face-pile__image face-pile__image--1 lazy-loaded' alt='IdProofe2' src='{i.image2.url}'><img class='artdeco-entity-image artdeco-entity-image--circle-1 face-pile__image face-pile__image--1 lazy-loaded' alt='IdProofe1' src='{i.image1.url}'></div></a>"
                    # else:
                    #     resa['id_proofe'] = f"<a class='documentview' data-target='#IdProofemodel' data-toggle='modal' data='{i.id}'><div class='face-pile__images-container'><img class='artdeco-entity-image artdeco-entity-image--circle-1 face-pile__image face-pile__image--1 lazy-loaded' alt='IdProofe1' src='{i.image1.url}'></div></a>"
                        
                    if i.image2 and i.image1:
                        resa['id_proofe'] = f"<a class='documentview' data-target='#IdProofemodel' data-toggle='modal' data='{i.id}'><div class='face-pile__images-container'><img class='artdeco-entity-image artdeco-entity-image--circle-1 face-pile__image face-pile__image--1 lazy-loaded' alt='IdProofe2' src='{i.image2.url}'><img class='artdeco-entity-image artdeco-entity-image--circle-1 face-pile__image face-pile__image--1 lazy-loaded' alt='IdProofe1' src='{i.image1.url}'></div></a>"
                    if (not i.image2) and i.image1:
                        resa['id_proofe'] = f"<a class='documentview' data-target='#IdProofemodel' data-toggle='modal' data='{i.id}'><div class='face-pile__images-container'><img class='artdeco-entity-image artdeco-entity-image--circle-1 face-pile__image face-pile__image--1 lazy-loaded' alt='IdProofe1' src='{i.image1.url}'></div></a>"
                    if (not i.image1) and i.image2:
                        resa['id_proofe'] = f"<a class='documentview' data-target='#IdProofemodel' data-toggle='modal' data='{i.id}'><div class='face-pile__images-container'><img class='artdeco-entity-image artdeco-entity-image--circle-1 face-pile__image face-pile__image--1 lazy-loaded' alt='IdProofe2' src='{i.image2.url}'></div></a>"
                    if (not i.image2) and (not i.image1):
                        resa['id_proofe'] = f"No ID Upload Here"
                    resa['create_at'] = i.create_at.strftime("%d-%b-%Y ", ) + "<br><br>" + i.create_at.strftime("%I:%M %p", )
                    results.append(resa)
                    if ending_number >= allu.count():
                        b = allu.count()
                    else:
                        b = ending_number
                return JsonResponse({"results":results,'a' : starting_number + 1,'b' : b,'t' : allu.count()})
        except:
            return JsonResponse({"results":[''],'a' : 0,'b' : 0,'t' : allu.count()})
        return render(request,'doxer_admin/all_passenger.html',context)
    else:
        return redirect("doxer_admin:loginpage")

@csrf_exempt   
def Rejected_Cars(request):
    if 'id' in request.session:
        allu = Vehicle.objects.filter(status='2').order_by('id')
        per_page = car_per_page
        # Paginator in a view function to paginate a queryset
        # show 4 news per page
        obj_paginator = Paginator(allu, per_page)
        # list of objects on first page
        first_page = obj_paginator.page(1).object_list
        
        page_range =  obj_paginator.page_range
        pages_range = page_range[-1]
        pages = pages_range

        context = {
        'obj_paginator':obj_paginator,
        'first_page':first_page,
        'page_range':page_range,
        'pages' : pages,
        'pages1' : pages-1,
        't1' : '2',
        'title': "Rejected Cars Page"
        }
        try:
            if request.method == 'POST':
                #getting page number
                page_no = request.POST.get('page_no', None)
                starting_number= (int(page_no)-1)*per_page
                ending_number= int(page_no)*per_page
                allw = Vehicle.objects.filter(status='2')
                res = Vehicle.objects.filter(status='2').order_by('-updated')[starting_number:ending_number]
                results = []
                for i in res:
                    resa = {}
                    resa['id'] = i.id
                    resa['pro_image'] = i.driverid.pro_image.url
                    resa['pro_image'] = i.vehical_variant.photo_of_vehicle.url
                    resa['driverid'] = i.driverid.name.title() if i.driverid.name.title() else i.driverid.email_or_num
                    resa['reg_num'] = i.reg_num.upper()
                    resa['vehical_variant'] = f'{i.vehical_variant.brand},{i.vehical_variant.cars}'
                    resa['vehicle_color'] = i.vehicle_color.title()
                    resa['status'] = i.status
                    resa['date'] = i.updated.strftime("%d-%b-%Y") + "<br><br>" + i.updated.strftime("%I:%M %p")
                    results.append(resa)
                    if ending_number >= allw.count():
                        b = allw.count()
                    else:
                        b = ending_number
                return JsonResponse({"results":results,'a' : starting_number + 1,'b' : b,'t' : allw.count()})
        except:
            return JsonResponse({"results":[''],'a' : 0,'b' : 0,'t' : allu.count()})
        return render(request,'doxer_admin/rejectecar.html',context)
    else:
        return redirect("doxer_admin:loginpage")

@csrf_exempt    
def Accepted_Cars(request):
    if 'id' in request.session:
        allu = Vehicle.objects.filter(status='1').order_by('updated')
        per_page = car_per_page
        # Paginator in a view function to paginate a queryset
        # show 4 news per page
        obj_paginator = Paginator(allu, per_page)
        # list of objects on first page
        first_page = obj_paginator.page(1).object_list
        
        page_range =  obj_paginator.page_range
        pages_range = page_range[-1]
        pages = pages_range

        context = {
        'obj_paginator':obj_paginator,
        'first_page':first_page,
        'page_range':page_range,
        'pages' : pages,
        'pages1' : pages-1,
        't1' : '2',
        'title': "Accepted Cars Page"
        }
        try:
            if request.method == 'POST':
                #getting page number
                page_no = request.POST.get('page_no', None)
                starting_number= (int(page_no)-1)*per_page
                ending_number= int(page_no)*per_page
                allw = Vehicle.objects.filter(status='1')
                res = Vehicle.objects.filter(status='1').order_by('-updated')[starting_number:ending_number]
                results = []
                for i in res:
                    resa = {}
                    resa['id'] = i.id
                    # resa['pro_image'] = i.driverid.pro_image.url
                    resa['pro_image'] = i.vehical_variant.photo_of_vehicle.url
                    resa['driverid'] = i.driverid.name.title() if i.driverid.name.title() else i.driverid.email_or_num
                    resa['reg_num'] = i.reg_num.upper()
                    resa['vehical_variant'] = f'{i.vehical_variant.brand},{i.vehical_variant.cars}'
                    resa['vehicle_color'] = i.vehicle_color.title()
                    resa['status'] = i.status
                    resa['date'] = i.updated.strftime("%d-%b-%Y") + "<br><br>" + i.updated.strftime("%I:%M %p")
                    results.append(resa)
                    if ending_number >= allw.count():
                        b = allw.count()
                    else:
                        b = ending_number
                return JsonResponse({"results":results,'a' : starting_number + 1,'b' : b,'t' : allw.count()})
        except:
            return JsonResponse({"results":[''],'a' : 0,'b' : 0,'t' : allu.count()})
        return render(request,'doxer_admin/acceptecar.html',context)
    else:
        return redirect("doxer_admin:loginpage")

@csrf_exempt    
def All_Cars(request):
    if 'id' in request.session:
        allu = Vehicle.objects.filter(status='0').order_by('-created')
        per_page = car_per_page
        # Paginator in a view function to paginate a queryset
        # show 4 news per page
        obj_paginator = Paginator(allu, per_page)
        # list of objects on first page
        first_page = obj_paginator.page(1).object_list
        
        page_range =  obj_paginator.page_range
        pages_range = page_range[-1]
        pages = pages_range

        context = {
        'obj_paginator':obj_paginator,
        'first_page':first_page,
        'page_range':page_range,
        'pages' : pages,
        'pages1' : pages-1,
        't1' : '2',
        'title': "All New Registered Cars Page"
        }
        try:
            if request.method == 'POST':
                #getting page number
                page_no = request.POST.get('page_no', None)
                starting_number= (int(page_no)-1)*per_page
                ending_number= int(page_no)*per_page
                allw = Vehicle.objects.filter(status='0')
                res = Vehicle.objects.filter(status='0').order_by('-created')[starting_number:ending_number]
                results = []
                for i in res:
                    resa = {}
                    resa['id'] = i.id
                    resa['pro_image'] = i.vehical_variant.photo_of_vehicle.url
                    # resa['pro_image'] = i.driverid.pro_image.url
                    resa['driverid'] = i.driverid.name.title() if i.driverid.name.title() else i.driverid.email_or_num
                    resa['reg_num'] = i.reg_num.upper()
                    resa['vehical_variant'] = f'{i.vehical_variant.brand},{i.vehical_variant.cars}'
                    resa['vehicle_color'] = i.vehicle_color.title()
                    resa['status'] = i.status
                    resa['date'] = i.created.strftime("%d-%b-%Y")
                    results.append(resa)
                    if ending_number >= allw.count():
                        b = allw.count()
                    else:
                        b = ending_number
                return JsonResponse({"results":results,'a' : starting_number + 1,'b' : b,'t' : allw.count()})
        except:
            return JsonResponse({"results":[''],'a' : 0,'b' : 0,'t' : allu.count()})
        return render(request,'doxer_admin/all_cars.html',context)
    else:
        return redirect("doxer_admin:loginpage")

@csrf_exempt    
def All_Rides(request):
    if 'id' in request.session:
        allu = Ride.objects.filter(publish='1',fullbooked="0").order_by('trip_status2','-ride_time')
        per_page = rides_per_page
        # Paginator in a view function to paginate a queryset
        # show 4 news per page
        obj_paginator = Paginator(allu, per_page)
        # list of objects on first page
        first_page = obj_paginator.page(1).object_list
        
        page_range =  obj_paginator.page_range
        pages_range = page_range[-1]
        pages = pages_range

        context = {
        'obj_paginator':obj_paginator,
        'page_range':page_range,
        'pages' : pages,
        'pages1' : pages-1,
        't1' : '5',
        'google_api_key' : settings.GOOGLE_API_KEY,
        'title': "All Rides Page"
        }
        # try:
        if request.method == 'POST':
            #getting page number
            page_no = request.POST.get('page_no', None) 
            starting_number= (int(page_no)-1)*per_page
            ending_number= int(page_no)*per_page
            res = Ride.objects.filter(publish='1',fullbooked="0").order_by('trip_status2','-ride_time')[starting_number:ending_number]
            results = []
            for i in res:
                resa = {}
                if i.ride_type == "C":
                    if i.car:
                        cars = Vehicle.objects.get(id=i.car.id)
                        resa['vehicle'] = f"{cars.vehical_variant.brand.brand} {cars.vehical_variant.cars}<br><br> {cars.reg_num.upper()} <br><br> {cars.vehicle_color.capitalize()}"
                    else:
                        cars = 'None'
                        resa['vehicle'] = cars
                
                if i.ride_type == "T":
                    resa['vehicle'] = 'Truck'
                    
                resa['id'] = i.id
                rat = Driver_Report.objects.filter(tri=i.id)
                if len(rat) > 0:
                    resa['str'] = '1'
                else:
                    resa['str'] = '0'
                rd = Ride_pin.objects.filter(getride=i.id)
                for h in rd:
                    rat1 = Passenger_Report.objects.filter(tri=h.id)
                    if len(rat1) > 0:
                        resa['str'] = '1'
                        break
                    else:
                        resa['str'] = '0'
                    
                    
                if i.as_user == "Driver":
                    resa['getdr'] = i.getdriver.name.title()
                    resa['trip_date'] = i.date.strftime("%d-%m-%Y" )
                    resa['ride_time'] = i.time
                    rid = Ride_pin.objects.filter(getride=i.id,as_user='Passenger_bid',status='1')
                    if i.fees == 'null' or i.fees == None:
                        resa['fees'] = ""
                    else:
                        if len(rid) > 0:
                            fees = 0
                            for l in rid:
                                fees = fees + float(l.fees)
                            resa['fees'] = f"{format(fees,'.2f')}"
                        else:
                            resa['fees'] = f"{format(i.fees,'.2f')}"
                    pas = []
                    if len(rid) > 0:
                        for j in rid:
                            pas.append(j.passengerid.name.title())
                        st = '<br>'
                        for jj in pas:
                            st = st + jj + '<br><br>'
                        resa['getpas'] = st
                    else:
                        resa['getpas'] = ""
                if i.as_user == "Passenger":
                    if i.fees == 'null' or i.fees == None:
                        resa['fees'] = ""
                    else:
                        resa['fees'] = f"{format(i.fees,'.2f')}"
                    rids = Ride_pin.objects.filter(getride=i.id,as_user='Driver_bid',status='1')
                    if len(rids) > 0:
                        resa['getdr'] = rids[0].getdriver.name.title()
                    else:
                        resa['getdr'] = ""
                    resa['getpas'] = i.getpassenger.name.title()
                    resa['trip_date'] = i.date
                    resa['ride_time'] = i.time
                resa['rid'] = i.id
                resa['Location'] = i.pickUp.capitalize()
                resa['destination'] = i.dropout.capitalize()
                resa['create_at'] = i.create_at.strftime("%d-%b-%Y ", ) + "<br><br>" + i.create_at.strftime("%I:%M %p", )
                if i.status == "3":
                    resa['status'] = "<label class='badge badge-danger'>Ride Cancel</label>"
                else:
                    if i.trip_status == 'P':
                        resa['status'] = "<label class='badge badge-info'>Waiting</label>"
                    if  i.trip_status == 'O':
                        resa['status'] = "<label class='badge badge-warning'>On The Way</label>"
                    if  i.trip_status == 'E':
                        resa['status'] = "<label class='badge badge-success'>Ride End</label>"
                results.append(resa)
            if ending_number >= allu.count():
                b = allu.count()
            else:
                b = ending_number
            return JsonResponse({"results":results,'a' : starting_number + 1,'b' : b,'t' : allu.count()})
        # except:
        #     return JsonResponse({"results":[''],'a' : 0,'b' : 0,'t' : allu.count()})
        return render(request,'doxer_admin/all_ride.html',context)
    else:
        return redirect("doxer_admin:loginpage")

@csrf_exempt    
def with_in_city_Rides(request):
    if 'id' in request.session:
        allu = InRide.objects.filter(status="1").order_by('trip_status2','-ride_time')
        # allu = InRide.objects.filter(publish='1',fullbooked='0',InCity='1').order_by('trip_status2','-ride_time')
        per_page = rides_per_page
        obj_paginator = Paginator(allu, per_page)
        first_page = obj_paginator.page(1).object_list
        
        page_range =  obj_paginator.page_range
        pages_range = page_range[-1]
        pages = pages_range

        context = {
        'obj_paginator':obj_paginator,
        'page_range':page_range,
        'pages' : pages,
        'pages1' : pages-1,
        't1' : '5',
        'google_api_key' : settings.GOOGLE_API_KEY,
        'title': "City Rides Page"
        }
        # try:
        if request.method == 'POST':
            page_no = request.POST.get('page_no', None) 
            starting_number= (int(page_no)-1)*per_page
            ending_number= int(page_no)*per_page
            # res = Ride.objects.filter(publish='1',fullbooked='0',InCity='1').order_by('trip_status2','-ride_time')[starting_number:ending_number]
            res = InRide.objects.filter(status="1").order_by('trip_status2','-ride_time')[starting_number:ending_number]
            results = []
            for i in res:
                resa = {}
                if i.vehicle:
                    resa['vehicle'] = i.vehicle.capitalize()
                else:
                    resa['vehicle'] = ""
                resa['id'] = i.id
                resa['str'] = '0'
                
                resa['trip_date'] = i.date.strftime("%d-%m-%Y" )
                resa['ride_time'] = i.time
                if i.fees == 'null' or i.fees == None:
                    resa['fees'] = ""
                else:
                    resa['fees'] = f"{format(i.fees,'.2f')}"
                if i.getdriver:
                    resa['getdr'] = i.getdriver.name.title()
                else:
                    resa['getdr'] = ""
                if i.getpassenger:
                    resa['getpas'] = i.getpassenger.name.title()
                else:
                    resa['getpas'] = ""
                resa['rid'] = i.id
                resa['Location'] = i.pickup_address1.capitalize() +"<br><br>" + i.pickUp.capitalize()
                resa['destination'] = i.dropout_address1.capitalize() + "<br><br>"+ i.dropout.capitalize()
                resa['create_at'] = i.create_at.strftime("%d-%b-%Y ", ) + "<br><br>" + i.create_at.strftime("%I:%M %p", )
                if i.status == "3":
                    resa['status'] = "<label class='badge badge-danger'>Ride Cancel</label>"
                else:
                    if i.trip_status == 'P':
                        resa['status'] = "<label class='badge badge-info'>Waiting</label>"
                    if  i.trip_status == 'O':
                        resa['status'] = "<label class='badge badge-warning'>On The Way</label>"
                    if  i.trip_status == 'E':
                        resa['status'] = "<label class='badge badge-success'>Ride End</label>"
                results.append(resa)
            if ending_number >= allu.count():
                b = allu.count()
            else:
                b = ending_number
            return JsonResponse({"results":results,'a' : starting_number + 1,'b' : b,'t' : allu.count()})
        # except:
        #     return JsonResponse({"results":[''],'a' : 0,'b' : 0,'t' : allu.count()})
        return render(request,'doxer_admin/with_in_city_ride.html',context)
    else:
        return redirect("doxer_admin:loginpage")

@csrf_exempt
def LogoutAdmin(request):
    try:
        if 'id' in request.session:
            del request.session['id']
            return redirect("doxer_admin:loginpage")
        else:
            return redirect("doxer_admin:loginpage")
    except:
        return redirect("doxer_admin:loginpage")

@csrf_exempt
def car_accept(request):
    if 'id' in request.session:
        if request.method=='POST':
            id = request.POST.get('pid')
            date = request.POST.get('date')
            showtime = strftime("%Y-%m-%d %H:%M:%S", )
            getpas = Vehicle.objects.get(pk=id)
            if getpas.status == '0':
                getpas.status = '1'
                getpas.updated = showtime #date[0:15]
                getpas.save()
                
                allu = Vehicle.objects.filter(status='0').order_by('created')
                allw = Vehicle.objects.filter(status='0')
                pagess = allu.count()
                per_page = car_per_page
                # Paginator in a view function to paginate a queryset
                # show 4 news per page
                obj_paginator = Paginator(allu, per_page)
                # list of objects on first page
                first_page = obj_paginator.page(1).object_list
                
                page_range =  obj_paginator.page_range
                pages_range = page_range[-1]
                pages = pages_range

                #getting page number
                page_no = request.POST.get('page_no', None)
                if int(page_no) > 0:
                    starting_number= (int(page_no)-1)*per_page
                    ending_number= (int(page_no))*per_page
                    res = Vehicle.objects.filter(status='0').order_by('created')[starting_number:ending_number]
                    result = []
                    for i in res:
                        resa = {}
                        resa['id'] = i.id
                        # resa['pro_image'] = i.driverid.pro_image.url
                        resa['pro_image'] = i.vehical_variant.photo_of_vehicle.url
                        resa['driverid'] = i.driverid.name.title() if i.driverid.name.title() else i.driverid.email_or_num
                        resa['reg_num'] = i.reg_num.upper()
                        resa['vehical_variant'] = f'{i.vehical_variant.brand},{i.vehical_variant.cars}'
                        resa['vehicle_color'] = i.vehicle_color.title()
                        resa['status'] = i.status
                        resa['date'] = i.created.strftime("%d-%b-%Y")
                        results.append(resa)
                        if ending_number >= allw.count():
                            b = allw.count()
                        else:
                            b = ending_number
                    return JsonResponse({'status':1,"results":result,'page_range':pages,'a' : starting_number + 1,'b' : b,'t' : allw.count()})
                else:
                    if allu.count() == 0:
                        a = 0
                    else:
                        a = 1
                    return JsonResponse({'status':1,'results' : 'None','page_range':pages,'a' : a,'b' : allu.count(),'t' : allu.count()})
            else:
                return JsonResponse({'status':0})
        else:
            return JsonResponse({'status':0})
    else:
        return JsonResponse({'status':0})

@csrf_exempt
def car_reject(request):
    if 'id' in request.session:
        if request.method=='POST':
            id = request.POST.get('pid')
            date = request.POST.get('date')
            showtime = strftime("%Y-%m-%d %H:%M:%S", )
            getpas = Vehicle.objects.get(pk=id)
            if getpas.status == '0':
                getpas.status = '2'
                getpas.updated = showtime # date[0:15]
                getpas.save()
                allu = Vehicle.objects.filter(status='0').order_by('created')
                allw = Vehicle.objects.filter(status='0')
                pagess = allu.count()
                per_page = car_per_page
                # Paginator in a view function to paginate a queryset
                # show 4 news per page
                obj_paginator = Paginator(allu, per_page)
                # list of objects on first page
                first_page = obj_paginator.page(1).object_list
                
                page_range =  obj_paginator.page_range
                pages_range = page_range[-1]
                pages = pages_range

                page_no = request.POST.get('page_no', None)
                if int(page_no) > 0:
                    starting_number= (int(page_no)-1)*per_page
                    ending_number= (int(page_no))*per_page
                    res = Vehicle.objects.filter(status='0').order_by('created')[starting_number:ending_number]
                    result = []
                    for i in res:
                        results = {}
                        results['id'] = i.id
                        # results['pro_image'] = i.driverid.pro_image.url
                        results['pro_image'] = i.vehical_variant.photo_of_vehicle.url
                        results['driverid'] = i.driverid.name.title() if i.driverid.name.title() else i.driverid.email_or_num
                        results['reg_num'] = i.reg_num.upper()
                        results['vehical_variant'] = f'{i.vehical_variant.brand},{i.vehical_variant.cars}'
                        results['vehicle_color'] = i.vehicle_color.capitalize()
                        results['status'] = i.status
                        result.append(results)
                        if ending_number >= allw.count():
                            b = allw.count()
                        else:
                            b = ending_number
                    return JsonResponse({'status':1,"results":result,'page_range':pages,'a' : starting_number + 1,'b' : b,'t' : allw.count()})
                else:
                    if allu.count() == 0:
                        a = 0
                    else:
                        a = 1
                    return JsonResponse({'status':1,'results' : 'None','a' : a,'b' : allu.count(),'t' : allu.count()})
                # return JsonResponse({'status':1})
            else:
                return JsonResponse({'status':0})
        else:
            return JsonResponse({'status':0})
    else:  
        return JsonResponse({'status':0})

@csrf_exempt    
def BlockPassenger(request):
    if 'id' in request.session:
        if request.method=='POST':
            id = request.POST.get('pid')
            showtime = strftime("%Y-%m-%d %H:%M:%S", )
            getpas = user_all.objects.get(pk=id,as_user='Passenger')
            if getpas.status == 'Active':
                getride = Ride.objects.filter(getpassenger=id,publish='1',trip_status='P')
                for i in getride:
                    i.publish = '2'
                    i.save()
                getinride = InRide.objects.filter(getpassenger=id,publish='1',trip_status='P')
                for j in getinride:
                    j.publish = '2'
                    j.save()
                getpas.status = 'Deactive'
                getpas.update = showtime
                getpas.save()
                return JsonResponse({'status':1})
            elif getpas.status == 'Deactive':
                getride = Ride.objects.filter(getpassenger=id,publish='2',trip_status='P')
                for i in getride:
                    i.publish = '1'
                    i.save()
                getinride = InRide.objects.filter(getpassenger=id,publish='2',trip_status='P')
                for j in getinride:
                    j.publish = '1'
                    j.save()
                getpas.status = 'Active'
                getpas.update = showtime
                getpas.save()
                return JsonResponse({'status':2})
            else:
                return JsonResponse({'status':0})
        else:
            return JsonResponse({'status':0})
    else:
        return JsonResponse({'status':0})

@csrf_exempt    
def BlockDriver(request):
    if 'id' in request.session:
        if request.method=='POST':
            id = request.POST.get('pid')
            showtime = strftime("%Y-%m-%d %H:%M:%S", )
            getpas = user_all.objects.get(pk=id,as_user='Driver')
            if getpas.status == 'Active':
                getride = Ride.objects.filter(getdriver=id,publish='1',trip_status='P')
                for i in getride:
                    i.publish = '2'
                    i.save()
                getinride = InRide.objects.filter(getdriver=id,publish='1',trip_status='P')
                for j in getinride:
                    j.publish = '2'
                    j.save()
                getpas.status = 'Deactive'
                getpas.update = showtime
                getpas.save()
                driver_name = getpas.name.title() if getpas.name.title() else getpas.email_or_num
                return JsonResponse({'status':1,'driver': f"{driver_name} Block Successfully..!"})
            elif getpas.status == 'Deactive':
                getride = Ride.objects.filter(getdriver=id,publish='2',trip_status='P')
                for i in getride:
                    i.publish = '1'
                    i.save()
                getinride = InRide.objects.filter(getdriver=id,publish='2',trip_status='P')
                for j in getinride:
                    j.publish = '1'
                    j.save()
                getpas.status = 'Active'
                getpas.update = showtime
                getpas.save()
                driver_name = getpas.name.title() if getpas.name.title() else getpas.email_or_num
                return JsonResponse({'status':2,'driver': f"{driver_name} Unblock Successfully..!"})
            else:
                return JsonResponse({'status':0})
        else:
            return JsonResponse({'status':0})
    else:
        return JsonResponse({'status':0})

@csrf_exempt
def editprice(request):
    if 'id' in request.session:
        if request.method=='POST':
                id = request.POST.get('pid')
                showtime = strftime("%Y-%m-%d %H:%M:%S", )
                getda = user_all.objects.get(pk=id,as_user='Driver')
                driver_data = {'id' : getda.id,'email': getda.name.title() if getda.name.title() else getda.email_or_num, 'fees': format(getda.fare_per_km, '.2f')}
                return JsonResponse(driver_data)
    else:
        return JsonResponse({'status':0})

@csrf_exempt
def editcar(request):
    if 'id' in request.session:
        if request.method=='POST':
                id = request.POST.get('pid')
                showtime = strftime("%Y-%m-%d %H:%M:%S", )
                getda = Vehicle.objects.get(pk=id)   
                car = getda.vehical_variant.cars + ',' + getda.vehical_variant.brand.brand
                driver_data = {'id' : getda.id,'reg_num' : getda.reg_num,'vehicle_color' : getda.vehicle_color, 'car' : car}
                # driver_data = {'id' : getda.id,'email': getda.username if getda.username else getda.email_or_num, 'fees': getda.fare_per_km}
                return JsonResponse(driver_data)
    else:
        return JsonResponse({'status':0})

@csrf_exempt
def updateprice(request):
    if 'id' in request.session:
        try:    
            if request.method=='POST':
                id = request.POST.get('pid')
                price = float(request.POST.get('price'))
                showtime = strftime("%Y-%m-%d %H:%M:%S", )
                getpas = user_all.objects.get(pk=id,as_user='Driver')
                getpas.fare_per_km = price
                if price == 0.00 or price == "0.00" or price == 0 or price == "0":
                    return JsonResponse({'status':22,"msg" : "Please Enter Valid Price"})
                getpas.save()
                drive_name = getpas.name.title() if getpas.name.title() else getpas.email_or_num
                prices = f"{drive_name}'s Price {format(price, '.2f')} Credited Successfully..!"
                return JsonResponse({'status':1,'update_value' : prices,'price' : format(price, '.2f')})
            else:
                return JsonResponse({'status':0})
        except:
            return JsonResponse({'status':2})
    else:
        return JsonResponse({'status':2})

@csrf_exempt    
def map_view(request):
    if 'id' in request.session:
        if request.method=='POST':
            gid = request.POST.get('id')
            rid_pins = Ride.objects.get(id=gid)
            allr = Ride_pin.objects.filter(getride=rid_pins.id)
            lat = float(rid_pins.pickUp_latitude)
            lng = float(rid_pins.pickUp_longitude)
            lat_a = float(rid_pins.dropout_latitude)
            lng_a = float(rid_pins.dropout_longitude)
            context = {
                'lat' : lat,
                'lng' : lng,
                'lat_a' : lat_a,
                'lng_a' : lng_a,
                'rid' : rid_pins.id
            }
            return JsonResponse(context)
    else:
        return redirect("doxer_admin:loginpage")

@csrf_exempt    
def Incitymap_view(request):
    if 'id' in request.session:
        if request.method=='POST':
            gid = request.POST.get('id')
            rid_pins = InRide.objects.get(id=gid)
            allr = InRide_pin.objects.filter(getride=rid_pins.id)
            lat = float(rid_pins.pickUp_latitude)
            lng = float(rid_pins.pickUp_longitude)
            lat_a = float(rid_pins.dropout_latitude)
            lng_a = float(rid_pins.dropout_longitude)
            context = {
                'lat' : lat,
                'lng' : lng,
                'lat_a' : lat_a,
                'lng_a' : lng_a,
                'rid' : rid_pins.id
            }
            return JsonResponse(context)
    else:
        return redirect("doxer_admin:loginpage")

@csrf_exempt
def map(request):
    try:
        lat_a = request.GET.get("lat_a")
        long_a = request.GET.get("long_a")
        lat_b = request.GET.get("lat_b")
        long_b = request.GET.get("long_b")
        rideid = request.GET.get("rid") if request.GET.get("rid") else request.POST.get("rid")
        ridesta = Ride.objects.get(id=rideid)
        directions = Directions(
            lat_a= lat_a,
            long_a=long_a,
            lat_b = lat_b,
            long_b=long_b
            )
        context = {
            "google_api_key": settings.GOOGLE_API_KEY,
            "lat_a": lat_a,
            "long_a": long_a,
            "lat_b": lat_b,
            "long_b": long_b,
            "rid": rideid,
            "origin": f'{lat_a}, {long_a}',
            "destination": f'{lat_b}, {long_b}',
            "directions": directions,
            "title" : "Location Tracker Map View",
            "status" : ridesta.trip_status,
            "car" : ridesta.ride_type,
            "lat2" : ridesta.car_latitude,
            'lng2' : ridesta.car_longitude,
        }
        
        if request.method == "POST":
            rideid = request.POST.get("rid")
            timer = request.POST.get("time")
            km = request.POST.get("km")
            ridesta = Ride.objects.get(id=rideid)
            if ridesta.status == '0' and ridesta.publish == '0':
                timer = timer.replace('hours','H').replace('mins','M')
                if ridesta.as_user == "Passenger":
                    ridesta.dtime = timer
                    ridesta.map_date = timer
                    ridesta.publish = '1'
                    ridesta.save()
                if ridesta.as_user == "Driver":
                    km1 = re.sub(",","",km)
                    realkm = float(km1.replace("km",""))
                    price = realkm * float(ridesta.per_km)
                    fees = float(price) / int(ridesta.seats)
                    ridesta.fees = fees
                    ridesta.map_date = timer
                    ridesta.publish = '1'
                    ridesta.save()
            # rides = Ride.objects.filter(publish='0')
            # for i in rides:
            #     i.delete()
            directions = Directions(
                lat_a= lat_a,
                long_a=long_a,
                lat_b = lat_b,
                long_b=long_b
                )
            context = {
                "rid": rideid,
                'current_lat' : ridesta.car_latitude,
                'current_lng' : ridesta.car_longitude,
                'statuss' : ridesta.trip_status
            }
            return JsonResponse(context)
        return render(request, 'doxer_admin/maps.html', context)
    except:
        return redirect("doxer_admin:allrides")
        # return render(request,'Direction/Direction.html')

@csrf_exempt
def Id_proofes(request,pk):
    if pk == '1':
        id = request.POST.get('id')
        getid = user_all.objects.get(id=id,as_user='Driver')
        if getid.image1:
            image1 = getid.image1.url
        else:
            image1 = '0'
        if getid.image2:
            image2 = getid.image2.url
        else:
            image2 = '0'
            
        return JsonResponse({"name":getid.name.title(),"id1":image1,"id2":image2})
    if pk == '2':
        id = request.POST.get('id')
        getid = user_all.objects.get(id=id,as_user='Passenger')
        if getid.image1:
            image1 = getid.image1.url
        else:
            image1 = '0'
        if getid.image2:
            image2 = getid.image2.url
        else:
            image2 = '0'
        return JsonResponse({"name":getid.name.title(),"id1":image1,"id2":image2})

def mobile_map(request):
    try:
        lat_a = request.GET.get("lat_a")
        long_a = request.GET.get("long_a")
        lat_b = request.GET.get("lat_b")
        long_b = request.GET.get("long_b")
        rideid = request.GET.get("rid") if request.GET.get("rid") else request.POST.get("rid")
        ridesta = Ride.objects.get(id=rideid)
        print(ridesta)
        directions = Directions(
            lat_a= lat_a,
            long_a=long_a,
            lat_b = lat_b,
            long_b=long_b
            )
        context = {
            "google_api_key": settings.GOOGLE_API_KEY,
            "lat_a": lat_a,
            "long_a": long_a,
            "lat_b": lat_b,
            "long_b": long_b,
            "rid": rideid,
            "origin": f'{lat_a}, {long_a}',
            "destination": f'{lat_b}, {long_b}',
            "directions": directions,
            "title" : "Location Tracker Map View",
            "status" : ridesta.trip_status,
            "car" : ridesta.ride_type,
            "lat2" : ridesta.car_latitude,
            'lng2' : ridesta.car_longitude,
        }
        
        if request.method == "POST":
            rideid = request.POST.get("rid")
            timer = request.POST.get("time")
            km = request.POST.get("km")
            print('km',km)
            ridesta = Ride.objects.get(id=rideid)
            if ridesta.status == '0' and ridesta.publish == '0':
                timer = timer.replace('hours','H').replace('mins','M')
                if ridesta.as_user == "Passenger" and ridesta.trip_status == 'P':
                    ridesta.dtime = timer #.replace("hour",":")
                    ridesta.map_date = timer #.replace("mins",":")
                    ridesta.publish = '1'
                    ridesta.save()
                    print('passenger save',ridesta.id)
                if ridesta.as_user == "Driver" and ridesta.trip_status == 'P':
                    km1 = re.sub(",","",km)
                    realkm = float(km1.replace("km",""))
                    price = realkm * float(ridesta.per_km)
                    fees = float(price) / int(ridesta.seats)
                    # ridesta.fees = fees
                    ridesta.map_date = timer
                    ridesta.publish = '1'
                    ridesta.save()
                    print('driver save',ridesta.id)
            directions = Directions(
                lat_a= lat_a,
                long_a=long_a,
                lat_b = lat_b,
                long_b=long_b
                )
            context = {
                "rid": rideid,
                'current_lat' : ridesta.car_latitude,
                'current_lng' : ridesta.car_longitude
            }
            return JsonResponse(context)
        return render(request, 'doxer_admin/mobile-maps.html', context)
    except:
        return render(request,'Direction/Direction.html')

@csrf_exempt
def Id_Approval(request,pk):
    if pk == '1':
        id = request.POST.get('id')
        data = request.POST.get('sta')
        getid = user_all.objects.get(id=id,as_user='Driver')
        if data == "P" or data == "A" or data == "R":
            if getid.image1 or getid.image2:
                if data == "A" and (getid.fare_per_km == "0" or getid.fare_per_km == "0.00" or getid.fare_per_km == 0 or getid.fare_per_km == 0.00):
                    return JsonResponse({"status":3,"msg":"Please Add Price For Driver's Ride Per Km",'st':getid.img_status,'getid':id,"email" : getid.name.title(),"fees":getid.fare_per_km})
                getid.img_status = data
                getid.save()
            else:
                return JsonResponse({"status":2,"msg":"User Doesn't Upload Their ID!"})
            if getid.img_status == "P":
                msg = "Pending"
            if getid.img_status == "A":
                msg = "Approved"
                send_notification([getid.ntk] , 'Account verification alert!' , 'Your Driver account has been approved.')
            if getid.img_status == "R":
                msg = "Rejected"
                # send_notification([getid.ntk] , 'Account verification alert!' , 'Your Driver account has been rejected.')
            return JsonResponse({"status":1,"msg":msg,'st':getid.img_status,'getid':id})
        else:
            return JsonResponse({"status":0,"msg":"Error"})
    if pk == '2':
        id = request.POST.get('id')
        data = request.POST.get('sta')
        getid = user_all.objects.get(id=id,as_user='Passenger')
        if data == "P" or data == "A" or data == "R":
            if getid.image1 or getid.image2:
                getid.img_status = data
                getid.save()
            else:
                return JsonResponse({"status":2,"msg":"User Doesn't Upload Their ID!"})
            if getid.img_status == "P":
                msg = "Pending"
            if getid.img_status == "A":
                msg = "Approved"
                send_notification([getid.ntk] , 'Account verification alert!' , 'Your Passenger account has been approved.')
            if getid.img_status == "R":
                msg = "Rejected"
                # send_notification([getid.ntk] , 'Account verification alert!' , 'Your Passenger account has been rejected.')
            return JsonResponse({"status":1,"msg":msg,'st':getid.img_status,'getid':id})
        else:
            return JsonResponse({"status":0,"msg":"Error"})

@csrf_exempt
def Id_With_price(request):
    if 'id' in request.session:
        try:    
            if request.method=='POST':
                id = request.POST.get('pid')
                price = float(request.POST.get('price'))
                showtime = strftime("%Y-%m-%d %H:%M:%S", )
                getpas = user_all.objects.get(pk=id,as_user='Driver')
                getpas.fare_per_km = price
                if price == 0.00 or price == "0.00" or price == 0 or price == "0":
                    return JsonResponse({'status':22,"msg" : "Please Enter Valid Price"})
                getpas.img_status = "A"
                getpas.save()
                send_notification([getpas.ntk] , 'Account verification alert!' , 'Your Driver account has been approved.')
                price = int(price)
                drive_name = getpas.name.title() if getpas.name.title() else getpas.email_or_num
                prices = f"{drive_name}'s Price {format(price, '.2f')} Credited Successfully..!"
                return JsonResponse({'status':11,'update_value' : prices,'price' : format(price, '.2f'),'msg':"Approved",'st':getpas.img_status,'getid':id})
            else:
                return JsonResponse({'status':0})
        except:
            return JsonResponse({'status':2})
    else:
        return JsonResponse({'status':2})

def Incityride_Map(request):
    try:
        lat_a = request.GET.get("lat_a")
        long_a = request.GET.get("long_a")
        lat_b = request.GET.get("lat_b")
        long_b = request.GET.get("long_b")
        rideid = request.GET.get("rid") if request.GET.get("rid") else request.POST.get("rid")
        ridesta = InRide.objects.get(id=rideid)
        directions = Directions(
            lat_a= lat_a,
            long_a=long_a,
            lat_b = lat_b,
            long_b=long_b
            )
        context = {
            "google_api_key": settings.GOOGLE_API_KEY,
            "lat_a": lat_a,
            "long_a": long_a,
            "lat_b": lat_b,
            "long_b": long_b,
            "rid": rideid,
            "origin": f'{lat_a}, {long_a}',
            "destination": f'{lat_b}, {long_b}',
            "directions": directions,
            "title" : "Location Tracker Map View",
            "status" : ridesta.trip_status,
            "car" : "C",
            "lat2" : ridesta.driver_latitude,
            'lng2' : ridesta.driver_longitude,
        }
        
        if request.method == "POST":
            rideid = request.POST.get("rid")
            timer = request.POST.get("time")
            km = request.POST.get("km")
            ridesta = InRide.objects.get(id=rideid)
            # if ridesta.status == '0' and ridesta.publish == '0':
            #     timer = timer.replace('hours','H').replace('mins','M')
            #     if ridesta.as_user == "Passenger" and ridesta.trip_status == 'P':
            #         ridesta.dtime = timer #.replace("hour",":")
            #         ridesta.map_date = timer #.replace("mins",":")
            #         ridesta.publish = '1'
            #         ridesta.save()
            #     if ridesta.as_user == "Driver" and ridesta.trip_status == 'P':
            #         km1 = re.sub(",","",km)
            #         realkm = float(km1.replace("km",""))
            #         price = realkm * float(ridesta.per_km)
            #         fees = float(price) / int(ridesta.seats)
            #         ridesta.fees = fees
            #         ridesta.map_date = timer
            #         ridesta.publish = '1'
            #         ridesta.save()
            directions = Directions(
                lat_a= lat_a,
                long_a=long_a,
                lat_b = lat_b,
                long_b=long_b
                )
            context = {
                "rid": rideid,
                'current_status' : ridesta.trip_status,
                'current_lat' : ridesta.driver_latitude,
                'current_lng' : ridesta.driver_longitude
            }
            return JsonResponse(context)
        return render(request, 'doxer_admin/mobile-Inmaps.html', context)
    except:
        return render(request,'Direction/Direction.html')

def manage_brand(request,tt):
    if 'id' in request.session:
        allcolor = Vehical_Color.objects.all()
        dimension = Vehical_dimensions.objects.all()
        if tt == "Trucks" or tt == "trucks":
            type = "Trucks"
            ve = '1'
            allbrand = Vehical_brand.objects.filter(vehical_type=ve)
            allCar_name = Car_name.objects.filter(vehicle_type="T")
            context = {
                't1' : '6',
                'title': f"All Brands & {type} Manage Page",
                "type":tt,
                "brand" : allbrand,
                "Cars" : allCar_name,
                "colors" : allcolor,
                "dimension" : dimension
            }
            return render(request,'doxer_admin/manage-brands.html',context)
        elif tt == "Auto" or tt == "auto":
            type = "Auto"
            ve = '4'
            allCar_name = Car_name.objects.filter(vehicle_type="A")
            allbrand = Vehical_brand.objects.filter(vehical_type=ve)
            context = {
                't1' : '6',
                'title': f"All Brands & {type} Manage Page",
                "type":tt,
                "brand" : allbrand,
                "Cars" : allCar_name,
                "colors" : allcolor,
                "dimension" : dimension
            }
            return render(request,'doxer_admin/manage-brands.html',context)
        elif tt == "Bike" or tt == "bike":
            type = "Bike"
            ve = '3'
            allCar_name = Car_name.objects.filter(vehicle_type="B")
            allbrand = Vehical_brand.objects.filter(vehical_type=ve)
            context = {
                't1' : '6',
                'title': f"All Brands & {type} Manage Page",
                "type":tt,
                "brand" : allbrand,
                "Cars" : allCar_name,
                "colors" : allcolor,
                "dimension" : dimension
            }
            return render(request,'doxer_admin/manage-brands.html',context)
        elif tt == "Cars" or tt == "cars":
            type = "Cars"
            ve = '2'
            allCar_name = Car_name.objects.filter(vehicle_type="C")
            allbrand = Vehical_brand.objects.filter(vehical_type=ve)
            context = {
                't1' : '6',
                'title': f"All Brands & {type} Manage Page",
                "type":tt,
                "brand" : allbrand,
                "Cars" : allCar_name,
                "colors" : allcolor,
                "dimension" : dimension
            }
            return render(request,'doxer_admin/manage-brands.html',context)
        else:
            return render(request,'Direction/error404.html')
    else:
        return redirect('doxer_admin:loginpage')

def DeteleVehical_brand(request,data,tt):
    if 'id' in request.session:
        try:
            getid = Vehical_brand.objects.get(id=data)
            getid.delete()
            return redirect("doxer_admin:manage_brand",tt)
        except:
            return redirect("doxer_admin:manage_brand",tt)
    else:
        return redirect('doxer_admin:loginpage')
    
def DeteleCar_name(request,data,tt):
    if 'id' in request.session:
        try:
            getid = Car_name.objects.get(id=data)
            getid.delete()
            return redirect("doxer_admin:manage_brand",tt)
        except:
            return redirect("doxer_admin:manage_brand",tt)
    else:
        return redirect('doxer_admin:loginpage')
    
# def add_vehical_form(request,tt):
#     if 'id' in request.session:
#         allcolor = Vehical_Color.objects.all()
#         dimension = Vehical_dimensions.objects.all()
#         if tt == "Trucks" or tt == "trucks":
#             type = "Trucks"
#             ve = '1'
#             allbrand = Vehical_brand.objects.filter(vehical_type=ve)
#             context = {
#                 't1' : '6',
#                 'barnd':allbrand,
#                 'title': f"{type} From Page",
#                 "type":tt,
#                 "colors" : allcolor,
#                 "dimension" : dimension
#             }
#             return render(request,'doxer_admin/form-model-add.html',context)
#         elif tt == "Auto" or tt == "auto":
#             ve = '4'
#             type = "Auto"
#             allbrand = Vehical_brand.objects.filter(vehical_type=ve)
#             context = {
#                 't1' : '6',
#                 'barnd':allbrand,
#                 'title': f"{type} From Page",
#                 "type":tt,
#                 "colors" : allcolor,
#                 "dimension" : dimension
#             }
#             return render(request,'doxer_admin/form-model-add.html',context)
#         elif tt == "Bike" or tt == "bike":
#             ve = '3'
#             type = "Bike"
#             allbrand = Vehical_brand.objects.filter(vehical_type=ve)
#             context = {
#                 't1' : '6',
#                 'barnd':allbrand,
#                 'title': f"{type} From Page",
#                 "type":tt,
#                 "colors" : allcolor,
#                 "dimension" : dimension
#             }
#             return render(request,'doxer_admin/form-model-add.html',context)
#         elif tt == "Cars" or tt == "cars":
#             ve = '2'
#             type = "Cars"
#             allbrand = Vehical_brand.objects.filter(vehical_type=ve)
#             context = {
#                 't1' : '6',
#                 'barnd':allbrand,
#                 'title': f"{type} From Page",
#                 "type":tt,
#                 "colors" : allcolor,
#                 "dimension" : dimension
#             }
#             return render(request,'doxer_admin/form-model-add.html',context)
#         else:
#             return render(request,'Direction/error404.html')
#     else:
#         return redirect('doxer_admin:loginpage')

def add_vehical_store(request,tt):
    if request.method == "POST":
        if tt == "Trucks" or tt == "trucks":
            types = "T"
        if tt == "Auto" or tt == "auto":
            types = "A"
        if tt == "Bike" or tt == "bike":
            types = "B"
        if tt == "Cars" or tt == "cars":
            types = "C"
        showtime = strftime("%Y-%m-%d %H:%M:%S", )
        model_name = request.POST['model_name']
        company_name = request.POST['company_name']
        model_image = request.FILES['avatar']
        colordrop = request.POST['colordrop']
        if colordrop != "0":
            ls = []
            var = ""
            for i in colordrop:
                var = var + i.replace(',','')
                if i == ',':
                    ls.append(var)
                    var = ""
        else:
            ls = []
            
        dimensiondrop = request.POST['dimensiondrop']
        if dimensiondrop != "0":
            lis = []
            varw = ""
            for ii in dimensiondrop:
                varw = varw + ii.replace(',','')
                if ii == ',':
                    lis.append(varw)
                    varw = ""
        else:
            lis = []
                    
        brand = Vehical_brand.objects.get(id=company_name)
        car = Car_name.objects.create(
            cars = model_name,
            # colors = colordrop,
            # dimension = dimensiondrop,
            brand = brand,
            photo_of_vehicle = model_image,
            vehicle_type = types,
            create_at = showtime,
            update_at = showtime,
        )
        if ls:
            for hs in ls:
                car.colors.add(hs)
                car.save()
        if lis:
            for h in lis:
                car.dimension.add(h)
                car.save()
        
        return redirect('doxer_admin:manage_brand',tt)
    else:
        return redirect('doxer_admin:manage_brand',tt)
        
def add_brand_store(request,tt):
    if request.method == "POST":
        if tt == "Trucks" or tt == "trucks":
            allbrand = Vehical_Type.objects.get(vehical_type="Truck")
        if tt == "Auto" or tt == "auto":
            types = "A"
            allbrand = Vehical_Type.objects.get(vehical_type="Auto")
        if tt == "Bike" or tt == "bike":
            types = "B"
            allbrand = Vehical_Type.objects.get(vehical_type="Bike")
        if tt == "Cars" or tt == "cars":
            types = "C"
            allbrand = Vehical_Type.objects.get(vehical_type="Car")
        showtime = strftime("%Y-%m-%d %H:%M:%S", )
        Brand_name = request.POST['Brand_name'].title()
        if(not Brand_name):
            response = {
                "status":0,'msg':'Please Add Brand Name.'
            }
            return JsonResponse(response)
        
        car = Vehical_brand.objects.create(
            brand = Brand_name,
            vehical_type = allbrand,
            create_at = showtime,
            update_at = showtime,
        )
        response = {
            "status":1,'msg':'Your form has been submitted successfully'
        }
        return JsonResponse(response)
        # return redirect('doxer_admin:manage_brand',tt)
    else:
        return redirect('doxer_admin:manage_brand',tt)
    