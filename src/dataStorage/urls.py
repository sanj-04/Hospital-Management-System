from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from knox import views as knox_views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

app_name = 'dataStorage'

urlpatterns = [
	#path('/', login_required(iViews.familyList.as_view()), name='familyList'),
	path('', views.home, name='home'),
	# path("reset_password/",auth_views.PasswordResetView.as_view(), name="reset_password"),
	path('dashboard', views.dashboard, name='dashboard'),
	path('adminpg', views.adminpg, name='adminpg'),
	path('apttb', views.apttb, name='apttb'),
	path('pres', views.pres, name='pres'),
	# path('cards', views.cards, name='cards'),
	path('cards', TemplateView.as_view(template_name="cards.html"), name='cards'),
	path('configureDevice/', views.configureDevice, name='configureDevice'),
	path('api/login/', views.KnoxLoginAPI.as_view(), name='api_login'),
	path('api/rflogin/', views.RFLoginAPI.as_view(), name='api_login'),
	path('api/home/', views.HomeView.as_view(), name='api_home'),
	path('api/logout/', knox_views.LogoutView.as_view(), name='api_logout'),
	path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    
	path('generate_token', views.generate_token, name='generate_token'),
	path('bot', views.bot, name='bot'),
]
