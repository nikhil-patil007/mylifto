from django.urls import path
from . import views


app_name = "doxer_admin"

urlpatterns = [
    path('login-page/',views.LoginPage,name='loginpage'),
    path('',views.home,name='indexpage'),
    path('all-drivers/',views.All_Drivers,name='alldrivers'),
    path('all-passengers/',views.All_Passengers,name='allpassenger'),
    path('all-cars/',views.All_Cars,name='allcars'),
    path('all-rides/',views.All_Rides,name='allrides'),
    path('city-rides/',views.with_in_city_Rides,name='cityrides'),
    path('accepted-cars/',views.Accepted_Cars,name='acceptedcar'),
    path('rejected-cars/',views.Rejected_Cars,name='rejectedcar'),
    
    path('manage-brands-&-<str:tt>-Models/',views.manage_brand,name='manage_brand'),
    path('brand-<str:tt>-store/',views.add_brand_store,name='add_brand_store'),
    path('store-<str:tt>-Models/',views.add_vehical_store,name='add_vehical_store'),
    path('delete-<str:tt>-brand/<str:data>/',views.DeteleVehical_brand,name='DeteleVehical_brand'),
    path('delete-<str:tt>-Models/<str:data>/',views.DeteleCar_name,name='DeteleCar_name'),
    
    # path('admin-add-form/',views.Add_Driver_Form,name='driverform'),
    
    path('Car-accepted/',views.car_accept,name='caraccept'),
    path('Car-rejected/',views.car_reject,name='carreject'),
    path('block-unblock-passenger/',views.BlockPassenger,name='blockpas'),
    path('block-unblock-driver/',views.BlockDriver,name='blockdri'),
    path('edit-price/',views.editprice,name='editprices'),
    path('edit-editcar/',views.editcar,name='editcar'),
    path('show-User-ID/<str:pk>',views.Id_proofes,name='showid'),
    path('Approval-ID/<str:pk>',views.Id_Approval,name='Id_Approval'),
    path('update-price/',views.updateprice,name='updatepriceb'),
    path('Id_With_price/',views.Id_With_price,name='IdWithprice'),
    
    
    path('admin-login/',views.LoginAdmin,name='loginadmins'),
    path('admin-logout/',views.LogoutAdmin,name='Logoutadin'),
    
    # Map APIs
    path('map-view/',views.map_view,name='mapview'),
    path('in-map-view/',views.Incitymap_view,name='Incitymap_view'),
    path('Directions-View',views.map,name='map'),
    path('map',views.mobile_map,name='mobile_map'),
    path('Incityride_Map',views.Incityride_Map,name='Incityride_Map'),
    path('firebase-messaging-sw.js',views.showFirebaseJS,name="show_firebase_js"),
    
]
