from django.urls import path
from . import views,driver,passenger


# Drivers
driverurl = [
    # Profile View Login Signup And Update
    path(r"login-driver/",driver.LoginDriver),
    path(r"sign-up-driver/",driver.SignUpDriver),
    path(r"resend-otp-driver/",driver.ResendOtpDriver),
    path(r"forgot-otp-driver/",driver.ForgotOtpSendDriver),
    path(r"check-otp-driver/",driver.VerifyOtpDriver),
    path(r"forgot-new-password-driver/<str:dk>-<str:pk>/",driver.ForgotSetPasswordDriver),
    path(r"get-driver-profile-<str:pk>/",driver.DriverProfile),
    path(r"get-&-update-driver-<str:pk>/",driver.UpdateDriver),
    path(r"driver-password-update/<str:dk>-<str:pk>/",driver.DriverChangePassword),
    path(r"driver-add-document-/<str:dk>-<str:pk>/",driver.SendIDProofe),
    path(r"driver-get-document-<str:pk>/",driver.MyIdProofe),
    # Add Ride And Stop
    # ---->Car Listing
    path(r"cars-listing-<str:pk>/",driver.CarsListing),
    path(r"add-car-ride-<str:pk>/",driver.AddRideForCar),
    path(r"add-truck-ride-<str:pk>/",driver.AddRideForTruck),
    path(r"get-my-<str:tt>-rides-<str:pk>/",driver.GetMyRidelist),
    # path(r"get-my-truck-rides-<str:pk>/",driver.GetMyTruckRide),
    path(r"driver-stop-ride-<str:pk>/",driver.RidePublishedStop),
    path(r"driver-delete-ride-<str:pk>/<str:rr>/",driver.RidePublishedDelete),
    # Search For Ride Request By Passenger
    path(r"search-booking-<str:dd>-by-driver/",driver.SearchBookingFilter),
    # path(r"driver-get-booking-details-<str:pk>/",driver.DriverBookingList),
    path(r"driver-send-request-for-booking-<str:did>-<str:bid>/",driver.RequestForBooking),
    path(r"driver-get-own-bid-<str:tt>/<str:pk>/",driver.GetOwnBookin_PinListing),
    path(r"driver-own-bid-details-<str:rid>/",driver.getbookinglisting),
    # Request For Booking Accept And Reject
    path(r"get-all-ride-request-<str:pk>/",driver.RidesBookingFilter),
    path(r"ride-request-listing-<str:pk>/",driver.RideListingOfFilter),
    path(r"accept-passenger-request-<str:pk>/",driver.AcceptRequestForTripByDriver),
    path(r"reject-passenger-request-<str:pk>/",driver.RejectRequestForTripByDriver),
    path(r"driver-stop-request-<str:pk>/",driver.CancelRideRequest),
    # Car Add
    path(r"driver-add-car-<str:pk>-<str:mid>/",driver.DriverAddCar),
    path(r"car-check-drivers/<str:pk>/",driver.Check_My_Car),
    path(r"passengers-profile-view-<str:pk>/",driver.PassengerProfileViewByPassenger),
    path(r"driver-gives-rating-<str:Rid>/",driver.DriverGiveRating),
    path(r"driver-report-passenger-<str:Rid>/",driver.ReportPassengerBehavior),
    path(r"driver-add-history-<str:pk>/",driver.AddHistory),
    path(r"driver-view-history-<str:pk>-<str:ll>/",driver.HistoryView),
    path(r"driver-status-block-unblock-<str:pk>/",driver.BlockStatusForDriver),
    
    path(r"driver-driven-of-rating-<str:pk>/",driver.DriverGetRating),
    path(r"driver-list-of-rating-<str:pk>/",driver.DriverDrivenRatingList),
    
    path(r"driver-trip/<str:pk>/",driver.tripsetting),
    path(r"driver-cars-list/<str:pk>/",driver.MyCars),
    path(r"driver-contact-us/",driver.ContactUsDriver),
    path(r"driver-current-loction/<str:pk>/",driver.CurrentLoc),
    path(r"driver-RatingDetailsPageForRecieve/<str:pk>/",driver.RatingDetailsPageForRecieve),
    path(r"driver-GivenRatingDetailsPageFor/<str:pk>/",driver.GivenRatingDetailsPageFor),
    path(r"driver-BidDetalis/<str:pk>/<str:dd>/",driver.BidDetalis),
    path(r"driver-Ride-Enable-Disable/<str:pk>/",driver.EnableToDisableRide),
    path(r"driver-Book-for-day/<str:pk>/",driver.FullBookedDriver),
    path(r"driver-check-Book-for-day/<str:driverid>/<str:current_date>/",driver.CheckFullBooked),
    # Incity Rides
    path(r'driver-RideInCityadd/<str:pk>/',driver.AddInCityRide),
    path(r'driver-RideInCitySearch/',driver.RidesearchInCity),
    path(r'driver-request-for-Inride-booking-<str:did>-<str:rid>/',driver.RequestForInRide),
    path(r'driver-ListInRide-<str:did>/',driver.ListInRide),
    path(r'driver-deleteInRide/',driver.DeleteInRide),
    path(r'driver-ReqListInRide/<str:rid>/',driver.ReqListInRide),
    path(r'driver-AcceptInRide/<str:rid>/',driver.AcceptInRide),
    path(r'driver-RejectInRide/<str:pid>-<str:rid>/',driver.RejectInRide),
    path(r'driver-getlocationincity-<str:did>/',driver.getlocationincity),
    path(r'driver-get-passenger_request-<str:did>/<str:date>/',driver.passengerList),
    path(r'driver-NegoPrice-<str:pk>/',driver.NegoPrice),
]

