# from django.http import HttpResponseRedirect
# from django.urls import reverse

# def login_required_tm(func):
#     def wrapper(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             HttpResponseRedirect(reverse('dataStorage:doctor_home'), status=301)
#         return func(request, *args, **kwargs)
#     return wrapper

from dataStorage.models import Schedule, Doctor
from datetime import date
import calendar
from rest_framework.authtoken.models import Token
from django.contrib.auth import login

def login_required_tm(func):
    def wrapper(request, *args, **kwargs):
        if not request.is_ajax():
            try:
                token = request.headers.get('Authorization').split(' ')[1]
                tokenObj = Token.objects.get(key = token)
                # print(f"{token=}, {tokenObj.user=}")
                login(request, tokenObj.user)
                return func(request, *args, **kwargs)
            except Token.DoesNotExist:
                pass
            except AttributeError as ae:
                print(f"{ae=}")
        # return func(request, *args, **kwargs)
    return wrapper

def is_last_five_days(date_obj):
    last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
    return (date_obj.replace(day=last_day) - date_obj).days <= 4 or date_obj.day == last_day

def get_next_month_and_year(date_obj):
    if is_last_five_days(date_obj):
        next_month = (date_obj.month + 1) % 12
        next_year = date_obj.year if next_month != 1 else date_obj.year + 1
        date_obj = date_obj.replace(day=1)
        next_month_name = date_obj.replace(month=next_month).strftime("%B")
        return next_month, next_month_name, next_year
    else:
        return date_obj.month, date_obj.strftime("%B"), date_obj.year
    
def check_schedule(request, date_obj):
    doctorObj = Doctor.objects.get(user_id=request.user.id)
    if is_last_five_days(date_obj):
        next_month, next_month_name, next_year = get_next_month_and_year(date_obj)
        schedule_exists = Schedule.objects.filter(
            doctor=doctorObj,
            schedule_month_year = date(
                day=1,
                month=next_month,
                year=next_year,
            )
        ).exists()
        if not schedule_exists:
            try:
                Schedule.objects.create(
                    doctor=doctorObj,
                    schedule_month_year=date(day=1, month=next_month, year=next_year),
                    schedule_json={
                        "rejected_days": [],
                    },
                    status="Active",
                )
            except Exception as err:
                print(f"{err=}")
    else:
        schedule_exists = Schedule.objects.filter(
            doctor=doctorObj,
            schedule_month_year = date(
                day=1,
                month=date_obj.month,
                year=date_obj.year,
            )
        ).exists()
        if not schedule_exists:
            try:
                Schedule.objects.create(
                    doctor=doctorObj,
                    schedule_month_year=date(day=1, month=date_obj.month, year=date_obj.year),
                    schedule_json={
                        "rejected_days": [],
                    },
                    status="Active",
                )
            except Exception as err:
                print(f"{err=}")