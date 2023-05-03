from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from time import gmtime, strftime
       
class RideSerializer(ModelSerializer):
    class Meta:
        model = Ride
    
    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation["driver_Id"] = instance.getdriver.id
        representation["driver"] = instance.driver
        representation["capacity"] = instance.capacity
        representation["pickUp"] = instance.pickUp.capitalize()
        representation["pickUp_latitude"] = instance.pickUp_latitude
        representation["pickUp_longitude"] = instance.pickUp_longitude
        representation["dropout"] = instance.dropout.capitalize()
        representation["dropout_latitude"] = instance.dropout_latitude
        representation["dropout_longitude"] = instance.dropout_longitude
        representation["date"] = instance.date
        representation["seats"] = instance.seats
        representation["fees"] = instance.fees
        representation["add_information"] = instance.add_information.title()

        return representation
       
class RidepinSerializer(ModelSerializer):
    class Meta:
        model = Ride_pin
    def to_representation(self, instance):
        representations = dict()
        # representations['mine_ride'] = instance.mine_ride.username if instance.mine_ride.username else instance.mine_ride.email_or_num
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
        # representations['pickUp_latitude'] = instance.getride.pickUp_latitude
        # representations['pickUp_longitude'] = instance.getride.pickUp_longitude
        # representations['dropout_latitude'] = instance.getride.dropout_latitude
        # representations['dropout_longitude'] = instance.getride.dropout_longitude
        return representations

class MineRidepinSerializer(ModelSerializer):
    class Meta:
        model = Ride_pin
    def to_representation(self, instance):
        representations = dict()
        representations['bid'] = instance.id
        representations['Passenger_id'] = instance.passengerid.id
        representations['passenger_name'] = instance.passengerid.name.title()
        representations['passenger_profile'] = instance.passengerid.pro_image.url
        representations['for_passenger'] = instance.for_passenger
        representations['for_parcel'] = instance.for_parcel
        representations['Trip_status'] = instance.pas_status
        representations["Driver_Token"] = instance.getdriver.ntk
        representations["Passenger_Token"] = instance.passengerid.ntk
        representations['Location'] = instance.pickUp.capitalize()
        representations['fees'] = f"{instance.fees}"
        representations['per_seats_price'] = f"{instance.per_seat_fees}"
        representations['Location_latitude'] = instance.pickUp_latitude
        representations['Location_longitude'] = instance.pickUp_longitude
        representations['Destination'] = instance.dropout.capitalize()
        representations['Destination_latitude'] = instance.dropout_latitude
        representations['Destination_longitude'] = instance.dropout_longitude
        representations['request_date'] = instance.request_date.strftime("%Y-%m-%d")
        representations['note'] = instance.add_information
        return representations

class GetRidepinSerializer(ModelSerializer):
    class Meta:
        model = Ride_pin
        
    def to_representation(self, instance):
        representations = dict()
        representations['ride_id'] = instance.id
        # representations['booking_id'] = instance.id
        representations['booking_id'] = instance.getride.id
        representations['ride_status'] = instance.status
        representations['Driver_id'] = instance.getdriver.id
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
        representations['ride_dtime'] = instance.getride.dtime
        representations['Location'] = instance.pickUp.capitalize()
        representations['Destination'] = instance.dropout.capitalize()
        return representations

class BookingpinSerializer(ModelSerializer):
    class Meta:
        model = Ride_pin
        
    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation["Driver_id"] = instance.getdriver.id
        representation["Driver_Name"] = instance.getdriver.name.title()
        representation["Driver_pro_image"] = instance.getdriver.pro_image.url
        representation["pickUp"] = instance.pickUp.capitalize()
        representation["dropout"] = instance.dropout.capitalize()
        if instance.ride_type == "T":
            representation["car"] = "Truck"
        else:
            representation["car"] = f"{instance.car.vehical_variant.brand.brand} , {instance.car.vehical_variant.cars}"
        representation["offer_price"] = instance.offer_price
        representation['per_seats_price'] = f"{instance.per_seat_fees}"
        representation["req_date"] = instance.request_date.strftime("%Y-%m-%d")
        representation["status"] = instance.status
        representation["for_passenger"] = instance.for_passenger
        representation["for_parcel"] = instance.for_parcel
        representation["driver_token"] = instance.getdriver.ntk
        representation["note"] = instance.add_information.title()

        return representation
    