# Passenger
passengerurl = [
    # Login Signup And Profile
    path(r"login-passenger/",passenger.LoginPassanger),
    path(r"sign-up-passenger/",passenger.SignUpPassanger),
    path(r"resend-otp-passenger/",passenger.ResendOtpPassanger),
    path(r"forgot-otp-passenger/",passenger.ForgotOtpSendPassanger),
    path(r"check-otp-passenger/",passenger.VerifyOtpPassanger),
    path(r"forgot-new-password-passenger/<str:dk>-<str:pk>/",passenger.ForgotSetNewPasswordPassenger),
    path(r"get-passenger-profile-<str:pk>/",passenger.PassengerProfile),
    path(r"get-&-update-passenger-<str:pk>/",passenger.UpdatePassenger),
    path(r"passenger-password-update/<str:dk>-<str:pk>/",passenger.PassengerChangePassword),
    path(r"passenger-add-document-/<str:dk>-<str:pk>/",passenger.SendIDProofe),
    path(r"passenger-get-document-<str:pk>/",passenger.MyIdProofe),
    # Booking == Request Add For Published
    path(r"passenger-add-booking-<str:pk>/",passenger.PassengerAddBooking),
    path(r"passenger-get-own-request-listing-<str:pk>/<str:tt>/",passenger.PassengerRideList),
    path(r"passenger-stop-request-<str:pk>/",passenger.BookingPublishedStop),
    # Searching Ride
    path(r"passenger-search-ride-<str:dd>/",passenger.SearchForRide),
    path(r"get-ride-details-<str:pk>-<str:pp>/",passenger.ViewRideDetails),
    path(r"passenger-send-request-for-ride-booking-<str:pid>-<str:rid>/",passenger.RequestForRide),
    # Request For Booking Ride Listing And View Details
    # path(r"passenger-get-own-booking-listing-<str:pk>/",passenger.PassengerBookingList),
    # path(r"passenger-get-own-truck-booking-listing-<str:pk>/",passenger.PassengerBookingListByT),
    path(r"passenger-get-own-booking-listing-by-<str:tt>-<str:pk>/",passenger.PassengerBookingLists),
    path(r"passenger-get-own-booking-details-<str:pk>-<str:pp>/",passenger.OwnBookingFilterDetails),
    # Drive's Request Listing And Accept & Rejects
    path(r"get-all-booking-request-<str:pk>/",passenger.ViewPassengerRide),
    path(r"accept-driver-request-<str:pk>/",passenger.AcceptRequestForTripByPassenger),
    path(r"reject-driver-request-<str:pk>/",passenger.RejectRequestForTripByPassenger),
    path(r"passenger-stop-ride-<str:pk>/",passenger.CancelBooking),
    path(r"passenger-delete-ride-<str:pk>/<str:rr>/",passenger.DeleteBooking),
    path(r"cronejov-<str:pk>/",passenger.cronejov),
    # Filter
    # path(r"ride-filter-by-passenger/",passenger.MultiRideFilterByPassenger),
    # path(r"ride-time-by-show/",passenger.timeRideFilterByPassenger), 
    
    path(r"passenger-status-block-unblock-<str:pk>/",passenger.BlockStatusForPassenger),
    path(r"filter-ride-type-<str:pk>/",passenger.FilterRideType),
    path(r"passenger-gives-rating-<str:Rid>/<str:pp>/",passenger.PassengerGiveRating),
    # Passenger Recived Rating
    path(r"passenger-driven-of-rating-<str:pk>/",passenger.PassengerGetRating),
    # Passenger Driven Rating   
    path(r"passenger-list-of-rating-<str:pk>/",passenger.PassengerDrivenRating),
    path(r"drivers-profile-view-<str:pk>/",passenger.DriverProfileViewByPassenger),
    path(r"passenger-report-driver-<str:Rid>/<str:pk>/",passenger.ReportDriverBehavior),
    path(r"passenger-add-history-<str:pk>/",passenger.AddHistory),
    path(r"passenger-view-history-<str:pk>-<str:ll>/",passenger.HistoryView),
    path(r"passenger-trip/<str:pk>/",passenger.tripsetting),
    path(r'passenger-contact-us/',passenger.ContactUsPassenger),
    path(r'passenger-BidDetalis/<str:pk>/',passenger.BidDetalis),
    path(r'passenger-RatingDetailsPageForRecieve/<str:pk>/',passenger.RatingDetailsPageForRecieve),
    path(r'passenger-GivenRatingDetailsPageFor/<str:pk>/',passenger.GivenRatingDetailsPageFor),
    path(r'passenger-Get_Full-booking_listing/',passenger.FullBookingList),
    # Incity Rides
    path(r'passenger-RideInCityadd/<str:pk>/',passenger.AddInCityRide),
    path(r'passenger-RideInCitySearch/',passenger.RideInCitySearch),
    path(r'passenger-request-for-Inride-booking-<str:pid>-<str:rid>/',passenger.RequestForInRide),
    path(r'passenger-ListInRide-<str:pid>/',passenger.ListInRide),
    path(r'passenger-DeleteInRide/',passenger.DeleteInRide),
    path(r'passenger-ReqListInRide/<str:rid>/',passenger.ReqListInRide),
    path(r'passenger-AcceptInRide/<str:rid>/',passenger.AcceptInRide),
    path(r'passenger-RejectInRide/<str:did>-<str:rid>/',passenger.RejectInRide),
    path(r'passenger-getlocationincity-<str:pid>/',passenger.getlocationincity),
]

