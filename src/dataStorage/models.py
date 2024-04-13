from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import ulid, os
from datetime import date
from django.template.defaultfilters import slugify

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

def increment_ulid(name):
    return f"{name}_{((ulid.new()).timestamp()).str}"
    # return f"{name}_{((ulid.new()).from_randomness(os.urandom(10))).str}"
    # return f"{name}_{(ulid.from_randomness(os.urandom(10))).str}"

def slugify_data(name):
    return slugify(name)

status_choices = (
    ("Pending", "Pending"),
    ("Active", "Active"),
    ("Ongoing", "Ongoing"),
    ("Completed", "Completed"),
)

# Create your models here.
class Patient(models.Model):
    # patient_id = models.CharField(max_length=40, unique=True, default=increment_ulid("patient"), editable=True, primary_key=True)
    # patient_id = models.SlugField(max_length=40, unique=True, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, unique=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    @property
    def age(self):
        if self.date_of_birth is not None:
            today = date.today()
            years = today.year - self.date_of_birth.year
            months = today.month - self.date_of_birth.month
            if today.day < self.date_of_birth.day:
                months -= 1
            if months < 0:
                years -= 1
                months += 12
            return f"{years} year(s), {months} month(s)"
        else:
            return "0 year(s)"

    class Meta:
        db_table = 'patients'
        managed = True

    def __str__(self):
        return str(f"{self.user.username}:{self.age}")

class Doctor(models.Model):
    # doctor_id = models.CharField(max_length=40, unique=True, default=increment_ulid("doctor"), editable=True, primary_key=True)
    # doctor_id = models.SlugField(max_length=40, unique=True, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, unique=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    class Meta:
        db_table = 'doctors'
        managed = True
    
    def __str__(self):
        return str(f"{self.user.username}")

class Appointment(models.Model):
    # appointment_id = models.CharField(max_length=40, unique=True, default=increment_ulid("appt"), editable=True, primary_key=True)
    # appointment_id = models.SlugField(max_length=40, unique=True, primary_key=True)
    doctor = models.ForeignKey(Doctor, related_name='doctorLink', on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, related_name='patientLink', on_delete=models.DO_NOTHING)
    date_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=9, choices=status_choices, default="Pending")
    createTimestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'appointments'
        managed = True

    def __str__(self):
        return f"{self.doctor.user.username}:{self.patient.user.username}:{self.date_time.strftime('%d-%b-%Y %I:%M %p')}:{self.status}"

class Medicine(models.Model):
    medicine_name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    createTimestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'medicines'
        managed = True

    def __str__(self):
        return str(self.medicine_name)
    
class Prescription(models.Model):
    prescription_name = models.CharField(max_length=255, unique=True)
    prescription_json = models.JSONField(blank=True, null=True)
    doctor = models.ForeignKey(Doctor, related_name='doctorPrescriptionLink', on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, related_name='patientPrescriptionLink', on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    createTimestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'prescriptions'
        managed = True

    def __str__(self):
        return str(self.prescription_name)