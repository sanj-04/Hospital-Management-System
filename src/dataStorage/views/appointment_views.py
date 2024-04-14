from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http.request import QueryDict
from django.shortcuts import render
from dataStorage.models import Patient, Appointment, Doctor, Medicine, Prescription
from datetime import datetime
import json, hashlib

def hash_dict_content(dictionary):
    json_string = json.dumps(dictionary, sort_keys=True)
    hash_object = hashlib.sha256(json_string.encode())
    return hash_object.hexdigest()

@login_required
def appointment_operation(request):
    if request.method == "GET" and not request.is_ajax():
        appointmentObjs = Appointment.objects.all()
        patientObjs = Patient.objects.all()
        
        context = {
            'appointments' : [{
                'appointment_id': appointment.id,
                'patient_id': appointment.patient.id,
                'patient_name': appointment.patient.user.username,
                'appointment_from_date_time': appointment.from_date_time.strftime('%Y-%m-%dT%H:%M'),
                'appointment_to_date_time': appointment.to_date_time.strftime('%Y-%m-%dT%H:%M'),
                'appointment_from_date_time_str': appointment.from_date_time.strftime('%d-%b-%Y %I:%M %p'),
                'appointment_to_date_time_str': appointment.to_date_time.strftime('%d-%b-%Y %I:%M %p'),
                'appointment_status': appointment.status,
            } for appointment in appointmentObjs],
            'patients' : [{
                'name': patient.user.username,
                'id': patient.id,
            } for patient in patientObjs]
        }
        return render(request, 'appointment.html', context)

    elif request.method == "POST" and request.is_ajax():
        patient = request.POST.get('patient')
        try:
            patientObj = Patient.objects.get(
                id = int(patient)
            )
        except ValueError as ve:
            patientObj = Patient.objects.get(
                user__username = patient
            )
        from_date_time = request.POST.get('from_date_time')
        to_date_time = request.POST.get('to_date_time')
        appointment_status = request.POST.get('appointment_status', 'Pending')
        from_date_timeObj = datetime.strptime(from_date_time, "%Y-%m-%dT%H:%M")
        to_date_timeObj = datetime.strptime(to_date_time, "%Y-%m-%dT%H:%M")
        doctorObj = Doctor.objects.get(user = request.user)
        appointmentObj = Appointment.objects.create(
            doctor = doctorObj,
            patient = patientObj,
            from_date_time = from_date_timeObj,
            to_date_time = to_date_timeObj,
            status = appointment_status,
        )
        return JsonResponse(
            {
                'message': f'Created Appointment {appointmentObj.id} by {request.user.username}',
            },status=200
        )
    
    elif request.method == "PUT" and request.is_ajax():
        appointment_id = QueryDict(request.body).get('appointment_id')
        from_date_time = QueryDict(request.body).get('from_date_time')
        to_date_time = QueryDict(request.body).get('to_date_time')
        appointment_status = QueryDict(request.body).get('appointment_status')
        from_date_timeObj = datetime.strptime(from_date_time, "%Y-%m-%dT%H:%M")
        to_date_timeObj = datetime.strptime(to_date_time, "%Y-%m-%dT%H:%M")

        appointmentObj = Appointment.objects.get(id = appointment_id)
        appointmentObj.from_date_time = from_date_timeObj
        appointmentObj.to_date_time = to_date_timeObj
        if appointment_status:
            appointmentObj.status = appointment_status
        appointmentObj.save()
        return JsonResponse(
            {
                'message': f'Updated Appointment {appointment_id} by {request.user.username}',
            },status=200
        )
    
    elif request.method == "DELETE" and request.is_ajax():
        appointment_id = QueryDict(request.body).get('appointment_id')
        appointmentObj = Appointment.objects.get(id = appointment_id)
        appointmentObj.delete()
        return JsonResponse(
            {
                'message': f'Appointment Delete {appointment_id} by {request.user.username}',
            },status=200
        )