viewurl = [
    path(r"user-Account-listing/<str:Id>/",views.Account_listing),
    path(r"check-user-Id-status/<str:Id>/",views.Id_Verify_status),
    path(r"User_Logout/<str:pk>/",views.User_Logout),
    path(r"User_store_notification/<str:pk>/",views.User_store_notification),
    path(r"logout-Account-list/",views.LogOut_account),
    path(r"get-city/",views.SerachCities),
    path(r"get-all-city/",views.AllCities),
    path(r"get-all-brands/<str:tt>/",views.ShowAllBrand),
    path(r"get-car-name-of-brand-<str:pk>/",views.ShowCarOfBrand),
    path(r"get-car-colors-<str:pk>/",views.ShowCarOfColors),
    path(r"get-car-dimension-<str:pk>/",views.ShowCarOfDimensions),
    path(r"user-Login-api/",views.MultiLogin),
    path(r"user-signup-api/",views.SignUp),
    path(r"user-check-api/",views.checkUser),
    path(r"Otp-verification-api/<str:dk>-<str:pk>/",views.UserOtpVerification),
    # path(r"user-select-role-api/<str:pk>/",views.UserSelectRole),
    path(r"user-notification-list/<str:pk>/",views.notification_list),
    path(r"user-read-notification/<str:pk>/",views.notifivcation_read),
    path(r"user-add-notification/<str:pk>/",views.notifivcation_add),
    path(r"user-notification-count/<str:pk>/",views.notification_count),
    path(r"user-resend-otp-api/<str:dk>-<str:pk>/<str:typ>/",views.ResendOtp),
]

urlpatterns = driverurl + passengerurl + viewurl
