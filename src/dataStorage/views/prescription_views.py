from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.request import QueryDict
from django.shortcuts import render
from dataStorage.models import Patient, Appointment, Doctor, Schedule, Prescription
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

@login_required
def prescription_operation(request):
    if request.method == "GET" and not request.is_ajax():
        prescription_id = request.GET.get("prescription_id")
        prescriptionObj = Prescription.objects.get(id = prescription_id)
        context = {
            "hospital_name": "Hospital Name",
            "address": "Hospital Address",
            "phone": "Hospital Phone",
            "email": "Hospital Email",
            "patient_name": prescriptionObj.patient.user.username,
            "patient_id": prescriptionObj.patient.id,
            "patient_dob": prescriptionObj.patient.date_of_birth,
            "patient_age": prescriptionObj.patient.age,
            "doctor_name": prescriptionObj.doctor.user.username,
            "department": "-",
            "createTimestamp": prescriptionObj.createTimestamp,
            "medicines": prescriptionObj.prescription_json.get("medicines"),
        }
        return render(request, "prescription.html", context)