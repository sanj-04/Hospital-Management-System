from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.request import QueryDict
from django.shortcuts import render
from dataStorage.models import Patient, Appointment, Doctor, Schedule
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

def create_time_objects(dateObj, fromObj, toObj, interval_minutes):
    from_time_objects = []
    to_time_objects = []
    slots = {}
    slots_index = {}
    index = 0
    current_time = fromObj
    while current_time < toObj:
        from_time_objects.append(current_time)
        from_time=current_time
        current_time = (
            datetime.combine(dateObj, current_time) + timedelta(minutes=interval_minutes)
        ).time()
        to_time_objects.append(current_time)
        to_time=current_time
        slots[index]={
            "from_time": from_time,
            "to_time": to_time,
            "slot_index": index,
        }
        slots_index[from_time]={
            "from_time": from_time,
            "to_time": to_time,
            "slot_index": index,
        }
        index+=1
    # print(f"{from_time_objects=}, {to_time_objects=}")
    # print(f"{len(from_time_objects)=}, {len(to_time_objects)=}")
    return from_time_objects, to_time_objects, slots, slots_index

# python src\manage.py shell
# from dataStorage.views import book_appointment
# book_appointment(1, 1, '18-4-2024')
# book_appointment(1, '12-4-2024')
# book_appointment(1, '13-4-2024')
# book_appointment(1, '14-4-2024')
# book_appointment(1, '16-4-2024')
# book_appointment(1, '17-4-2024')
# book_appointment(1, '18-4-2024', '05:00 PM', '05:30 PM')
# book_appointment(1, '19-4-2024', '05:00 PM', '05:30 PM')
# book_appointment(1, '20-4-2024', '05:00 PM', '05:30 PM')

