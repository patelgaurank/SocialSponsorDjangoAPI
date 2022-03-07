from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, FindUserExistOrNot, ValidateUserAndPhoneNumber, FindUserLogOut, ValidateCode, FindUserAddress
# FindUserAddress
urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('finduser/', FindUserExistOrNot.as_view(), name="find_user"),
    path('findusersphonenumber/', ValidateUserAndPhoneNumber.as_view(), name="find_users_phonenumber"),
    path('validatecode/', ValidateCode.as_view(), name="find_users_phonenumber"),
    path('findusersaddress/', FindUserAddress.as_view(), name="find_users_address"),
    path('finduserlogout/', FindUserLogOut.as_view(), name="find_users_and_logout"),    
    path('signout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]
