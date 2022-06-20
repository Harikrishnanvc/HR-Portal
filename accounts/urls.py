from django.urls import path
from .views import clock_action, dashboard_view, employee_profile_view, edit_profile
urlpatterns = [
    path('clock-action/',clock_action, name="clock_action"),
    path('dashboard/', dashboard_view, name="dashboard"),
    path('employee-details/', employee_profile_view, name="employee_details"),
    path('employee-profile/', edit_profile, name="edit_profile"),

]
