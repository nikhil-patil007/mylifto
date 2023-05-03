from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from django.core.exceptions import *
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers  import make_password,check_password
from . import driver,passenger
from time import gmtime, strftime

email_pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
mobile_pattern = '^[0-9]{10,20}$'

import math,random
from random import randint
import re
def genrateOtp():
    digits = '0123456789'
    OTP = ''
    for i in range(4):
        OTP += digits[math.floor(random.random()*10)]
    return OTP

# All City Filter   
@api_view(['GET'])
def AllCities(request):
    data = request.data
    city = Cities.objects.all()
    allcity = CitySerializer(city,many=True)
    return Response(allcity.data)

# Search City Name
@api_view(['POST'])
def SerachCities(request):
    data = request.data
    cit = data['name'].casefold()
    name = cit.capitalize()
    city = Cities.objects.filter(name__startswith=name)
    if len(city) > 0:
        ls = []
        for i in city:
            dic = {}
            dic['city'] = i.name.capitalize()
            ls.append(dic)
        return Response({'status':1 ,'msg': 'City Founded','name' : ls})
    else:
        return Response({'status':0 ,"msg":"Record Not Founded"})

@api_view(['GET'])
def GetRides(request):
    ride = Ride.objects.all()
    gets = RideSerializer(ride,many=True)
    return Response({"status" : 1,"msg" : "success","data" : gets.data})

@api_view(['GET'])
def ShowAllBrand(request,tt):
    if tt == "T" or tt == "t":
        ve = '1'
    if tt == "A" or tt == "a":
        ve = '4'
    if tt == "B" or tt == "b":
        ve = '3'
    if tt == "C" or tt == "c":
        ve = '2'
    allbrand = Vehical_brand.objects.filter(vehical_type=ve)
    serial = Vehical_brandSeializer(allbrand,many=True)
    return Response({'status':1,"msg":"success","data":serial.data})

@api_view(['GET'])
def ShowCarOfBrand(request,pk):
    try:
        brand = Vehical_brand.objects.get(id=pk)
        allc = Car_name.objects.filter(brand=brand)
        if allc:
            se = CarsSeializer(allc,many=True)
            return Response({'status':1,"msg":"success","data":se.data})
        else:
            return Response({'status':0,"msg":"No Record"})
    except ObjectDoesNotExist:
        return Response({'status':0,"msg":"Wrong Id"})

@api_view(['GET'])
def ShowCarOfColors(request,pk):
    try:
        brand = Car_name.objects.get(id=pk)
        allc = brand.colors.all()
        if allc:
            lis = []
            for i in allc:
                res = {}
                res['color_name'] = i.vehical_color
                lis.append(res)
            return Response({'status':1,"msg":"success","data":lis})
        else:
            return Response({'status':0,"msg":"No Record"})
    except ObjectDoesNotExist:
        return Response({'status':0,"msg":"Wrong Id"})

@api_view(['GET'])
def ShowCarOfDimensions(request,pk):
    try:
        brand = Car_name.objects.get(id=pk)
        allc = brand.dimension.all()
        if allc:
            lis = []
            for i in allc:
                res = {}
                res['dimension'] = i.dimension
                lis.append(res)
            return Response({'status':1,"msg":"success","data":lis})
        else:
            return Response({'status':0,"msg":"No Record"})
    except ObjectDoesNotExist:
        return Response({'status':0,"msg":"Wrong Id"})

@api_view(['GET'])    
def Account_listing(request,Id):
    ac = User_login.objects.filter(DeviceId=Id)
    if len(ac) > 0:
        ls = []
        for i in ac:
            res = {}
            res['as_user'] = i.as_user
            res['User_id'] = i.user_id.id
            res['User_name'] = i.user_id.name.title()
            res['User_email'] = i.user_id.email if i.user_id.email else ''
            res['User_contact_no'] = i.user_id.contact_no if i.user_id.contact_no else ''
            if i.user_id.pro_image:
                res['User_Profile'] = i.user_id.pro_image.url
            else:
                res['User_Profile'] = ''
            ls.append(res)
        return Response({'status': 1,"msg": "success","data" : ls})
    else:
        return Response({'status': 1,"msg": "success","data" : []})
        
@api_view(['POST'])
def LogOut_account(request):
    try:
        data = request.data
        as_user = data['as_user']
        user_id = data['user_id']
        DeviceId = data['DeviceId']
        # if (not as_user):
        #     return Response({'status':0,'msg':"User Type Is Not Added!"})
        # if (not user_id):
        #     return Response({'status':0,'msg':"User Id Is Required!"})
        # if (not DeviceId):
        #     return Response({'status':0,'msg':"Device Id Is Required!"})
        
        ac = User_login.objects.filter(DeviceId=DeviceId,as_user=as_user,user_id=user_id)
        if len(ac) > 0:
            ac[0].delete()
            return Response({'status':1,"msg":"Logout Successfully"})
        else:
            return Response({'status':1,"msg":"Logout Successfully"})
    except:
        return Response({'status':1,"msg":"Logout Successfully"})


