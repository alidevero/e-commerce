from django.urls import path 
from .views import *

urlpatterns = [
    
    path('signup/',SignupView.as_view(),name="user-signup" ),
    path('verifyotp/',VerifyOTP.as_view(),name="verify-otp"),
    path('login/',LoginView.as_view(),name='login'),
    path('deleteaccountview/',DeleteAccountView.as_view(),name="deleteaccountview"),
    path('update/', UpdateView.as_view(),name="update"),
    path('userprofile/',UserProfileView.as_view(),name="user-profile"),
    path('logout/',LogoutView.as_view(), name="logut")
]
