from django.contrib import admin
from .models import Rooms, Messages, Private_rooms, Private_messages, User_Info


admin.site.register(Rooms)
admin.site.register(Messages)
admin.site.register(Private_messages)
admin.site.register(Private_rooms)
admin.site.register(User_Info)