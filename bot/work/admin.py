from django.contrib import admin
from .models import CustomUser, Groups, Session

admin.site.register(CustomUser)
admin.site.register(Groups)
admin.site.register(Session)