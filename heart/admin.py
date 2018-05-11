from django.contrib import admin
from .models import Status,  Device, Command, Rule, Default 

admin.site.register(Rule)
admin.site.register(Device)
admin.site.register(Status)
admin.site.register(Command)
admin.site.register(Default)
