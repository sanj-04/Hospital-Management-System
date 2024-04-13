from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.request import QueryDict
from dataStorage.models import Patient, Token
from django.views.decorators.csrf import csrf_exempt
import pyotp
from base64 import b32encode
from binascii import unhexlify

def get_token(hex_key):
	secret = b32encode((unhexlify(hex_key))).decode('UTF-8')
	totp = pyotp.TOTP(secret)
	return totp.now()

# @login_required
@csrf_exempt
def generate_token(request):
	if request.method == "POST":# and request.is_ajax():
		patient_id = request.POST.get('patient_id')
		patientObj = Patient.objects.get(id=int(patient_id))
		tokenObjs = Token.objects.filter(
			patient = patientObj,
			is_active = True,
		).order_by('createTimestamp')
		if tokenObjs.count() > 0:
			token_key = tokenObjs[0].token_number
		if tokenObjs.count() == 0:
			token_key = get_token(patientObj.token_key)
			Token.objects.create(
				patient = patientObj,
				token_number = token_key,
			)
		return JsonResponse({
			"message": f"Fetched patient Token of {patient_id}",
			"token_key": token_key,
		}, status=200)
	
	elif request.method == "PUT":
		try:
			patient_id = QueryDict(request.body).get('patient_id')
			token_key = QueryDict(request.body).get('token_key')
			patientObj = Patient.objects.get(id=int(patient_id))
			tokenObj = Token.objects.get(
				patient = patientObj,
				is_active = True,
				token_number = token_key,
			)
			tokenObj.is_active = False
			tokenObj.save()
			return JsonResponse({
				"message": f"Patient Token Valid",
				"valid": True,
			}, status=200)
		except Exception as e:
			print(f"{e=}")
		return JsonResponse({
			"message": f"Patient Token Invalid",
			"valid": False,
		}, status=200)
	
	elif request.method == "DELETE":
		patient_id = QueryDict(request.body).get('patient_id')
		patientObj = Patient.objects.get(id=int(patient_id))
		Token.objects.filter(
			patient = patientObj,
			is_active = True,
		).order_by('createTimestamp').delete()
		return JsonResponse({
			"message": f"Deleted patient Token of {patient_id}",
		}, status=200)