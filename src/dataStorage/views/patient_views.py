from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http.request import QueryDict
from dataStorage.models import Patient, Doctor, Prescription
from datetime import datetime
import json, hashlib

def hash_dict_content(dictionary):
    json_string = json.dumps(dictionary, sort_keys=True)
    hash_object = hashlib.sha256(json_string.encode())
    return hash_object.hexdigest()

@login_required
def patient_operation(request):
    if request.method == "GET" and request.is_ajax():
        patient_id = request.GET.get('patient_id')
        prescriptionObjs = Prescription.objects.filter(patient_id = patient_id)
        prescriptions = [{
            "id": prescription.id,
            "name": prescription.createTimestamp.strftime('%d-%b-%Y %I:%M %p'),
        } for prescription in prescriptionObjs]

        return JsonResponse({
            "message": f"Fetched Patient ({patient_id}) Prescription's by {request.user.username}",
            "prescriptions": prescriptions,
        }, status=200)
    
    elif request.method == "POST" and request.is_ajax():
        patient_name = request.POST.get('patient_name')
        date_of_birth = request.POST.get('date_of_birth')
        date_of_birthObj = datetime.strptime(date_of_birth, "%d-%b-%Y")# "%Y-%m-%d"
        phone_number = request.POST.get('phone_number')
        try:
            userObj = User.objects.get(username = patient_name)
        except User.DoesNotExist as e:
            userObj = User.objects.create_user(
                username = patient_name,
                email = None,
                password = phone_number,
            )
            userObj.save()
        try:
            patientObj = Patient.objects.get(user_id = userObj.id)
        except Patient.DoesNotExist:
            patientObj = Patient.objects.create(
                user_id = userObj.id,
                date_of_birth = date_of_birthObj.date(),
                phone_number = phone_number,
            )

            return JsonResponse({
                "message": f"Created patient {patient_name} by {request.user.username}",
            }, status=200)

        return JsonResponse({
            "message": f"Failed to Create patient {patient_name} by {request.user.username}",
        }, status=404)
    
    elif request.method == "PUT" and request.is_ajax():
        patient_id = QueryDict(request.body).get('patient_id')
        prescription = QueryDict(request.body).get('prescription')

        doctorObj = Doctor.objects.get(user = request.user)
        patientObj = Patient.objects.get(id=int(patient_id))
        prescription_json = json.loads(prescription)
        prescriptionObj = Prescription.objects.create(
            prescription_hash = hash_dict_content(prescription_json),
            prescription_json =  prescription_json,
            doctor = doctorObj,
            patient = patientObj,
        )
        return JsonResponse(
            {
                'message': f'Added Prescription of {patient_id} by {request.user.username}',
                'prescription_id': prescriptionObj.id,
            },status=200
        )