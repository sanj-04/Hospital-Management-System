from django.urls import path
from . import views
from knox import views as knox_views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

app_name = "dataStorage"

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home_old, name="home_old"),
    path("pres", views.pres, name="pres"),
    path("cards", TemplateView.as_view(template_name="cards.html"), name="cards"),
    path("generate_token", views.generate_token, name="generate_token"),
    path("bot_chat", views.bot_chat, name="bot_chat"),
    path("bot", views.bot, name="bot"),

    # path("reset_password/",auth_views.PasswordResetView.as_view(), name="reset_password"),
    # path("configureDevice/", views.configureDevice, name="configureDevice"),
    # path("api/login/", views.KnoxLoginAPI.as_view(), name="api_login"),
    # path("api/rflogin/", views.RFLoginAPI.as_view(), name="api_login"),
    # path("api/home/", views.HomeView.as_view(), name="api_home"),
    # path("api/logout/", knox_views.LogoutView.as_view(), name="api_logout"),
    # path("api/logoutall/", knox_views.LogoutAllView.as_view(), name="logoutall"),

    path("doctor_home", views.doctor_home, name="doctor_home"),
    path("patient_home", views.patient_home, name="patient_home"),
    path("patient_info", views.patient_info, name="patient_info"),
    path("patient_operation", views.patient_operation, name="patient_operation"),
    path("appointment_operation", views.appointment_operation, name="appointment_operation"),
    path("schedule_operation", views.schedule_operation, name="schedule_operation"),
    path("prescription_operation", views.prescription_operation, name="prescription_operation"),
]
