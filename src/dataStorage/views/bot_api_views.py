from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.request import QueryDict
from dataStorage.models import Patient, Token
from django.views.decorators.csrf import csrf_exempt
import pyotp
from base64 import b32encode
from binascii import unhexlify

def get_token(hex_key, hop=None):
    secret = b32encode((unhexlify(hex_key))).decode("UTF-8")
    # totp = pyotp.TOTP(secret)
    # return totp.now()
    hotp = pyotp.HOTP(secret)
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
            token_key = get_token(patientObj.token_key)
            Token.objects.create(
                patient=patientObj,
                token_number=token_key,
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

# @csrf_exempt
# def bot_chat(request):
#     if request.method == "POST" and request.is_ajax():
#         response = None
#         request_content = request.POST.get('content')
#         # request.session["patient_id"] = request.user.id
#         # request.session["patient_name"] = request.user.username

#         if request_content in ["Book Appointment"]:
#             if request.session.get("patient_id") and request.session.get("patient_name"):
#                 request.session["request"] = "get_appointment_date"
#                 response = "Provide Appointment Date in DD-MM-YYYY format."
#             else:
#                 request.session["request"] = "get_patient_id"
#                 response = "Provide Patient ID or Name."
        
#         elif type(request_content) in [type(1), type("a")] and request.session.get("request") == "get_patient_id":
#             try:
#                 patientObj = Patient.objects.get(id = int(request_content))
#                 request.session["patient_id"] = patientObj.id
#                 request.session["patient_name"] = patientObj.user.username
#             except ValueError as ve:
#                 patientObj = Patient.objects.get(user__username = request_content)
#                 request.session["patient_id"] = patientObj.id
#                 request.session["patient_name"] = patientObj.user.username
#             except Exception as err:
#                 request.session["request"] = "get_patient_id"
#                 response = "Please Provide Patient ID or Name."
        
#         elif type(request_content) is type("a") and request.session.get("request") == "get_appointment_date":
#             from dataStorage.views import book_appointment
#             responseDict = book_appointment(
#                 patient_info=request.session.get("patient_id"),
#                 doctor_info=None,
#                 appointment_date=request_content,
#                 appointment_from_time=None,
#                 appointment_to_time=None
#             )
#             response = responseDict.get("message")


#         return JsonResponse(
#             {
#                 "message": f"{request.POST.get('content')}",
#                 "response": response if response else "hello",
#             },
#             status=200,
#         )
from .intents import mappings

def login_falied(request):
    request.session["patient_id"] = None
    request.session["patient_name"] = None
    response = mappings.get("login_falied").get("title")
    request.session["next_action"] = mappings.get("login_falied").get("next_action")
    return response

def login_success(request, patientObj):
    request.session["patient_id"] = patientObj.id
    request.session["patient_name"] = patientObj.user.username
    response = mappings.get("home").get("title")
    response[0] = response[0].format(patient_name=request.session.get("patient_name"))
    options = list(mappings.get("home").get("options").values())
    request.session["next_action"] = mappings.get("home").get("next_action", None)
    return options, response

def bot_chat(request):
    if request.method == "POST" and request.is_ajax():
        response = None
        options = None
        request_selected_option = request.POST.get("option_id")
        request_next_option = request.session.get("next_action")
        request_content = request.POST.get("content")

        if request_content.lower() == "login" or request_next_option == "login":
            request.session["patient_id"] = None
            request.session["patient_name"] = None
            response = mappings.get("login").get("title")
            request.session["next_action"] = mappings.get("login").get("next_action")
        
        elif request_next_option == "home":
            try:
                patientObj = Patient.objects.get(id = int(request_content))
                options, response = login_success(request, patientObj)
            except Patient.DoesNotExist as err:
                response = login_falied(request)
            except ValueError as ve:
                try:
                    patientObj = Patient.objects.get(user__username = request_content)
                    options, response = login_success(request, patientObj)
                except Patient.DoesNotExist as err:
                    response = login_falied(request)

        elif request_content.lower() == "book appointment" or request_selected_option == "book_appointment":
            response = mappings.get(request_selected_option).get("title")
            request.session["next_action"] = mappings.get(request_selected_option).get("next_action")

        elif request_next_option == "book_appointment_slots":
            from dataStorage.views import book_appointment
            response_data = book_appointment(
                patient_info=request.session.get("patient_id"),
                doctor_info=None,
                appointment_date=request_content,
            )
            print(f"{response_data=}")
            response_message = response_data.get("message")
            response_created = response_data.get("created")
            response_available = response_data.get("available")
            available_slots = response_data.get("available_slots")

            options = []
            for available_slot in available_slots:
                options.append({
                    "text": f"{available_slot['from_time']} to {available_slot['to_time']}",
                    "class_list": "chat_option btn btn-sm btn-outline-info m-2",
                    "option_id": f"{available_slot['from_time'].replace(" ", "_")}-{available_slot['to_time'].replace(" ", "_")}",
                })
            response = [response_message, *mappings.get("book_appointment_slots").get("title")]
            request.session["next_action"] = mappings.get("book_appointment_slots").get("next_action")
        
        elif request_next_option == "book_appointment_with_slot":
            print(f"{request_next_option=}")
            print(f"{request_content=}, {request_selected_option=}")
            from_slot, to_slot = request_selected_option.replace("_", " ").split("-") #12:15_PM-12:30_PM
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
                response = [response_message, *mappings.get("book_appointment_complete").get("title")]
                request.session["next_action"] = mappings.get("book_appointment_complete").get("next_action")
                options = list(mappings.get("home").get("options").values())
            else:
                response = [response_message, *mappings.get("book_appointment_slot_error").get("title")]
                request.session["next_action"] = mappings.get("book_appointment_slot_error").get("next_action")
                available_slots = response_data.get("available_slots")
                options = []
                for available_slot in available_slots:
                    options.append({
                        "text": f"{available_slot['from_time']} to {available_slot['to_time']}",
                        "class_list": "chat_option btn btn-sm btn-outline-info m-2",
                        "option_id": f"{available_slot['from_time'].replace(" ", "_")}-{available_slot['to_time'].replace(" ", "_")}",
                    })

        return JsonResponse(
            {
                "message": f"{request.POST.get('content')}",
                "response": response if response else ["hello"],
                "options": options if options else [],
            },
            status=200,
        )