def book_appointment(patient_info, doctor_info, appointment_date, appointment_from_time=None, appointment_to_time=None):
    print(f"{patient_info=}, {doctor_info=}, {appointment_date=}, {appointment_from_time=}, {appointment_to_time=}")
    try:
        patientObj = Patient.objects.get(id = int(patient_info))
    except ValueError as ve:
        patientObj = Patient.objects.get(user__username = patient_info)
    
    if doctor_info:
        try:
            doctorObj = Doctor.objects.get(id = int(doctor_info))
        except ValueError as ve:
            doctorObj = Doctor.objects.get(user__username = doctor_info)
    else:
        doctorObj = Doctor.objects.first()
    
    unavailable_days = list(doctorObj.setting_json.get("unavailable_days").keys())
    available_settings = doctorObj.setting_json.get("available")
    appointment_dateObj = datetime.strptime(appointment_date, "%d-%m-%Y")
    is_future_date = appointment_dateObj.date() >= timezone.now().date()
    if not is_future_date:
        return {
            "message": f"Appointment closed for {appointment_dateObj.strftime("%d-%B-%Y")}.",
            "created": False,
            "available": False,
        }
    
    appointment_weekday = appointment_dateObj.strftime("%A")# .weekday() # 5 => Saturday, 6 => Sunday
    if appointment_weekday in unavailable_days:# == "Sunday":
        return {
            "message": f"{appointment_dateObj.strftime("%d-%B-%Y")} is Sunday, We are Closed on Sunday.",
            "created": False,
            "available": False,
        }
    
    scheduleObj = Schedule.objects.filter(
        Q(schedule_month_year__month = appointment_dateObj.month)
        &Q(schedule_month_year__year = appointment_dateObj.year)
    )
    schedule_exists = scheduleObj.exists()
    if not schedule_exists:
        return {
            "message": f"Schedule not created for {appointment_dateObj.strftime("%B-%Y")}.",
            "created": False,
            "available": False,
        }
    
    if appointment_dateObj.strftime("%d-%m-%Y") in scheduleObj[0].schedule_json.get("rejected_days"):
        return {
            "message": f"Sorry, We are closed on {appointment_dateObj.strftime("%d-%B-%Y")}.",
            "created": False,
            "available": False,
        }
    
    available_from = available_settings[appointment_weekday]['from']
    available_to = available_settings[appointment_weekday]['to']
    available_fromObj = datetime.strptime(available_from, "%I:%M %p").time()
    available_toObj = datetime.strptime(available_to, "%I:%M %p").time()
    available_slot_count = available_settings[appointment_weekday]['slot_count']
    available_duration = available_settings[appointment_weekday]['duration']
    # print(f"{available_from=}, {available_to=}, {available_slot_count=}, {available_duration=}")
    available_fromObj_list, available_toObj_list, slotObjs, slots_index = create_time_objects(
        appointment_dateObj,
        available_fromObj,
        available_toObj,
        available_duration
    )
    # print(f"{available_fromObj_list=}, {available_toObj_list=}, {slotObjs=}")
    appointmentObjs = Appointment.objects.filter(
        appointment_date = appointment_dateObj.date(),
    )

    if appointmentObjs.count() >= available_slot_count:
        return {
            "message": f"Sorry, We are Full on {appointment_dateObj.strftime("%d-%B-%Y")}.",
            "created": False,
            "available": False,
        }
    else:
        # for appointmentObj in appointmentObjs:
        #     if appointmentObj.from_time in available_fromObj_list:
        #         index = available_fromObj_list.index(appointmentObj.from_time)
        #         available_toObj_list.pop(index)
        #         del slotObjs[index]
        #     if appointmentObj.to_time in available_toObj_list:
        #         index = available_toObj_list.index(appointmentObj.to_time)
        #         available_fromObj_list.pop(index)
        #         del slotObjs[index]

        # print(f"{slotObjs=}")
        for appointmentObj in appointmentObjs:
            # print(f"{appointmentObj.slot_index=}, {type(appointmentObj.slot_index)=}")
            # print(f"{slotObjs[appointmentObj.slot_index]=}")
            del slotObjs[appointmentObj.slot_index]

        # print(f"{slotObjs=}")
        
        # available_from_slots = [timeObj.strftime("%I:%M %p") for timeObj in available_fromObj_list]
        # available_to_slots = [timeObj.strftime("%I:%M %p") for timeObj in available_toObj_list]
        available_slots = [{
            "from_time": slotObj.get("from_time").strftime("%I:%M %p"),
            "to_time": slotObj.get("to_time").strftime("%I:%M %p"),
            "slot_index": slotObj.get("slot_index"),
            "from_time_obj": slotObj.get("from_time").strftime("%H:%M"),
            "to_time_obj": slotObj.get("to_time").strftime("%H:%M"),
        } for slotObj in slotObjs.values()]

        # print(f"{available_slots=}")
        if appointment_from_time is None or appointment_to_time is None:
            return {
                "message": f"Available Slot(s) on {appointment_dateObj.strftime("%d-%B-%Y")}.",
                "created": False,
                "available": True,
                # "available_from_slots": available_from_slots,
                # "available_to_slots": available_to_slots,
                "available_slots": available_slots,
            }
        
        appointment_fromObj = datetime.strptime(appointment_from_time, "%I:%M %p").time()
        appointment_toObj = datetime.strptime(appointment_to_time, "%I:%M %p").time()
        # print(f"{slots_index[appointment_fromObj]=}, {slots_index[appointment_fromObj].get("slot_index")=}")
        # print(f"{slots_index[appointment_toObj]=}, {slots_index[appointment_toObj].get("slot_index")=}")
        try:
            appointmentObj = Appointment.objects.create(
                doctor = doctorObj,
                patient = patientObj,
                appointment_date = appointment_dateObj,
                from_time = appointment_fromObj,
                to_time = appointment_toObj,
                slot_index = int(slots_index[appointment_fromObj].get("slot_index")),
                status = "Active",
            )
        
            return {
                "message": f"Appointment Created on {appointment_dateObj.strftime("%d-%B-%Y")} from {appointment_fromObj.strftime("%I:%M %p")} to {appointment_toObj.strftime("%I:%M %p")}, with {appointmentObj.id} as Appointment ID.",
                "created": True,
                "appointment_id": appointmentObj.id,
                "appointmentObj": appointmentObj,
                # "available": True,
                # "available_from_slots": available_from_slots,
                # "available_to_slots": available_to_slots,
                # "available_slots": available_slots,
            }
        except Exception as err:
            print(f"{err=}")
            pass
        # print(f"{appointment_fromObj in available_fromObj_list=}, {appointment_toObj in available_toObj_list=}")
        # if appointment_fromObj in available_fromObj_list and appointment_toObj in available_toObj_list:
        #     from_index = available_fromObj_list.index(appointment_fromObj)
        #     to_index = available_toObj_list.index(appointment_toObj)
        #     print(f"{from_index=}, {to_index=}, {from_index == to_index}")
        #     print(f"{doctorObj=}, {patientObj=}, {appointment_dateObj=}, {appointment_fromObj=}, {appointment_toObj=}")
        #     if from_index and to_index and from_index == to_index:
        #         try:
        #             appointmentObj = Appointment.objects.create(
        #                 doctor = doctorObj,
        #                 patient = patientObj,
        #                 appointment_date = appointment_dateObj,
        #                 from_time = appointment_fromObj,
        #                 to_time = appointment_toObj,
        #                 slot_index = int(slots_index[appointment_fromObj].get("slot_index")),
        #                 status = "Active",
        #             )
                
        #             return {
        #                 "message": f"Appointment Created on {appointment_dateObj.strftime("%d-%B-%Y")}, with {appointmentObj.id} as Appointment ID.",
        #                 "created": True,
        #                 "appointment_id": appointmentObj.id,
        #                 "appointmentObj": appointmentObj,
        #                 # "available": True,
        #                 # "available_from_slots": available_from_slots,
        #                 # "available_to_slots": available_to_slots,
        #                 # "available_slots": available_slots,
        #             }
        #         except Exception as err:
        #             print(f"{err=}")
        #             pass

        return {
            "message": f"Failed to create Appointment on {appointment_dateObj.strftime("%d-%B-%Y")} at {appointment_from_time} and {appointment_to_time}",
            "created": False,
            "available": True,
            # "available_from_slots": available_from_slots,
            # "available_to_slots": available_to_slots,
            "available_slots": available_slots,
        }

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
        if not request.user.is_staff:
            patientObj = Patient.objects.get(user = request.user)
            doctor_info = None
        else:
            doctor_info = request.user.id
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

        # doctorObj = Doctor.objects.get(user_id=request.user.id)
        # appointmentObj = Appointment.objects.create(
        #     doctor = doctorObj,
        #     patient = patientObj,
        #     appointment_date = appointment_dateObj,
        #     from_time = appointment_from_timeObj,
        #     to_time = appointment_to_timeObj,
        #     status = appointment_status,
        # )

        response = book_appointment(
            patient_info=patientObj.id,
            doctor_info=doctor_info,
            appointment_date=appointment_dateObj.strftime("%d-%m-%Y"),
            appointment_from_time=appointment_from_timeObj.strftime("%I:%M %p"),
            appointment_to_time=appointment_to_timeObj.strftime("%I:%M %p"),
        )
        # print(f"{response=}")
        if response.get("created"):
            appointment_id = response.get("appointment_id")
            appointmentObj = response.get("appointmentObj")
            appointmentObj.status = appointment_status
            appointmentObj.save()
            return JsonResponse(
                {
                    "message": f"Created Appointment {appointmentObj.id} by {request.user.username}",
                    "res_message": response.get("message").split(",")[0],
                },
                status=200,
            )
        return JsonResponse(
            {
                "message": f"Failed to Create Appointment.",
                "res_message": response.get("message"),
                "available_slots": response.get("available_slots", []),
            },
            status=404,
        )

    elif request.method == "PUT" and request.is_ajax():
        appointment_id = QueryDict(request.body).get("appointment_id")
        if not request.user.is_staff:
            appointment_idList = Appointment.objects.filter(
                patient__user = request.user
            ).values_list("id", flat=True)
            if int(appointment_id) not in appointment_idList:
                return JsonResponse(
                    {
                        "message": f"Failed to Update Appointment {appointment_id} by {request.user.username}",
                    },
                    status=404,
                )
        appointment_date = QueryDict(request.body).get("appointment_date")
        appointment_from_time = QueryDict(request.body).get("appointment_from_time")
        appointment_to_time = QueryDict(request.body).get("appointment_to_time")
        appointment_status = QueryDict(request.body).get("appointment_status")

        appointment_dateObj = datetime.strptime(appointment_date, "%d-%b-%Y")
        appointment_from_timeObj = datetime.strptime(appointment_from_time, "%H:%M")
        appointment_to_timeObj = datetime.strptime(appointment_to_time, "%H:%M")

        appointmentObj = Appointment.objects.get(id=appointment_id)
        response = book_appointment(
            patient_info=appointmentObj.doctor.id,
            doctor_info=appointmentObj.patient.id,
            appointment_date=appointment_dateObj.strftime("%d-%m-%Y"),
        )
        if response.get("available_slots"):
            for slot in response.get("available_slots"):
                if slot.get("from_time_obj") == appointment_from_timeObj.strftime("%H:%M") and slot.get("to_time_obj") == appointment_to_timeObj.strftime("%H:%M"):
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
        return JsonResponse(
            {
                "message": f"Failed to Update Appointment.",
                "res_message": response.get("message"),
                "available_slots": response.get("available_slots", []),
            },
            status=404,
        )

    elif request.method == "DELETE" and request.is_ajax():
        appointment_id = QueryDict(request.body).get("appointment_id")
        if not request.user.is_staff:
            appointment_idList = Appointment.objects.filter(
                patient__user = request.user
            ).values_list("id", flat=True)
            if int(appointment_id) not in appointment_idList:
                return JsonResponse(
                    {
                        "message": f"Failed to Delete Appointment {appointment_id} by {request.user.username}",
                    },
                    status=404,
                )
        appointmentObj = Appointment.objects.get(id = appointment_id)
        appointmentObj.delete()
        return JsonResponse(
            {
                "message": f"Appointment Delete {appointment_id} by {request.user.username}",
            },
            status=200,
        )