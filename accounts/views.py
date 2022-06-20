from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Timesheet
from admin_panel.models import AdminUser
from django.utils.timezone import utc
from datetime import datetime,date
from pytz import timezone
from django.contrib.auth import authenticate, login


def dashboard_view(request):
    if request.user.is_authenticated:
        user = request.user
        today=date.today()
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%I:%M %p')
        current_date = today.strftime("%B %d, %Y")
        employee_count = AdminUser.objects.all().exclude(is_superuser=True).count()

        try:
            employee_timesheet = Timesheet.objects.filter(employee=user).order_by('-recorded_datetime')[:4]
            employee_timesheet_list =[]
            for i in employee_timesheet:
                employee_timesheet_list.append(i)
            time_sheet = Timesheet.objects.filter(employee=user).last()
            time_in,time_out = str(time_sheet.clock_in_time),str(time_sheet.clock_out_time)
            print(time_in,time_out)

            if time_sheet.clock_out_time == None:
                status = 'Pending'
                gross_hour = "None"
            else:
                time_format = '%I:%M:%S'
                gross_hour = datetime.strptime(time_out, time_format) - datetime.strptime(time_in, time_format)
                status = 'Success'

            context = {
                'current_date': current_date,
                'current_time': ind_time,
                'username': user,
                'time_sheet': time_sheet,
                'status': time_sheet.logging,
                'employee_count':employee_count,
                'gross_hour':gross_hour,
                'status':status,
                'employee_timesheet_list':employee_timesheet_list
            }
            return render(request, 'dashboard.html', context)

        except AttributeError:
            print('AttributeError')
            context = {'status':"Please Clock In",
                       'current_date': current_date,
                       'current_time': ind_time,
                       'employee_count':employee_count
                       }
            return render(request, 'dashboard.html', context)
    else:
        return HttpResponse("Please Login")




def clock_action(request):
    """Receives the users input e.g. clock in / out actions, stores and retrieves records to and from the database"""
    # When the employee clocks in/out the post is received, the date and time is recorded and it is logged to the employees user_id
    print('inside clock action')
    if request.method == 'POST':
        clock_action = request.POST.get('clock_action')
        now = datetime.utcnow().replace(tzinfo=utc)
        print(clock_action)
        current_user = request.user
        # logged_status = Timesheet.objects.filter(employee=current_user).latest()
        print("Login and clock in status : ", clock_action)
        print(clock_action == "IN")
        # when the employee logs in they can not log in again until they logout first
        if clock_action == 'IN':
            print('inside clock in function')
            # if logged_status.logging == "OUT":
            clock_in_time = datetime.now(timezone("Asia/Kolkata")).strftime('%I:%M %p')
            timesheet = Timesheet(employee=current_user, recorded_by=current_user, clocking_time=now,
                                  logging="IN", clock_in_time = clock_in_time, status=True,
                                  ip_address=request.META.get('REMOTE_ADDR','NA'))
            timesheet.save()
            print('end')
            return redirect('dashboard')

        elif clock_action == "OUT":
            print('inside clock out function')
            clock_out_time = datetime.now(timezone("Asia/Kolkata")).strftime('%I:%M %p')
            try:
                timesheet = Timesheet.objects.filter(employee=current_user).last()
                timesheet.clock_out_time = clock_out_time
                timesheet.logging = "OUT"
                timesheet.status=False
                timesheet.save()
                return redirect('dashboard')
            except Timesheet.DoesNotExist:
                return HttpResponse('Please Login before logout')
                clock_action = "IN"

        else:
            print('out side both function')
            error_message = "You must clock in before you can clock out.\n"

        return render(request, 'dashboard.html')

def employee_profile_view(request):
    if request.user.is_authenticated:
        employee_details = AdminUser.objects.get(username = request.user)
        context = {
            'username':employee_details,
            'first_name':employee_details.first_name,
            'second_name':employee_details.second_name,
            'email':employee_details.email,
            'employee_id':employee_details.employee_id,
            'city':employee_details.city,
            'designation':employee_details.designation,
            'mobile_no':employee_details.mobile_no,
            'department':employee_details.department,
            'profile_pic':employee_details.profile_pic,
        }
        return render(request,'employee/employee_profile_edit.html', context)
    else:
        return HttpResponse('Please Login')

def edit_profile(request):
    print('innnnnnnn')
    if request.method == "POST":
        print('post method')
        register = AdminUser.objects.get(username=request.user)
        register.first_name = request.POST.get('first_name')
        register.second_name = request.POST.get('second_name')
        register.mobile_no = request.POST.get('mobile_no')
        register.email = request.POST.get('email')
        register.designation = request.POST.get('designation')
        register.employee_id = request.POST.get('employee_id')
        register.department = request.POST.get('department')
        register.city = request.POST.get('city')
        register.save()
        return redirect('employee_details')
    return HttpResponse(400)


