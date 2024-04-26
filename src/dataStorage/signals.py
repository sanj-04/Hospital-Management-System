from django.db.models.signals import post_save, pre_save
from django.conf import settings
from django.dispatch import receiver
from registration.signals import user_registered
from dataStorage.models import Patient, Doctor
# from .main.password import fetch
from credentials.credentials import credentials
from datetime import datetime

# from rest_framework.authtoken.models import Token
# from django_otp.plugins.otp_totp.models import TOTPDevice
#
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def updateOpenSearch(sender, instance, created, **kwargs):
# 	if created:
# 		Token.objects.create(user = instance)
# 	obj = TOTPDevice.objects.filter(user = instance)
# 	if instance.is_active and obj.count() == 0:
# 		TOTPDevice.objects.create(
# 			user = instance,
# 			name = "Android",
# 			confirmed = False,
# 			tolerance = 3,
# 		)
#
# # qrcode==7.3.1
# # django-otp==1.1.3

@receiver(user_registered)
def preRegistrations(sender, user, request, **kwargs):
    date_of_birth = request.POST.get("date_of_birth")
    date_of_birthObj = datetime.strptime(date_of_birth, "%d-%b-%Y")
    phone_number = request.POST.get("phone_number")
    Patient.objects.create(
        user = user,
        date_of_birth=date_of_birthObj.date(),
        phone_number=phone_number,
    )

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def postRegistrations(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        Doctor.objects.create(
            user = instance,
            setting_json = credentials.get("default_setting_json"),
        )
    # if created and not instance.is_staff:
    #     Patient.objects.create(
    #         user = instance,
    #         date_of_birth=request.session.get("date_of_birth").date(),
    #         phone_number=request.session.get("phone_number"),
    #     )
