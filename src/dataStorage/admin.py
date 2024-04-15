from django.contrib import admin
from dataStorage.models import (
    Patient,
    Appointment,
    Doctor,
    Medicine,
    Prescription,
    Token,
    Schedule,
)

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Medicine)
admin.site.register(Prescription)
admin.site.register(Token)
admin.site.register(Schedule)
