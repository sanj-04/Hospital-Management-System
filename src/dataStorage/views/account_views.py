from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import (
    user_logged_out,
    user_logged_in,
    user_login_failed,
)
from django.dispatch import receiver
from django.db.models import Q
from django.http import JsonResponse
from dataStorage.forms import PatientForm

@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.info(request, "[" + request.user.username + "] Logged out.")

@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    messages.success(request, "[" + request.user.username + "] Logged in.")

@receiver(user_login_failed)
def on_user_login_failed(sender, request, **kwargs):
    messages.warning(request, "Logged in failed.")


# @login_required
def home(request):
    if request.method == "GET" and not request.is_ajax():
        context = {
            "patientForm": PatientForm(),
        }
        return render(request, "main.html", context)
    
def home_old(request):
    if request.method == "GET" and not request.is_ajax():
        context = {
            "patientForm": PatientForm(),
        }
        return render(request, "main_OLD.html", context)

def pres(request):
    context = {}
    return render(request, "pres.html", context)

def bot(request):
    if request.user.is_authenticated and not request.user.is_staff:
        request.session["patient_id"] = request.user.id
        request.session["patient_name"] = request.user.username
        # request.session["next_action"] = "login"
    context = {}
    return render(request, "bot_index.html", context)

@login_required
def configureDevice(request):
    if request.method == "GET":
        try:
            totpObj = TOTPDevice.objects.get(Q(user=request.user) & Q(confirmed=False))
            qrCode = qrcode.make(totpObj.config_url)
            qrCode = qrCode.resize((162, 162))
            qrCodeBytes = io.BytesIO()
            qrCode.save(qrCodeBytes, format="JPEG")
            qrCodeBytes = qrCodeBytes.getvalue()
            qrCode = base64.b64encode(qrCodeBytes).decode("utf-8")
            context = {"qrCode": qrCode}
            return render(request, "account/totp.html", context)
        except:
            return redirect("spapp:index")

    elif request.method == "POST":
        totpObj = TOTPDevice.objects.get(Q(user=request.user) & Q(confirmed=False))
        if totpObj.verify_token(request.POST["totp"]):
            totpObj.confirmed = True
            totpObj.save()
            return JsonResponse(
                {
                    "message": f"Device Updated : {totpObj.id}",
                },
                status=204,
            )
        else:
            return JsonResponse(
                {
                    "message": f"Device Update Falied : {totpObj.id}",
                },
                status=404,
            )


def custom_csrf_failure_view(request, reason):
    return render(request, "account/custom_csrf_failure.html", {"reason": reason})
