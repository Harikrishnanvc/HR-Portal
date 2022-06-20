import base64
import pyotp
from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client

from major.settings import EMAIL_HOST_USER
from .models import AdminUser, FakeAddress
from .search import lookup


# Create your views here.


#   logout view
def logout_view(request):
    logout(request)
    return redirect('employee_login')


#   elastic search
def search_view(request):
    query_params = request.GET
    q = query_params.get('q')

    context = {}
    if q is not None:
        results = lookup(q)
        context['results'] = results
        context['query'] = q
    return render(request, 'search.html', context)


#   auto complete search
def search_address(request):
    address = request.GET.get('address')
    payload = []
    if address:
        fake_address_objs = FakeAddress.objects.filter(address__icontains=address)

        for fake_address_obj in fake_address_objs:
            payload.append(fake_address_obj.address)
    return JsonResponse({'status': 200, 'data': payload})


#   view users in admin panel
class UserView(APIView):
    def post(self, request):
        post_list = AdminUser.objects.all()
        return render(request, 'search.html', {'post_list': post_list})

    def get(self, request):
        post_list = AdminUser.objects.all()
        return render(request, 'search.html', {'post_list': post_list})


#   view users in admin panel
class AdminView(APIView):
    def post(self, request):
        post_list = AdminUser.objects.all()

        if request.user.is_authenticated:
            return HttpResponse('Please login')
        else:
            return render(request, 'admin_panel.html', {'post_list': post_list})

    def get(self, request):
        post_list = AdminUser.objects.all()
        if request.user.is_superuser == False:
            return HttpResponse('Please login')
        else:
            return render(request, 'admin_panel.html', {'post_list': post_list})


#   create user url
class CreateUser(APIView):
    def post(self, request):
        return render(request, 'create_user.html')

    def get(self, request):
        return render(request, 'create_user.html')


#   mail
def welcome_mail(email, first_name, password):
    Subject = 'Welcome ' + first_name
    Message = 'Hi ' + first_name + '\n This mail contains your credentials for HR portal login \n E-mail/Username : '
    + email + '\n Password : ' + password + '\n please change your password after logging in'
    Recepient = str(email)
    send_mail(Subject, Message, EMAIL_HOST_USER, [Recepient], fail_silently=False)
    return redirect('admin_panel.html')

#   sms
def welcome_sms(mobile_no, first_name):
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f'Welcome ' + first_name,
        from_= settings.TWILIO_NO,
        to=mobile_no, )
    return redirect('admin_panel.html')


#   create users by admin
class CreateAdminUser(APIView):
    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            first_name = request.POST['first_name']
            second_name = request.POST['second_name']
            email = request.POST['email']
            employee_id = request.POST['employee_id']
            city = request.POST['city']
            designation = request.POST['designation']
            mobile_no = request.POST['mobile_no']
            department = request.POST['department']
            profile_pic = request.FILES.get('profile_pic')
            password = AdminUser.objects.make_random_password()  # random password generator
            welcome_mail(email, first_name, password)  # sending the credentials through mail
            password = make_password(password)  # hashing the password for validation
            AdminUser(first_name=first_name, second_name=second_name, email=email,
                      employee_id=employee_id, city=city, designation=designation, mobile_no=mobile_no,
                      department=department, profile_pic=profile_pic, password=password,
                      username=username).save()  # saving the data
            welcome_sms(mobile_no, first_name)  # sending credentials through sms
        return redirect('admin')

    def get(self):
        return HttpResponse('failed to register user')


#   view full details of user registered by admin
def user_profile(request, pk):
    user_details = AdminUser.objects.get(pk=pk)
    return render(request, 'user_profile.html', {'user_details': user_details})


#   edit user profile details
def edit_user_profile(request, pk):
    profile_details = AdminUser.objects.filter(pk=pk)
    return render(request, 'edit_user_profile.html', {'profile_details': profile_details})


#   update user details
def edit_user(request, pk):
    if request.method == "POST":
        register = AdminUser.objects.get(pk=pk)
        register.first_name = request.POST.get('first_name')
        register.second_name = request.POST.get('second_name')
        register.mobile_no = request.POST.get('mobile_no')
        register.email = request.POST.get('email')
        register.designation = request.POST.get('designation')
        register.employee_id = request.POST.get('employee_id')
        register.department = request.POST.get('department')
        register.city = request.POST.get('city')
        register.save()
        messages.success(request, "Successfully updated " + register.first_name + 's profile ')
    if request.user.is_superuser == False:
        return redirect('dashboard')
    else:
        return redirect('admin')


#   delete user
def delete_user_profile(request, pk):
    profile_details = AdminUser.objects.filter(pk=pk)
    profile_details.delete()
    messages.success(request, "Deleted Successfully")
    return redirect('admin')


#   employee login
def employee_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser == False:
                login(request, user)
                return redirect('dashboard')
            else:
                login(request, user)
                return redirect('admin')
        else:
            messages.success(request, 'E-mail / Password is incorrect')
            return render(request, 'employee_login.html')
    return render(request, 'employee_login.html')


# forgot password
class ForgotPasswordView(TemplateView):
    template_name = 'otp/otp_generation.html'


#   forgot password
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            get_item = AdminUser.objects.get(email=email)
            get_item.password = make_password(password)
            get_item.save()
            messages.success(request, 'Password changed successfully')
            return redirect('employee_login')
        else:
            messages.success(request, 'password not matching')
            return render(request, 'otp/reset_password.html')

    return render(request, 'otp/reset_password.html')


# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


# Time after which OTP will expire
EXPIRY_TIME = 60  # seconds


class getPhoneNumberRegistered_TimeBased(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = AdminUser.objects.get(email=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            return HttpResponse('E-mail is not registered')
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.TOTP(key, interval=EXPIRY_TIME)  # TOTP Model for OTP is created
        print(OTP.now())
        Subject = 'One Time Password '
        Message = 'Hi ' + Mobile.first_name + ', \n This mail contains your OTP for resetting your Passwrod \n OTP : ' + OTP.now()
        Recepient = str(Mobile.email)
        send_mail(Subject, Message, EMAIL_HOST_USER, [Recepient], fail_silently=False)

        # Using Multi-Threading send the OTP Using Messaging Services like Twilio
        return render(request, 'otp/otp_verification.html', {'mobile': phone})  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = AdminUser.objects.get(email=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.TOTP(key, interval=EXPIRY_TIME)  # TOTP Model
        if OTP.verify(request.data["OTP"]):  # Verifying the OTP
            return render(request, 'otp/reset_password.html', {'email': Mobile.email})
        return HttpResponse("OTP is wrong/expired", status=400)
