from django.contrib import admin
from .models import *

# Register your models here.

class Driveradmin(admin.ModelAdmin):
    # model = User
    list_per_page = 15 # No of records per page 
    list_display = ('id','as_user','name', 'email', 'contact_no', 'gender','city', 'otp', 'create_at', 'update_at')
    list_display_links = ('id','as_user','name', 'email', 'contact_no', 'gender', 'city', 'otp', 'create_at', 'update_at')
    list_filter = ('gender'),
    ordering = ('-id'),
    search_fields = ('name','email','contact_no')

# class Passangerradmin(admin.ModelAdmin):
#     list_per_page = 15 # No of records per page 
#     list_display = ('id','name', 'email', 'contact_no', 'gender','city', 'otp', 'create', 'update')
#     list_display_links = ('id','name', 'email', 'contact_no', 'gender', 'city', 'otp', 'create', 'update')
#     list_filter = ('gender'),
#     ordering = ('-id'),
#     search_fields = ('name','email','contact_no')

class rideadmin(admin.ModelAdmin):
    list_per_page = 15 # No of records per page 
    list_display = ('id','as_user','ride_type','pickUp','dropout','date','trip_status','seats','capacity','fees','status')
    list_display_links = ('id','as_user','ride_type','pickUp','dropout','date','seats','capacity')
    ordering = ('trip_status2'),
    list_editable = ('fees'),('status'),('trip_status')
    search_fields = ('driver'),

class Inrideadmin(admin.ModelAdmin):
    list_per_page = 15 # No of records per page 
    list_display = ('id','as_user','pickup_address1','dropout_address1','date','trip_status','seats','capacity','fees','status')
    list_display_links = ('id','as_user','pickup_address1','dropout_address1','date','seats','capacity')
    ordering = ('trip_status2'),
    list_editable = ('fees'),('status'),('trip_status')
    search_fields = ('driver'),

class vehicaladmin(admin.ModelAdmin):
    list_per_page = 15 # No of records per page 
    list_display = ('id','driverid','reg_num','vehical_variant','vehicle_color','status','created','updated')
    list_display_links = ('id','driverid','reg_num','vehical_variant','vehicle_color','created','updated')
    ordering = ('-id'),
    list_editable = ('status'),
    list_filter = ('status'),

class ridepin(admin.ModelAdmin):
    list_per_page = 15 # No of records per page 
    list_display = ('id','as_user','getdriver','getride','passengerid','ride_type','today','status','fees')
    list_display_links = ('id','getdriver','getride','passengerid','ride_type','today','status','fees')
    ordering = ('-id'),

# class Inridepin(admin.ModelAdmin):
#     list_per_page = 15 # No of records per page 
#     list_display = ('id','as_user','getdriver','getride','passengerid','ride_type','today','status','fees')
#     list_display_links = ('id','getdriver','getride','passengerid','ride_type','today','status','fees')
#     ordering = ('-id'),

class city(admin.ModelAdmin):
    list_per_page = 15 # No of records per page 
    list_display = ('id','name')
    list_display_links = ('id','name')
    ordering = ('-id'),
    search_fields = ('name'),
    
class Car_Admin(admin.ModelAdmin):
    list_per_page = 15 # No of records per page 
    list_display = ('id','make','model','version','notes','image_url','key_seating_capacity','seating_capacity','no_of_seating_rows','bootspace')
    list_display_links = ('id','make','model','version','notes','image_url','key_seating_capacity','seating_capacity','no_of_seating_rows','bootspace')
    ordering = ('-id'),
    list_filter = ('make'),('notes'),
    search_fields = ('make','model'),
    
# SHOW ON ADMIN PANEL 
admin.site.register(Car_Details,Car_Admin)
admin.site.register(Car_name)
admin.site.register(Cities,city)
admin.site.register(Driver_Report)#,Inridepin)
admin.site.register(Drivers_Rating)#,Inridepin)
admin.site.register(firebase_notifications)
admin.site.register(InRide,Inrideadmin)
admin.site.register(InRide_pin)#,Inridepin)
admin.site.register(Passenger_Rating)
admin.site.register(Passenger_Report)
admin.site.register(Ride,rideadmin)
admin.site.register(Ride_pin,ridepin)
admin.site.register(user_all,Driveradmin)
admin.site.register(User_login)
admin.site.register(Vehical_brand)
admin.site.register(Vehical_Color)
admin.site.register(Vehical_dimensions)
admin.site.register(Vehicle,vehicaladmin)
