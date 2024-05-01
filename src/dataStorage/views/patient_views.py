from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http.request import QueryDict
from dataStorage.models import Patient, Doctor, Prescription, Appointment
from dataStorage.forms import PatientForm
from django.db.models import Q
from datetime import datetime
from django.shortcuts import render, redirect

@login_required
def patient_home(request):
    if request.user.is_staff:
        return redirect('dataStorage:home')

    if request.method == "GET" and not request.user.is_staff:
        patientObj = Patient.objects.get(user = request.user)
        current_datetime = datetime.now()
        appointmentObjs = Appointment.objects.filter(
            Q(patient = patientObj)
            &Q(
                Q(appointment_date__lte = current_datetime.date())
                &Q(from_time__lte = current_datetime.time())
            )
        )
        for appointmentObj in appointmentObjs:
            appointmentObj.status = "Completed"
            appointmentObj.save()
        appointmentObjs = Appointment.objects.filter(
            patient = patientObj
        ).order_by("appointment_date")
        prescriptionObjs = Prescription.objects.filter(patient__user=request.user)
        doctorObj = Doctor.objects.first()
        
        context = {
            "patient": {
                "id": patientObj.id,
                "name": patientObj.user.username,
                "age": patientObj.age,
                "date_of_birth": patientObj.date_of_birth.strftime("%d-%b-%Y"),
                "phone_number": patientObj.phone_number,
            },
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
            "prescriptions": [
                {
                    "id": prescription.id,
                    "name": prescription.createTimestamp.strftime("%d-%b-%Y %I:%M %p"),
                }
                for prescription in prescriptionObjs
            ],
            "unavailable": list(doctorObj.setting_json.get("unavailable_days").values()),
        }
        if not request.is_ajax():
            context["patientForm"] = PatientForm()
            return render(request, "patient_home.html", context)

        elif request.is_ajax():
            return JsonResponse(
                {
                    "message": f"Reloaded by {request.user.username}",
                    "data": context,
                },
                status=200,
            )

@login_required
def patient_operation(request):
    if request.method == "GET" and request.is_ajax() and request.user.is_staff:
        patient_id = request.GET.get("patient_id")
        prescriptionObjs = Prescription.objects.filter(patient_id=patient_id)
        prescriptions = [
            {
                "id": prescription.id,
                "name": prescription.createTimestamp.strftime("%d-%b-%Y %I:%M %p"),
            }
            for prescription in prescriptionObjs
        ]

        return JsonResponse(
            {
                "message": f"Fetched Patient ({patient_id}) Prescription's by {request.user.username}",
                "prescriptions": prescriptions,
            },
            status=200,
        )

    elif request.method == "POST" and request.is_ajax() and request.user.is_staff:
        patient_name = request.POST.get("patient_name")
        date_of_birth = request.POST.get("date_of_birth")
        date_of_birthObj = datetime.strptime(date_of_birth, "%d-%b-%Y")  # "%Y-%m-%d"
        phone_number = request.POST.get("phone_number")
        try:
            userObj = User.objects.get(username=patient_name)
        except User.DoesNotExist as e:
            userObj = User.objects.create_user(
                username=patient_name,
                email=None,
                password=phone_number,
            )
            userObj.save()
        try:
            patientObj = Patient.objects.get(user_id=userObj.id)
        except Patient.DoesNotExist:
            patientObj = Patient.objects.create(
                user_id=userObj.id,
                date_of_birth=date_of_birthObj.date(),
                phone_number=phone_number,
            )

            return JsonResponse(
                {
                    "message": f"Created patient {patient_name} by {request.user.username}",
                },
                status=200,
            )

        return JsonResponse(
            {
                "message": f"Failed to Create patient {patient_name} by {request.user.username}",
            },
            status=404,
        )

    elif request.method == "PUT" and request.is_ajax() and not request.user.is_staff:
        try:
            patient_name = QueryDict(request.body).get("patient_name")
            date_of_birth = QueryDict(request.body).get("date_of_birth")
            date_of_birthObj = datetime.strptime(date_of_birth, "%d-%b-%Y")  # "%Y-%m-%d"
            phone_number = QueryDict(request.body).get("phone_number")
            patientObj = Patient.objects.get(user_id=request.user.id)
            patientObj.date_of_birth = date_of_birthObj
            patientObj.phone_number = phone_number
            patientObj.save()
            return JsonResponse(
                {
                    "message": f"Updated patient {patient_name} by {request.user.username}",
                },
                status=200,
            )
        except Exception as err:
            return JsonResponse(
                {
                    "message": f"Failed to Create patient {patient_name} by {request.user.username}",
                },
                status=404,
            )

@login_required
def patient_info(request):
    if request.method == "GET" and request.is_ajax() and request.user.is_staff:
        patient_id = request.GET.get("patient_id")
        patientObj = Patient.objects.get(id = patient_id)
        patient = {
            "id": patientObj.id,
            "name": patientObj.user.username,
            "age": patientObj.age,
            "date_of_birth": patientObj.date_of_birth.strftime("%d-%b-%Y"),
            "phone_number": patientObj.phone_number,
        }
        return JsonResponse(
            {
                "message": f"Fetched Patient ({patient_id}) info by {request.user.username}",
                "patient": patient,
            },
            status=200,
        )

    elif request.method == "POST" and request.is_ajax() and request.user.is_staff:
        try:
            patient_name = request.POST.get("patient_name")
            date_of_birth = request.POST.get("date_of_birth")
            date_of_birthObj = datetime.strptime(date_of_birth, "%d-%b-%Y")  # "%Y-%m-%d"
            phone_number = request.POST.get("phone_number")
            patientObj = Patient.objects.get(user__username = patient_name)
            patientObj.date_of_birth = date_of_birthObj
            patientObj.phone_number = phone_number
            patientObj.save()
            return JsonResponse(
                {
                    "message": f"Updated patient {patient_name} by {request.user.username}",
                },
                status=200,
            )
        except Exception as err:
            return JsonResponse(
                {
                    "message": f"Failed to Update patient {patient_name} by {request.user.username}",
                },
                status=404,
            )