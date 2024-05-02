from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.request import QueryDict
from dataStorage.models import Schedule, Doctor
from datetime import datetime


@login_required
def schedule_operation(request):
    if request.method == "POST" and request.is_ajax() and request.user.is_staff:
        schedule_month = request.POST.get("schedule_month")
        schedule_monthObj = datetime.strptime(schedule_month, "%Y-%m")
        schedule_exists = Schedule.objects.filter(schedule_month_year = schedule_monthObj).exists()
        if schedule_exists:
            return JsonResponse(
                {
                    "message": f"Duplicate Schedule {schedule_month} Exists.",
                },
                status=200,
            )
        schedule_days = request.POST.get("schedule_days").split(",")
        schedule_days_list = [
            datetime.strptime(schedule_day, "%d-%b-%Y").strftime("%d-%m-%Y")
            for schedule_day in schedule_days
            if datetime.strptime(schedule_day, "%d-%b-%Y").month
            == schedule_monthObj.month and datetime.strptime(schedule_day, "%d-%b-%Y").year
            == schedule_monthObj.year
        ]
        schedule_status = request.POST.get("schedule_status")
        schedule_json = {
            "rejected_days": schedule_days_list,
        }
        doctorObj = Doctor.objects.get(user=request.user.id)
        Schedule.objects.create(
            doctor=doctorObj,
            schedule_month_year=schedule_monthObj,
            schedule_json=schedule_json,
            status=schedule_status,
        )
        return JsonResponse(
            {
                "message": f"Created Schedule {schedule_month} by {request.user.username}",
            },
            status=200,
        )

    elif request.method == "PUT" and request.is_ajax() and request.user.is_staff:
        schedule_id = QueryDict(request.body).get("schedule_id")
        unavailable_count = QueryDict(request.body).get("unavailable_count").split(",")
        schedule_status = QueryDict(request.body).get("schedule_status")
        scheduleObj = Schedule.objects.get(id=int(schedule_id))
        try:
            schedule_days_list = [
                datetime.strptime(schedule_day, "%d-%m-%Y").strftime("%d-%m-%Y")
                for schedule_day in unavailable_count
                if datetime.strptime(schedule_day, "%d-%m-%Y").month
                == scheduleObj.schedule_month_year.month and datetime.strptime(schedule_day, "%d-%m-%Y").year
                == scheduleObj.schedule_month_year.year
            ]
        except:
            schedule_days_list = [
                datetime.strptime(schedule_day, "%d-%b-%Y").strftime("%d-%m-%Y")
                for schedule_day in unavailable_count
                if datetime.strptime(schedule_day, "%d-%b-%Y").month
                == scheduleObj.schedule_month_year.month and datetime.strptime(schedule_day, "%d-%b-%Y").year
                == scheduleObj.schedule_month_year.year
            ]
        schedule_json = {
            "rejected_days": schedule_days_list,
        }

        scheduleObj.schedule_json = schedule_json
        scheduleObj.status = schedule_status
        scheduleObj.save()
        return JsonResponse(
            {
                "message": f"Updated Schedule of {schedule_id} by {request.user.username}",
            },
            status=200,
        )

    elif request.method == "DELETE" and request.is_ajax() and request.user.is_staff:
        schedule_id = QueryDict(request.body).get("schedule_id")
        scheduleObj = Schedule.objects.get(id=schedule_id)
        scheduleObj.delete()
        return JsonResponse(
            {
                "message": f"Schedule Deleted {schedule_id} by {request.user.username}",
            },
            status=200,
        )
