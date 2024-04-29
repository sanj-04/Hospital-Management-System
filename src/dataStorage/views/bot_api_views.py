from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http.request import QueryDict
from dataStorage.models import Patient, Token, Appointment
from django.views.decorators.csrf import csrf_exempt
import pyotp
from base64 import b32encode
from binascii import unhexlify
from datetime import datetime
from .intents import mappings

def get_token(hex_key, hop=None):
    secret = b32encode((unhexlify(hex_key))).decode("UTF-8")
    # totp = pyotp.TOTP(secret)
    # return totp.now()
    hotp = pyotp.HOTP(secret, digits=8)
    return hotp.at(hop)

# @login_required
@csrf_exempt
def generate_token(request):
    if request.method == "POST":  # and request.is_ajax():
        patient_id = request.POST.get("patient_id")
        patientObj = Patient.objects.get(id=int(patient_id))
        tokenObjs = Token.objects.filter(
            patient=patientObj,
            is_active=True,
        ).order_by("createTimestamp")
        if tokenObjs.count() > 0:
            token_key = tokenObjs[0].token_number
        if tokenObjs.count() == 0:
            token_key = get_token(patientObj.token_key, patientObj.hop_index)
            patientObj.hop_index = patientObj.hop_index + 1
            patientObj.save()
            Token.objects.create(
                patient=patientObj,
                token_number=token_key,
                hop_index = patientObj.hop_index,
            )
        return JsonResponse(
            {
                "message": f"Fetched patient Token of {patient_id}",
                "token_key": token_key,
            },
            status=200,
        )

    elif request.method == "PUT":
        try:
            patient_id = QueryDict(request.body).get("patient_id")
            token_key = QueryDict(request.body).get("token_key")
            patientObj = Patient.objects.get(id=int(patient_id))
            tokenObj = Token.objects.get(
                patient=patientObj,
                is_active=True,
                token_number=token_key,
            )
            tokenObj.is_active = False
            tokenObj.save()
            return JsonResponse(
                {
                    "message": f"Patient Token Valid",
                    "valid": True,
                },
                status=200,
            )
        except Exception as e:
            print(f"{e=}")
        return JsonResponse(
            {
                "message": f"Patient Token Invalid",
                "valid": False,
            },
            status=200,
        )

    elif request.method == "DELETE":
        patient_id = QueryDict(request.body).get("patient_id")
        patientObj = Patient.objects.get(id=int(patient_id))
        Token.objects.filter(
            patient=patientObj,
            is_active=True,
        ).order_by("createTimestamp").delete()
        return JsonResponse(
            {
                "message": f"Deleted patient Token of {patient_id}",
            },
            status=200,
        )

request_mapping = {
    "get_patient_id": {
        "message": "Please Provide Patient ID or Name.",
        "function": "",
    },
    "get_patient_id_error": {
        "message": "Provided Patient ID or Name is invalid.",
        "function": "",
    },
}

def generate_otp(patient_id):
    patientObj = Patient.objects.get(id=int(patient_id))
    token_key = get_token(patientObj.token_key, patientObj.hop_index)
    patientObj.hop_index = patientObj.hop_index + 1
    patientObj.save()
    Token.objects.create(
        patient=patientObj,
        token_number=token_key,
        hop_index = patientObj.hop_index,
    )
    phone_number = patientObj.phone_number
    phone_number = f"{phone_number[:2]}****{phone_number[6:]}"
    return token_key, phone_number

def verify_otp(patient_id, token_key):
    try:
        patientObj = Patient.objects.get(id=int(patient_id))
        tokenObj = Token.objects.get(
            patient=patientObj,
            is_active=True,
            token_number=token_key,
        )
        tokenObj.is_active = False
        tokenObj.save()
        return True
    except Exception as e:
        return False

def login_falied(request):
    request.session["patient_id"] = None
    request.session["patient_name"] = None
    response = mappings.get("login_falied").get("title")
    request.session["next_action"] = mappings.get("login_falied").get("next_action")
    return response

def login_success(request, patientObj):
    request.session["patient_id"] = patientObj.id
    request.session["patient_name"] = patientObj.user.username
    token_key, phone_number = generate_otp(request.session.get("patient_id"))
    response = mappings.get("check_otp").get("title")
    response[0]["text"] = response[0].get("text").format(phone_number=phone_number)
    request.session["next_action"] = mappings.get("check_otp").get("next_action")
    return response

