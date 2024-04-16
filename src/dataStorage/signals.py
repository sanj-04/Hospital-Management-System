from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from dataStorage.models import Patient, Doctor
# from .main.password import fetch
from credentials.credentials import credentials

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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def postRegistrations(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        Doctor.objects.create(
            user = instance,
            setting_json = credentials.get("default_setting_json"),
        )
    # if created and not instance.is_staff:
    #     Patient.objects.create(user=instance)
