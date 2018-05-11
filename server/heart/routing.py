from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/status_update/(?P<room_name>[^/]+)/$', consumers.StatusConsumer)
]
