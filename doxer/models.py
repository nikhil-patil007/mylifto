from django.conf import settings
from django.core.mail import send_mail
from django.db import models
# Create your models here.
rate = (('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5))
Gender = (('0',''),('M', 'Male'), ('F', 'Female'), ('O', 'Other'))

class Vehical_Type(models.Model):
    vehical_type = models.CharField(max_length=255)
    
    def __str__(self):
        return self.vehical_type

class Vehical_Color(models.Model):
    vehical_color = models.CharField(max_length=255)
    
    def __str__(self):
        return self.vehical_color

class Vehical_dimensions(models.Model):
    dimension = models.CharField(max_length=255)
    
    def __str__(self):
        return self.dimension

class Vehical_brand(models.Model):
    brand = models.CharField(max_length=255)
    vehical_type = models.ForeignKey(Vehical_Type, on_delete=models.CASCADE,null=True,blank=True)
    create_at = models.DateTimeField(blank=True,null=True)
    update_at = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return self.brand
    
class Car_name(models.Model):
    cars = models.CharField(max_length=255)
    colors = models.ManyToManyField(Vehical_Color,blank=True)
    dimension = models.ManyToManyField(Vehical_dimensions,blank=True)
    brand = models.ForeignKey(Vehical_brand, on_delete=models.CASCADE)
    photo_of_vehicle = models.ImageField(upload_to="Vehical_images/", height_field=None, width_field=None, max_length=255,blank=True,null=True)
    vehicle_type = models.CharField(max_length=20,default='C',choices=[('T','Truck'),('C','Car'),('A','Auto'),('B','Bike')])
    # ac_non_ac = models.CharField(max_length=10,default='0',choices=[('0',"No"),("1","Yes")])
    create_at = models.DateTimeField(blank=True,null=True)
    update_at = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return self.cars
    
class user_all(models.Model):
    as_user = models.CharField(max_length=255,blank=True)
    name = models.CharField(max_length=255,blank=True)
    DeviceId = models.CharField(max_length=255,blank=True,null=True)
    pro_image = models.ImageField(upload_to="Users/", height_field=None, width_field=None, default='Users/Image.jpg', max_length=255)
    image1 = models.ImageField(upload_to="Users_documents/",default='Users_documents/idproof.png', height_field=None, width_field=None, max_length=255,blank=True,null=True)
    image2 = models.ImageField(upload_to="Users_documents/",height_field=None, width_field=None, max_length=255,blank=True,null=True)
    img_status = models.CharField(max_length=255,default='P',choices=[('P',"Pending"),("A","Approval"),("R","Rejected")])
    active_ac_with_otp = models.CharField(max_length=10,default='0',choices=[('1',"Verified"),("0","Not Verified"),("2","Forget")])
    email_or_num = models.CharField(max_length=60,blank=True)
    email = models.EmailField(max_length=40,blank=True)
    contact_no = models.CharField(max_length=15,blank=True)
    gender = models.CharField(max_length=10,default='0',choices=Gender)
    fare_per_km = models.FloatField(max_length=20,default=255.05)
    dob = models.DateField(blank=True,null=True)
    city = models.CharField(max_length=255,blank=True)
    bio = models.CharField(max_length=255,blank=True)
    otp = models.CharField(max_length=4,blank=True)
    password = models.CharField(max_length=255,blank=True)
    cpassword = models.CharField(max_length=255,blank=True)
    
    latitude = models.CharField(max_length=255,blank=True)
    longitude = models.CharField(max_length=255,blank=True)
    
    fullbooked = models.CharField(default=0,max_length=20,choices=[('0','No'),('1','Yes')])
    car_booked = models.ForeignKey("Vehicle", on_delete=models.SET_NULL,null=True,blank=True)
    current_location = models.CharField(null=True,blank=True,max_length=255)
    current_date = models.DateField(blank=True,null=True)
    
    ntk = models.CharField(max_length=255,null=True,blank=True)
    status = models.CharField(max_length=25,null=False,blank=False,choices=(('Active',"Active"),("Deactive","Deactive")))
    create_at = models.DateTimeField(blank=True,null=True)
    update_at = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return f"{self.name} {self.as_user}"

# class Driver(models.Model):
#     name = models.CharField(max_length=255,blank=True)
#     DeviceId = models.CharField(max_length=255,blank=True,null=True)
#     pro_image = models.ImageField(upload_to="Drivers/", height_field=None, width_field=None, default='Drivers/Image.jpg', max_length=255)
#     image1 = models.ImageField(upload_to="Drivers_documents/",default='Drivers_documents/idproof.png', height_field=None, width_field=None, max_length=255,blank=True,null=True)
#     image2 = models.ImageField(upload_to="Drivers_documents/",default='Drivers_documents/idproof.png', height_field=None, width_field=None, max_length=255,blank=True,null=True)
#     img_status = models.CharField(max_length=255,default='0')
#     active_ac_with_otp = models.CharField(max_length=10,default='0',choices=[('1',"Verified"),("0","Not Verified"),("2","Forget")])
#     email_or_num = models.CharField(max_length=60,blank=True)
#     email = models.EmailField(max_length=40,blank=True)
#     contact_no = models.CharField(max_length=15,blank=True)
#     gender = models.CharField(max_length=10,default='0',choices=Gender)
#     fare_per_km = models.FloatField(max_length=20,default=255.05)
#     dob = models.DateField(blank=True,null=True)
#     city = models.CharField(max_length=255,blank=True)
#     bio = models.CharField(max_length=255,blank=True)
#     otp = models.CharField(max_length=4,blank=True)
#     password = models.CharField(max_length=255,blank=True)
#     cpassword = models.CharField(max_length=255,blank=True)
#     ntk = models.CharField(max_length=255,null=True,blank=True)
#     status = models.CharField(max_length=25,null=False,blank=False,choices=(('Active',"Active"),("Deactive","Deactive")))
#     create_at = models.DateTimeField(blank=True,null=True)
#     update_at = models.DateTimeField(blank=True,null=True)

#     def __str__(self):
#         return self.name if self.name else self.email_or_num

class Vehicle(models.Model):
    driverid = models.ForeignKey(user_all, on_delete=models.CASCADE,null=True)
    reg_num = models.CharField(max_length=12)
    Car_Img = models.ImageField(upload_to="Cars/Cars_Img/", height_field=None, width_field=None, max_length=255,blank=True,null=True)
    Car_Doc = models.ImageField(upload_to="Cars/Cars_Doc/", height_field=None, width_field=None, max_length=255,blank=True,null=True)
    vehical_variant = models.ForeignKey(Car_name, on_delete=models.SET_NULL,null=True,blank=True)
    vehicle_color = models.CharField(max_length=255,blank=True,null=True)
    vehicle_type = models.CharField(max_length=20,default='C',choices=[('T','Truck'),('C','Car'),('A','Auto'),('B','Bike')])
    vehicle_model_year = models.CharField(max_length=4,blank=True,null=True)
    dimension = models.CharField(max_length=255,blank=True,null=True)
    length_in_feet = models.CharField(max_length=4,blank=True,null=True)
    width_in_feet = models.CharField(max_length=4,blank=True,null=True)
    ac_non_ac = models.CharField(max_length=10,default='N',choices=[('N',"No"),("Y","Yes")])
    status = models.CharField(max_length=25,default='0',choices=(('0','Pending'),('1','Approval'),('2','Rejected')))
    created = models.DateTimeField(blank=True,null=True)
    updated = models.DateTimeField(blank=True,null=True)


# class Passanger(models.Model):
#     name = models.CharField(max_length=255,blank=True)
#     DeviceId = models.CharField(max_length=255,blank=True,null=True)
#     pro_image = models.ImageField(upload_to="Passenger/",default='Passenger/Image.png', height_field=None, width_field=None, max_length=255)
#     image1 = models.ImageField(upload_to="Passengers_documents/",default='Passengers_documents/idproof.png', height_field=None, width_field=None, max_length=255,blank=True,null=True)
#     image2 = models.ImageField(upload_to="Passengers_documents/",default='Passengers_documents/idproof.png', height_field=None, width_field=None, max_length=255,blank=True,null=True)
#     img_status = models.CharField(max_length=255,default='0')
#     active_ac_with_otp = models.CharField(max_length=10,default='0',choices=[('1',"Verified"),("0","Not Verified"),("2","Forget")])
#     email_or_num = models.CharField(max_length=60,blank=True)
#     email = models.EmailField(max_length=40,blank=True)
#     contact_no = models.CharField(max_length=15,blank=True)
#     gender = models.CharField(max_length=10,default='0',choices=Gender)
#     dob = models.DateField(blank=True,null=True)
#     city = models.CharField(max_length=255,blank=True)
#     bio = models.CharField(max_length=255,blank=True)
#     otp = models.CharField(max_length=4,blank=True)
#     password = models.CharField(max_length=255,blank=True)
#     cpassword = models.CharField(max_length=255,blank=True)
#     ntk = models.CharField(max_length=255,null=True,blank=True)
#     status = models.CharField(max_length=25,null=False,blank=False,choices=(('Active',"Active"),("Deactive","Deactive")))
#     create = models.DateTimeField(blank=True)
#     update = models.DateTimeField(blank=True)
    
#     def __str__(self):
#         return self.name
    
class Cities(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
class Ride(models.Model):
    as_user = models.CharField(max_length=255,blank=True,null=True)
    getdriver = models.ForeignKey(user_all, on_delete=models.CASCADE,null=True,blank=True,related_name='Driver')
    getpassenger = models.ForeignKey(user_all, on_delete=models.CASCADE,null=True,blank=True,related_name='Passenger')
    ride_type = models.CharField(max_length=20,default="-",choices=[('-','--'),('A','Auto'),('C','Car'),('B','Bike'),('T','Truck'),('M','Many')])
    route = models.TextField(blank=True,null=True)
    car = models.ForeignKey(Vehicle, on_delete=models.SET_NULL,null=True,blank=True)
    manycar = models.ManyToManyField(Vehicle,related_name='ManyCars',blank=True)
    pickUp = models.CharField(max_length=255,blank=True,null=True)
    pickUp_latitude = models.CharField(blank=True,max_length=255)
    pickUp_longitude = models.CharField(blank=True,max_length=255)
    dropout = models.CharField(max_length=255,blank=True,null=True)
    dropout_latitude = models.CharField(blank=True,max_length=255)
    dropout_longitude = models.CharField(blank=True,max_length=255)
    pickup_address1 = models.CharField(blank=True,max_length=255)
    pickup_address2 = models.CharField(blank=True,max_length=255)
    dropout_address1 = models.CharField(blank=True,max_length=255)
    dropout_address2 = models.CharField(blank=True,max_length=255)
    car_latitude = models.CharField(blank=True,max_length=255)
    car_longitude = models.CharField(blank=True,max_length=255)
    per_km = models.CharField(blank=True,max_length=255)
    date = models.DateField(blank=True,null=True)
    time = models.CharField(blank=True,max_length=255,null=True)
    dtime = models.CharField(blank=True,max_length=255,null=True)
    seats = models.CharField(default=0,max_length=25,blank=True)
    Max_seats = models.BigIntegerField(default=0,blank=True)
    fees = models.FloatField(max_length=6,blank=True,null=True)
    capacity = models.CharField(max_length=255,null=True,blank=True)
    Max_parcel = models.BigIntegerField(default=0,blank=True)
    # pfees = models.FloatField(max_length=6,blank=True,null=True)
    add_information = models.TextField(blank=True)
    map_date = models.CharField(blank=True,max_length=255,null=True)
    publish = models.CharField(default=0,max_length=20,choices=[('0','No'),('1','Yes'),('2','BLOCK USER'),('3','Disable')])
    status = models.CharField(default=0,max_length=20,choices=[('0','Pending'),('1','Ride Full'),('3','Ride Cancel')])
    trip_status = models.CharField(default='P',max_length=20,choices=[('P','Pending'),('O','On The Way'),('E','Complete Trip')])
    trip_status2 = models.CharField(default='2',max_length=20,choices=[('2','Pending'),('1','On The Way'),('3','Complete Trip'),('4','Ride Cancel')])
    ride_time = models.DateTimeField(blank=True,null=True)
    # Full Booked Ride
    fullbooked = models.CharField(default=0,max_length=20,choices=[('0','No'),('1','Yes'),('2','Show only in Passenger Not For Driver')])
    current_location = models.CharField(null=True,blank=True,max_length=255)
    current_date = models.DateField(blank=True,null=True)
    
    create_at = models.DateTimeField(blank=True,null=True)
    update_at = models.DateTimeField(blank=True,null=True)
    
    # def __str__(self):
    #     if self.getdriver and (not self.getpassenger):
    #         return f"{self.as_user} {self.getdriver}'s {self.pickUp.capitalize()} To {self.dropout.capitalize()} Ride"
    #     if (not self.getdriver) and self.getpassenger:
    #         return f"{self.as_user} {self.getpassenger}'s {self.pickUp.capitalize()} To {self.dropout.capitalize()} Ride"
    #     if self.getdriver and self.getpassenger:
    #         if self.as_user == "Passenger":
    #             return f"{self.as_user} {self.getpassenger}'s {self.pickUp.capitalize()} To {self.dropout.capitalize()} Ride"
    #         if self.as_user == "Driver":
    #             return f"{self.as_user} {self.getdriver}'s {self.pickUp.capitalize()} To {self.dropout.capitalize()} Ride"

class InRide(models.Model):
    as_user = models.CharField(max_length=255,blank=True,null=True)
    getdriver = models.ForeignKey(user_all, on_delete=models.CASCADE,null=True,blank=True,related_name='DriverId')
    getpassenger = models.ForeignKey(user_all, on_delete=models.CASCADE,null=True,blank=True,related_name='PassengerId')
    getmultidriver = models.ManyToManyField(user_all,blank=True,related_name='DrivermultiId')
    getmultipassenger = models.ManyToManyField(user_all,blank=True,related_name='PassengermultiId')
    vehicle = models.CharField(max_length=255,blank=True,null=True)
    pickUp = models.CharField(max_length=255,blank=True,null=True)
    pickUp_latitude = models.CharField(blank=True,max_length=255)
    pickUp_longitude = models.CharField(blank=True,max_length=255)
    dropout = models.CharField(max_length=255,blank=True,null=True)
    dropout_latitude = models.CharField(blank=True,max_length=255)
    dropout_longitude = models.CharField(blank=True,max_length=255)
    pickup_address1 = models.TextField(blank=True,max_length=255)
    pickup_address2 = models.TextField(blank=True,max_length=255)
    dropout_address1 = models.TextField(blank=True,max_length=255)
    dropout_address2 = models.TextField(blank=True,max_length=255)
    driver_latitude = models.CharField(blank=True,max_length=255)
    driver_longitude = models.CharField(blank=True,max_length=255)
    passenger_latitude = models.CharField(blank=True,max_length=255)
    passenger_longitude = models.CharField(blank=True,max_length=255)
    per_km = models.CharField(blank=True,max_length=255)
    date = models.DateField(blank=True,null=True)
    time = models.CharField(blank=True,max_length=255,null=True)
    dtime = models.CharField(blank=True,max_length=255,null=True)
    seats = models.CharField(default=0,max_length=25,blank=True)
    Max_seats = models.BigIntegerField(default=0,blank=True)
    fees = models.FloatField(max_length=6,blank=True,null=True)
    capacity = models.CharField(max_length=255,null=True,blank=True)
    Max_parcel = models.BigIntegerField(default=0,blank=True)
    add_information = models.TextField(blank=True)
    map_date = models.CharField(blank=True,max_length=255,null=True)
    publish = models.CharField(default=1,max_length=20,choices=[('0','No'),('1','Yes'),('2','BLOCK USER'),('3','Disable')])
    status = models.CharField(default=0,max_length=20,choices=[('0','Pending'),('1','Ride Full'),('3','Ride Cancel')])
    trip_status = models.CharField(default='P',max_length=20,choices=[('P','Pending'),('O','On The Way'),('E','Complete Trip')])
    trip_status2 = models.CharField(default='2',max_length=20,choices=[('2','Pending'),('1','On The Way'),('3','Complete Trip'),('4','Ride Cancel')])
    ride_time = models.DateTimeField(blank=True,null=True)
    create_at = models.DateTimeField(blank=True,null=True)
    update_at = models.DateTimeField(blank=True,null=True)

class Ride_pin(models.Model):
    as_user = models.CharField(max_length=255,blank=True,null=True)
    getdriver = models.ForeignKey(user_all, on_delete=models.CASCADE,null=True,blank=True,related_name='Driver1')
    passengerid = models.ForeignKey(user_all, on_delete=models.CASCADE,null=True,blank=True,related_name='Passenger1')
    getride = models.ForeignKey(Ride, on_delete=models.CASCADE,null=True,blank=True,related_name='Driver_ride')
    getride1 = models.ForeignKey(Ride, on_delete=models.CASCADE,null=True,blank=True,related_name='Passenger_ride')
    car = models.ForeignKey(Vehicle, on_delete=models.SET_NULL,null=True,blank=True)
    ride_type = models.CharField(max_length=25,blank=True,null=True,choices=[('T','Truck'),('C','Car')])
    ride_date = models.DateField(blank=True,null=True)
    ride_time = models.CharField(blank=True,max_length=255)
    offer_price = models.CharField(max_length=255,blank=True,null=True)
    pickup_address1 = models.CharField(blank=True,max_length=255)
    pickup_address2 = models.CharField(blank=True,max_length=255)
    dropout_address1 = models.CharField(blank=True,max_length=255)
    dropout_address2 = models.CharField(blank=True,max_length=255)
    for_passenger = models.CharField(default=0,blank=True,max_length=255)
    for_parcel = models.CharField(default=0,blank=True,max_length=255)
    pickUp = models.CharField(max_length=255,blank=True,null=True)
    pickUp_latitude = models.CharField(blank=True,max_length=255)
    pickUp_longitude = models.CharField(blank=True,max_length=255)
    dropout = models.CharField(max_length=255,blank=True,null=True)
    dropout_latitude = models.CharField(blank=True,max_length=255)
    dropout_longitude = models.CharField(blank=True,max_length=255)
    add_information = models.TextField(blank=True)
    status = models.CharField(default=0,max_length=20,choices=[('0','Pending'),('1','Request Confirm'),('2','Request Cancel'),('3','Ride Cancel')])
    pas_status = models.CharField(default='W',max_length=20,choices=[('W','Waiting'),('O','On The Way'),('E','Complete')])
    fees = models.FloatField(max_length=20,blank=True,null=True)
    per_seat_fees = models.CharField(max_length=20,blank=True,null=True)
    today = models.DateField(blank=True,null=True)
    request_date = models.DateTimeField(blank=True)

class InRide_pin(models.Model):
    as_user = models.CharField(max_length=255,blank=True,null=True)
    getdriver = models.ForeignKey(user_all, on_delete=models.CASCADE,null=True,blank=True,related_name='InDriver1')
    passengerid = models.ForeignKey(user_all, on_delete=models.CASCADE,null=True,blank=True,related_name='InPassenger1')
    getride = models.ForeignKey(InRide, on_delete=models.CASCADE,null=True,blank=True,related_name='Driver_Inride')
    ride_type = models.CharField(max_length=25,blank=True,null=True)
    ride_date = models.DateField(blank=True,null=True)
    ride_time = models.CharField(blank=True,max_length=255)
    offer_price = models.CharField(max_length=255,blank=True,null=True)
    pickup_address1 = models.CharField(blank=True,max_length=255)
    pickup_address2 = models.CharField(blank=True,max_length=255)
    dropout_address1 = models.CharField(blank=True,max_length=255)
    dropout_address2 = models.CharField(blank=True,max_length=255)
    for_passenger = models.BigIntegerField(default=0,blank=True)
    for_parcel = models.BigIntegerField(default=0,blank=True)
    pickUp = models.CharField(max_length=255,blank=True,null=True)
    pickUp_latitude = models.CharField(blank=True,max_length=255)
    pickUp_longitude = models.CharField(blank=True,max_length=255)
    dropout = models.CharField(max_length=255,blank=True,null=True)
    dropout_latitude = models.CharField(blank=True,max_length=255)
    dropout_longitude = models.CharField(blank=True,max_length=255)
    add_information = models.TextField(blank=True)
    status = models.CharField(default=0,max_length=20,choices=[('-1','Negotiate'),('0','Pending'),('1','Request Confirm'),('2','Request Cancel'),('3','Ride Cancel')])
    pas_status = models.CharField(default='W',max_length=20,choices=[('W','Waiting'),('O','On The Way'),('E','Complete')])
    fees = models.FloatField(max_length=20,blank=True,null=True)
    today = models.DateField(blank=True,null=True)
    request_date = models.DateTimeField(blank=True)

class Drivers_Rating(models.Model):
    mine = models.ForeignKey(user_all, on_delete=models.CASCADE,related_name='Driver_me')
    tri = models.ForeignKey(Ride,on_delete=models.CASCADE,blank=True,null=True)
    passengerid = models.ForeignKey(user_all, on_delete=models.SET_NULL,blank=True,null=True,related_name='Passenger_you')
    rates = models.CharField(max_length=5 ,blank=True,null=True,choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')))
    review = models.TextField(blank=True)
    create = models.DateTimeField(blank=True,null=True)
    # create = models.DateField(blank=True,null=True)

class Driver_Report(models.Model):
    mine = models.ForeignKey(user_all,on_delete=models.CASCADE,related_name='for_Driver')
    tri = models.ForeignKey(Ride,on_delete=models.CASCADE,blank=True,null=True)
    passengerid = models.ForeignKey(user_all,on_delete=models.SET_NULL,blank=True,null=True,related_name='for_Passenger')
    report_text = models.TextField(blank=True)
    create = models.DateTimeField(blank=True,null=True)
    # create = models.DateField(blank=True,null=True)

class Passenger_Rating(models.Model):
    mine = models.ForeignKey(user_all, on_delete=models.CASCADE,related_name='Passenger_me1')
    tri = models.ForeignKey(Ride_pin,on_delete=models.CASCADE,blank=True,null=True)
    driverid = models.ForeignKey(user_all, on_delete=models.SET_NULL,blank=True,null=True,related_name='Driver_u')
    rates = models.CharField(max_length=2 ,choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')))
    review = models.TextField(blank=True)
    create = models.DateTimeField(blank=True,null=True)
    # create = models.DateField(blank=True,null=True)

class Passenger_Report(models.Model):
    mine = models.ForeignKey(user_all, on_delete=models.CASCADE,related_name='Passenger_me2')
    tri = models.ForeignKey(Ride_pin,on_delete=models.CASCADE,blank=True,null=True)
    driverid = models.ForeignKey(user_all, on_delete=models.SET_NULL,blank=True,null=True,related_name='Driver_u1')
    report_text = models.TextField(blank=True)
    create = models.DateTimeField(blank=True,null=True)
    # create = models.DateField(blank=True,null=True)

class Search_History(models.Model):
    driverid = models.ForeignKey(user_all,on_delete=models.CASCADE,blank=True,null=True,related_name='Driver_u2')
    passengerid = models.ForeignKey(user_all,on_delete=models.CASCADE,blank=True,null=True,related_name='Passenger_me3')
    pick = models.CharField(max_length=255)
    drop = models.CharField(max_length=255)
    pick_lat = models.CharField(max_length=255)
    pick_lng = models.CharField(max_length=255)
    drop_lat = models.CharField(max_length=255)
    drop_lng = models.CharField(max_length=255)
    date = models.DateField(null=True,blank=True)
    location = models.CharField(max_length=255)
    create = models.DateField(blank=True,null=True)

class Car_Details(models.Model):
    # source_url = models.CharField(db_column='Source URL', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    make = models.CharField(db_column='Make', max_length=9, blank=True, null=True)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=20, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=29, blank=True, null=True)  # Field name made lowercase.
    notes = models.CharField(db_column='Notes', max_length=12, blank=True, null=True)  # Field name made lowercase.
    image_url = models.CharField(db_column='Image URL', max_length=1061, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    key_seating_capacity = models.CharField(db_column='Key Seating Capacity', max_length=8, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    seating_capacity = models.CharField(db_column='Seating Capacity', max_length=8, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    no_of_seating_rows = models.CharField(db_column='No of Seating Rows', max_length=6, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bootspace = models.CharField(db_column='Bootspace', max_length=10, blank=True, null=True)  # Field name made lowercase.

class User_login(models.Model):
    as_user = models.CharField(max_length=255,blank=True)
    user_id = models.ForeignKey(user_all, on_delete=models.CASCADE)
    DeviceId = models.CharField(max_length=255,blank=True,null=True)
    ntk = models.CharField(max_length=255,blank=True,null=True)
    create_at = models.DateTimeField(blank=True,null=True)
    
class firebase_notifications(models.Model):
    userid = models.ForeignKey(user_all,on_delete=models.CASCADE,blank=True,null=True)
    rideid = models.ForeignKey(Ride,on_delete=models.CASCADE,blank=True,null=True)
    cancel_by = models.CharField(max_length=20,null=True,blank=True)
    inrideid = models.ForeignKey(InRide,on_delete=models.CASCADE,blank=True,null=True)
    notification_text = models.TextField(blank=True)
    isread = models.CharField(max_length=20,default='0',choices=[('0','NotSeen'),('1','Seen')])
    create_at = models.DateTimeField(blank=True,null=True)
    