@api_view(['GET'])
def Id_Verify_status(request,Id):
    try:
        getuser = user_all.objects.get(id=Id)
        if getuser.img_status == "P":
            if getuser.image1 or getuser.image2:
                return Response({'status':3,"msg":"Your Id Verification still pending."})
            else:
                return Response({'status':0,"msg":"Please upload your ID to verify your account."})
        if getuser.img_status == "A":
            return Response({'status':1,"msg":"ID Verification Successfully."})
        if getuser.img_status == "R":
            return Response({'status': 2,"msg":"Please upload your Valid ID to verify your account."})
    except:
        return Response({'status':0,"msg":"Id Is Not Founded"})
        
        
@api_view(["POST"])
def MultiLogin(request):
    data = request.data
    raw = data['email_or_num'].casefold()
    getpass = data['password']
    # nks = data['token']
    nks = ''
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
          
        if(re.search(email_pattern, raw)):
            mail = user_all.objects.filter(email=raw,as_user = 'Driver').exclude(active_ac_with_otp="0")
            mail1 = user_all.objects.filter(email=raw,as_user = 'Passenger').exclude(active_ac_with_otp="0")
            
            if len(mail) > 0 and len(mail1) > 0:
                dri = user_all.objects.get(id=mail[0].id,as_user = 'Driver')
                pas = user_all.objects.get(id=mail1[0].id,as_user = 'Passenger')
                if dri.status == 'Active' or pas.status == 'Active':
                    passwrd = check_password(getpass, dri.password)
                    passwrd1 = check_password(getpass, pas.password)
                    # Both
                    if passwrd and passwrd1:
                        dri = user_all.objects.get(id=dri.id,as_user = 'Driver')
                        dri.ntk = nks
                        pas = user_all.objects.get(id=pas.id,as_user = 'Passenger')
                        pas.ntk = nks
                        
                        if dri.status == 'Active' and pas.status == 'Deactive':
                            dri.save()
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
                            Driver_name = dri.name.title() 
                            Passenger_name = ""
                            return Response({"status" : 1 , "msg" : "Login Success","Driver_id": f"{dri.id}","Passenger_id": f"0",'Driver_name':Driver_name,"Passenger_name":Passenger_name,"data":"2"})
                        
                        if dri.status == 'Deactive' and pas.status == 'Active':
                            pas.save()
                            logi1 = User_login.objects.filter(as_user='Passenger',user_id=pas,DeviceId=DeviceId)
                            if len(logi1) > 0:
                                pass
                            else:
                                logi = User_login.objects.create(
                                    as_user = 'Passenger',
                                    user_id = pas,
                                    DeviceId = DeviceId,
                                    ntk = nks,
                                    create_at = showtime
                                )
                            Driver_name = ""
                            Passenger_name = pas.name.title()
                            return Response({"status" : 1 , "msg" : "Login Success","Driver_id": f"0","Passenger_id": f"{pas.id}",'Driver_name':Driver_name,"Passenger_name":Passenger_name,"data":"3"})
                        dri.save()
                        pas.save()
                        Driver_name = dri.name.title()
                        Passenger_name = pas.name.title()
                        return Response({"status" : 1 , "msg" : "Login Success","Driver_id": f"{dri.id}","Passenger_id": f"{pas.id}",'Driver_name':Driver_name,"Passenger_name":Passenger_name,"data":"1"})
                    
                    # Driver
                    elif passwrd:
                        dri = user_all.objects.get(id=dri.id,as_user = 'Driver')
                        dri.ntk = nks
                        if dri.status == 'Active' and pas.status == 'Deactive':
                            dri.save()
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
                            Driver_name = dri.name.title() 
                            Passenger_name = ""
                            return Response({"status" : 1 , "msg" : "Login Success","Driver_id": f"{dri.id}","Passenger_id": f"0",'Driver_name':Driver_name,"Passenger_name":Passenger_name,"data":"2"})
                        else:
                            return Response({"status" : 0 , "msg" : "Account Is Blocked"})
                        
                    # Passenger
                    elif passwrd1:
                        pas = user_all.objects.get(id=pas.id,as_user = 'Passenger')
                        pas.ntk = nks
                        if dri.status == 'Deactive' and pas.status == 'Active':
                            pas.save()
                            
                            logi1 = User_login.objects.filter(as_user='Passenger',user_id=pas,DeviceId=DeviceId)
                            if len(logi1) > 0:
                                pass
                            else:
                                logi = User_login.objects.create(
                                    as_user = 'Passenger',
                                    user_id = pas,
                                    DeviceId = DeviceId,
                                    ntk = nks,
                                    create_at = showtime
                                )
                            Driver_name = ""
                            Passenger_name = pas.name.title()
                            return Response({"status" : 1 , "msg" : "Login Success","Driver_id": f"0","Passenger_id": f"{pas.id}",'Driver_name':Driver_name,"Passenger_name":Passenger_name,"data":"3"})
                        else:
                            return Response({"status" : 0 , "msg" : "Account Is Blocked"})
                    else:
                        return Response({"status" : 0 , "msg" : "Password Is Wrong"})
                else:
                    return Response({"status" : 0 , "msg" : "Account Is Blocked"})
            
            elif len(mail) > 0:
                dri = user_all.objects.get(id=mail[0].id,as_user = 'Driver')
                if dri.active_ac_with_otp == "0":
                    return Response({"status" : 0 , "msg" : "Account Is Not Created"})
                else:
                    if dri.status == 'Active':
                        passwrd = check_password(getpass, dri.password)
                        if passwrd:
                            dri = user_all.objects.get(id=dri.id,as_user = 'Driver')
                            dri.ntk = nks
                            dri.save()
                            logi = User_login.objects.filter(as_user='Driver',user_id=dri,DeviceId=dri.DeviceId)
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
                            Driver_name = dri.name.title() 
                            Passenger_name = ""
                            return Response({"status" : 1 , "msg" : "Login Success","Driver_id": f"{dri.id}","Passenger_id": f"0",'Driver_name':Driver_name,"Passenger_name":Passenger_name,"data":"2"})
                        else:
                            return Response({"status" : 0 , "msg" : "Password Is Wrong"})
                    else:
                        return Response({"status" : 0 , "msg" : "Account Is Blocked"})
            
            elif len(mail1) > 0:
                pas = user_all.objects.get(id=mail1[0].id,as_user = 'Passenger')
                if pas.active_ac_with_otp == "0":
                    return Response({"status" : 0 , "msg" : "Account Is Not Created"})
                else:
                    if pas.status == 'Active':
                        passwrd = check_password(getpass, pas.password)
                        if passwrd:
                            pas = user_all.objects.get(id=pas.id,as_user = 'Passenger')
                            pas.ntk = nks
                            pas.save()
                            logi = User_login.objects.filter(as_user='Passenger',user_id=pas,DeviceId=pas.DeviceId)
                            if len(logi) > 0:
                                pass
                            else:
                                logi = User_login.objects.create(
                                    as_user = 'Passenger',
                                    user_id = pas,
                                    DeviceId = DeviceId,
                                    ntk = nks,
                                    create_at = showtime
                                )
                            Driver_name = ""
                            Passenger_name = pas.name.title()
                            return Response({"status" : 1 , "msg" : "Login Success","Driver_id": f"0","Passenger_id": f"{pas.id}",'Driver_name':Driver_name,"Passenger_name":Passenger_name,"data":"3"})
                        else:
                            return Response({"status" : 0 , "msg" : "Password Is Wrong"})
                    else:
                        return Response({"status" : 0 , "msg" : "Account Is Blocked"})
            
            else:
                return Response({"status" : 0 , "msg" : "Unknown User Please Signup First."})  
        else:
            # if raw[0] == '0' or raw[0] == 0:
            #     raw = raw
            # else:
            #     raw = f"0{raw}"
            num = user_all.objects.filter(contact_no=raw,as_user = 'Driver').exclude(active_ac_with_otp="0")
            num1 = user_all.objects.filter(contact_no=raw,as_user = 'Passenger').exclude(active_ac_with_otp="0")
            # Both
            if len(num) > 0 and len(num1) >0:
                print("if 1")
                dri = user_all.objects.get(id=num[0].id,as_user = 'Driver')
                pas = user_all.objects.get(id=num1[0].id,as_user = 'Passenger')
                if dri.status == 'Active' or pas.status == 'Active':
                    passwrd = check_password(getpass, dri.password)
                    passwrd1 = check_password(getpass, pas.password)
                    # Both
                    if passwrd and passwrd1:
                        dri = user_all.objects.get(id=dri.id,as_user = 'Driver')
                        dri.ntk = nks
                        pas = user_all.objects.get(id=pas.id,as_user = 'Passenger')
                        pas.ntk = nks
                        if dri.status == 'Active' and pas.status == 'Deactive':
                            dri.save()
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
                            Driver_name = dri.name.title() 
                            Passenger_name = ""
                            return Response({"status" : 1 , "msg" : "Login Success","Driver_id": f"{dri.id}","Passenger_id": f"0",'Driver_name':Driver_name,"Passenger_name":Passenger_name,"data":"2"})

                        pas = user_all.objects.get(id=pas.id,as_user = 'Passenger')
                        pas.ntk = nks
                        if dri.status == 'Deactive' and pas.status == 'Active':
                            pas.save()
                            logi1 = User_login.objects.filter(as_user='Passenger',user_id=pas,DeviceId=DeviceId)
                            if len(logi1) > 0:
                                pass
                            else:
                                logi = User_login.objects.create(
                                    as_user = 'Passenger',
                                    user_id = pas,
                                    DeviceId = DeviceId,
                                    ntk = nks,
                                    create_at = showtime
                                )
                            Driver_name = ""
                            Passenger_name = pas.name.title()
                            return Response({"status" : 1 , "msg" : "Login Success","Driver_id": f"0","Passenger_id": f"{pas.id}",'Driver_name':Driver_name,"Passenger_name":Passenger_name,"data":"3"})
                        
                        dri.save()
                        pas.save()     
                        Driver_name = dri.name.title()
                        Passenger_name = pas.name.title()
                        return Response({"status" : 1 , "msg" : "Login Success","Driver_id": f"{dri.id}","Passenger_id": f"{pas.id}",'Driver_name':Driver_name,"Passenger_name":Passenger_name,"data":"1"})
                    
                    # Driver
                    elif passwrd:
                        dri = user_all.objects.get(id=dri.id,as_user = 'Driver')
                        dri.ntk = nks
                        if dri.status == 'Active' and pas.status == 'Deactive':
                            dri.save()
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
                            Driver_name = dri.name.title() 
                            Passenger_name = ""
                            return Response({"status" : 1 , "msg" : "Login Success","Driver_id": f"{dri.id}","Passenger_id": f"0",'Driver_name':Driver_name,"Passenger_name":Passenger_name,"data":"2"})
                        else:
                            return Response({"status" : 0 , "msg" : "Account Is Blocked"})

                    # Passenger
                    elif passwrd1:
                        pas = user_all.objects.get(id=pas.id,as_user = 'Passenger')
                        pas.ntk = nks
                        if dri.status == 'Deactive' and pas.status == 'Active':
                            pas.save()
                            
                            logi1 = User_login.objects.filter(as_user='Passenger',user_id=pas,DeviceId=DeviceId)
                            if len(logi1) > 0:
                                pass
                            else:
                                logi = User_login.objects.create(
                                    as_user = 'Passenger',
                                    user_id = pas,
                                    DeviceId = DeviceId,
                                    ntk = nks,
                                    create_at = showtime
                                )
                            Driver_name = ""
                            Passenger_name = pas.name.title()
                            return Response({"status" : 1 , "msg" : "Login Success","Driver_id": f"0","Passenger_id": f"{pas.id}",'Driver_name':Driver_name,"Passenger_name":Passenger_name,"data":"3"})
                        else:
                            return Response({"status" : 0 , "msg" : "Account Is Blocked"})
                    else:
                        return Response({"status" : 0 , "msg" : "Password Is Wrong"})
                else:
                    return Response({"status" : 0 , "msg" : "Account Is Blocked"})

            # Driver
            elif len(num) > 0:
                print("if 2")
                dri = user_all.objects.get(id=num[0].id,as_user = 'Driver')
                if dri.status == 'Active':
                    passwrd = check_password(getpass, dri.password)
                    if passwrd:
                        dri = user_all.objects.get(id=dri.id,as_user = 'Driver')
                        dri.ntk = nks
                        dri.save()
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
                        Driver_name = dri.name.title() 
                        Passenger_name = ""
                        return Response({"status" : 1 , "msg" : "Login Success","Driver_id": f"{dri.id}","Passenger_id": f"0",'Driver_name':Driver_name,"Passenger_name":Passenger_name,"data":"2"})
                    else:
                        return Response({"status" : 0 , "msg" : "Password Is Wrong"})
                else:
                    return Response({"status" : 0 , "msg" : "Account Is Blocked"})
            
            # Passenger
            elif len(num1) > 0:
                print("if 3")
                pas = user_all.objects.get(id=num1[0].id,as_user = 'Passenger')
                if pas.status == 'Active':
                    passwrd = check_password(getpass, pas.password)
                    if passwrd:
                        pas = user_all.objects.get(id=pas.id,as_user = 'Passenger')
                        pas.ntk = nks
                        pas.save()
                        logi = User_login.objects.filter(as_user='Passenger',user_id=pas,DeviceId=DeviceId)
                        if len(logi) > 0:
                            pass
                        else:
                            logi = User_login.objects.create(
                                as_user = 'Passenger',
                                user_id = pas,
                                DeviceId = DeviceId,
                                ntk = nks,
                                create_at = showtime
                            )
                        Driver_name = ""
                        Passenger_name = pas.name.title()
                        return Response({"status" : 1 , "msg" : "Login Success","Driver_id": f"0","Passenger_id": f"{pas.id}",'Driver_name':Driver_name,"Passenger_name":Passenger_name,"data":"3"})
                    else:
                        return Response({"status" : 0 , "msg" : "Password Is Wrong"})
                else:
                    return Response({"status" : 0 , "msg" : "Account Is Blocked"})
                
            else:
                print("else")
                return Response({"status" : 0 , "msg" : "Unknown User Please Signup First."})
              

