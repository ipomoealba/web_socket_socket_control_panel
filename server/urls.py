from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from heart.views import device_handshaker, control_panel, force_change_status,\
    ajax_update_device_status, ajax_now_status, reset, fuckMusic 

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    url(r'^device_handshaker/$', device_handshaker),
    url(r'^force_change_status/$', force_change_status),
    url(r'^ajax/update_device_status/$', ajax_update_device_status),
    url(r'^ajax/status/$', ajax_now_status),
    url(r'^$', control_panel),
    url(r'^reset/$', reset), 
    url(r'^music/$', fuckMusic)
]
