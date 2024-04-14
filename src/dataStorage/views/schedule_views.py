from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http.request import QueryDict
from dataStorage.models import Patient, Appointment, Doctor, Medicine, Prescription, Schedule
from datetime import datetime
import json, hashlib

def hash_dict_content(dictionary):
    json_string = json.dumps(dictionary, sort_keys=True)
    hash_object = hashlib.sha256(json_string.encode())
    return hash_object.hexdigest()

@login_required
def schedule_operation(request):
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
        schedule_month = request.POST.get('schedule_month')
        schedule_monthObj = datetime.strptime(schedule_month, "%Y-%m")
        schedule_days = request.POST.get('schedule_days').split(',')
        schedule_days_list = [datetime.strptime(schedule_day, "%d-%b-%Y").strftime('%d-%m-%Y')
            for schedule_day in schedule_days if datetime.strptime(schedule_day, "%d-%b-%Y").month == schedule_monthObj.month]
        schedule_status = request.POST.get('schedule_status')
        schedule_json = {
            "rejected_days": schedule_days_list,
        }
        
        Schedule.objects.create(
            schedule_month_year = schedule_monthObj,
            schedule_json = schedule_json,
            status = schedule_status,
        )
        return JsonResponse({
            "message": f"Created Schedule {schedule_month} by {request.user.username}",
        }, status=200)
    
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