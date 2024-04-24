from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import ulid, os
from datetime import date
from django.template.defaultfilters import slugify
from django_otp.util import hex_validator, random_hex

phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
)


def increment_ulid(name):
    return f"{name}_{((ulid.new()).timestamp()).str}"
    # return f"{name}_{((ulid.new()).from_randomness(os.urandom(10))).str}"
    # return f"{name}_{(ulid.from_randomness(os.urandom(10))).str}"


def slugify_data(name):
    return slugify(name)


def default_key():
    return random_hex(20)


def key_validator(value):
    return hex_validator()(value)


status_choices = (
    ("Pending", "Pending"),
    ("Active", "Active"),
    ("Ongoing", "Ongoing"),
    ("Completed", "Completed"),
    ("Canceled", "Canceled"),
)

schedule_status_choices = (
    ("Inactive", "Inactive"),
    ("Active", "Active"),
    ("Deleted", "Deleted"),
)


# Create your models here.
class Patient(models.Model):
    # patient_id = models.CharField(max_length=40, unique=True, default=increment_ulid("patient"), editable=True, primary_key=True)
    # patient_id = models.SlugField(max_length=40, unique=True, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    token_key = models.CharField(
        max_length=80,
        validators=[key_validator],
        default=default_key,
        help_text="A hex-encoded secret key of up to 40 bytes.",
    )

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
        db_table = "patients"
        managed = True

    def __str__(self):
        return f"{self.user.username}"


class Doctor(models.Model):
    # doctor_id = models.CharField(max_length=40, unique=True, default=increment_ulid("doctor"), editable=True, primary_key=True)
    # doctor_id = models.SlugField(max_length=40, unique=True, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, unique=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    setting_json = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "doctors"
        managed = True

    def __str__(self):
        return f"{self.user.username}"


class Appointment(models.Model):
    # appointment_id = models.CharField(max_length=40, unique=True, default=increment_ulid("appt"), editable=True, primary_key=True)
    # appointment_id = models.SlugField(max_length=40, unique=True, primary_key=True)
    doctor = models.ForeignKey(
        Doctor, related_name="doctorLink", on_delete=models.DO_NOTHING
    )
    patient = models.ForeignKey(
        Patient, related_name="patientLink", on_delete=models.DO_NOTHING
    )
    appointment_date = models.DateField(blank=False, null=False)
    from_time = models.TimeField(blank=False, null=False)
    to_time = models.TimeField(blank=False, null=False)
    slot_index = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=9, choices=status_choices, default="Pending")
    createTimestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updateTimestamp = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = "appointments"
        managed = True
        unique_together = ("doctor", "patient", "appointment_date", "from_time", "to_time")

    def __str__(self):
        return f"{self.doctor.user.username}:{self.patient.user.username}:{self.createTimestamp.strftime('%d-%b-%Y %I:%M %p')}:{self.status}"


class Medicine(models.Model):
    medicine_name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    createTimestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updateTimestamp = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = "medicines"
        managed = True

    def __str__(self):
        return f"{self.medicine_name}"


class Prescription(models.Model):
    prescription_json = models.JSONField(blank=True, null=True)
    prescription_hash = models.CharField(max_length=255, unique=True)
    doctor = models.ForeignKey(
        Doctor, related_name="doctorPrescriptionLink", on_delete=models.DO_NOTHING
    )
    patient = models.ForeignKey(
        Patient, related_name="patientPrescriptionLink", on_delete=models.DO_NOTHING
    )
    is_active = models.BooleanField(default=True)
    createTimestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = "prescriptions"
        managed = True

    def __str__(self):
        return f"{self.prescription_hash}:{self.doctor.user.username}:{self.patient.user.username}"

class Token(models.Model):
    patient = models.ForeignKey(
        Patient, related_name="patientTokenLink", on_delete=models.DO_NOTHING
    )
    token_number = models.CharField(max_length=8)
    is_active = models.BooleanField(default=True)
    createTimestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = "tokens"
        managed = True

    def __str__(self):
        return str(f"{self.patient.user.username}:{self.token_number}")


class Schedule(models.Model):
    schedule_month_year = models.DateField(blank=False, null=False, unique=True)
    doctor = models.ForeignKey(
        Doctor, related_name="doctorScheduleLink", on_delete=models.DO_NOTHING
    )
    schedule_json = models.JSONField(blank=True, null=True)
    status = models.CharField(
        max_length=9, choices=schedule_status_choices, default="Active"
    )
    createTimestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updateTimestamp = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = "schedules"
        managed = True

    @property
    def rejected_days_count(self):
        return f"{len(self.schedule_json.get('rejected_days'))} day(s)"

    def __str__(self):
        return str(self.schedule_month_year.strftime("%B-%Y"))
