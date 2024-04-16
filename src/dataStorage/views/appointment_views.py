from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.request import QueryDict
from django.shortcuts import render
from dataStorage.models import Patient, Appointment, Doctor, Schedule
from datetime import datetime
from django.utils import timezone

@login_required
def appointment_operation(request):
    if request.method == "GET" and not request.is_ajax():
        appointmentObjs = Appointment.objects.all()
        patientObjs = Patient.objects.all()

        context = {
            "appointments": [
                {
                    "appointment_id": appointment.id,
                    "patient_id": appointment.patient.id,
                    "patient_name": appointment.patient.user.username,
                    "appointment_date": appointment.appointment_date.strftime("%d-%b-%Y"),
                    "appointment_from_time": appointment.from_time.strftime("%H:%M"),
                    "appointment_to_time": appointment.to_time.strftime("%H:%M"),
                    "appointment_status": appointment.status,
                }
                for appointment in appointmentObjs
            ],
            "patients": [
                {
                    "name": patient.user.username,
                    "id": patient.id,
                }
                for patient in patientObjs
            ],
        }
        return render(request, "appointment.html", context)

    elif request.method == "POST" and request.is_ajax():
        appointment_patient = request.POST.get("appointment_patient")
        try:
            patientObj = Patient.objects.get(id = int(appointment_patient))
        except ValueError as ve:
            patientObj = Patient.objects.get(user__username = appointment_patient)
        
        appointment_date = request.POST.get("appointment_date")
        appointment_from_time = request.POST.get("appointment_from_time")
        appointment_to_time = request.POST.get("appointment_to_time")
        appointment_status = request.POST.get("appointment_status", "Pending")

        appointment_dateObj = datetime.strptime(appointment_date, "%d-%b-%Y")
        appointment_from_timeObj = datetime.strptime(appointment_from_time, "%H:%M")
        appointment_to_timeObj = datetime.strptime(appointment_to_time, "%H:%M")

        doctorObj = Doctor.objects.get(user_id=request.user.id)
        appointmentObj = Appointment.objects.create(
            doctor = doctorObj,
            patient = patientObj,
            appointment_date = appointment_dateObj,
            from_time = appointment_from_timeObj,
            to_time = appointment_to_timeObj,
            status = appointment_status,
        )
        return JsonResponse(
            {
                "message": f"Created Appointment {appointmentObj.id} by {request.user.username}",
            },
            status=200,
        )

    elif request.method == "PUT" and request.is_ajax():
        appointment_id = QueryDict(request.body).get("appointment_id")
        appointment_date = QueryDict(request.body).get("appointment_date")
        appointment_from_time = QueryDict(request.body).get("appointment_from_time")
        appointment_to_time = QueryDict(request.body).get("appointment_to_time")
        appointment_status = QueryDict(request.body).get("appointment_status")

        appointment_dateObj = datetime.strptime(appointment_date, "%d-%b-%Y")
        appointment_from_timeObj = datetime.strptime(appointment_from_time, "%H:%M")
        appointment_to_timeObj = datetime.strptime(appointment_to_time, "%H:%M")

        appointmentObj = Appointment.objects.get(id=appointment_id)
        appointmentObj.appointment_date = appointment_dateObj
        appointmentObj.from_time = appointment_from_timeObj
        appointmentObj.to_time = appointment_to_timeObj
        if appointment_status:
            appointmentObj.status = appointment_status
        appointmentObj.save()
        return JsonResponse(
            {
                "message": f"Updated Appointment {appointment_id} by {request.user.username}",
            },
            status=200,
        )

    elif request.method == "DELETE" and request.is_ajax():
        appointment_id = QueryDict(request.body).get("appointment_id")
        appointmentObj = Appointment.objects.get(id = appointment_id)
        appointmentObj.delete()
        return JsonResponse(
            {
                "message": f"Appointment Delete {appointment_id} by {request.user.username}",
            },
            status=200,
        )

# python src\manage.py shell
# from dataStorage.views import *
# book_appointment('12-4-2024')
# book_appointment('13-4-2024')
# book_appointment('14-4-2024')
# book_appointment('16-4-2024')
# book_appointment('17-4-2024')
# book_appointment('18-4-2024')
def book_appointment(appointment_date, appointment_from_time=None, appointment_to_time=None):
    appointment_dateObj = datetime.strptime(appointment_date, "%d-%m-%Y")
    is_future_date = appointment_dateObj.date() >= timezone.now().date()
    if not is_future_date:
        return f"Appointment closed for {appointment_dateObj.strftime("%d-%B-%Y")}."
    
    appointment_weekday = appointment_dateObj.weekday() # 5 => Saturday, 6 => Sunday
    if appointment_weekday == 6:
        return f"{appointment_dateObj.strftime("%d-%B-%Y")} is Sunday, We are Closed on Sunday."
    
    scheduleObj = Schedule.objects.filter(
        schedule_month_year__month = appointment_dateObj.month,
        schedule_month_year__year = appointment_dateObj.year,
    )
    schedule_exists = scheduleObj.exists()
    if not schedule_exists:
        return f"Schedule not created for {appointment_dateObj.strftime("%B-%Y")}."
    
    if appointment_dateObj.strftime("%d-%m-%Y") in scheduleObj[0].schedule_json.get("rejected_days"):
        return f"Sorry, We are closed on {appointment_dateObj.strftime("%d-%B-%Y")}."

    print(f"{schedule_exists=}, {appointment_weekday=}, {is_future_date=}")
    if appointment_from_time is None and appointment_to_time is None:
        print("None")