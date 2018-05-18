from django.contrib import admin
from .models import Status,  Device, Command, Rule, Default, Restrict  

admin.site.register(Rule)
admin.site.register(Device)
admin.site.register(Status)
admin.site.register(Command)
admin.site.register(Restrict)
admin.site.register(Default)
