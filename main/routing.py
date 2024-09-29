from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/artwork/(?P<artwork_id>\d+)/$', consumers.ArtWorkConsumer.as_asgi()),
]
