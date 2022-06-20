from django.urls import path
from .views import *
urlpatterns = [
    path('adminpanel/', AdminView.as_view(), name='admin'),
    path('create-user/', CreateUser.as_view(), name='create_user'),
    path('create-admin-user/', CreateAdminUser.as_view(), name='create_admin_user'),
    path('user-profile/<pk>',user_profile, name='user_profile'),
    path('edit-user-profile/<pk>',edit_user_profile, name='edit_user_profile'),
    path('edit-user/<pk>', edit_user, name='edit_user'),
    path('delete-user/<pk>', delete_user_profile, name='delete_user_profile'),
    path('search/', search_address),
    path('es/', search_view, name='elastic_search'),
    path('user-profile-details/<pk>/', UserView.as_view(), name='get_user'),
    path('login/', employee_login, name='employee_login'),
    path('logout/', logout_view, name='logout'),
    path('forget-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', forgot_password, name='reset-password'),
    path("verify/<phone>/", getPhoneNumberRegistered_TimeBased.as_view(), name="otp-verification"),
]