@api_view(['POST'])
def SignUp(request):
    if request.method  == "POST":
        data = request.data
        name = data['name'].casefold()
        per_km_price = '00'
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
            
        otp = ''
        for i in range (4):
            otp+=str(randint(1,9))
        
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
            if number:
            # if(re.search(mobile_pattern,number)):
                # if number[0] == '0' or number[0] == 0:
                #     number = number
                # else:
                #     number = f"0{number}"
                drive = user_all.objects.filter(as_user = "Driver",contact_no=number)
                passe = user_all.objects.filter(as_user = "Passenger",contact_no=number)
                if len(drive) > 0 and len(passe) > 0:
                    driveid = user_all.objects.get(id=drive[0].id)
                    passeid = user_all.objects.get(id=passe[0].id)
                    if driveid.status == 'Deactivate' and passeid.status == 'Deactivate':
                        return Response({'status' : 0 , 'msg' : "This Account has been Block"})
                    else:
                        if driveid.active_ac_with_otp == "0" and passeid.active_ac_with_otp == "0":
                            if password != cpassword:
                                    return Response({'status' : 0 , 'msg' : "Password Doesn't Match.!"})
                            else:
                                driveid.password = make_password(password)
                                driveid.cpassword = cpassword
                                driveid.otp = otp
                                driveid.name = name
                                driveid.image1 = Id_proofe1
                                driveid.fare_per_km = per_km_price
                                driveid.status = 'Active'
                                driveid.create_at = showtime
                                driveid.DeviceId = DeviceId
                                driveid.update_at = showtime
                                driveid.ntk = nks
                                driveid.active_ac_with_otp = "1"
                                driveid.save()

                                passeid.password = make_password(password)
                                passeid.cpassword = cpassword
                                passeid.otp = otp
                                passeid.name = name
                                passeid.image1 = Id_proofe1
                                passeid.active_ac_with_otp = "1"
                                passeid.fare_per_km = per_km_price
                                passeid.status = 'Active'
                                passeid.create_at = showtime
                                passeid.DeviceId = DeviceId
                                passeid.update_at = showtime
                                passeid.ntk = nks
                                passeid.save()
                                return Response({'status' : 1,'msg':'Register Succesfully','driver_Id' : driveid.id,'passenger_Id' : passeid.id,'Type': "Mobile" ,'OTP': passeid.otp})
                                # return Response({'status' : 1,'msg':'User Register Succesfully',"Id":getid.id,'Type':"Mobile",'OTP':getid.otp})
                        else:
                            return Response({'status' : 0 , 'msg' : "Phone Num Is Alread Used"})  
                else:
                    number = number     
            # else:
            #     return Response({'status' : 0 , 'msg' : "Phone Number Is Not Valid"})
            else:
                return Response({'status' : 0 , 'msg' : "Phone Number Is Required"})

            if email:                
                if(re.search(email_pattern, email)):
                    drive = user_all.objects.filter(as_user = "Driver",email=email)
                    passe = user_all.objects.filter(as_user = "Passenger",email=email)
                    if len(drive) > 0 and len(passe) > 0:
                        driveid = user_all.objects.get(id=drive[0].id)
                        passeid = user_all.objects.get(id=passe[0].id)
                        if driveid.status == 'Deactivate' and passeid.status == 'Deactivate':
                            return Response({'status' : 0 , 'msg' : "This Account has been Block"})
                        else:
                            if driveid.active_ac_with_otp == "0" and passeid.active_ac_with_otp == "0":
                                if password != cpassword:
                                        return Response({'status' : 0 , 'msg' : "Password Doesn't Match.!"})
                                else:
                                    driveid.password = make_password(password)
                                    driveid.cpassword = cpassword
                                    driveid.otp = otp
                                    driveid.name = name
                                    driveid.image1 = Id_proofe1
                                    driveid.fare_per_km = per_km_price
                                    driveid.status = 'Active'
                                    driveid.create_at = showtime
                                    driveid.DeviceId = DeviceId
                                    driveid.update_at = showtime
                                    driveid.active_ac_with_otp = "1"
                                    driveid.ntk = nks
                                    driveid.save()

                                    passeid.password = make_password(password)
                                    passeid.cpassword = cpassword
                                    passeid.otp = otp
                                    passeid.name = name
                                    passeid.image1 = Id_proofe1
                                    passeid.fare_per_km = per_km_price
                                    passeid.status = 'Active'
                                    passeid.create_at = showtime
                                    passeid.DeviceId = DeviceId
                                    passeid.update_at = showtime
                                    passeid.active_ac_with_otp = "1"
                                    passeid.ntk = nks
                                    passeid.save()

                                    mail_subject = 'Sign Up With Otp.'
                                    message = f'Hi {passeid.name.title()},\n Mail Sent Properly \n Otp is:-\'{passeid.otp}\'\n Thank You' 
                                    email_from = settings.EMAIL_HOST_USER
                                    to_email = [passeid.email,]
                                    send_mail(mail_subject, message, email_from, to_email)

                                    return Response({'status' : 1,'msg':'Register Succesfully','driver_Id' : driveid.id,'passenger_Id' : passeid.id,'Type': "Email" ,'OTP': passeid.otp})
                            else:
                                return Response({'status' : 0 , 'msg' : "Phone Num Is Alread Used"})  
                    else:
                        email = email
                else:
                    return Response({'status' : 0 , 'msg' : "Email Is Not Valid"})
            else:
                email = email

            if password != cpassword:
                return Response({'status' : 0 , 'msg' : "Password Doesn't Match.!"})
            else:
                driver = user_all.objects.create(
                    as_user = "Driver",
                    name = name,
                    fare_per_km = per_km_price,
                    email = email,
                    image1 = Id_proofe1,
                    active_ac_with_otp = "1",
                    contact_no = number,
                    DeviceId = DeviceId,
                    password = password,
                    cpassword = cpassword,
                    status = 'Active',
                    ntk = nks,
                    create_at = showtime,
                    update_at = showtime,
                )
                passenger = user_all.objects.create(
                    as_user = "Passenger",
                    name = name,
                    fare_per_km = per_km_price,
                    email = email,
                    image1 = Id_proofe1,
                    pro_image = "Users/passanger.png",
                    active_ac_with_otp = "1",
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
                
                passenger.password = make_password(passenger.password)
                passenger.cpassword = passenger.cpassword
                passenger.otp = otp
                passenger.save()
                if passenger.email or driver.email:
                    types = 'Email'
                    mail_subject = 'Sign Up With Otp.'
                    message = f'Hi {passenger.name.title()},\n Mail Sent Properly \n Otp is:-\'{passenger.otp}\'\n Thank You' 
                    email_from = settings.EMAIL_HOST_USER
                    to_email = [passenger.email,]
                    send_mail(mail_subject, message, email_from, to_email)
                    
                if passenger.contact_no or driver.contact_no:
                    types = 'Mobile'
            return Response({'status' : 1,'msg':'User Register Succesfully','driver_Id' : driver.id, 'passenger_Id' : passenger.id,'Type': types ,'OTP': driver.otp})

@api_view(["POST"])
def UserOtpVerification(request,dk,pk):
    try:
        data = request.data
        getotp = data['otp']
        showtime = data['datetime']
        otp = ''
        for i in range (4):
            otp+=str(randint(1,9))
        newotp = otp
        
        if(not getotp):
            return Response({"status" : 0 , "msg" : "OTP Field Is Required"})
            
        Driver = user_all.objects.get(id=dk,as_user = "Driver")
        Passenger = user_all.objects.get(id=pk,as_user = "Passenger")
        if Driver.active_ac_with_otp == "1" and Passenger.active_ac_with_otp == "1":
            return Response({"status" : 0 , "msg" : "Otp Already Verify"})
        else:
            if Driver.otp == getotp and Passenger.otp == getotp:
                Driver.active_ac_with_otp = "1"
                Driver.otp = newotp
                Driver.save()
                
                Passenger.active_ac_with_otp = "1"
                Passenger.otp = newotp
                Passenger.save()
                return Response({"status" : 1 , "msg" : "Otp Verify Successfully",'Driver_id':Driver.id,"Passenger_id":Passenger.id})
            else:
                return Response({"status" : 0 , "msg" : "Otp Is Not Match"})
    except:
        return Response({"status" : 0 , "msg" : "User Id Not Exists"})

@api_view(["GET"])
def ResendOtp(request,dk,pk,typ):
    # try:
    otp = ''
    for i in range (4):
        otp+=str(randint(1,9))
    newotp = otp
            
    Driver = user_all.objects.get(id=dk,as_user = "Driver")
    Passenger = user_all.objects.get(id=pk,as_user = "Passenger")
    if Driver.active_ac_with_otp == "1" and Passenger.active_ac_with_otp == "1":
        return Response({"status" : 0 , "msg" : "Otp Already Verify"})
    else:
        Driver.otp = newotp
        Driver.save()
        
        Passenger.otp = newotp
        Passenger.save()
        
        if typ == "Mobile" or typ == "mobile":
            return Response({'status' : 1 , 'msg' : "Otp Send Successfully Via Text","Driver_id" : Driver.id,"Passenger_id" :Passenger.id ,"otp":Driver.otp,'Type':"Mobile","token":Driver.ntk})
        
        if typ == "email" or typ == "Email":
            mail_subject = 'Sign Up With Otp.'
            message = f'Hi {Passenger.name.title()},\n Mail Sent Properly \n Otp is:-\'{Passenger.otp}\'\n Thank You' 
            email_from = settings.EMAIL_HOST_USER
            to_email = [Passenger.email,]
            send_mail(mail_subject, message, email_from, to_email)
            return Response({'status' : 1 , 'msg' : "Otp Send Successfully Via Email","Driver_id" : Driver.id,"Passenger_id" :Passenger.id ,"otp":Driver.otp,'Type':"Email","token":Driver.ntk})
    # except:
    #     return Response({"status" : 0 , "msg" : "User Id Not Exists"})
            
# @api_view(["POST"])
# def UserSelectRole(request,pk):
#     try:
#         data = request.data
#         getrole = data['role']
#         showtime = data['datetime']
        
#         if(not getrole):
#             return Response({"status" : 0 , "msg" : "Please Select Any Role Here"})
#         if getrole == 'p' or getrole == "P":
#             getrole = "Passenger"
#         elif getrole == 'd' or getrole == "D":
#             getrole = "Driver"
#         else:
#             return Response({"status" : 0 , "msg" : "Please Select Valid Role Here"})
            
#         dri = user_all.objects.get(id=pk)
#         if dri.active_ac_with_otp == "1":
#             return Response({"status" : 0 , "msg" : "User Is Already Exists"})
#         else:
#             dri.active_ac_with_otp = "1"
#             dri.as_user = getrole
#             dri.save()
#             logi = User_login.objects.filter(as_user=getrole,user_id=dri,DeviceId=dri.DeviceId)
#             if len(logi) > 0:
#                 pass
#             else:
#                 logi = User_login.objects.create(
#                     as_user = getrole,
#                     user_id = dri,
#                     DeviceId = dri.DeviceId,
#                     ntk = dri.ntk,
#                     create_at = showtime
#                 )
#             return Response({"status" : 1 , "msg" : "User Add Successfully",'id':dri.id,"Role" : dri.as_user})
#     except:
#         return Response({"status" : 0 , "msg" : "User Id Not Exists"})

@api_view(['POST'])
def checkUser(request):
    data = request.data
    number = data['number']
    email = data['email']
    if number and email:
        if(re.search(email_pattern, email)):
            drive = user_all.objects.filter(as_user = "Driver",contact_no=number).exclude(active_ac_with_otp="0")
            passe = user_all.objects.filter(as_user = "Passenger",contact_no=number).exclude(active_ac_with_otp="0")
            if len(drive) > 0 and len(passe) > 0:
                if drive[0].email or passe[0].email:
                    if (drive[0].email == email) or (passe[0].email == email):
                        return Response({"status":0,"msg":"Number and Email Already Used."})
                    else:
                        return Response({"status":0,"msg":"Number Already Used."})
                else:
                    return Response({"status":0,"msg":"Number Already Used."})
            else:
                return Response({"status":1,"msg":"Number and Email Not Used."})
        else:
            return Response({"status" : 0 , "msg" : "Please Add Vaild Email"})
        
    if number and (not email):
        drive = user_all.objects.filter(as_user = "Driver",contact_no=number).exclude(active_ac_with_otp="0")
        passe = user_all.objects.filter(as_user = "Passenger",contact_no=number).exclude(active_ac_with_otp="0")
        if len(drive) > 0 and len(passe) > 0:
            return Response({"status":0,"msg":"Number Already Used."})
        else:
            return Response({"status":1,"msg":"Number Not Used."})
    else:
        return Response({"status":0,"msg":"Please Add Number"})

    if email and (not number):                
        if(re.search(email_pattern, email)):
            drive = user_all.objects.filter(as_user = "Driver",email=email).exclude(active_ac_with_otp="0")
            passe = user_all.objects.filter(as_user = "Passenger",email=email).exclude(active_ac_with_otp="0")
            if len(drive) > 0 and len(passe) > 0:
                return Response({"status":0,"msg":"Email Already Used."})
            else:
                return Response({"status":1,"msg":"Number Not Used."})
        else:
            return Response({"status" : 0 , "msg" : "Please Add Vaild Email"})

@api_view(['GET'])
def notification_list(request,pk):
    Notid = firebase_notifications.objects.filter(userid=pk).order_by('-id')
    lis = []
    for i in Notid:
        res = {}
        res['id'] = i.id
        res['msg'] = i.notification_text
        if i.rideid:
            res['type'] = "CityToCity"
            res['rideid'] = i.rideid.id
            res['user_name'] = ""
            if i.rideid.as_user == "Passenger":
                res['ride_owner'] = i.rideid.getpassenger.name.title()
            else:
                res['ride_owner'] = i.rideid.getdriver.name.title()
            res['pickup'] = i.rideid.pickUp.capitalize()
            res['dropout'] = i.rideid.dropout.capitalize()
            res['date'] = i.rideid.date.strftime("%Y-%m-%d")
            if i.rideid.fees:
                res['price'] = format(i.rideid.fees, '.2f')
            else:
                res['price'] = "0.00"
        # else:
        #     res['rideid'] = ""
        #     res['ride_owner'] = ""
        #     res['pickup'] = ""
        #     res['dropout'] = ""
        #     res['date'] = ""
        elif i.inrideid:
            res['type'] = "InCity"
            res['rideid'] = i.inrideid.id
            res['user_name'] = ""
            if i.inrideid.as_user == "Passenger":
                res['ride_owner'] = i.inrideid.getpassenger.name.title()
            else:
                res['ride_owner'] = i.inrideid.getdriver.name.title()
            res['pickup'] = i.inrideid.pickup_address1.capitalize()
            res['dropout'] = i.inrideid.dropout_address1.capitalize()
            res['date'] = i.inrideid.date.strftime("%Y-%m-%d")
            if i.inrideid.fees:
                res['price'] = format(i.inrideid.fees, '.2f')
            else:
                res['price'] = "0.00"
        else:
            res['type'] = ""
            res['rideid'] = ""
            res['user_name'] = ""
            res['ride_owner'] = ""
            res['pickup'] = ""
            res['dropout'] = ""
            res['date'] = ""
            res['price'] = "0.00"
            
        res['is_seen'] = i.isread
        lis.append(res)
    return Response({"status":1,"msg":"Success","data":lis})

@api_view(['POST'])
def notifivcation_add(request,pk):
    
    data = request.data
    rideid = data['rideid']
    # username = data['username']
    inrideid = data['inrideid']
    try:
        userid = user_all.objects.get(id=pk)
    except:
        return Response({"status":0,"msg":"user id Invalid"})
    if(rideid):
        try:
            dRide = Ride.objects.get(id=rideid)
        except:
            dRide = None
    else:
        dRide = None
        
    if(inrideid):
        try:
            dInRide = InRide.objects.get(id=inrideid)
        except:
            dInRide = None
    else:
        dInRide = None
        
    msg = data['msg']
    showtime = data['datetime']
    if(not msg):
        return Response({"status":0,'msg':"Please Add Notification Text."})
    # if(not username):
    #     return Response({"status":0,'msg':"Username is Required...!"})
    
    if(dRide == None and dInRide == None):
        return Response({"status":0,'msg':"Ride Id Not Founded."})
    else:
        notid = firebase_notifications.objects.create(
            userid = userid,
            rideid = dRide,
            # cancel_by = username,
            inrideid = dInRide,
            notification_text = msg,
            isread = "0",
            create_at = showtime
            )
        return Response({"status":1,'msg':"Notification add Successfully.","notificationid":notid.id})
    

@api_view(['POST'])
def notifivcation_read(request,pk):
    try:
        if(not request.data['isread']):
            return Response({"status":0,"msg":"isread is required.!!"})
            
        Notid = firebase_notifications.objects.get(id=pk)
        Notid.isread = request.data['isread']
        Notid.save()
        return Response({"status":1,"msg":"Success"})
    except:
        return Response({"status":0,"msg":"ID Not Match"})
    

@api_view(['GET'])
def notification_count(request,pk):
    Notid = firebase_notifications.objects.filter(userid=pk,isread=0).order_by('-id')
    return Response({"status":1,"msg":"Success","count_msg":Notid.count()})


@api_view(['POST'])
def User_store_notification(request,pk):
    try:
        user = user_all.objects.get(id=pk)
        user.ntk = request.data['token']
        user.save()
        return Response({'status' : 1 , 'msg' : "Success"})
    except:
        return Response({'status' : 0 , 'msg' : "fail"})

@api_view(['GET'])
def User_Logout(request,pk):
    try:
        user = user_all.objects.get(id=pk)
        user.ntk = ""
        user.save()
        return Response({'status' : 1 , 'msg' : "Success"})
    except:
        return Response({'status' : 0 , 'msg' : "fail"})