def bot_chat(request):
    if request.method == "POST" and request.is_ajax():
        response = None
        options = None
        request_selected_option = request.POST.get("option_id")
        request_next_option = request.session.get("next_action")
        request_content = request.POST.get("content")

        # print(f"{request_selected_option=}")
        # print(f"{request_next_option=}")
        # print(f"{request_content=}")

        if request_selected_option == "login" or request_content.lower() == "login" or request_next_option == "login":
            request.session["patient_id"] = None
            request.session["patient_name"] = None
            del request.session["patient_id"]
            del request.session["patient_name"]
            response = mappings.get("login").get("title")
            request.session["next_action"] = mappings.get("login").get("next_action")

        elif request_next_option == "otp_verify":
            verify_flag = verify_otp(request.session.get("patient_id"), request_content)
            if verify_flag:
                response = mappings.get("home").get("title")
                response[0]["text"] = response[0].get("text").format(patient_name=request.session.get("patient_name"))
                response = [
                    *response,
                    {
                        "text": "Select a Operation.",
                        "class_list": "",
                    },
                ]
                request.session["next_action"] = "home"
                options = list(mappings.get("home").get("options").values())
            else:
                response = [
                    {
                        "text": "Please login.",
                        "class_list": "error",
                    },
                    *mappings.get("login").get("title"),
                ]
                request.session["patient_id"] = None
                request.session["patient_name"] = None
                del request.session["patient_id"]
                del request.session["patient_name"]
                options = None
                request.session["next_action"] = "check_otp"

        elif request_selected_option == "home":
            request.session["next_action"] = None
            if request.session.get("patient_id"):
                response = [{
                    "text": "Select a Operation.",
                    "class_list": "",
                },]
                options = list(mappings.get("home").get("options").values())
            else:
                response = [
                    {
                        "text": "Please login.",
                        "class_list": "",
                    },
                    *mappings.get("login").get("title"),
                ]
                request.session["patient_id"] = None
                request.session["patient_name"] = None
                del request.session["patient_id"]
                del request.session["patient_name"]
                options = None
                request.session["next_action"] = "login"

        elif request_next_option == "check_otp":
            try:
                patientObj = Patient.objects.get(id = int(request_content))
                response = login_success(request, patientObj)
            except Patient.DoesNotExist as err:
                response = login_falied(request)
            except ValueError as ve:
                try:
                    patientObj = Patient.objects.get(user__username = request_content)
                    response = login_success(request, patientObj)
                except Patient.DoesNotExist as err:
                    response = login_falied(request)

        elif request_selected_option == "logout" or request_content.lower() == "logout":
            request.session["patient_id"] = None
            request.session["patient_name"] = None
            del request.session["patient_id"]
            del request.session["patient_name"]
            response = mappings.get("logout").get("title")
            request.session["next_action"] = mappings.get("login").get("next_action")
            options = list(mappings.get("logout").get("options").values())
        
        elif request_selected_option == "register" or request_content.lower() == "register":
            request.session["patient_id"] = None
            request.session["patient_name"] = None
            request.session["register_patient_name"] = None
            request.session["register_patient_phone"] = None
            request.session["register_patient_dob"] = None
            request.session["reschedule_appointment_id"] = None
            del request.session["patient_id"]
            del request.session["patient_name"]
            del request.session["register_patient_name"]
            del request.session["register_patient_phone"]
            del request.session["register_patient_dob"]
            del request.session["reschedule_appointment_id"]
            response = mappings.get("register").get("title")
            request.session["next_action"] = mappings.get("register").get("next_action")
            
        elif request_next_option == "register_dob":
            request.session["register_patient_name"] = None
            del request.session["register_patient_name"]
            try:
                patientObj = Patient.objects.get(user__username = request_content)
                response = [
                    {
                        "text": "User with name already Exists, Try different Name.",
                        "class_list": "error",
                    },
                    *mappings.get("register").get("title"),
                ]
                request.session["next_action"] = mappings.get("register").get("next_action")
            except Patient.DoesNotExist as err:
                request.session["register_patient_name"] = request_content
                response = mappings.get("register_dob").get("title")
                request.session["next_action"] = mappings.get("register_dob").get("next_action")

        elif request_next_option == "register_phone" and request.session.get("register_patient_name"):
            request.session["register_patient_dob"] = None
            del request.session["register_patient_dob"]
            try:
                patient_dobObj = datetime.strptime(request_content, "%d-%m-%Y")
                request.session["register_patient_dob"] = request_content
                response = mappings.get("register_phone").get("title")
                request.session["next_action"] = mappings.get("register_phone").get("next_action")
            except Exception as err:
                print(f"{err=}")
                request.session["register_patient_dob"] = None
                del request.session["register_patient_dob"]
                response = [
                    {
                        "text": "Entered Date of Birth is Invalid.",
                        "class_list": "error",
                    },
                    *mappings.get("register_dob").get("title"),
                ]
                request.session["next_action"] = mappings.get("register_dob").get("next_action")

        elif request_next_option == "register_check" and request.session.get("register_patient_dob"):
            try:
                patientObj = Patient.objects.get(phone_number = request_content)
                response = [
                    {
                        "text": "User with phone number already Exists, Try different Phone Number.",
                        "class_list": "error",
                    },
                    *mappings.get("register_phone").get("title"),
                ]
                request.session["next_action"] = mappings.get("register_phone").get("next_action")
            except Patient.DoesNotExist as err:
                request.session["register_patient_phone"] = request_content
                try:
                    date_of_birthObj = datetime.strptime(
                        request.session.get("register_patient_dob"),
                        "%d-%m-%Y"
                    )  # "%Y-%m-%d"
                    try:
                        userObj = User.objects.get(
                            username = request.session.get("register_patient_name")
                        )
                    except User.DoesNotExist as e:
                        userObj = User.objects.create_user(
                            username = request.session.get("register_patient_name"),
                            email = None,
                            password = request.session.get("register_patient_phone"),
                        )
                        userObj.save()
                    try:
                        patientObj = Patient.objects.get(user_id=userObj.id)
                        request.session["register_patient_name"] = None
                        request.session["register_patient_phone"] = None
                        request.session["register_patient_dob"] = None
                        del request.session["register_patient_name"]
                        del request.session["register_patient_phone"]
                        del request.session["register_patient_dob"]
                        response = mappings.get("register_failed").get("title")
                        request.session["next_action"] = mappings.get("register_failed").get("next_action")
                        options = list(mappings.get("register_failed").get("options").values())
                    except Patient.DoesNotExist:
                        patientObj = Patient.objects.create(
                            user_id=userObj.id,
                            date_of_birth=date_of_birthObj.date(),
                            phone_number=request.session.get("register_patient_phone"),
                        )
                        response = mappings.get("register_success").get("title")
                        request.session["next_action"] = mappings.get("register_success").get("next_action")
                        options = list(mappings.get("register_success").get("options").values())
                        request.session["register_patient_name"] = None
                        request.session["register_patient_phone"] = None
                        request.session["register_patient_dob"] = None
                        del request.session["register_patient_name"]
                        del request.session["register_patient_phone"]
                        del request.session["register_patient_dob"]
                except Exception as err:
                    request.session["register_patient_name"] = None
                    request.session["register_patient_phone"] = None
                    request.session["register_patient_dob"] = None
                    del request.session["register_patient_name"]
                    del request.session["register_patient_phone"]
                    del request.session["register_patient_dob"]
                    response = mappings.get("register_failed").get("title")
                    request.session["next_action"] = mappings.get("register_failed").get("next_action")
                    options = list(mappings.get("register_failed").get("options").values())

        elif (request_selected_option == "book_appointment" or request_next_option == "book_appointment") and request.session.get("patient_id"):
            response = mappings.get("book_appointment").get("title")
            request.session["next_action"] = mappings.get("book_appointment").get("next_action")

        elif request_next_option == "book_appointment_slots" and request.session.get("patient_id"):
            from dataStorage.views import book_appointment
            response_data = book_appointment(
                patient_info=request.session.get("patient_id"),
                doctor_info=None,
                appointment_date=request_content,
            )
            response_message = response_data.get("message")
            response_created = response_data.get("created")
            response_available = response_data.get("available")
            available_slots = response_data.get("available_slots", [])

            if response_data.get("available", False):
                options = []
                for available_slot in available_slots:
                    options.append({
                        "text": f"{available_slot['from_time']} to {available_slot['to_time']}",
                        "class_list": "chat_option btn btn-sm btn-outline-info m-2",
                        "option_id": f"{available_slot['from_time'].replace(" ", "_")}-{available_slot['to_time'].replace(" ", "_")}",
                    })
                options.append({
                    "text": "Home",
                    "class_list": "chat_option btn btn-sm btn-outline-secondary m-2",
                    "option_id": "home",
                })
                response = [
                    {
                        "text": response_message,
                        "class_list": "",
                    },
                    *mappings.get("book_appointment_slots").get("title"),
                ]
                request.session["next_action"] = mappings.get("book_appointment_slots").get("next_action")
            else:
                options = []
                response = [
                    {
                        "text": response_message,
                        "class_list": "",
                    },
                    *mappings.get("book_appointment_unaviable").get("title"),
                ]
                request.session["next_action"] = mappings.get("book_appointment_unaviable").get("next_action")
        
        elif request_next_option == "book_appointment_with_slot" and request.session.get("patient_id"):
            from_slot, to_slot = request_selected_option.replace("_", " ").split("-")
            from dataStorage.views import book_appointment
            response_data = book_appointment(
                patient_info=request.session.get("patient_id"),
                doctor_info=None,
                appointment_date=request_content,
                appointment_from_time=from_slot,
                appointment_to_time=to_slot,
            )
            response_message = response_data.get("message")
            if response_data.get("created"):
                response = [
                    {
                        "text": response_message,
                        "class_list": "",
                    },
                    *mappings.get("book_appointment_complete").get("title"),
                ]
                request.session["next_action"] = mappings.get("book_appointment_complete").get("next_action")
                options = list(mappings.get("home").get("options").values())
            else:
                if response_data.get("available", False):
                    response = [
                        {
                            "text": response_message,
                            "class_list": "",
                        },
                        *mappings.get("book_appointment_slot_error").get("title"),
                    ]
                    request.session["next_action"] = mappings.get("book_appointment_slot_error").get("next_action")
                    available_slots = response_data.get("available_slots", [])
                    options = []
                    for available_slot in available_slots:
                        options.append({
                            "text": f"{available_slot['from_time']} to {available_slot['to_time']}",
                            "class_list": "chat_option btn btn-sm btn-outline-info m-2",
                            "option_id": f"{available_slot['from_time'].replace(" ", "_")}-{available_slot['to_time'].replace(" ", "_")}",
                        })
                    options.append({
                        "text": "Home",
                        "class_list": "chat_option btn btn-sm btn-outline-secondary m-2",
                        "option_id": "home",
                    })
                else:
                    response = [
                        {
                            "text": response_message,
                            "class_list": "",
                        },
                        *mappings.get("book_appointment_unaviable").get("title"),
                    ]
                    request.session["next_action"] = mappings.get("book_appointment_unaviable").get("next_action")
                    options = []

        elif request_selected_option == "view_appointment" and request.session.get("patient_id"):
            appointmentObjs = Appointment.objects.filter(
                patient_id = request.session.get("patient_id"),
                status = "Active",
            ).order_by("appointment_date")
            response = [
                {
                    "text": f"{appointmentObj.appointment_date.strftime("%d-%B-%Y")} from {appointmentObj.from_time.strftime("%I:%M %p")} to {appointmentObj.to_time.strftime("%I:%M %p")}",
                    "class_list": "",
                } for appointmentObj in appointmentObjs
            ]
            if appointmentObjs.count() == 0:
                response = [
                    {
                        "text": "No Appointment(s).",
                        "class_list": "",
                    },
                ]
            options = list(mappings.get("home").get("options").values())
            request.session["next_action"] = None

        elif request_selected_option == "cancel_appointment" and request.session.get("patient_id"):
            appointmentObjs = Appointment.objects.filter(
                patient_id = request.session.get("patient_id"),
                status = "Active",
            ).order_by("appointment_date")
            options = []
            if appointmentObjs.count() == 0:
                request.session["next_action"] = None
                response = [
                    {
                        "text": "No Appointment(s).",
                        "class_list": "",
                    },
                ]
                options = list(mappings.get("home").get("options").values())
            else:
                request.session["next_action"] = "cancel_appointment_selected"
                response = [
                    {
                        "text": "Select a Appointment to Cancel.",
                        "class_list": "",
                    },
                ]
                for appointmentObj in appointmentObjs:
                    options.append({
                        "text": f"{appointmentObj.appointment_date.strftime("%d-%B-%Y")} from {appointmentObj.from_time.strftime("%I:%M %p")} to {appointmentObj.to_time.strftime("%I:%M %p")}",
                        "class_list": "chat_option btn btn-sm btn-outline-info m-2",
                        "option_id": f"{appointmentObj.id}",
                    })
                options.append({
                    "text": "Home",
                    "class_list": "chat_option btn btn-sm btn-outline-secondary m-2",
                    "option_id": "home",
                })
        
        elif request_next_option == "cancel_appointment_selected" and request.session.get("patient_id"):
            appointmentObj = Appointment.objects.get(id = request_selected_option)
            if appointmentObj.patient_id == request.session.get("patient_id"):
                # appointmentObj.status = "Canceled"
                # appointmentObj.save()
                appointmentObj.delete()
                response = [
                    {
                        "text": "Appointment Canceled.",
                        "class_list": "",
                    },
                ]
            else:
                response = [
                    {
                        "text": "Failed to Cancel Appointment.",
                        "class_list": "error",
                    },
                ]
            options = list(mappings.get("home").get("options").values())
            request.session["next_action"] = None

        elif (request_selected_option == "reschedule_appointment" or request_content.lower() == "reschedule appointment") and request.session.get("patient_id"):
            request.session["reschedule_appointment_id"] = None
            del request.session["reschedule_appointment_id"]
            appointmentObjs = Appointment.objects.filter(
                patient_id = request.session.get("patient_id"),
            ).order_by("appointment_date")
            
            if appointmentObjs.count() == 0:
                response = [
                    {
                        "text": "No Appointment(s).",
                        "class_list": "",
                    },
                ]
                options = list(mappings.get("home").get("options").values())
                request.session["next_action"] = None
            else:
                response = [
                    {
                        "text": "Select a Appointment to be Reschedule.",
                        "class_list": "",
                    },
                ]
                options = [{
                    "text": f"{appointmentObj.appointment_date.strftime("%d-%B-%Y")} from {appointmentObj.from_time.strftime("%I:%M %p")} to {appointmentObj.to_time.strftime("%I:%M %p")}",
                    "class_list": "chat_option btn btn-sm btn-outline-info m-2",
                    "option_id": appointmentObj.id,
                } for appointmentObj in appointmentObjs]
                options.append({
                    "text": "Home",
                    "class_list": "chat_option btn btn-sm btn-outline-secondary m-2",
                    "option_id": "home",
                })
                request.session["next_action"] = "reschedule_appointment_book"

        elif (request_selected_option == "reschedule_appointment_book" or request_next_option == "reschedule_appointment_book") and request.session.get("patient_id"):
            appointment_idList = Appointment.objects.filter(
                patient_id = request.session.get("patient_id")
            ).values_list("id", flat=True)
            if int(request_selected_option) not in appointment_idList:
                appointmentObjs = Appointment.objects.filter(
                    patient_id = request.session.get("patient_id"),
                ).order_by("appointment_date")
                
                if appointmentObjs.count() == 0:
                    response = [
                        {
                            "text": "No Appointment(s).",
                            "class_list": "",
                        },
                    ]
                    options = list(mappings.get("home").get("options").values())
                    request.session["next_action"] = None
                else:
                    response = [
                        {
                            "text": "Select a Appointment to be Reschedule.",
                            "class_list": "",
                        },
                    ]
                    options = [{
                        "text": f"{appointmentObj.appointment_date.strftime("%d-%B-%Y")} from {appointmentObj.from_time.strftime("%I:%M %p")} to {appointmentObj.to_time.strftime("%I:%M %p")}",
                        "class_list": "chat_option btn btn-sm btn-outline-info m-2",
                        "option_id": appointmentObj.id,
                    } for appointmentObj in appointmentObjs]
                    options.append({
                        "text": "Home",
                        "class_list": "chat_option btn btn-sm btn-outline-secondary m-2",
                        "option_id": "home",
                    })
                    request.session["next_action"] = "reschedule_appointment_book"
            else:
                request.session["reschedule_appointment_id"] = request_selected_option
                response = [
                    {
                        "text": "Provide New Appointment Date in DD-MM-YYYY format.",
                        "class_list": "",
                    },
                ]
                request.session["next_action"] = "reschedule_appointment_book_slot"

        elif request_next_option == "reschedule_appointment_book_slot" and request.session.get("patient_id"):
            from dataStorage.views import book_appointment
            response_data = book_appointment(
                patient_info=request.session.get("patient_id"),
                doctor_info=None,
                appointment_date=request_content,
            )
            response_message = response_data.get("message")
            # response_created = response_data.get("created")
            # response_available = response_data.get("available")
            available_slots = response_data.get("available_slots", [])

            if response_data.get("available", False):
                options = []
                for available_slot in available_slots:
                    options.append({
                        "text": f"{available_slot['from_time']} to {available_slot['to_time']}",
                        "class_list": "chat_option btn btn-sm btn-outline-info m-2",
                        "option_id": f"{available_slot['from_time'].replace(" ", "_")}-{available_slot['to_time'].replace(" ", "_")}",
                    })
                options.append({
                    "text": "Home",
                    "class_list": "chat_option btn btn-sm btn-outline-secondary m-2",
                    "option_id": "home",
                })
                response = [
                    {
                        "text": response_message,
                        "class_list": "",
                    },
                    *mappings.get("book_appointment_slots").get("title"),
                ]
                request.session["next_action"] = "reschedule_appointment_book_with_slot"
            else:
                options = []
                response = [
                    {
                        "text": response_message,
                        "class_list": "",
                    },
                    *mappings.get("book_appointment_unaviable").get("title"),
                ]
                request.session["next_action"] = "reschedule_appointment_book"
        
        elif request_next_option == "reschedule_appointment_book_with_slot":
            from_slot, to_slot = request_selected_option.replace("_", " ").split("-")
            from dataStorage.views import book_appointment
            response_data = book_appointment(
                patient_info=request.session.get("patient_id"),
                doctor_info=None,
                appointment_date=request_content,
                appointment_from_time=from_slot,
                appointment_to_time=to_slot,
            )
            response_message = response_data.get("message")
            if response_data.get("created"):
                response = [
                    {
                        "text": response_message,
                        "class_list": "",
                    },
                    *mappings.get("book_appointment_complete").get("title"),
                ]
                request.session["next_action"] = mappings.get("book_appointment_complete").get("next_action")
                options = list(mappings.get("home").get("options").values())
                Appointment.objects.get(
                    id = int(request.session.get("reschedule_appointment_id")),
                ).delete()
                request.session["reschedule_appointment_id"] = None
                del request.session["reschedule_appointment_id"]
            else:
                if response_data.get("available", False):
                    response = [
                        {
                            "text": response_message,
                            "class_list": "",
                        },
                        *mappings.get("book_appointment_slot_error").get("title"),
                    ]
                    request.session["next_action"] = "reschedule_appointment_book_with_slot"
                    available_slots = response_data.get("available_slots", [])
                    options = []
                    for available_slot in available_slots:
                        options.append({
                            "text": f"{available_slot['from_time']} to {available_slot['to_time']}",
                            "class_list": "chat_option btn btn-sm btn-outline-info m-2",
                            "option_id": f"{available_slot['from_time'].replace(" ", "_")}-{available_slot['to_time'].replace(" ", "_")}",
                        })
                    options.append({
                        "text": "Home",
                        "class_list": "chat_option btn btn-sm btn-outline-secondary m-2",
                        "option_id": "home",
                    })
                else:
                    response = [
                        {
                            "text": response_message,
                            "class_list": "",
                        },
                        *mappings.get("book_appointment_unaviable").get("title"),
                    ]
                    request.session["next_action"] = "reschedule_appointment_book"
                    options = []
        else:
            response = [
                {
                    "text": "Falied to Process.",
                    "class_list": "error",
                },
            ]
            options = []
            if request.session.get("patient_id"):
                options.append({
                    "text": "Home",
                    "class_list": "chat_option btn btn-sm btn-outline-secondary m-2 float-end",
                    "option_id": "home",
                })
            else:
                options.append({
                    "text": "Register",
                    "class_list": "chat_option btn btn-sm btn-outline-success m-2 float-begin",
                    "option_id": "register",
                })
                options.append({
                    "text": "Login",
                    "class_list": "chat_option btn btn-sm btn-outline-info m-2 float-end",
                    "option_id": "login",
                })

        return JsonResponse(
            {
                "message": f"{request.POST.get('content')}",
                "response": response if response else [{
                    "text": "Falied to Process.",
                    "class_list": "error",
                }],
                "options": options if options else [],
            },
            status=200,
        )