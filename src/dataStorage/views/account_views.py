from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse, get_resolver
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import (
    user_logged_out,
    user_logged_in,
    user_login_failed,
)
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models import Q
from django.http import JsonResponse
from django.http.request import QueryDict
from datetime import datetime
from dataStorage.models import (
    Patient,
    Appointment,
    Doctor,
    Medicine,
    Prescription,
    Schedule,
)
from dataStorage.models import status_choices, schedule_status_choices
from dataStorage.forms import PatientForm
import json, hashlib


def hash_dict_content(dictionary):
    json_string = json.dumps(dictionary, sort_keys=True)
    hash_object = hashlib.sha256(json_string.encode())
    return hash_object.hexdigest()


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.info(request, "[" + request.user.username + "] Logged out.")


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    messages.success(request, "[" + request.user.username + "] Logged in.")


@receiver(user_login_failed)
def on_user_login_failed(sender, request, **kwargs):
    messages.warning(request, "Logged in failed.")


# @login_required
def home(request):
    if request.method == "GET" and request.is_ajax():
        context = {}
        return render(request, "main.html", context)

    if request.method == "GET" and not request.is_ajax():
        patients = Patient.objects.all()
        context = {
            "patients": [
                {
                    "id": patient.id,
                    "name": patient.user.username,
                    "phone_number": patient.phone_number,
                    "date_of_birth": patient.date_of_birth,
                    "age": patient.age,
                }
                for patient in patients
            ]
        }
        return render(request, "main.html", context)

    elif request.method == "POST" and request.is_ajax():
        patient_id = request.POST.get("patient")
        try:
            patient = Patient.objects.get(id=int(patient_id))
        except (Patient.DoesNotExist, ValueError):
            return JsonResponse({"error": "Invalid patient ID"}, status=400)

        date_of_birth = request.POST.get("date_of_birth")
        name = request.POST.get("name")
        phone_number = request.POST.get("phone_number")

        patient.date_of_birth = date_of_birth
        # patient.name = name
        patient.phone_number = phone_number
        patient.save()

        return JsonResponse(
            {
                "message": f"Updated patient {patient.id} by {request.user.username}",
            },
            status=200,
        )


@login_required
def dashboard(request):
    context = {}
    return render(request, "home.html", context)


def pres(request):
    context = {}
    return render(request, "pres.html", context)


def bot(request):
    context = {}
    return render(request, "bot_index.html", context)


@login_required
def doctor_home(request):
    if request.method == "GET":
        patientObjs = Patient.objects.all()
        medicineObjs = Medicine.objects.all()
        appointmentObjs = Appointment.objects.all().order_by("appointment_date")
        scheduleObjs = Schedule.objects.filter(doctor_id=request.user.id)
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
        }

        if not request.is_ajax():
            context["status_choices"] = status_choices
            context["schedule_status_choices"] = schedule_status_choices
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


# def cards(request):
# 	context = {}
# 	return render(request, 'cards.html', context)


# @ensure_csrf_cookie
@login_required
def configureDevice(request):
    if request.method == "GET":
        try:
            totpObj = TOTPDevice.objects.get(Q(user=request.user) & Q(confirmed=False))
            qrCode = qrcode.make(totpObj.config_url)
            qrCode = qrCode.resize((162, 162))
            qrCodeBytes = io.BytesIO()
            qrCode.save(qrCodeBytes, format="JPEG")
            qrCodeBytes = qrCodeBytes.getvalue()
            qrCode = base64.b64encode(qrCodeBytes).decode("utf-8")
            context = {"qrCode": qrCode}
            return render(request, "account/totp.html", context)
        except:
            return redirect("spapp:index")

    elif request.method == "POST":
        totpObj = TOTPDevice.objects.get(Q(user=request.user) & Q(confirmed=False))
        if totpObj.verify_token(request.POST["totp"]):
            totpObj.confirmed = True
            totpObj.save()
            return JsonResponse(
                {
                    "message": f"Device Updated : {totpObj.id}",
                },
                status=204,
            )
        else:
            return JsonResponse(
                {
                    "message": f"Device Update Falied : {totpObj.id}",
                },
                status=404,
            )


def custom_csrf_failure_view(request, reason):
    return render(request, "account/custom_csrf_failure.html", {"reason": reason})