class DriverBookingpinSerializer(ModelSerializer):
    class Meta:
        model = Ride_pin
    
    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation["rid"] = instance.getride.id
        representation["trip_pas_status"] = instance.getride.trip_status
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
        representation["time"] = instance.getride.time
        representation["dtime"] = instance.getride.dtime
        representation["map_time"] = instance.getride.map_date
        representation["Passenger"] = instance.for_passenger
        representation["Parcel"] = instance.for_parcel
        representation["offer_price"] = f"{instance.offer_price}"
        representation["req_date"] = instance.request_date#.strftime("%d-%m-%Y")
        representation["status"] = instance.status

        return representation

class Filterserializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        
    def to_representation(self, instance):
        representation = dict()
        representation["ride_id"] = instance.id
        representation["driver"] = instance.getdriver.name.title()
        representation["pro_image"] = instance.getdriver.pro_image.url
        representation["seats"] = instance.seats
        representation["capacity"] = instance.capacity
        representation["pickUp"] = instance.pickUp.capitalize()
        representation["dropout"] = instance.dropout.capitalize()
        representation["time"] = instance.time
        representation["dtime"] = instance.dtime
        representation["map_time"] = instance.map_date
        representation["date"] = instance.date
        representation["fees"] = f"{instance.fees}"
        representation["add_information"] = instance.add_information.title()

        return representation
    
class MultiFilterserializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        
    def to_representation(self, instance):
        representation = dict()
        representation["ride_id"] = instance.id
        representation["driver"] = instance.getdriver.name.title()
        representation["seats"] = instance.seats
        representation["capacity"] = instance.capacity
        representation["pickUp"] = instance.pickUp.capitalize()
        representation["dropout"] = instance.dropout.capitalize()
        representation["date"] = instance.date
        representation["time"] = instance.time
        # representation["dtime"] = instance.dtime
        representation["map_time"] = instance.map_date
        representation["fees"] = f"{instance.fees}"
        representation["add_information"] = instance.add_information.title()
        representation["Animal"] = instance.pet_allowed
        representation["Cigarate"] = instance.smoke_allowed
        representation["Back_seat"] = instance.max_seat_in_back
        representation["Gov_id"] = instance.gov_id

        return representation
    
class CarRideFilterserializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        
    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation["driver"] = instance.getdriver.name.title()
        representation["Profile"] = instance.getdriver.pro_image.url
        representation["pickUp"] = instance.pickUp.capitalize() if instance.pickUp.capitalize() else ""
        representation["dropout"] = instance.dropout.capitalize() if instance.dropout.capitalize() else ""
        representation["seats"] = instance.seats
        representation["capacity"] = instance.capacity
        representation["date"] = instance.date.strftime("%d-%m-%Y")
        representation["time"] = instance.time
        representation["dtime"] = instance.dtime
        representation["map_time"] = instance.map_date
        representation["fees"] = instance.fees
        if instance.publish == '1':
            representation["EnableDisable"] = "1"
        else:
            representation["EnableDisable"] = "0"
        representation["status"] = instance.status
        representation["trip_status"] = instance.trip_status
        representation["add_information"] = instance.add_information.title()

        return representation
    
class TruckRideFilterserializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        
    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation["driver"] = instance.getdriver.name.title()
        representation["Profile"] = instance.getdriver.pro_image.url
        representation["trip_pas_status"] = instance.trip_status
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
        representation["add_information"] = instance.add_information.title()

        return representation

class Vehical_brandSeializer(serializers.ModelSerializer):
    class Meta:
        model = Vehical_brand
        fields = '__all__'
        
class CarsSeializer(serializers.ModelSerializer):
    class Meta:
        model = Car_name
        fields = ['id','cars']

class ModelsSeializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        
    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation["reg_num"] = instance.reg_num
        if instance.Car_Img:
            representation["Car_img"] = instance.Car_Img.url
        else:
            representation["Car_img"] = ""
        representation["vehical_variant"] = f"{instance.vehical_variant.brand.brand} , {instance.vehical_variant.cars}"
        representation["vehicle_color"] = instance.vehicle_color
        representation["status_car"] = instance.status
        # representation["model"] = instance.model

        return representation
    
class PassengerGetRatingSeializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger_Rating
    
    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation["driver_username"] = instance.driverid.name.title()
        # representation["passenger_id"] = instance.mine.username 
        representation["pro_image"] = instance.driverid.pro_image.url 
        representation["pickUp"] = instance.tri.pickUp.capitalize()
        representation["dropout"] = instance.tri.dropout.capitalize()
        representation["date"] = instance.tri.request_date.strftime("%d-%m-%Y")
        representation["review"] = instance.review
        representation["rate"] = instance.rates
        return representation
    
class DriverDrivenRatingSeializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger_Rating
    
    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation["passenger_id"] = instance.mine.name.title()
        representation["passenger_pro_image"] = instance.mine.pro_image.url 
        representation["pickUp"] = instance.tri.getride.pickUp.capitalize()
        representation["dropout"] = instance.tri.getride.dropout.capitalize()
        representation["date"] = instance.tri.request_date.strftime("%d-%m-%Y")
        # representation["Driver_id"] = instance.driverid.username if instance.driverid.username else instance.driverid.email_or_num
        representation["rate"] = instance.rates
        representation["review"] = instance.review

        return representation
        
class PassengerDrivenRatingSeializer(serializers.ModelSerializer):
    class Meta:
        model = Drivers_Rating
           
    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation["driver_username"] = instance.mine.name.title()
        representation["pro_image"] = instance.mine.pro_image.url
        representation["pickUp"] = instance.tri.pickUp.capitalize()
        representation["dropout"] = instance.tri.dropout.capitalize()
        representation["date"] = instance.tri.date.strftime("%d-%m-%Y")
        representation["rate"] = instance.rates
        representation["review"] = instance.review

        return representation
    
class DriverGetRatingSeializer(serializers.ModelSerializer):
    class Meta:
        model = Drivers_Rating
    
    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation["passenger_id"] = instance.passengerid.name.title()
        representation["pro_image"] = instance.passengerid.pro_image.url
        representation["pickUp"] = instance.tri.pickUp.capitalize()
        representation["dropout"] = instance.tri.dropout.capitalize()
        representation["date"] = instance.tri.date.strftime("%d-%m-%Y")
        representation["rate"] = float(instance.rates)
        representation["review"] = instance.review

        return representation

class CarListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        
    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation['Car_name'] = f'{instance.vehical_variant.brand.brand} {instance.vehical_variant.cars}'
        return representation
   
class HistoryViewForDriver(serializers.ModelSerializer):
    class Meta:
        model = Search_History

    def to_representation(self, instance):
        representation = dict()
        representation["Driver"] = instance.driverid.name.title()
        representation["pick"] = instance.pick
        representation["drop"] = instance.drop
        representation["pick_lat"] = instance.pick_lat
        representation["pick_lng"] = instance.pick_lng
        representation["drop_lat"] = instance.drop_lat
        representation["drop_lng"] = instance.drop_lng
        representation["date"] = instance.date
        representation["location"] = instance.location
        return representation
    
class HistoryViewForPassenger(serializers.ModelSerializer):
    class Meta:
        model = Search_History

    def to_representation(self, instance):
        representation = dict()
        representation["driverid"] = instance.passengerid.name.title()
        representation["pick"] = instance.pick
        representation["drop"] = instance.drop
        representation["pick_lat"] = instance.pick_lat
        representation["pick_lng"] = instance.pick_lng
        representation["drop_lat"] = instance.drop_lat
        representation["drop_lng"] = instance.drop_lng
        representation["date"] = instance.date
        representation["location"] = instance.location
        return representation
    
class TripcountSerial(serializers.ModelSerializer):
    class Meta:
        model = Ride_pin

    def to_representation(self, instance):
        representation = dict()
        representation["Tid"] = instance.id
        representation["status"] = instance.pas_status
        return representation
    
class MycarsSerial(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        
    def to_representation(self, instance):
        representation = dict()
        representation["Cid"] = instance.id
        representation["car"] = f"{instance.vehical_variant.brand} {instance.vehical_variant}"
        return representation