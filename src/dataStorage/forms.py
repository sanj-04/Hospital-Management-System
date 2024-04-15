from django import forms
from dataStorage.models import Patient

class DateInput(forms.DateInput):
    input_type = 'text'
    # input_type = 'date'

class PatientForm(forms.ModelForm):
    patient = forms.CharField(required=True, label="Patient Name")
    date_of_birth = forms.DateInput()
    phone_number = forms.CharField(required=True, label="Phone Number")

    class Meta:
        model = Patient
        # exclude = ["user",]
        fields = [
            "patient",
            "date_of_birth",
            "phone_number",
        ]

        labels = {
            "patient"       : "Patient Name",
            "date_of_birth" : "Date of Birth*",
            "phone_number"  : "Phone Number",
        }

        widgets = {
            "patient"       : forms.TextInput(),
            "date_of_birth" : DateInput(
                format='%Y-%m-%d',
                attrs={
                    'tabindex' : "1",
                    'class': 'datepicker_single',
                    'data-date-format': 'dd/mm/yyyy',
                    'required': 'required',
                    'autocomplete': 'off',
                }
            ),
            "phone_number"  : forms.TextInput(),
        }