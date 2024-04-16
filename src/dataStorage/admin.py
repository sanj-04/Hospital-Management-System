from django.contrib import admin
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
import json
from datetime import datetime
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

class SessionAdmin(admin.ModelAdmin):
	def _session_data(self, obj):
		return json.dumps(obj.get_decoded(), indent=4)
	
	def _expire_date(self, obj):
		if obj.expire_date<datetime.now():
			diff_string = "Expired"
		else:
			diff = obj.expire_date - datetime.now()
			days = diff.days
			hours, remainder = divmod(diff.seconds, 3600)
			minutes, seconds = divmod(remainder, 60)
			diff_string = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
		return f"{obj.expire_date.strftime('%d-%b-%Y %I:%M %p')} [{diff_string}]"
	_expire_date.short_description = "Expire Date [Remaning Time]"
	
	def remove_expired(self, request, queryset):
		for obj in queryset:
			if obj.expire_date < datetime.now():
				obj.delete()

	def _username(self, obj):
		userObj = User.objects.get(id=obj.get_decoded().get('_auth_user_id'))
		return f"{userObj.username} [{userObj.last_login.strftime('%d-%b-%Y %I:%M %p')}]"
	_username.short_description = "Username [Last Login]"
	# _username.boolean = True

	actions = ["remove_expired"]
	readonly_fields = ['_session_data']
	list_display = ['session_key', '_expire_date', '_username'] #, '_session_data'
	fieldsets = (('', {'fields': (("session_key", "expire_date",), "session_data", "_session_data",)}),)
admin.site.register(Session, SessionAdmin)
