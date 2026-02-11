from django.contrib import admin
from .models import Application, Integration, ChatMessage

admin.site.register(Application)
admin.site.register(Integration)
admin.site.register(ChatMessage)