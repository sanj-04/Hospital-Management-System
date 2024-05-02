from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect
from dataStorage.models import Patient, Appointment, Medicine, Schedule, Doctor
from dataStorage.forms import PatientForm
from dataStorage.models import status_choices, schedule_status_choices
from django.db.models import Q
from datetime import datetime, date
from .common import check_schedule

@login_required
# @user_passes_test(lambda u: u.is_staff)
def doctor_home(request):
    date_obj = date.today()# date(day=31, month=5, year=2024)
    check_schedule(request, date_obj)

    if not request.user.is_staff:
        return redirect('dataStorage:home')

    if request.method == "GET" and request.user.is_staff:
        patientObjs = Patient.objects.all()
        medicineObjs = Medicine.objects.all()
        doctorObj = Doctor.objects.get(user=request.user.id)
        scheduleObjs = Schedule.objects.filter(doctor=doctorObj)
        current_datetime = datetime.now()
        appointmentObjs = Appointment.objects.filter(
            Q(doctor = doctorObj)
            &Q(
                Q(appointment_date__lte = current_datetime.date())
                &Q(from_time__lte = current_datetime.time())
            )
        )
        for appointmentObj in appointmentObjs:
            appointmentObj.status = "Completed"
            appointmentObj.save()
        appointmentObjs = Appointment.objects.all().order_by("appointment_date")
        patientFormObj = PatientForm()
        context = {
            "patients": [
                {
                    "id": patient.id,
                    "name": patient.user.username,
                    "age": patient.age,
                }
                for patient in patientObjs
            ],
            "medicines": [
                {
                    "id": medicine.id,
                    "name": medicine.medicine_name,
                }
                for medicine in medicineObjs
            ],
            "appointments": [
                {
                    "appointment_id": appointment.id,
                    "patient_id": appointment.patient.id,
                    "patient_name": appointment.patient.user.username,
                    "appointment_date": appointment.appointment_date.strftime("%d-%b-%Y"),
                    "appointment_from_time": appointment.from_time.strftime("%H:%M"),
                    "appointment_from_time_str": appointment.from_time.strftime("%I:%M %p"),
                    "appointment_to_time": appointment.to_time.strftime("%H:%M"),
                    "appointment_to_time_str": appointment.to_time.strftime("%I:%M %p"),
                    "appointment_status": appointment.status,
                }
                for appointment in appointmentObjs
            ],
            "schedules": [
                {
                    "schedule_id": scheduleObj.id,
                    "schedule_month_year": scheduleObj.schedule_month_year.strftime(
                        "%B-%Y"
                    ),
                    "rejected_days": ",".join(
                        scheduleObj.schedule_json.get("rejected_days")
                    ),
                    "rejected_days_count": scheduleObj.rejected_days_count,
                    "status": scheduleObj.status,
                }
                for scheduleObj in scheduleObjs
            ],
            "status_choices": status_choices,
            "schedule_status_choices": schedule_status_choices,
            "unavailable": list(doctorObj.setting_json.get("unavailable_days").values()),
        }

        if not request.is_ajax():
            context["patientForm"] = patientFormObj
            ver = request.GET.get("ver", "0")
            if ver == "0":
                return render(request, "doctor_home.html", context)
            else:
                return render(request, "adminpg.html", context)

        elif request.is_ajax():
            return JsonResponse(
                {
                    "message": f"Reloaded by {request.user.username}",
                    "data": context,
                },
                status=200,
            )