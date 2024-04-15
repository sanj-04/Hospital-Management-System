# from django_otp.plugins.otp_totp.models import TOTPDevice
# from django.db.models import Q
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from dataStorage.models import Patient, Doctor
# from django.contrib import messages
# from django.contrib.auth import logout
# from django.contrib.sessions.models import Session
# from datetime import datetime
#
# class TOTPMiddleware(MiddlewareMixin):
#
#     def process_request(self, request):
#         Session.objects.filter(expire_date__lt=datetime.now()).delete()
#         if request.user.is_authenticated:
#             fullUrl = request.get_full_path().split('?')[0]
#             if not "/configureDevice" in fullUrl and not "/logout" in fullUrl:
#                 obj = TOTPDevice.objects.filter(Q(user = request.user)&Q(confirmed = False)).count()
#                 if obj != 0:
#                     messages.warning(request, 'Configure TOTP device and verify.')
#                     # return redirect('spapp:configureDevice')

class AjaxMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        def is_ajax(self) -> bool:
            return (
                request.headers.get('x-requested-with') == 'XMLHttpRequest'
            )

        request.is_ajax = is_ajax.__get__(request)
        response = self.get_response(request)
        return response

class AccountMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                Doctor.objects.get(user_id = request.user.id)
                is_doctor = True
            except Doctor.DoesNotExist:
                is_doctor = False

            try:
                Patient.objects.get(user_id = request.user.id)
                is_patient = True
            except Patient.DoesNotExist:
                is_patient = False
            
            fullUrl = request.get_full_path().split('?')[0]
            if is_doctor and "/doctor_home" not in fullUrl:
                return redirect('dataStorage:doctor_home')
            
            if is_patient and "/bot" not in fullUrl:
                return redirect('dataStorage:bot')