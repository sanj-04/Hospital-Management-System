from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from dataStorage.models import Prescription
import qrcode, io, base64

@login_required
def prescription_operation(request):
    if request.method == "GET" and not request.is_ajax():
        prescription_id = request.GET.get("prescription_id")
        prescriptionObj = Prescription.objects.get(id = prescription_id)

        qrCode = qrcode.make(prescriptionObj.prescription_hash)
        qrCode = qrCode.resize((162, 162))
        qrCodeBytes = io.BytesIO()
        qrCode.save(qrCodeBytes, format='JPEG')
        qrCodeBytes = qrCodeBytes.getvalue()
        qrCode = base64.b64encode(qrCodeBytes).decode('utf-8')

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
            "qrCode": qrCode,
        }
        return render(request, "prescription.html", context)